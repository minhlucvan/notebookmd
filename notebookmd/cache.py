"""Caching utilities inspired by Streamlit's @st.cache_data / @st.cache_resource.

Provides two decorators:
- ``cache_data``: Caches function return values based on input args. Ideal for
  expensive computations, data loading, API calls.  Cached values are serialized
  and stored on disk so they survive process restarts.
- ``cache_resource``: Caches singleton resources (DB connections, ML models).
  Stored in-memory only — cleared on restart.

Usage::

    from notebookmd import cache_data, cache_resource

    @cache_data(ttl=3600)
    def load_prices(ticker: str) -> pd.DataFrame:
        return pd.read_csv(f"https://api.example.com/{ticker}.csv")

    @cache_resource
    def get_db():
        return sqlite3.connect("analytics.db")
"""

from __future__ import annotations

import functools
import hashlib
import json
import logging
import os
import pickle
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar, overload

logger = logging.getLogger("notebookmd.cache")

F = TypeVar("F", bound=Callable[..., Any])

# ---------------------------------------------------------------------------
# Cache configuration
# ---------------------------------------------------------------------------

_DEFAULT_CACHE_DIR = Path(os.environ.get("NOTEBOOKMD_CACHE_DIR", ".notebookmd_cache"))


@dataclass
class CacheStats:
    """Runtime statistics for a cache store."""

    hits: int = 0
    misses: int = 0
    size: int = 0
    evictions: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


@dataclass
class CacheEntry:
    """A single cached value with metadata."""

    value: Any
    created_at: float
    ttl: float | None = None
    access_count: int = 0
    last_accessed: float = 0.0

    @property
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.created_at) > self.ttl


# ---------------------------------------------------------------------------
# Key hashing
# ---------------------------------------------------------------------------


def _make_key(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    """Build a deterministic cache key from function identity + call arguments."""
    parts: list[str] = [func.__module__, func.__qualname__]

    for arg in args:
        parts.append(_hash_arg(arg))
    for k in sorted(kwargs):
        parts.append(f"{k}={_hash_arg(kwargs[k])}")

    raw = ":".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()


def _hash_arg(obj: Any) -> str:
    """Produce a stable string representation for a single argument."""
    # Fast path for common immutable types
    if isinstance(obj, (str, int, float, bool, type(None))):
        return repr(obj)
    if isinstance(obj, (bytes, bytearray)):
        return hashlib.md5(obj).hexdigest()
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(_hash_arg(v) for v in obj) + "]"
    if isinstance(obj, dict):
        items = sorted((k, _hash_arg(v)) for k, v in obj.items())
        return "{" + ",".join(f"{k}:{v}" for k, v in items) + "}"
    if isinstance(obj, (set, frozenset)):
        return "{" + ",".join(sorted(_hash_arg(v) for v in obj)) + "}"

    # pandas DataFrame / Series
    try:
        import pandas as pd

        if isinstance(obj, pd.DataFrame):
            h = hashlib.md5()
            h.update(pickle.dumps(obj.shape))
            h.update(pickle.dumps(list(obj.columns)))
            # Use a sample for large DataFrames to keep hashing fast
            if len(obj) > 1000:
                h.update(pickle.dumps(obj.head(500).values.tobytes()))
                h.update(pickle.dumps(obj.tail(500).values.tobytes()))
            else:
                h.update(obj.values.tobytes())
            return f"df:{h.hexdigest()}"
        if isinstance(obj, pd.Series):
            return f"series:{hashlib.md5(obj.values.tobytes()).hexdigest()}"
    except (ImportError, Exception):
        pass

    # Fallback: pickle then hash
    try:
        return hashlib.md5(pickle.dumps(obj)).hexdigest()
    except Exception:
        return repr(obj)


# ---------------------------------------------------------------------------
# In-memory cache store (used by cache_resource + as primary for cache_data)
# ---------------------------------------------------------------------------


class MemoryStore:
    """Thread-safe in-memory LRU cache store."""

    def __init__(self, max_entries: int | None = None) -> None:
        self._data: dict[str, CacheEntry] = {}
        self._max_entries = max_entries
        self._lock = threading.Lock()
        self.stats = CacheStats()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self.stats.misses += 1
                return _SENTINEL
            if entry.is_expired:
                del self._data[key]
                self.stats.misses += 1
                self.stats.evictions += 1
                return _SENTINEL
            entry.access_count += 1
            entry.last_accessed = time.time()
            self.stats.hits += 1
            return entry.value

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        with self._lock:
            self._data[key] = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl=ttl,
                access_count=1,
                last_accessed=time.time(),
            )
            self.stats.size = len(self._data)
            self._maybe_evict()

    def _maybe_evict(self) -> None:
        """Evict oldest entries if we exceed max_entries (called under lock)."""
        if self._max_entries is None or len(self._data) <= self._max_entries:
            return
        # Sort by last_accessed, evict least-recently-used
        sorted_keys = sorted(self._data, key=lambda k: self._data[k].last_accessed)
        while len(self._data) > self._max_entries:
            k = sorted_keys.pop(0)
            del self._data[k]
            self.stats.evictions += 1
        self.stats.size = len(self._data)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self.stats = CacheStats()

    def remove(self, key: str) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                self.stats.size = len(self._data)
                return True
            return False

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._data.keys())


