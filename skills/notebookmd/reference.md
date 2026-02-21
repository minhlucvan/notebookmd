# notebookmd — Complete API Reference

## Factory & Configuration

### `nb(out_md, title="Report", assets_dir=None, cfg=None) -> Notebook`

Create a new report builder.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `out_md` | `str` | *required* | Path to output `.md` file |
| `title` | `str` | `"Report"` | Report title (rendered as `# Title`) |
| `assets_dir` | `str \| None` | `None` | Directory for figures/CSVs. Default: `<out_dir>/assets/` |
| `cfg` | `NotebookConfig \| None` | `None` | Rendering configuration |

### `NotebookConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_table_rows` | `int` | `30` | Maximum rows displayed in tables |
| `float_format` | `str` | `"{:.4f}"` | Format string for floating point numbers |

---

## Text Elements

### `n.title(text, anchor=None)`
Emit a title heading (`# Title`).

### `n.header(text, anchor=None, divider=False)`
Emit a section header (`## Header`). Set `divider=True` to add `---` below.

### `n.subheader(text, anchor=None, divider=False)`
Emit a subheader (`### Sub`). Set `divider=True` to add `---` below.

### `n.caption(text)`
Emit small caption text (`_Caption text_`).

### `n.md(text)`
Emit raw markdown text. Passes through unchanged.

### `n.note(text)`
Emit a callout blockquote (`> **Note:** text`).

### `n.code(source, lang="python")`
Emit a fenced code block with syntax highlighting.

### `n.text(body)`
Emit fixed-width preformatted text in a code block.

### `n.latex(body)`
Emit a LaTeX math expression (`$$..$$`).

### `n.divider()`
Emit a horizontal rule (`---`).

### `n.write(*args)`
Auto-format and display any value. Type dispatch:
- `str` → markdown text
- `dict` → JSON code block
- `DataFrame` → markdown table
- `int/float` → bold number
- `list/tuple` → bullet list
- `Exception` → error callout
- `None` → `None`
- other → `str(obj)`

---

## Sections & Layout

### `n.section(title, description="")`
Start a new section with `## Title`. Can be used as context manager:

```python
# Plain call
n.section("Metrics")
n.metric("Revenue", "$1.2M")

# Context manager (adds divider on exit)
with n.section("Analysis"):
    n.write("Content")
```

### `n.expander(label, expanded=False)` — context manager
Create a collapsible section.

```python
with n.expander("Show details"):
    n.table(df)
```

### `n.container(border=False)` — context manager
Create a visual container. `border=True` renders as blockquote.

### `n.tabs(labels) -> _TabGroup`
Create tab sections. Returns a `_TabGroup` with `.tab(label)` context manager.

```python
tabs = n.tabs(["Overview", "Details"])
with tabs.tab("Overview"):
    n.metric("Revenue", "$1.2M")
with tabs.tab("Details"):
    n.table(df)
```

### `n.columns(spec) -> _ColumnGroup`
Create column layout. `spec` is int (number of columns) or list of relative widths.

```python
cols = n.columns(3)
with cols.col(0):
    n.metric("A", "100")
with cols.col(1):
    n.metric("B", "200")
```

---

## Metrics & KPIs

### `n.metric(label, value, delta=None, delta_color="normal")`
Display a metric card with optional delta indicator.

| Parameter | Type | Description |
|-----------|------|-------------|
| `label` | `str` | Short metric description |
| `value` | `Any` | Primary metric value |
| `delta` | `Any \| None` | Change from previous value |
| `delta_color` | `"normal" \| "inverse" \| "off"` | Delta coloring behavior |

### `n.metric_row(metrics)`
Display multiple metrics side-by-side.

```python
n.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])
```

Each dict supports keys: `label` (required), `value` (required), `delta` (optional), `delta_color` (optional).

### `n.kv(data, title="Metrics")`
Display a key-value dictionary as a formatted table.

```python
n.kv({"LTV": "$14,400", "CAC": "$2,100", "Ratio": "6.9x"}, title="Unit Economics")
```

---

## Data Display

### `n.table(df_obj, name="Table", max_rows=None)`
Display a DataFrame as a markdown table. Uses `cfg.max_table_rows` if `max_rows` not set.

### `n.dataframe(df_obj, name="", max_rows=None, use_container_width=False)`
Display a DataFrame (alias with Streamlit-compatible signature).

### `n.summary(df_obj, title="Data Summary")`
Auto-generate a statistical summary: shape, null counts, numeric stats.

### `n.json(data, expanded=True)`
Display any JSON-serializable object as a formatted JSON code block.

---

## Charts

### `n.line_chart(data, x=None, y=None, title="", x_label="", y_label="", filename=None) -> str|None`
Display a line chart. Returns relative path to saved image if matplotlib available.

### `n.area_chart(data, x=None, y=None, title="", x_label="", y_label="", filename=None) -> str|None`
Display an area chart. Returns relative path to saved image if matplotlib available.

