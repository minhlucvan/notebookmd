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

### `st.title(text, anchor=None)`
Emit a title heading (`# Title`).

### `st.header(text, anchor=None, divider=False)`
Emit a section header (`## Header`). Set `divider=True` to add `---` below.

### `st.subheader(text, anchor=None, divider=False)`
Emit a subheader (`### Sub`). Set `divider=True` to add `---` below.

### `st.caption(text)`
Emit small caption text (`_Caption text_`).

### `st.md(text)`
Emit raw markdown text. Passes through unchanged.

### `st.note(text)`
Emit a callout blockquote (`> **Note:** text`).

### `st.code(source, lang="python")`
Emit a fenced code block with syntax highlighting.

### `st.text(body)`
Emit fixed-width preformatted text in a code block.

### `st.latex(body)`
Emit a LaTeX math expression (`$$..$$`).

### `st.divider()`
Emit a horizontal rule (`---`).

### `st.write(*args)`
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

### `st.section(title, description="")`
Start a new section with `## Title`. Can be used as context manager:

```python
# Plain call
st.section("Metrics")
st.metric("Revenue", "$1.2M")

# Context manager (adds divider on exit)
with st.section("Analysis"):
    st.write("Content")
```

### `st.expander(label, expanded=False)` — context manager
Create a collapsible section.

```python
with st.expander("Show details"):
    st.table(df)
```

### `st.container(border=False)` — context manager
Create a visual container. `border=True` renders as blockquote.

### `st.tabs(labels) -> _TabGroup`
Create tab sections. Returns a `_TabGroup` with `.tab(label)` context manager.

```python
tabs = st.tabs(["Overview", "Details"])
with tabs.tab("Overview"):
    st.metric("Revenue", "$1.2M")
with tabs.tab("Details"):
    st.table(df)
```

### `st.columns(spec) -> _ColumnGroup`
Create column layout. `spec` is int (number of columns) or list of relative widths.

```python
cols = st.columns(3)
with cols.col(0):
    st.metric("A", "100")
with cols.col(1):
    st.metric("B", "200")
```

---

## Metrics & KPIs

### `st.metric(label, value, delta=None, delta_color="normal")`
Display a metric card with optional delta indicator.

| Parameter | Type | Description |
|-----------|------|-------------|
| `label` | `str` | Short metric description |
| `value` | `Any` | Primary metric value |
| `delta` | `Any \| None` | Change from previous value |
| `delta_color` | `"normal" \| "inverse" \| "off"` | Delta coloring behavior |

### `st.metric_row(metrics)`
Display multiple metrics side-by-side.

```python
st.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])
```

Each dict supports keys: `label` (required), `value` (required), `delta` (optional), `delta_color` (optional).

### `st.kv(data, title="Metrics")`
Display a key-value dictionary as a formatted table.

```python
st.kv({"LTV": "$14,400", "CAC": "$2,100", "Ratio": "6.9x"}, title="Unit Economics")
```

---

## Data Display

### `st.table(df_obj, name="Table", max_rows=None)`
Display a DataFrame as a markdown table. Uses `cfg.max_table_rows` if `max_rows` not set.

### `st.dataframe(df_obj, name="", max_rows=None, use_container_width=False)`
Display a DataFrame (alias with Streamlit-compatible signature).

### `st.summary(df_obj, title="Data Summary")`
Auto-generate a statistical summary: shape, null counts, numeric stats.

### `st.json(data, expanded=True)`
Display any JSON-serializable object as a formatted JSON code block.

---

## Charts

### `st.line_chart(data, x=None, y=None, title="", x_label="", y_label="", filename=None) -> str|None`
Display a line chart. Returns relative path to saved image if matplotlib available.

### `st.area_chart(data, x=None, y=None, title="", x_label="", y_label="", filename=None) -> str|None`
Display an area chart. Returns relative path to saved image if matplotlib available.

### `st.bar_chart(data, x=None, y=None, title="", x_label="", y_label="", horizontal=False, filename=None) -> str|None`
Display a bar chart. Set `horizontal=True` for horizontal bars.

