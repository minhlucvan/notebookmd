# API Reference

This page documents the core classes and functions that make up the notebookmd public API.

For widget methods (`metric()`, `table()`, `line_chart()`, etc.), see [Widgets Reference](widgets.md).
For the plugin system (`PluginSpec`, `register_plugin()`), see [Plugin System](plugins.md).
For caching decorators (`@cache_data`, `@cache_resource`), see [Caching](caching.md).
For the CLI and script runner, see [CLI Reference](cli.md).

## `nb()` Factory Function

```python
def nb(
    out_md: str,
    title: str = "Report",
    assets_dir: str | None = None,
    cfg: NotebookConfig | None = None,
) -> Notebook
```

Creates a new `Notebook` instance. This is the primary entry point for notebookmd.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `out_md` | `str` | _(required)_ | Path to the output Markdown file (e.g. `"dist/report.md"`) |
| `title` | `str` | `"Report"` | Report title (rendered as H1 heading with timestamp) |
| `assets_dir` | `str \| None` | `None` | Directory for saving figures and artifacts. Defaults to `<out_md_dir>/assets/` |
| `cfg` | `NotebookConfig \| None` | `None` | Optional configuration for rendering behavior |

**Returns:** A configured `Notebook` instance

```python
from notebookmd import nb, NotebookConfig

# Minimal
n = nb("output/report.md")

# Fully configured
cfg = NotebookConfig(max_table_rows=50, float_format="{:.2f}")
n = nb(
    "output/report.md",
    title="Q4 Analysis",
    assets_dir="output/images",
    cfg=cfg,
)
```

---

## `Notebook` Class

```python
class Notebook:
    """Streamlit-like report builder that renders to markdown."""
```

The central class of notebookmd. Provides markdown buffering, asset management, plugin loading, and report lifecycle methods. Widget methods are added dynamically by plugins.

### Constructor

```python
def __init__(
    self,
    out_md: str,
    title: str = "Report",
    assets_dir: str | None = None,
    cfg: NotebookConfig | None = None,
)
```

Usually you should use the `nb()` factory instead of constructing directly.

### Instance Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `out_path` | `Path` | Path to the output Markdown file |
| `assets_path` | `Path` | Path to the assets directory |
| `cfg` | `NotebookConfig` | Configuration object |

### Public Methods

#### `section(title, description="") -> _SectionContext`

Start a new semantic section with an H2 heading.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | _(required)_ | Section heading text |
| `description` | `str` | `""` | Optional caption below the heading |

**Returns:** A `_SectionContext` that can optionally be used as a context manager

```python
# Plain call
n.section("Overview")

# With description
n.section("Revenue", description="All figures in USD")

# As context manager (adds divider on exit)
with n.section("Analysis"):
    n.metric("Score", "95")
```

#### `save() -> Path`

Write the accumulated report Markdown to disk. Creates the output directory if needed. Appends an artifacts index section at the end of the report.

**Returns:** `Path` to the saved file

```python
path = n.save()
```

#### `to_markdown() -> str`

Get the report content as a Markdown string without writing to disk.

**Returns:** Complete Markdown content as a string

```python
md = n.to_markdown()
```

#### `use(plugin_cls) -> None`

Add a plugin to this notebook instance.

| Parameter | Type | Description |
|-----------|------|-------------|
| `plugin_cls` | `type[PluginSpec]` | A `PluginSpec` subclass |

**Raises:** `TypeError` if `plugin_cls` is not a `PluginSpec` subclass

```python
from notebookmd.plugins import PluginSpec

class MyPlugin(PluginSpec):
    name = "my_plugin"
    def greet(self, name: str) -> None:
        self._w(f"Hello, **{name}**!\n\n")

n.use(MyPlugin)
n.greet("World")
```

#### `get_plugins() -> dict[str, Any]`

Return a dictionary of loaded plugin names to plugin instances.

**Returns:** `dict[str, Any]`

```python
for name, instance in n.get_plugins().items():
    print(name)
```

### Internal Methods

These are used by plugin authors. Not intended for direct use in reports.

#### `_w(s: str) -> None`

Append a chunk of Markdown to the internal buffer.

```python
# Inside a plugin method:
self._w("**Bold text**\n\n")
```