### `n.bar_chart(data, x=None, y=None, title="", x_label="", y_label="", horizontal=False, filename=None) -> str|None`
Display a bar chart. Set `horizontal=True` for horizontal bars.

### `n.figure(fig, filename, caption="", dpi=160) -> str`
Save a matplotlib figure and embed it. Returns relative path.

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(x, y)
n.figure(fig, "my_chart.png", caption="Custom Chart")
```

### `n.plotly_chart(fig, filename=None, caption="", use_container_width=True) -> str`
Save and display a Plotly figure. Auto-generates filename if not provided.

### `n.altair_chart(chart, filename=None, caption="", use_container_width=True) -> str`
Save and display an Altair/Vega-Lite chart.

---

## Analytics Helpers

### `n.stat(label, value, description="", fmt=None)`
Display a single-line statistic.

```python
n.stat("Average Price", 95.4, fmt=".2f")
n.stat("Total", 1_234_567, description="All-time total", fmt=",.0f")
n.stat("Return", 0.123, "annualized", fmt=".1%")
```

### `n.stats(stats, separator=" · ")`
Display multiple inline stats on one line.

```python
n.stats([
    {"label": "Mean", "value": 95.4, "fmt": ".2f"},
    {"label": "Std", "value": 3.2, "fmt": ".2f"},
    {"label": "N", "value": 1000, "fmt": ",d"},
])
```

Each dict keys: `label` (required), `value` (required), `fmt` (optional), `description` (optional).

### `n.badge(text, style="default")`
Display an inline badge/pill label.

| Style | Use |
|-------|-----|
| `"success"` | Positive signal (BULLISH, ON TRACK, PASS) |
| `"warning"` | Caution signal (HOLD, AT RISK, SLOW) |
| `"error"` | Negative signal (BEARISH, FAIL, CRITICAL) |
| `"info"` | Neutral information (Q4 2026, BETA) |
| `"default"` | Plain badge |

### `n.change(label, current, previous, fmt=".2f", pct=True, invert=False)`
Display a value with absolute and percentage change.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | *required* | Metric name |
| `current` | `float` | *required* | Current period value |
| `previous` | `float` | *required* | Previous period value |
| `fmt` | `str` | `".2f"` | Number format string |
| `pct` | `bool` | `True` | Show percentage change |
| `invert` | `bool` | `False` | Invert good/bad (for metrics like churn) |

```python
n.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f", pct=True)
# Output: **Revenue**: 1,200,000 (▲ +200,000 / +20.0%)
```

### `n.ranking(label, value, rank=None, total=None, percentile=None, fmt=None)`
Display a value with rank/percentile context.

```python
n.ranking("Product A", value="$1.2M", rank=1, total=50)
n.ranking("Strategy X", value="12.3%", rank=3, total=20, percentile=85)
```

---

## Status Messages

### `n.success(body, icon="✅")`
Emit a success callout (`> **Success:** body`).

### `n.error(body, icon="❌")`
Emit an error callout (`> **Error:** body`).

### `n.warning(body, icon="⚠️")`
Emit a warning callout (`> **Warning:** body`).

### `n.info(body, icon="ℹ️")`
Emit an info callout (`> **Info:** body`).

### `n.exception(exc)`
Display an exception with traceback info.

### `n.progress(value, text="")`
Emit a text-based progress bar. `value` is 0.0 to 1.0.

### `n.toast(body, icon="🔔")`
Emit a toast notification callout.

### `n.balloons()`
Emit a celebration marker.

### `n.snow()`
Emit a snow celebration marker.

---

## Media

### `n.image(source, caption="", width=None, filename=None) -> str`
Display an image. `source` can be file path, URL, PIL Image, or numpy array.

### `n.audio(source, caption="")`
Display an audio player link.

### `n.video(source, caption="")`
Display a video link.

---

## Code Display

### `n.code(source, lang="python")`
Emit a syntax-highlighted code block.

### `n.echo(source, output="")`
Display code and its output together.

```python
n.echo('df = pd.read_csv("data.csv")\nprint(len(df))', "1234")
```

---

## Export & Output

### `n.save() -> Path`
Write the report to disk. Returns `Path` to the saved file.

### `n.to_markdown() -> str`
Return the report content as a markdown string (no file written).

### `n.export_csv(df, filename, name=None) -> str`
Save a DataFrame as CSV artifact. Returns relative path.

### `n.connection_status(name, status="connected", details="")`
Display a data connection status indicator. `status`: `"connected"`, `"disconnected"`, or `"error"`.

---

## Helper Classes

### `_SectionContext`
Returned by `n.section()`. Can be used as context manager (adds divider on exit) or ignored.

### `_TabGroup`
Returned by `n.tabs()`. Use `.tab(label)` as context manager.

### `_ColumnGroup`
Returned by `n.columns()`. Use `.col(index)` as context manager (0-based index).