### `st.figure(fig, filename, caption="", dpi=160) -> str`
Save a matplotlib figure and embed it. Returns relative path.

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(x, y)
st.figure(fig, "my_chart.png", caption="Custom Chart")
```

### `st.plotly_chart(fig, filename=None, caption="", use_container_width=True) -> str`
Save and display a Plotly figure. Auto-generates filename if not provided.

### `st.altair_chart(chart, filename=None, caption="", use_container_width=True) -> str`
Save and display an Altair/Vega-Lite chart.

---

## Analytics Helpers

### `st.stat(label, value, description="", fmt=None)`
Display a single-line statistic.

```python
st.stat("Average Price", 95.4, fmt=".2f")
st.stat("Total", 1_234_567, description="All-time total", fmt=",.0f")
st.stat("Return", 0.123, "annualized", fmt=".1%")
```

### `st.stats(stats, separator=" · ")`
Display multiple inline stats on one line.

```python
st.stats([
    {"label": "Mean", "value": 95.4, "fmt": ".2f"},
    {"label": "Std", "value": 3.2, "fmt": ".2f"},
    {"label": "N", "value": 1000, "fmt": ",d"},
])
```

Each dict keys: `label` (required), `value` (required), `fmt` (optional), `description` (optional).

### `st.badge(text, style="default")`
Display an inline badge/pill label.

| Style | Use |
|-------|-----|
| `"success"` | Positive signal (BULLISH, ON TRACK, PASS) |
| `"warning"` | Caution signal (HOLD, AT RISK, SLOW) |
| `"error"` | Negative signal (BEARISH, FAIL, CRITICAL) |
| `"info"` | Neutral information (Q4 2026, BETA) |
| `"default"` | Plain badge |

### `st.change(label, current, previous, fmt=".2f", pct=True, invert=False)`
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
st.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f", pct=True)
# Output: **Revenue**: 1,200,000 (▲ +200,000 / +20.0%)
```

### `st.ranking(label, value, rank=None, total=None, percentile=None, fmt=None)`
Display a value with rank/percentile context.

```python
st.ranking("Product A", value="$1.2M", rank=1, total=50)
st.ranking("Strategy X", value="12.3%", rank=3, total=20, percentile=85)
```

---

## Status Messages

### `st.success(body, icon="✅")`
Emit a success callout (`> **Success:** body`).

### `st.error(body, icon="❌")`
Emit an error callout (`> **Error:** body`).

### `st.warning(body, icon="⚠️")`
Emit a warning callout (`> **Warning:** body`).

### `st.info(body, icon="ℹ️")`
Emit an info callout (`> **Info:** body`).

### `st.exception(exc)`
Display an exception with traceback info.

### `st.progress(value, text="")`
Emit a text-based progress bar. `value` is 0.0 to 1.0.

### `st.toast(body, icon="🔔")`
Emit a toast notification callout.

### `st.balloons()`
Emit a celebration marker.

### `st.snow()`
Emit a snow celebration marker.

---

## Media

### `st.image(source, caption="", width=None, filename=None) -> str`
Display an image. `source` can be file path, URL, PIL Image, or numpy array.

### `st.audio(source, caption="")`
Display an audio player link.

### `st.video(source, caption="")`
Display a video link.

---

## Code Display

### `st.code(source, lang="python")`
Emit a syntax-highlighted code block.

### `st.echo(source, output="")`
Display code and its output together.

```python
st.echo('df = pd.read_csv("data.csv")\nprint(len(df))', "1234")
```

---

## Export & Output

### `st.save() -> Path`
Write the report to disk. Returns `Path` to the saved file.

### `st.to_markdown() -> str`
Return the report content as a markdown string (no file written).

### `st.export_csv(df, filename, name=None) -> str`
Save a DataFrame as CSV artifact. Returns relative path.

### `st.connection_status(name, status="connected", details="")`
Display a data connection status indicator. `status`: `"connected"`, `"disconnected"`, or `"error"`.

---

## Helper Classes

### `_SectionContext`
Returned by `st.section()`. Can be used as context manager (adds divider on exit) or ignored.

### `_TabGroup`
Returned by `st.tabs()`. Use `.tab(label)` as context manager.

### `_ColumnGroup`
Returned by `st.columns()`. Use `.col(index)` as context manager (0-based index).
