# notebookmd

**The notebook for AI agents.** Write Python. Get Markdown reports.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-128%20passed-brightgreen.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)]()

```python
from notebookmd import nb

n = nb("report.md", title="Q4 Revenue Analysis")
n.metric("Revenue", "$4.2M", delta="+18%")
n.line_chart(df, x="month", y="revenue", title="Monthly Trend")
n.table(df.head(), name="Top Performers")
n.success("Analysis complete!")
n.save()
```

---

## The Problem

AI agents are great at data analysis. But when it comes to presenting results, they're stuck
with `print()` statements and unstructured text dumps. Meanwhile:

- **Jupyter** requires a running kernel, interactive cells, and a browser — none of which
  exist in an agent's world
- **Streamlit** needs a live server — great for dashboards, useless for batch analysis
- **Plain Markdown** by hand means every agent reinvents table formatting, chart embedding,
  and report structure from scratch

AI agents think sequentially. They call functions one after another. They need a tool that
works the same way — call a function, get structured output. No kernel. No server. No GUI.

## The Solution

notebookmd is a **Jupyter-style notebook that runs as plain Python function calls** and
outputs clean Markdown. Think of it as `print()`, but for structured reports.

```python
n = nb("dist/analysis.md", title="Stock Analysis")

n.section("Price Data")
n.dataframe(df.head(10), name="Recent Prices")
n.summary(df, title="Statistical Summary")

n.section("Trend")
n.line_chart(df, x="date", y="close", title="30-Day Price Trend")

n.section("Export")
n.export_csv(df, "prices.csv", name="Full price data")
n.save()
```

The output is a self-contained Markdown file with tables, charts (as PNGs), metrics, and an
artifact index — readable by humans, parseable by other agents, committable to git.

---

## Why notebookmd?

### Built for how agents actually work
Agents generate code sequentially — one function call at a time. notebookmd matches that
mental model exactly. No cells, no execution context, no state management. Just call
`n.metric()`, `n.table()`, `n.line_chart()` in order.

### Markdown is the universal format
LLMs read Markdown natively. Humans read Markdown natively. GitHub renders it. CI/CD logs
display it. It's the one format that works everywhere agents operate.

### Zero dependencies by default
The core package needs nothing — not even pandas. Add optional packages only when you need
them. Your agent never crashes because a charting library isn't installed; it degrades
gracefully with a helpful message instead.

### 40+ widgets out of the box
Metrics with delta arrows, DataFrames as tables, line/bar/area charts, collapsible sections,
tabs, JSON display, progress bars, badges, LaTeX math, code blocks — everything you need
for a real analysis report.

### Artifact management built in
Figures and CSVs are auto-saved to an `assets/` directory with deduplication and relative
path linking. The report includes an auto-generated artifact index. No manual file management.

---

## Installation

```bash
# Core package (zero dependencies)
pip install notebookmd

# With pandas — tables, DataFrames, CSV export, data summaries
pip install "notebookmd[pandas]"

# With matplotlib — chart image generation
pip install "notebookmd[plotting]"

# Everything
pip install "notebookmd[all]"
```

**Requirements:** Python 3.11+

---

## Quick Start

### Agent Tool Pattern

The most common use case — wrap notebookmd as an agent tool:

```python
from notebookmd import nb

def analyze(query: str, data: dict) -> str:
    """Agent tool: generate a structured analysis report."""
    n = nb("dist/agent_report.md", title=query)

    n.section("Data Overview")
    n.kv(data["metadata"], title="Dataset Info")
    n.table(data["df"].head(), name="Sample Data")

    n.section("Key Findings")
    n.metric_row([
        {"label": "Mean", "value": f"{data['df']['value'].mean():.2f}"},
        {"label": "Std", "value": f"{data['df']['value'].std():.2f}"},
        {"label": "N", "value": f"{len(data['df']):,}"},
    ])

    n.section("Conclusion")
    n.badge("BULLISH", style="success")
    n.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f")

    n.save()
    return n.to_markdown()
```

### Data Analysis

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/analysis.md", title="Stock Analysis")

df = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=30),
    "close": [95 + i * 0.5 for i in range(30)],
    "volume": [1_000_000 + i * 50_000 for i in range(30)],
})

n.section("Price Data")
n.dataframe(df.head(10), name="Recent Prices")
n.summary(df, title="Statistical Summary")

n.section("Trend")
n.line_chart(df, x="date", y="close", title="30-Day Price Trend")
n.bar_chart(df.tail(7), x="date", y="volume", title="Weekly Volume")

n.section("Export")
n.export_csv(df, "prices.csv", name="Full price data")
n.save()
```

### Sections and Layout

```python
from notebookmd import nb

n = nb("dist/report.md", title="Structured Report")

# Sections as context managers (add dividers on exit)
with n.section("Setup", "Initialize data sources"):
    n.kv({"Database": "Connected", "API": "Ready"}, title="Status")

# Collapsible sections
with n.expander("Methodology", expanded=True):
    n.write("Multi-factor model combining value, momentum, and quality.")

# Tab groups
tabs = n.tabs(["Overview", "Technical", "Fundamental"])
with tabs.tab("Overview"):
    n.metric("Price", "$95.40", delta="+1.2%")
with tabs.tab("Technical"):
    n.kv({"RSI": "62.3", "MACD": "Bullish"}, title="Indicators")

