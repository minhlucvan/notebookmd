"""Tests for notebookmd.cache module."""

import time
from pathlib import Path

import pytest

from notebookmd.cache import (
    CacheEntry,
    CacheManager,
    CacheStats,
    DiskStore,
    MemoryStore,
    _SENTINEL,
    _hash_arg,
    _make_key,
    cache_data,
    cache_resource,
    get_cache_manager,
    reset_cache_manager,
)


# ---------------------------------------------------------------------------
# CacheStats
# ---------------------------------------------------------------------------


class TestCacheStats:
    def test_defaults(self):
        s = CacheStats()
        assert s.hits == 0
        assert s.misses == 0
        assert s.hit_rate == 0.0

    def test_hit_rate(self):
        s = CacheStats(hits=3, misses=7)
        assert s.hit_rate == pytest.approx(0.3)

    def test_hit_rate_no_accesses(self):
        s = CacheStats()
        assert s.hit_rate == 0.0


# ---------------------------------------------------------------------------
# CacheEntry
# ---------------------------------------------------------------------------


class TestCacheEntry:
    def test_not_expired(self):
        e = CacheEntry(value=42, created_at=time.time(), ttl=3600)
        assert not e.is_expired

    def test_expired(self):
        e = CacheEntry(value=42, created_at=time.time() - 100, ttl=10)
        assert e.is_expired

    def test_no_ttl_never_expires(self):
        e = CacheEntry(value=42, created_at=0, ttl=None)
        assert not e.is_expired


# ---------------------------------------------------------------------------
# Key hashing
# ---------------------------------------------------------------------------


class TestKeyHashing:
    def test_hash_primitives(self):
        assert _hash_arg(42) == "42"
        assert _hash_arg("hello") == "'hello'"
        assert _hash_arg(True) == "True"
        assert _hash_arg(None) == "None"

    def test_hash_collections(self):
        h1 = _hash_arg([1, 2, 3])
        h2 = _hash_arg([1, 2, 3])
        assert h1 == h2

        h3 = _hash_arg({"a": 1, "b": 2})
        h4 = _hash_arg({"b": 2, "a": 1})
        assert h3 == h4  # dict hashing is order-independent

    def test_make_key_deterministic(self):
        def my_func(x):
            return x

        k1 = _make_key(my_func, (1, "a"), {"z": 3})
        k2 = _make_key(my_func, (1, "a"), {"z": 3})
        assert k1 == k2

    def test_make_key_different_args(self):
        def my_func(x):
            return x

        k1 = _make_key(my_func, (1,), {})
        k2 = _make_key(my_func, (2,), {})
        assert k1 != k2


# ---------------------------------------------------------------------------
# MemoryStore
# ---------------------------------------------------------------------------


class TestMemoryStore:
    def test_put_and_get(self):
        store = MemoryStore()
        store.put("k1", "hello")
        assert store.get("k1") == "hello"

    def test_miss_returns_sentinel(self):
        store = MemoryStore()
        result = store.get("missing")
        assert result is _SENTINEL

    def test_ttl_expiry(self):
        store = MemoryStore()
        store.put("k1", "value", ttl=0.01)
        time.sleep(0.02)
        assert store.get("k1") is _SENTINEL

    def test_stats_tracking(self):
        store = MemoryStore()
        store.put("k1", "v1")
        store.get("k1")
        store.get("missing")
        assert store.stats.hits == 1
        assert store.stats.misses == 1

    def test_max_entries_eviction(self):
        store = MemoryStore(max_entries=2)
        store.put("a", 1)
        store.put("b", 2)
        store.put("c", 3)
        # 'a' should be evicted (LRU)
        assert store.get("a") is _SENTINEL
        assert store.get("c") == 3

    def test_clear(self):
        store = MemoryStore()
        store.put("k1", "v1")
        store.clear()
        assert store.get("k1") is _SENTINEL
        assert store.stats.hits == 0

    def test_remove(self):
        store = MemoryStore()
        store.put("k1", "v1")
        assert store.remove("k1")
        assert not store.remove("missing")

    def test_keys(self):
        store = MemoryStore()
        store.put("a", 1)
        store.put("b", 2)
        assert sorted(store.keys()) == ["a", "b"]


# ---------------------------------------------------------------------------
# DiskStore
# ---------------------------------------------------------------------------


class TestDiskStore:
    def test_put_and_get(self, tmp_path):
        store = DiskStore(tmp_path / "cache")
        store.put("k1", {"data": [1, 2, 3]})
        assert store.get("k1") == {"data": [1, 2, 3]}

    def test_miss_returns_sentinel(self, tmp_path):
        store = DiskStore(tmp_path / "cache")
        assert store.get("missing") is _SENTINEL

    def test_ttl_expiry(self, tmp_path):
        store = DiskStore(tmp_path / "cache")
        store.put("k1", "value", ttl=0.01)
        time.sleep(0.02)
        assert store.get("k1") is _SENTINEL

    def test_clear(self, tmp_path):
        store = DiskStore(tmp_path / "cache")
        store.put("k1", "v1")
        store.clear()
        assert store.get("k1") is _SENTINEL

    def test_keys(self, tmp_path):
        store = DiskStore(tmp_path / "cache")
        store.put("a", 1)
        store.put("b", 2)
        assert sorted(store.keys()) == ["a", "b"]

    def test_creates_dir(self, tmp_path):
        cache_dir = tmp_path / "nested" / "deep" / "cache"
        store = DiskStore(cache_dir)
        store.put("k1", "v1")
        assert cache_dir.exists()


