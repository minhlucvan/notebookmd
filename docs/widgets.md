# Widgets Reference

All widget methods are available directly on the `Notebook` instance. They are organized into 8 plugin categories.

## Text Widgets

Methods for headings, text content, and formatting.

### `n.title(text, anchor=None)`

Emit a top-level heading (H1).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Title text |
| `anchor` | `str \| None` | `None` | Optional HTML anchor ID |

```python
n.title("Quarterly Report")
n.title("Analysis", anchor="analysis")
```

### `n.header(text, anchor=None, divider=False)`

Emit a section header (H2).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Header text |
| `anchor` | `str \| None` | `None` | Optional HTML anchor ID |
| `divider` | `bool` | `False` | Add a horizontal rule below |

```python
n.header("Revenue Analysis")
n.header("Summary", divider=True)
```

### `n.subheader(text, anchor=None, divider=False)`

Emit a subheader (H3).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Subheader text |
| `anchor` | `str \| None` | `None` | Optional HTML anchor ID |
| `divider` | `bool` | `False` | Add a horizontal rule below |

```python
n.subheader("By Region")
```

### `n.caption(text)`

Emit small caption text (rendered as italics).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Caption text (supports markdown) |

```python
n.caption("Source: company database, Q4 2024")
```

### `n.md(text)`

Emit raw markdown text. Use this when you need full control over formatting.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Raw markdown text |

```python
n.md("This is **bold** and this is *italic*.")
n.md("- Item 1\n- Item 2\n- Item 3")
```

### `n.note(text)`

Emit a callout/note as a blockquote.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Note text |

```python
n.note("Data is preliminary and subject to revision.")
```

Output:
```markdown
> **Note:** Data is preliminary and subject to revision.
```

### `n.code(source, lang="python")`

Emit a fenced code block with syntax highlighting.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | `str` | _(required)_ | Code source |
| `lang` | `str` | `"python"` | Language for syntax highlighting |

```python
n.code("SELECT * FROM users WHERE active = 1", lang="sql")
```

### `n.text(body)`

Emit fixed-width preformatted text (monospace).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | Plain text |

```python
n.text("Fixed-width output text")
```

### `n.latex(body)`

Emit a LaTeX math expression.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | LaTeX expression |

```python
n.latex(r"E = mc^2")
n.latex(r"\sum_{i=1}^{n} x_i = X")
```

### `n.divider()`

Emit a horizontal rule (`---`).

```python
n.divider()
```

---

## Data Widgets

Methods for displaying tables, metrics, and structured data. Requires `pandas` for table/DataFrame methods.

### `n.table(df_obj, name="Table", max_rows=None)`

Display a DataFrame as a markdown table with automatic truncation.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df_obj` | DataFrame | _(required)_ | A pandas DataFrame |
| `name` | `str` | `"Table"` | Table heading |
| `max_rows` | `int \| None` | `None` | Max rows to show (defaults to `cfg.max_table_rows`) |

```python
n.table(df, name="Revenue by Region")
n.table(df, name="Top 10", max_rows=10)
```

When the DataFrame has more rows than `max_rows`, an ellipsis row is added and the total shape is noted.

### `n.dataframe(df_obj, name="", max_rows=None, use_container_width=False)`

Display a DataFrame. Functionally identical to `table()` with slightly different defaults, provided for Streamlit API compatibility.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df_obj` | DataFrame | _(required)_ | A pandas DataFrame |
| `name` | `str` | `""` | Optional heading |
| `max_rows` | `int \| None` | `None` | Max rows to show |
| `use_container_width` | `bool` | `False` | Ignored (Streamlit API compat) |

```python
n.dataframe(df, name="Full Dataset")
```

### `n.metric(label, value, delta=None, delta_color="normal")`

Display a single metric card with an optional delta indicator.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | _(required)_ | Short description |
| `value` | `Any` | _(required)_ | Primary metric value |
| `delta` | `Any \| None` | `None` | Change from previous value |
| `delta_color` | `"normal" \| "inverse" \| "off"` | `"normal"` | Delta styling: `normal` = green up/red down, `inverse` = opposite, `off` = no arrow |

```python
n.metric("Revenue", "$1.2M", delta="+12%")
n.metric("Error Rate", "2.1%", delta="-0.5%", delta_color="inverse")
n.metric("Users", "10,432")
```

### `n.metric_row(metrics)`