n.save()
```

---

## API Reference

### Factory

| Function | Description |
|----------|-------------|
| `nb(out_md, title, assets_dir, cfg)` | Create a new Notebook report builder |
| `NotebookConfig(max_table_rows, float_format)` | Configure rendering behavior |

### Text Elements

| Method | Description |
|--------|-------------|
| `n.title(text)` | Top-level `# heading` |
| `n.header(text, divider)` | Section `## heading` |
| `n.subheader(text, divider)` | Subsection `### heading` |
| `n.caption(text)` | Small italic caption |
| `n.text(body)` | Preformatted monospace text |
| `n.latex(body)` | LaTeX math expression |
| `n.md(text)` | Raw Markdown passthrough |
| `n.code(source, lang)` | Fenced code block |
| `n.divider()` | Horizontal rule |
| `n.write(*args)` | Auto-format any value type |

### Data Display

| Method | Description |
|--------|-------------|
| `n.metric(label, value, delta, delta_color)` | Single metric card with optional delta arrow |
| `n.metric_row(metrics)` | Multiple metrics side-by-side in one table |
| `n.table(df, name, max_rows)` | DataFrame as Markdown table with truncation |
| `n.dataframe(df, name, max_rows)` | Alias for `table()` |
| `n.json(data, expanded)` | Formatted JSON code block |
| `n.kv(data, title)` | Key-value dictionary as Markdown table |
| `n.summary(df, title)` | Auto-generated DataFrame summary (shape, nulls, stats) |

### Charts and Visualization

| Method | Description |
|--------|-------------|
| `n.line_chart(data, x, y, title)` | Line chart (saves PNG via matplotlib) |
| `n.bar_chart(data, x, y, horizontal)` | Bar chart with optional horizontal mode |
| `n.area_chart(data, x, y, title)` | Area chart with fill |
| `n.figure(fig, filename, caption)` | Save any matplotlib figure as PNG |
| `n.plotly_chart(fig, filename)` | Save Plotly figure (PNG or HTML fallback) |
| `n.altair_chart(chart, filename)` | Save Altair/Vega-Lite chart |
| `n.image(source, caption, width)` | Display image from path, URL, PIL, or numpy |

### Status and Feedback

| Method | Description |
|--------|-------------|
| `n.success(body)` | Green success blockquote |
| `n.error(body)` | Red error blockquote |
| `n.warning(body)` | Yellow warning blockquote |
| `n.info(body)` | Blue info blockquote |
| `n.exception(exc)` | Exception display with type and message |
| `n.progress(value, text)` | Text-based progress bar (0.0-1.0) |
| `n.toast(body)` | Toast notification message |
| `n.balloons()` / `n.snow()` | Celebration markers |

### Layout and Structure

| Method | Description |
|--------|-------------|
| `n.section(title, description)` | Semantic section (plain call or context manager) |
| `n.expander(label, expanded)` | Collapsible `<details>` section |
| `n.tabs(labels)` | Tab group — use with `tabs.tab(label)` |
| `n.columns(spec)` | Column layout — use with `cols.col(index)` |
| `n.container(border)` | Visual container with optional border |

### Analytics Helpers

| Method | Description |
|--------|-------------|
| `n.stat(label, value, description, fmt)` | Single-line statistic with bold value |
| `n.stats(stats, separator)` | Multiple inline stats on one line |
| `n.badge(text, style)` | Inline badge/pill (success, warning, error, info) |
| `n.change(label, current, previous, fmt, pct)` | Value with absolute and percentage change |
| `n.ranking(label, value, rank, total, percentile)` | Value with rank/percentile context |

### Output and Export

| Method | Description |
|--------|-------------|
| `n.save()` | Write report to disk, returns `Path` |
| `n.to_markdown()` | Get report as string without saving |
| `n.export_csv(df, filename, name)` | Save DataFrame as CSV artifact |

---

## How It Compares

| | notebookmd | Jupyter | Streamlit | Plain print() |
|---|-----------|---------|-----------|---------------|
| Works without a kernel | Yes | No | No | Yes |
| Works without a server | Yes | Yes | No | Yes |
| Agent-friendly (sequential calls) | Yes | No | No | Yes |
| Rich widgets (tables, charts, metrics) | 40+ | Unlimited | Unlimited | None |
| Structured, parseable output | Yes | JSON blobs | HTML | No |
| Built-in artifact management | Yes | Manual | N/A | Manual |
| CI/CD and git friendly | Yes | Painful | N/A | Yes |
| Zero dependencies | Yes | No | No | Yes |

---

## Configuration

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(
    max_table_rows=50,      # Max rows before truncation (default: 30)
    float_format="{:.2f}",  # Number format for floats (default: "{:.4f}")
)

n = nb("report.md", title="Report", cfg=cfg)
```

---

## Examples

See [`examples/`](examples/):

- **[`analysis.py`](examples/analysis.py)** — Financial analysis with data loading, aggregation, charting, CSV export
- **[`streamlit_widgets.py`](examples/streamlit_widgets.py)** — All 40+ widgets demo

```bash
python examples/analysis.py
python examples/streamlit_widgets.py
```

---

## Contributing

```bash
git clone https://github.com/minhlucvan/notebookmd.git
cd notebookmd
pip install -e ".[dev]"
pytest tests/ -v
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