# ---------------------------------------------------------------------------
# CacheManager
# ---------------------------------------------------------------------------


class TestCacheManager:
    def test_data_cache_roundtrip(self, tmp_path):
        mgr = CacheManager(cache_dir=tmp_path / "cache")
        mgr.put_data("k1", [1, 2, 3])
        assert mgr.get_data("k1") == [1, 2, 3]

    def test_data_cache_disk_persistence(self, tmp_path):
        cache_dir = tmp_path / "cache"
        mgr1 = CacheManager(cache_dir=cache_dir)
        mgr1.put_data("k1", "persisted", persist=True)

        # New manager (simulating restart) should find it on disk
        mgr2 = CacheManager(cache_dir=cache_dir)
        assert mgr2.get_data("k1") == "persisted"

    def test_resource_cache_roundtrip(self, tmp_path):
        mgr = CacheManager(cache_dir=tmp_path / "cache")
        mgr.put_resource("r1", {"conn": "db"})
        assert mgr.get_resource("r1") == {"conn": "db"}

    def test_clear_data(self, tmp_path):
        mgr = CacheManager(cache_dir=tmp_path / "cache")
        mgr.put_data("k1", "v1")
        mgr.clear_data()
        assert mgr.get_data("k1") is _SENTINEL

    def test_clear_all(self, tmp_path):
        mgr = CacheManager(cache_dir=tmp_path / "cache")
        mgr.put_data("k1", "v1")
        mgr.put_resource("r1", "v2")
        mgr.clear_all()
        assert mgr.get_data("k1") is _SENTINEL
        assert mgr.get_resource("r1") is _SENTINEL

    def test_summary(self, tmp_path):
        mgr = CacheManager(cache_dir=tmp_path / "cache")
        info = mgr.summary()
        assert "cache_dir" in info
        assert "data" in info
        assert "resource" in info


# ---------------------------------------------------------------------------
# cache_data decorator
# ---------------------------------------------------------------------------


class TestCacheDataDecorator:
    def setup_method(self):
        reset_cache_manager()

    def teardown_method(self):
        reset_cache_manager()

    def test_basic_caching(self):
        call_count = 0

        @cache_data
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert compute(5) == 10
        assert call_count == 1  # Second call served from cache

    def test_different_args(self):
        call_count = 0

        @cache_data
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        assert compute(6) == 12
        assert call_count == 2

    def test_with_ttl(self):
        call_count = 0

        @cache_data(ttl=0.01)
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert compute(5) == 10
        time.sleep(0.02)
        assert compute(5) == 10
        assert call_count == 2  # Re-computed after TTL

    def test_with_kwargs(self):
        @cache_data
        def compute(x, multiplier=2):
            return x * multiplier

        assert compute(5, multiplier=3) == 15
        assert compute(5, multiplier=3) == 15

    def test_none_return_cached(self):
        call_count = 0

        @cache_data
        def returns_none():
            nonlocal call_count
            call_count += 1
            return None

        assert returns_none() is None
        assert returns_none() is None
        assert call_count == 1

    def test_clear_method(self):
        call_count = 0

        @cache_data
        def compute(x):
            nonlocal call_count
            call_count += 1
            return x

        compute(1)
        compute.clear()
        compute(1)
        assert call_count == 2


# ---------------------------------------------------------------------------
# cache_resource decorator
# ---------------------------------------------------------------------------


class TestCacheResourceDecorator:
    def setup_method(self):
        reset_cache_manager()

    def teardown_method(self):
        reset_cache_manager()

    def test_basic_caching(self):
        call_count = 0

        @cache_resource
        def get_resource():
            nonlocal call_count
            call_count += 1
            return {"type": "connection"}

        r1 = get_resource()
        r2 = get_resource()
        assert r1 is r2  # Same object in memory
        assert call_count == 1

    def test_with_ttl(self):
        call_count = 0

        @cache_resource(ttl=0.01)
        def get_resource():
            nonlocal call_count
            call_count += 1
            return {"n": call_count}

        get_resource()
        time.sleep(0.02)
        r = get_resource()
        assert r["n"] == 2
        assert call_count == 2

    def test_clear_method(self):
        call_count = 0

        @cache_resource
        def get_resource():
            nonlocal call_count
            call_count += 1
            return call_count

        get_resource()
        get_resource.clear()
        get_resource()
        assert call_count == 2


# ---------------------------------------------------------------------------
# Global manager
# ---------------------------------------------------------------------------


class TestGlobalManager:
    def setup_method(self):
        reset_cache_manager()

    def teardown_method(self):
        reset_cache_manager()

    def test_singleton(self):
        m1 = get_cache_manager()
        m2 = get_cache_manager()
        assert m1 is m2

    def test_reset(self):
        m1 = get_cache_manager()
        reset_cache_manager()
        m2 = get_cache_manager()
        assert m1 is not m2