Display multiple metrics side-by-side in a single table row.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metrics` | `list[dict]` | _(required)_ | List of metric dictionaries |

Each dict supports keys: `label` (required), `value` (required), `delta` (optional), `delta_color` (optional).

```python
n.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Profit", "value": "$300K", "delta": "+8%"},
    {"label": "Customers", "value": "8,421", "delta": "+3.2%"},
])
```

### `n.json(data, expanded=True)`

Display data as a formatted JSON code block.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | `Any` | _(required)_ | Any JSON-serializable object |
| `expanded` | `bool` | `True` | Pretty-print with indentation |

```python
n.json({"model": "gpt-4", "temperature": 0.7, "max_tokens": 1000})
```

### `n.kv(data, title="Metrics")`

Display a key-value dictionary as a two-column table.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | `dict[str, Any]` | _(required)_ | Key-value pairs |
| `title` | `str` | `"Metrics"` | Table heading |

```python
n.kv({
    "Model": "XGBoost",
    "Accuracy": "94.2%",
    "F1 Score": "0.91",
    "Training Samples": "50,000",
}, title="Model Performance")
```

### `n.summary(df_obj, title="Data Summary")`

Generate an automatic summary of a DataFrame: shape, column names, null counts, and basic statistics.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df_obj` | DataFrame | _(required)_ | A pandas DataFrame |
| `title` | `str` | `"Data Summary"` | Section heading |

```python
n.summary(df, title="Dataset Overview")
```

Includes:
- Shape (rows x columns)
- Column names (up to 20, with count of remaining)
- Null counts for columns with missing values (top 10)
- Basic stats for numeric columns (mean, std, min, max)

---

## Chart Widgets

Methods for rendering charts. Chart images require `matplotlib` (`pip install "notebookmd[plotting]"`). Without matplotlib, a text description of the chart data is emitted instead.

All chart methods return the relative path to the saved image file (or `None` if no image was saved).

### `n.line_chart(data, x=None, y=None, title="", x_label="", y_label="", filename=None)`

Display a line chart.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | DataFrame / dict | _(required)_ | Data to plot |
| `x` | `str \| None` | `None` | Column name for x-axis |
| `y` | `str \| Sequence[str] \| None` | `None` | Column name(s) for y-axis |
| `title` | `str` | `""` | Chart title |
| `x_label` | `str` | `""` | X-axis label |
| `y_label` | `str` | `""` | Y-axis label |
| `filename` | `str \| None` | `None` | Custom filename for saved image |

**Returns:** `str | None` -- relative path to saved image

```python
n.line_chart(df, x="date", y="revenue", title="Daily Revenue")
n.line_chart(df, x="month", y=["actual", "forecast"], title="Actual vs Forecast")
```

### `n.area_chart(data, x=None, y=None, title="", x_label="", y_label="", filename=None)`

Display an area chart. Same parameters as `line_chart()`.

```python
n.area_chart(df, x="date", y="cumulative_users", title="User Growth")
```

### `n.bar_chart(data, x=None, y=None, title="", x_label="", y_label="", horizontal=False, filename=None)`

Display a bar chart.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | DataFrame / dict | _(required)_ | Data to plot |
| `x` | `str \| None` | `None` | Column name for x-axis |
| `y` | `str \| Sequence[str] \| None` | `None` | Column name(s) for y-axis |
| `title` | `str` | `""` | Chart title |
| `x_label` | `str` | `""` | X-axis label |
| `y_label` | `str` | `""` | Y-axis label |
| `horizontal` | `bool` | `False` | Render horizontal bars |
| `filename` | `str \| None` | `None` | Custom filename for saved image |

**Returns:** `str | None`

```python
n.bar_chart(df, x="region", y="revenue", title="Revenue by Region")
n.bar_chart(df, x="category", y="count", horizontal=True)
```

### `n.figure(fig, filename, caption="", dpi=160)`

Save a matplotlib figure and embed it in the report.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fig` | matplotlib Figure | _(required)_ | A matplotlib Figure object |
| `filename` | `str` | _(required)_ | Output filename (e.g. `"my_chart.png"`) |
| `caption` | `str` | `""` | Optional caption |
| `dpi` | `int` | `160` | Image resolution |

**Returns:** `str` -- relative path to saved figure

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(df["date"], df["revenue"])
ax.set_title("Revenue Trend")
n.figure(fig, "revenue_trend.png", caption="Monthly revenue")
plt.close(fig)
```

### `n.plotly_chart(fig, filename=None, caption="", use_container_width=True)`

