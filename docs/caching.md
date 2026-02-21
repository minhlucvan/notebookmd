# Caching

notebookmd provides two caching decorators inspired by Streamlit's `@st.cache_data` and `@st.cache_resource`. They speed up reports by caching expensive computations across runs.

```python
from notebookmd import cache_data, cache_resource
```

## `@cache_data`

Cache the return value of a function based on its input arguments. Cached values are serialized to disk (via pickle) so they survive process restarts.

```python
from notebookmd import cache_data
import pandas as pd

@cache_data
def load_data(path: str) -> pd.DataFrame:
    """This only runs once per unique path."""
    return pd.read_csv(path)

@cache_data(ttl=3600)
def fetch_prices(ticker: str) -> pd.DataFrame:
    """Re-fetches after 1 hour."""
    return pd.read_csv(f"https://api.example.com/prices/{ticker}.csv")

df = load_data("data/sales.csv")       # First call: loads from disk
df = load_data("data/sales.csv")       # Second call: returns cached value instantly
df = load_data("data/other.csv")       # Different args: cache miss, loads again
```

### Parameters

```python
@cache_data(ttl=None, persist=True, max_entries=None, show_spinner=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ttl` | `float \| None` | `None` | Time-to-live in seconds. `None` means no expiration. |
| `persist` | `bool` | `True` | Write cache to disk so it survives restarts. |
| `max_entries` | `int \| None` | `None` | Maximum cached entries (LRU eviction). |
| `show_spinner` | `bool` | `True` | Reserved for future use (Streamlit API compat). |

### Cache Key

The cache key is built from:
1. The function's qualified name
2. The positional arguments
3. The keyword arguments

Arguments are hashed using a stable string representation. DataFrames, numpy arrays, and other complex objects are converted to a hash of their contents.

### Clearing the Cache

Each decorated function gets a `.clear()` method:

```python
@cache_data
def load_data(path):
    return pd.read_csv(path)

load_data("data.csv")    # Cached
load_data.clear()        # Clears all cached values for this function
load_data("data.csv")    # Cache miss -- recomputes
```

### Cache Info

Inspect cache state with `.cache_info()`:

```python
info = load_data.cache_info()
# {'hits': 5, 'misses': 2, 'size': 2, 'evictions': 0, 'hit_rate': 0.714}
```

## `@cache_resource`

Cache singleton resources like database connections, ML models, or API clients. Unlike `@cache_data`, resources are stored **in memory only** and are not serialized to disk.

```python
from notebookmd import cache_resource

@cache_resource
def get_db_connection():
    """Created once, reused across the entire run."""
    import sqlalchemy
    return sqlalchemy.create_engine("postgresql://localhost/mydb")

@cache_resource
def load_model(path: str):
    """Heavy model loaded once per unique path."""
    import joblib
    return joblib.load(path)

conn = get_db_connection()   # First call: creates connection
conn = get_db_connection()   # Second call: returns same object
```

### Parameters

```python
@cache_resource(ttl=None, show_spinner=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ttl` | `float \| None` | `None` | Time-to-live in seconds. `None` means no expiration. |
| `show_spinner` | `bool` | `True` | Reserved for future use (Streamlit API compat). |

### Clearing Resources

```python
@cache_resource
def get_db():
    return create_connection()

get_db()
get_db.clear()   # Clears all cached instances
get_db()         # Reconnects
```

## `@cache_data` vs `@cache_resource`

| | `@cache_data` | `@cache_resource` |
|---|---|---|
| **Use for** | Data: DataFrames, query results, computations | Singletons: connections, models, clients |
| **Storage** | Memory + disk (pickle) | Memory only |
| **Survives restart** | Yes (when `persist=True`) | No |
| **Serializable** | Values must be picklable | No restriction |
| **Max entries** | Configurable LRU eviction | No limit |
| **`.cache_info()`** | Yes | No |

## Cache Management

### CLI

```bash
# View cache statistics
notebookmd cache show

# Clear all cached data
notebookmd cache clear

# Clear only data cache (keep resources)
notebookmd cache clear --data-only

# Use a custom cache directory
notebookmd cache show --cache-dir /path/to/cache
```

### Programmatic

```python
from notebookmd.cache import get_cache_manager, reset_cache_manager

# Get the global cache manager
mgr = get_cache_manager()

# View statistics
print(mgr.summary())
# {'data': {'hits': 10, 'misses': 3, ...}, 'resource': {'hits': 5, ...}}

# Clear data cache
mgr.clear_data()

# Clear resource cache
mgr.clear_resource()

# Clear everything
mgr.clear_all()

# Reset the entire cache manager (mainly for testing)
reset_cache_manager()
```

### Cache Directory

The default cache directory is `.notebookmd_cache` in the current working directory. Override it via:

1. **Environment variable**: `NOTEBOOKMD_CACHE_DIR=/path/to/cache`
2. **CLI flag**: `notebookmd run script.py --cache-dir /path/to/cache`
3. **Programmatic**: `get_cache_manager(cache_dir=Path("/path/to/cache"))`

### Disabling Caching

```bash
# Via CLI
notebookmd run script.py --no-cache
```

## CacheManager API

The `CacheManager` coordinates two stores: a disk-backed `DiskStore` for `@cache_data` and an in-memory `MemoryStore` for `@cache_resource`.

### `CacheStats`

```python
from notebookmd.cache import CacheStats
```

| Field | Type | Description |
|-------|------|-------------|
| `hits` | `int` | Number of cache hits |
| `misses` | `int` | Number of cache misses |
| `size` | `int` | Number of entries currently cached |
| `evictions` | `int` | Number of entries evicted |
| `hit_rate` | `float` | Property: `hits / (hits + misses)` |

### `CacheManager` Methods

| Method | Description |
|--------|-------------|
| `get_data(key)` | Retrieve from data cache |
| `put_data(key, value, ttl, persist)` | Store in data cache |
| `get_resource(key)` | Retrieve from resource cache |
| `put_resource(key, value, ttl)` | Store in resource cache |
| `clear_data()` | Clear data cache |
| `clear_resource()` | Clear resource cache |
| `clear_all()` | Clear both caches |
| `summary()` | Get cache statistics as dict |
| `cache_dir` | Property: path to cache directory |
| `data_stats` | Property: `CacheStats` for data cache |
| `resource_stats` | Property: `CacheStats` for resource cache |

## Example: Caching in a Report Script

```python
from notebookmd import nb, cache_data, cache_resource
import pandas as pd

@cache_resource
def get_db():
    import sqlalchemy
    return sqlalchemy.create_engine("postgresql://localhost/analytics")

@cache_data(ttl=3600)
def query_revenue(year: int) -> pd.DataFrame:
    engine = get_db()
    return pd.read_sql(f"SELECT * FROM revenue WHERE year = {year}", engine)

@cache_data
def compute_summary(df: pd.DataFrame) -> dict:
    return {
        "total": df["amount"].sum(),
        "mean": df["amount"].mean(),
        "count": len(df),
    }

# --- Report ---
n = nb("output/revenue.md", title="Revenue Report")
df = query_revenue(2024)        # Cached after first run
summary = compute_summary(df)   # Cached after first run

n.section("Summary")
n.kv(summary, title="Revenue Stats")
n.table(df, name="Revenue Data")
n.save()
```

On the first run, `query_revenue()` hits the database and `compute_summary()` runs the computation. On subsequent runs, both return cached results instantly.