#### `_ensure_started() -> None`

Lazily initialize the report. Creates directories, writes the title header and timestamp. Called automatically on first widget use.

#### `_next_id() -> int`

Return an auto-incrementing counter. Useful for generating unique filenames.

```python
# Inside a plugin method:
filename = f"chart_{self._next_id()}.png"
```

#### `_try_render_mpl_chart(chart_type, data, x, y, title, x_label, y_label, filename) -> str | None`

Try to render a chart using matplotlib. Returns the relative path to the saved image, or `None` if matplotlib is unavailable.

| Parameter | Type | Description |
|-----------|------|-------------|
| `chart_type` | `str` | One of `"line"`, `"area"`, `"bar"`, `"barh"` |
| `data` | `Any` | DataFrame or dict-like data |
| `x` | `str \| None` | Column for x-axis |
| `y` | `str \| Sequence[str] \| None` | Column(s) for y-axis |
| `title` | `str` | Chart title |
| `x_label` | `str` | X-axis label |
| `y_label` | `str` | Y-axis label |
| `filename` | `str \| None` | Optional filename |

---

## `NotebookConfig` Class

```python
@dataclass
class NotebookConfig:
    max_table_rows: int = 30
    float_format: str = "{:.4f}"
```

Configuration dataclass for controlling rendering behavior.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_table_rows` | `int` | `30` | Maximum table rows before truncation. Tables with more rows get an ellipsis row and a note showing total shape. |
| `float_format` | `str` | `"{:.4f}"` | Python format string for floating-point numbers in tables and other output |

```python
from notebookmd import NotebookConfig

# Show more rows, fewer decimal places
cfg = NotebookConfig(max_table_rows=100, float_format="{:.2f}")
n = nb("report.md", cfg=cfg)
```

---

## `AssetManager` Class

```python
class AssetManager:
    """Manages saved artifacts (images, CSVs) and generates the artifact index section."""
```

Handles saving figures, CSVs, and other files to the assets directory, and generates the artifact index at the end of reports. Accessible within plugins via `self._asset_mgr`.

### Constructor

```python
def __init__(self, assets_dir: Path, base_dir: Path)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `assets_dir` | `Path` | Directory where assets are saved |
| `base_dir` | `Path` | Parent directory of the output Markdown (for relative paths) |

### Methods

#### `ensure_dir() -> None`

Create the assets directory if it doesn't exist.

#### `rel_path(absolute: Path) -> str`

Get the relative path from the Markdown output directory to an asset.

#### `register(rel: str) -> None`

Register an artifact path in the index. Deduplicates automatically.

#### `artifacts -> list[str]` (property)

Get a copy of the registered artifact paths.

#### `save_figure(fig, filename, dpi=160) -> str`

Save a matplotlib Figure.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fig` | matplotlib Figure | _(required)_ | The figure to save |
| `filename` | `str` | _(required)_ | Output filename |
| `dpi` | `int` | `160` | Image resolution |

**Returns:** Relative path to saved figure

#### `save_csv(df, filename) -> str`

Save a pandas DataFrame as CSV.

| Parameter | Type | Description |
|-----------|------|-------------|
| `df` | DataFrame | The data to save |
| `filename` | `str` | Output filename |

**Returns:** Relative path to saved CSV

#### `save_plotly(fig, filename) -> str`

Save a Plotly figure. Tries PNG first (requires `kaleido`), falls back to HTML.

**Returns:** Relative path to saved file

#### `save_altair(chart, filename) -> str`

Save an Altair chart. Tries PNG first (requires `vl-convert-python`), falls back to HTML, then to JSON spec.

**Returns:** Relative path to saved file

#### `save_image(source, filename) -> str`

Save a PIL Image or numpy array.

**Returns:** Relative path to saved image

#### `save_json(data, filename) -> str`

Save any JSON-serializable data as a `.json` file.

**Returns:** Relative path to saved JSON

#### `render_index() -> str`

Render the artifacts index as Markdown. Returns a bullet list of links to all registered artifacts, or `"_No artifacts generated._"` if empty.

---

## `CapturedOutput` Class

```python
@dataclass
class CapturedOutput:
    stdout: str = ""
    stderr: str = ""
    exception: Exception | None = None
    traceback_str: str = ""