Save and display a Plotly figure.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fig` | plotly Figure | _(required)_ | A Plotly Figure object |
| `filename` | `str \| None` | `None` | Output filename |
| `caption` | `str` | `""` | Optional caption |
| `use_container_width` | `bool` | `True` | Ignored (Streamlit API compat) |

**Returns:** `str` -- relative path to saved chart

Requires `plotly` and `kaleido` for static image export. Falls back to HTML if kaleido is unavailable.

```python
import plotly.express as px

fig = px.scatter(df, x="x", y="y", color="category")
n.plotly_chart(fig, filename="scatter.png")
```

### `n.altair_chart(chart, filename=None, caption="", use_container_width=True)`

Save and display an Altair chart.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chart` | altair Chart | _(required)_ | An Altair Chart object |
| `filename` | `str \| None` | `None` | Output filename |
| `caption` | `str` | `""` | Optional caption |
| `use_container_width` | `bool` | `True` | Ignored (Streamlit API compat) |

**Returns:** `str` -- relative path to saved chart

Requires `altair` and `vl-convert-python` for static image export.

```python
import altair as alt

chart = alt.Chart(df).mark_bar().encode(x="category", y="count")
n.altair_chart(chart, filename="categories.png")
```

---

## Status Widgets

Methods for status messages, progress indicators, and celebrations.

### `n.success(body, icon="✅")`

Emit a success message.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | Message text |
| `icon` | `str` | `"✅"` | Icon prefix |

```python
n.success("All tests passed")
```

### `n.error(body, icon="❌")`

Emit an error message.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | Message text |
| `icon` | `str` | `"❌"` | Icon prefix |

```python
n.error("Failed to connect to database")
```

### `n.warning(body, icon="⚠️")`

Emit a warning message.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | Message text |
| `icon` | `str` | `"⚠️"` | Icon prefix |

```python
n.warning("Data is older than 24 hours")
```

### `n.info(body, icon="ℹ️")`

Emit an info message.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | Message text |
| `icon` | `str` | `"ℹ️"` | Icon prefix |

```python
n.info("Processing 10,000 records")
```

### `n.exception(exc)`

Display an exception with its type and message.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exc` | `Exception` | _(required)_ | The exception to display |

```python
try:
    result = 1 / 0
except Exception as e:
    n.exception(e)
```

### `n.progress(value, text="")`

Emit a text-based progress bar.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `float` | _(required)_ | Progress from 0.0 to 1.0 |
| `text` | `str` | `""` | Optional label text |

```python
n.progress(0.75, text="Processing...")
```

### `n.toast(body, icon="🔔")`

Emit a toast notification.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | _(required)_ | Toast message |
| `icon` | `str` | `"🔔"` | Icon prefix |

```python
n.toast("Report generation complete")
```

### `n.balloons()`

Emit a celebration marker (balloon emoji).

```python
n.balloons()
```

### `n.snow()`

Emit a celebration marker (snow emoji).

```python
n.snow()
```

---

## Layout Widgets

Methods for organizing content with collapsible sections, containers, tabs, and columns.

### `n.expander(label, expanded=False)`

Create a collapsible `<details>` section. Use as a context manager.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | _(required)_ | The expander heading |
| `expanded` | `bool` | `False` | If `True`, section is open by default |

```python
with n.expander("Show raw data"):
    n.table(raw_df, name="Raw Data")

with n.expander("Details", expanded=True):
    n.md("This section is open by default.")
```

### `n.container(border=False)`

Create a visual container. Use as a context manager.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `border` | `bool` | `False` | If `True`, render as a blockquote for visual separation |

```python
with n.container(border=True):
    n.metric("Score", "95")
    n.md("Additional context here.")
```

### `n.tabs(labels)`

Create a tab group. Returns a `_TabGroup` object. Use `tabs.tab(label)` as a context manager for each tab.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `labels` | `Sequence[str]` | _(required)_ | List of tab labels |

**Returns:** `_TabGroup` object

```python
tabs = n.tabs(["Overview", "Details", "Raw Data"])

with tabs.tab("Overview"):
    n.metric("Revenue", "$1.2M")

with tabs.tab("Details"):
    n.table(details_df)

with tabs.tab("Raw Data"):
    n.code(raw_output)
