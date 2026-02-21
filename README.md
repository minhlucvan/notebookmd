# notebookmd

**Streamlit-like API for AI agents to generate structured Markdown reports.**

notebookmd lets AI agents produce rich, human-readable data analysis reports using
a familiar `st.*`-style API — no cells, no execution contexts, no Jupyter kernel.
Just call functions sequentially and get clean, agent-readable Markdown output.

## Why notebookmd?

AI agents doing data analysis need a way to produce structured output that is:

- **Readable by humans** — Markdown renders everywhere (GitHub, VS Code, docs sites)
- **Readable by other agents** — downstream LLMs can parse the structured sections
- **Easy to produce** — no notebook kernel, no GUI, just Python function calls
- **Minimal dependencies** — zero required deps; pandas/matplotlib/plotly are optional

notebookmd bridges the gap between Jupyter notebooks (interactive, human-driven) and
plain text logs (unstructured, hard to parse). It gives agents the expressive power
of a notebook with the simplicity of a script.

## Installation

```bash
# Core (zero dependencies)
pip install notebookmd

# With pandas support (tables, DataFrames, CSV export)
pip install notebookmd[pandas]

# With matplotlib support (chart images)
pip install notebookmd[plotting]

# Everything
pip install notebookmd[all]
```

## Quick Start

```python
from notebookmd import nb

st = nb("dist/report.md", title="VCB Investment Analysis")

st.header("Key Metrics")
st.metric("ROE", "22.5%", delta="+4.5%")
st.metric_row([
    {"label": "P/E", "value": "15.2x"},
    {"label": "P/B", "value": "2.3x"},
    {"label": "Dividend", "value": "1.2%"},
])

st.header("Price Trend")
st.line_chart(df, x="date", y="close", title="VCB Close Price")
st.dataframe(df.head(), name="Recent Prices")

st.header("Analysis")
st.write("VCB shows **strong fundamentals** with best-in-class ROE.")
st.success("Analysis complete!")

with st.expander("Raw Data"):
    st.dataframe(df)

st.save()
```

## API Reference

### Factory

| Function | Description |
|----------|-------------|
| `nb(out_md, title, assets_dir, cfg)` | Create a new report builder |

### Text Elements

| Method | Streamlit Equivalent |
|--------|---------------------|
| `st.title(text)` | `st.title` |
| `st.header(text)` | `st.header` |
| `st.subheader(text)` | `st.subheader` |
| `st.caption(text)` | `st.caption` |
| `st.text(body)` | `st.text` |
| `st.latex(body)` | `st.latex` |
| `st.md(text)` | `st.markdown` |
| `st.code(source, lang)` | `st.code` |
| `st.divider()` | `st.divider` |
| `st.write(*args)` | `st.write` |

### Data Display

| Method | Description |
|--------|-------------|
| `st.metric(label, value, delta)` | Single metric card with delta |
| `st.metric_row(metrics)` | Multiple metrics side-by-side |
| `st.table(df, name)` | DataFrame as markdown table |
| `st.dataframe(df, name)` | DataFrame display |
| `st.json(data)` | Formatted JSON |
| `st.kv(data, title)` | Key-value table |
| `st.summary(df)` | Auto-generated DataFrame summary |

### Charts

| Method | Description |
|--------|-------------|
| `st.line_chart(data, x, y)` | Line chart (matplotlib if available) |
| `st.bar_chart(data, x, y)` | Bar chart |
| `st.area_chart(data, x, y)` | Area chart |
| `st.figure(fig, filename)` | Save matplotlib figure |
| `st.plotly_chart(fig)` | Save Plotly figure |
| `st.altair_chart(chart)` | Save Altair chart |

### Status Elements

| Method | Description |
|--------|-------------|
| `st.success(body)` | Success message |
| `st.error(body)` | Error message |
| `st.warning(body)` | Warning message |
| `st.info(body)` | Info message |
| `st.progress(value, text)` | Progress bar |
| `st.exception(exc)` | Exception display |

### Layout

| Method | Description |
|--------|-------------|
| `st.section(title)` | Semantic section (plain call or context manager) |
| `st.expander(label)` | Collapsible section (context manager) |
| `st.tabs(labels)` | Tab group |
| `st.columns(spec)` | Column layout |
| `st.container(border)` | Visual container |

### Analytics Helpers

| Method | Description |
|--------|-------------|
| `st.stat(label, value)` | Single-line statistic |
| `st.stats(stats)` | Multiple inline stats |
| `st.badge(text, style)` | Inline badge/pill |
| `st.change(label, current, previous)` | Value with change indicator |
| `st.ranking(label, value, rank)` | Value with rank/percentile |

### Output

| Method | Description |
|--------|-------------|
| `st.save()` | Write report to disk |
| `st.to_markdown()` | Get markdown string without saving |
| `st.export_csv(df, filename)` | Save DataFrame as CSV artifact |

## Architecture

```
notebookmd/
├── __init__.py      # Public API: nb() factory, Notebook, NotebookConfig
├── core.py          # Notebook class — orchestrates sections, emitters, assets
├── widgets.py       # Streamlit-compatible widget renderers (metric, chart, layout)
├── emitters.py      # Low-level markdown emitters (table, figure, code, kv)
├── capture.py       # Stdout/stderr capture utilities
├── assets.py        # AssetManager — saves figures, CSVs, tracks artifacts
└── py.typed         # PEP 561 marker for type checking support
```

## License

MIT