# ---------------------------------------------------------------------------
# Disk cache store (for cache_data persistence)
# ---------------------------------------------------------------------------


class DiskStore:
    """Disk-backed cache using pickle files."""

    def __init__(self, cache_dir: Path) -> None:
        self._dir = cache_dir
        self._lock = threading.Lock()
        self.stats = CacheStats()

    def _path(self, key: str) -> Path:
        return self._dir / f"{key}.pkl"

    def _meta_path(self, key: str) -> Path:
        return self._dir / f"{key}.meta"

    def get(self, key: str) -> Any:
        with self._lock:
            p = self._path(key)
            mp = self._meta_path(key)
            if not p.exists():
                self.stats.misses += 1
                return _SENTINEL
            # Check TTL from metadata
            if mp.exists():
                try:
                    meta = json.loads(mp.read_text())
                    ttl = meta.get("ttl")
                    created = meta.get("created_at", 0)
                    if ttl is not None and (time.time() - created) > ttl:
                        p.unlink(missing_ok=True)
                        mp.unlink(missing_ok=True)
                        self.stats.misses += 1
                        self.stats.evictions += 1
                        return _SENTINEL
                except Exception:
                    pass
            try:
                value = pickle.loads(p.read_bytes())
                self.stats.hits += 1
                return value
            except Exception:
                self.stats.misses += 1
                return _SENTINEL

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        with self._lock:
            self._dir.mkdir(parents=True, exist_ok=True)
            p = self._path(key)
            try:
                p.write_bytes(pickle.dumps(value))
                meta = {"created_at": time.time(), "ttl": ttl}
                self._meta_path(key).write_text(json.dumps(meta))
                self.stats.size += 1
            except Exception as exc:
                logger.warning("Failed to write cache entry %s: %s", key[:12], exc)

    def clear(self) -> None:
        with self._lock:
            if self._dir.exists():
                for f in self._dir.iterdir():
                    if f.suffix in (".pkl", ".meta"):
                        f.unlink(missing_ok=True)
            self.stats = CacheStats()

    def keys(self) -> list[str]:
        with self._lock:
            if not self._dir.exists():
                return []
            return [f.stem for f in self._dir.glob("*.pkl")]


# Sentinel value to distinguish "not found" from None
class _Sentinel:
    """Sentinel for cache misses (distinct from None)."""

    def __repr__(self) -> str:
        return "<CACHE_MISS>"


_SENTINEL = _Sentinel()

# ---------------------------------------------------------------------------
# Global cache manager
# ---------------------------------------------------------------------------