```

Holds captured stdout, stderr, and exception info. Used with `capture_streams()`.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `has_stdout` | `bool` | `True` if stdout is non-empty |
| `has_stderr` | `bool` | `True` if stderr is non-empty |
| `has_error` | `bool` | `True` if an exception was raised |

---

## `capture_streams()` Context Manager

```python
@contextmanager
def capture_streams(echo: bool = True) -> Generator[CapturedOutput, None, None]
```

Context manager that captures stdout/stderr and any raised exception during execution.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `echo` | `bool` | `True` | Also print to the real console while capturing |

```python
from notebookmd.capture import capture_streams

with capture_streams() as out:
    print("Hello, world!")
    x = 42

print(out.stdout)   # "Hello, world!\n"
print(out.has_error) # False
```

---

## `Runner` Class

```python
from notebookmd.runner import Runner, RunConfig, RunResult, RunStatus
```

Executes notebookmd scripts with runtime enhancements (live output, variable injection, caching). This is the engine behind `notebookmd run`.

### `RunConfig`

```python
@dataclass
class RunConfig:
    live: bool = False
    output: str | None = None
    variables: dict[str, str] = field(default_factory=dict)
    cache_dir: str | None = None
    log_level: str = "INFO"
    no_cache: bool = False
    stream: TextIO | None = None
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `live` | `bool` | `False` | Stream Markdown to stderr as it's generated |
| `output` | `str \| None` | `None` | Override the output file path |
| `variables` | `dict[str, str]` | `{}` | Variables injected into the script's global namespace |
| `cache_dir` | `str \| None` | `None` | Custom cache directory |
| `log_level` | `str` | `"INFO"` | Logging verbosity |
| `no_cache` | `bool` | `False` | Disable caching |
| `stream` | `TextIO \| None` | `None` | Destination for live output (default: stderr) |

### `RunResult`

```python
@dataclass
class RunResult:
    status: RunStatus
    script: str
    output_path: str | None = None
    duration_seconds: float = 0.0
    error: str | None = None
    traceback: str | None = None
    artifacts: list[str] = field(default_factory=list)
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | `RunStatus` | `SUCCESS`, `ERROR`, or `INTERRUPTED` |
| `script` | `str` | Path to the script that was executed |
| `output_path` | `str \| None` | Path to the generated Markdown file |
| `duration_seconds` | `float` | Total execution time |
| `error` | `str \| None` | Error message (if failed) |
| `traceback` | `str \| None` | Full traceback (if failed) |
| `artifacts` | `list[str]` | Paths to generated artifacts |
| `ok` | `bool` | Property: `True` if `status == SUCCESS` |

#### `summary() -> str`

Returns a human-readable summary of the run result.

### `RunStatus` Enum

```python
class RunStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    INTERRUPTED = "interrupted"
```

### `Runner` Methods

#### `execute(script_path: str) -> RunResult`

Execute a Python script and return the result.

```python
runner = Runner(RunConfig(live=True))
result = runner.execute("analysis.py")
```

### `LiveWriter`

Hooks into `Notebook._w()` to stream Markdown chunks in real time.

```python
from notebookmd.runner import LiveWriter

writer = LiveWriter(stream=sys.stderr)
writer.on_write("## Section\n\n")
print(writer.total_bytes)   # Bytes written
print(writer.chunk_count)   # Chunks written
```

---

## Module-Level Constants

```python
__version__ = "0.3.0"
```

The current version of the notebookmd package.

## Public Exports

```python
__all__ = [
    "Notebook", "NotebookConfig", "PluginSpec",
    "cache_data", "cache_resource",
    "nb", "register_plugin",
]
```

These are the seven symbols exported from `notebookmd`:

| Export | Type | Description |
|--------|------|-------------|
| `nb` | function | Factory for creating Notebook instances |
| `Notebook` | class | The core report builder |
| `NotebookConfig` | dataclass | Rendering configuration |
| `PluginSpec` | class | Base class for plugins |
| `register_plugin` | function | Register a plugin globally |
| `cache_data` | decorator | Cache function return values (disk + memory) |
| `cache_resource` | decorator | Cache singleton resources (memory only) |