```

Since Markdown doesn't support interactive tabs, each tab renders as an H4 heading followed by its content and a horizontal rule.

### `n.columns(spec=2)`

Create a column layout. Returns a `_ColumnGroup` object. Use `cols.col(index)` as a context manager for each column.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spec` | `int \| Sequence[float]` | `2` | Number of columns, or list of relative widths |

**Returns:** `_ColumnGroup` object

```python
cols = n.columns(3)
with cols.col(0):
    n.metric("A", "100")
with cols.col(1):
    n.metric("B", "200")
with cols.col(2):
    n.metric("C", "300")

# With custom widths
cols = n.columns([2.0, 1.0])  # First column is 2x wider
```

---

## Media Widgets

Methods for embedding images, audio, and video.

### `n.image(source, caption="", width=None, filename=None)`

Display an image. Supports file paths, URLs, PIL Images, and numpy arrays.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | `str / Path / PIL.Image / ndarray` | _(required)_ | Image source |
| `caption` | `str` | `""` | Optional caption |
| `width` | `int \| None` | `None` | Width in pixels (renders as HTML `<img>` if set) |
| `filename` | `str \| None` | `None` | Output filename for image data |

**Returns:** `str` -- path or URL to the image

```python
# From file path
n.image("charts/overview.png", caption="Overview chart")

# From URL
n.image("https://example.com/logo.png", caption="Logo")

# From PIL Image
from PIL import Image
img = Image.open("photo.jpg")
n.image(img, filename="photo.png", caption="Photo", width=400)
```

### `n.audio(source, caption="")`

Display an audio player link.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | `str` | _(required)_ | Path or URL to audio file |
| `caption` | `str` | `""` | Optional caption |

```python
n.audio("recordings/interview.mp3", caption="Interview recording")
```

### `n.video(source, caption="")`

Display a video link.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | `str` | _(required)_ | Path or URL to video file |
| `caption` | `str` | `""` | Optional caption |

```python
n.video("demos/walkthrough.mp4", caption="Product walkthrough")
```

---

## Analytics Widgets

Specialized methods for data analysis reporting: statistics, badges, change indicators, and rankings.

### `n.stat(label, value, description="", fmt=None)`

Display a single-line statistic with bold value and optional context.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | _(required)_ | Stat name |
| `value` | `Any` | _(required)_ | The value |
| `description` | `str` | `""` | Optional parenthetical context |
| `fmt` | `str \| None` | `None` | Format spec (e.g. `"+.1f"`, `".2%"`) |

```python
n.stat("Quality z-score", 1.5, description="93rd percentile", fmt="+.1f")
# Output: Quality z-score: **+1.5** (93rd percentile)
```

### `n.stats(stats, separator=" · ")`

Display multiple inline stats on one line.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `stats` | `list[dict]` | _(required)_ | List of stat dicts |
| `separator` | `str` | `" · "` | Delimiter between stats |

Each dict supports keys: `label`, `value`, `fmt` (optional), `description` (optional).

```python
n.stats([
    {"label": "P/E", "value": 15.2, "fmt": ".1f"},
    {"label": "P/B", "value": 2.8, "fmt": ".1f"},
    {"label": "ROE", "value": 0.221, "fmt": ".1%"},
])
# Output: P/E: **15.2** · P/B: **2.8** · ROE: **22.1%**
```

### `n.badge(text, style="default")`

Display an inline badge/pill label.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | _(required)_ | Badge text |
| `style` | `str` | `"default"` | One of: `"default"`, `"success"`, `"warning"`, `"error"`, `"info"` |

```python
n.badge("BULLISH", style="success")
n.badge("HOLD", style="warning")
n.badge("SELL", style="error")
```

### `n.change(label, current, previous, fmt=".2f", pct=True, invert=False)`

Display a value with its absolute and percentage change.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | _(required)_ | Metric name |
| `current` | `float` | _(required)_ | Current value |
| `previous` | `float` | _(required)_ | Previous/baseline value |
| `fmt` | `str` | `".2f"` | Format spec for values |
| `pct` | `bool` | `True` | Show percentage change |
| `invert` | `bool` | `False` | If `True`, decrease is positive (e.g. error rate) |

```python
n.change("Revenue", 1_200_000, 1_000_000)
# Output: Revenue: **1200000.00** (▲ +200000.00, +20.0%)

n.change("Error Rate", 0.02, 0.05, fmt=".2%", invert=True)
# Output: Error Rate: **2.00%** (▲ -3.00%, -60.0%)  [green because invert=True]
```

### `n.ranking(label, value, rank=None, total=None, percentile=None, fmt=None)`