class CacheManager:
    """Central cache manager that coordinates memory and disk stores."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        self._cache_dir = cache_dir or _DEFAULT_CACHE_DIR
        self._data_memory = MemoryStore()
        self._data_disk = DiskStore(self._cache_dir / "data")
        self._resource_memory = MemoryStore()

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    @property
    def data_stats(self) -> CacheStats:
        return self._data_memory.stats

    @property
    def resource_stats(self) -> CacheStats:
        return self._resource_memory.stats

    def get_data(self, key: str) -> Any:
        """Get from data cache (memory first, then disk)."""
        val = self._data_memory.get(key)
        if val is not _SENTINEL:
            return val
        # Try disk
        val = self._data_disk.get(key)
        if val is not _SENTINEL:
            # Promote to memory
            self._data_memory.put(key, val)
            # Fix stats: the memory miss was already counted, undo it
            self._data_memory.stats.misses -= 1
            self._data_memory.stats.hits += 1
            return val
        return _SENTINEL

    def put_data(self, key: str, value: Any, ttl: float | None = None, persist: bool = True) -> None:
        """Store in data cache (memory + optionally disk)."""
        self._data_memory.put(key, value, ttl=ttl)
        if persist:
            self._data_disk.put(key, value, ttl=ttl)

    def get_resource(self, key: str) -> Any:
        return self._resource_memory.get(key)

    def put_resource(self, key: str, value: Any, ttl: float | None = None) -> None:
        self._resource_memory.put(key, value, ttl=ttl)

    def clear_data(self) -> None:
        self._data_memory.clear()
        self._data_disk.clear()

    def clear_resource(self) -> None:
        self._resource_memory.clear()

    def clear_all(self) -> None:
        self.clear_data()
        self.clear_resource()

    def summary(self) -> dict[str, Any]:
        """Return cache summary for CLI display."""
        return {
            "cache_dir": str(self._cache_dir),
            "data": {
                "memory_keys": len(self._data_memory.keys()),
                "disk_keys": len(self._data_disk.keys()),
                "hits": self._data_memory.stats.hits,
                "misses": self._data_memory.stats.misses,
                "hit_rate": f"{self._data_memory.stats.hit_rate:.1%}",
            },
            "resource": {
                "memory_keys": len(self._resource_memory.keys()),
                "hits": self._resource_memory.stats.hits,
                "misses": self._resource_memory.stats.misses,
                "hit_rate": f"{self._resource_memory.stats.hit_rate:.1%}",
            },
        }


# Global singleton
_manager: CacheManager | None = None
_manager_lock = threading.Lock()


def get_cache_manager(cache_dir: Path | None = None) -> CacheManager:
    """Get or create the global CacheManager singleton."""
    global _manager
    with _manager_lock:
        if _manager is None:
            _manager = CacheManager(cache_dir=cache_dir)
        return _manager


def reset_cache_manager() -> None:
    """Reset the global CacheManager (for testing)."""
    global _manager
    with _manager_lock:
        if _manager is not None:
            _manager.clear_all()
        _manager = None


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------


@overload
def cache_data(func: F) -> F: ...


@overload
def cache_data(
    *,
    ttl: float | None = None,
    max_entries: int | None = None,
    persist: bool = True,
    show_spinner: bool = True,
) -> Callable[[F], F]: ...


def cache_data(
    func: F | None = None,
    *,
    ttl: float | None = None,
    max_entries: int | None = None,
    persist: bool = True,
    show_spinner: bool = True,
) -> F | Callable[[F], F]:
    """Cache the return value of a data-producing function.

    Works as a decorator with or without arguments::

        @cache_data
        def load_data():
            return pd.read_csv("big_file.csv")

        @cache_data(ttl=3600, persist=True)
        def fetch_prices(ticker: str):
            return api.get_prices(ticker)

    Args:
        ttl: Time-to-live in seconds. ``None`` means no expiry.
        max_entries: Maximum number of entries to keep per function. ``None`` for unlimited.
        persist: If True, cache values are also written to disk and survive restarts.
        show_spinner: If True, log a message on cache miss (for CLI live output).

    Returns:
        The decorated function with caching behavior.
    """

    def decorator(fn: F) -> F:
        mgr = get_cache_manager()

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _make_key(fn, args, kwargs)
            cached = mgr.get_data(key)
            if cached is not _SENTINEL:
                logger.debug("cache hit: %s(%s)", fn.__name__, key[:12])
                return cached

            if show_spinner:
                logger.info("Computing %s ...", fn.__name__)

            result = fn(*args, **kwargs)
            mgr.put_data(key, result, ttl=ttl, persist=persist)
            return result

        # Attach cache management helpers
        wrapper.clear = lambda: mgr.clear_data()  # type: ignore[attr-defined]

        @functools.wraps(fn)
        def cache_info() -> dict[str, Any]:
            return {"function": fn.__qualname__, "stats": mgr.data_stats}

        wrapper.cache_info = cache_info  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    if func is not None:
        return decorator(func)
    return decorator  # type: ignore[return-value]


@overload
def cache_resource(func: F) -> F: ...


@overload
def cache_resource(
    *,
    ttl: float | None = None,
    show_spinner: bool = True,
) -> Callable[[F], F]: ...


def cache_resource(
    func: F | None = None,
    *,
    ttl: float | None = None,
    show_spinner: bool = True,
) -> F | Callable[[F], F]:
    """Cache a singleton resource (DB connections, ML models, etc.).

    Unlike ``cache_data``, resources are stored in memory only and are never
    serialized to disk.  Use this for objects that are expensive to create but
    cannot (or should not) be pickled::

        @cache_resource
        def get_db():
            return sqlite3.connect("analytics.db")

        @cache_resource(ttl=7200)
        def load_model():
            return heavy_ml_framework.load("model.bin")

    Args:
        ttl: Time-to-live in seconds. ``None`` means no expiry.
        show_spinner: If True, log a message on cache miss.

    Returns:
        The decorated function with caching behavior.
    """

    def decorator(fn: F) -> F:
        mgr = get_cache_manager()

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _make_key(fn, args, kwargs)
            cached = mgr.get_resource(key)
            if cached is not _SENTINEL:
                logger.debug("resource cache hit: %s(%s)", fn.__name__, key[:12])
                return cached

            if show_spinner:
                logger.info("Initializing %s ...", fn.__name__)

            result = fn(*args, **kwargs)
            mgr.put_resource(key, result, ttl=ttl)
            return result

        wrapper.clear = lambda: mgr.clear_resource()  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    if func is not None:
        return decorator(func)
    return decorator  # type: ignore[return-value]