Display a value with rank or percentile context.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | _(required)_ | Metric name |
| `value` | `Any` | _(required)_ | The metric value |
| `rank` | `int \| None` | `None` | Position in ranking (1-based) |
| `total` | `int \| None` | `None` | Total items in ranking |
| `percentile` | `float \| None` | `None` | Percentile (0-100) |
| `fmt` | `str \| None` | `None` | Format spec for the value |

```python
n.ranking("Quality z-score", 1.5, percentile=93, fmt="+.1f")
# Output: Quality z-score: **+1.5** (93rd percentile, top 7%)

n.ranking("Market Cap", 12500, rank=3, total=50)
# Output: Market Cap: **12,500** (#3 of 50)
```

---

## Utility Widgets

General-purpose methods for output and data export.

### `n.write(*args)`

Auto-format and display any combination of values. Dispatches based on type:

| Input Type | Rendered As |
|-----------|-------------|
| `str` | Markdown text |
| `dict` | JSON code block |
| `DataFrame` | Markdown table |
| `int` / `float` | Bold number |
| `list` / `tuple` | Bullet list |
| `Exception` | Error blockquote |
| `bool` | Inline code (`True` / `False`) |
| `None` | Inline code (`None`) |
| Other | `str(obj)` |

```python
n.write("Here are the results:")
n.write(42)
n.write({"key": "value"})
n.write(["item 1", "item 2", "item 3"])
n.write(df)
```

### `n.echo(source, output="")`

Display code and its output together.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | `str` | _(required)_ | Source code |
| `output` | `str` | `""` | Output produced by the code |

```python
n.echo(
    "df.groupby('region')['revenue'].sum()",
    "region\nNorth    500000\nSouth    350000"
)
```

### `n.empty()`

Emit an empty placeholder. Included for Streamlit API compatibility.

```python
n.empty()
```

### `n.connection_status(name, status="connected", details="")`

Display a data connection status indicator.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | _(required)_ | Connection name |
| `status` | `"connected" \| "disconnected" \| "error"` | `"connected"` | Current status |
| `details` | `str` | `""` | Optional extra information |

```python
n.connection_status("PostgreSQL", status="connected", details="prod-db-1")
n.connection_status("Redis", status="error", details="timeout after 30s")
```

Output examples:
```
🟢 **PostgreSQL**: connected — prod-db-1
🔴 **Redis**: error — timeout after 30s
```

### `n.export_csv(df, filename, name=None)`

Save a DataFrame as CSV and link it in the artifacts index.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | DataFrame | _(required)_ | A pandas DataFrame |
| `filename` | `str` | _(required)_ | Output filename (e.g. `"data.csv"`) |
| `name` | `str \| None` | `None` | Display name (defaults to filename) |

**Returns:** `str` -- relative path to saved CSV

```python
path = n.export_csv(df, "quarterly_data.csv", name="Quarterly Data Export")
```

---

## Core Methods

These methods are on the `Notebook` class itself, not provided by plugins.

### `n.section(title, description="")`

Start a new semantic section. The primary organizational unit for reports.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | _(required)_ | Section heading (rendered as H2) |
| `description` | `str` | `""` | Optional description (rendered as caption) |

Can be used as a plain call or as a context manager:

```python
# Plain call -- just emits the heading
n.section("Key Metrics")
n.metric("Revenue", "$1.2M")

# Context manager -- adds divider on exit
with n.section("Analysis"):
    n.metric("Score", "95")
    n.table(results_df)
```

### `n.save()`

Write the report to disk at the path specified when creating the notebook.

**Returns:** `Path` to the saved file

```python
path = n.save()
print(f"Report saved to {path}")
```

### `n.to_markdown()`

Get the report content as a string without writing to disk.

**Returns:** `str` -- complete markdown content

```python
md = n.to_markdown()
print(md)
```

### `n.use(plugin_cls)`

Add a custom plugin to this notebook instance. See [Plugin System](plugins.md) for details.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plugin_cls` | `type[PluginSpec]` | _(required)_ | A PluginSpec subclass |

```python
n.use(MyCustomPlugin)
```

### `n.get_plugins()`

Get a dictionary of all loaded plugins.

**Returns:** `dict[str, Any]` -- plugin names mapped to plugin instances

```python
plugins = n.get_plugins()
print(list(plugins.keys()))
# ['text', 'data', 'charts', 'status', 'layout', 'media', 'analytics', 'utility']
```
