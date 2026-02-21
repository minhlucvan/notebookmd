# notebookmd

**Python markup-to-Markdown report generator with Streamlit-like API — built for AI agents doing data analysis.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-128%20passed-brightgreen.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)]()

notebookmd lets AI agents and Python scripts produce rich, structured data analysis reports
using a familiar `st.*`-style API. No Jupyter kernel, no GUI, no execution context needed.
Just call functions and get clean Markdown output — like a human analyst using Streamlit,
Jupyter Notebooks, or Excel, but fully programmatic.

```python
from notebookmd import nb

st = nb("report.md", title="Q4 Revenue Analysis")
st.metric("Revenue", "$4.2M", delta="+18%")
st.line_chart(df, x="month", y="revenue", title="Monthly Trend")
st.table(df.head(), name="Top Performers")
st.success("Analysis complete!")
st.save()
```

---

## Key Features

### Streamlit-Compatible API
Use the same `st.metric()`, `st.line_chart()`, `st.dataframe()`, `st.expander()` patterns
you already know from Streamlit. Drop-in familiar for any Python developer.

### Built for AI Agent Workflows
Designed specifically for LLM agents (Claude, GPT, Gemini, LLaMA) performing autonomous
data analysis. Agents call Python functions sequentially — no interactive cells, no kernel
state, no GUI rendering. The output is structured Markdown that both humans and downstream
agents can read and act on.

### Zero Required Dependencies
Core text and Markdown operations work out of the box with no `pip install` overhead.
Add pandas, matplotlib, plotly, or altair only when you need them.

### 40+ Built-in Widgets
Metrics, charts, tables, DataFrames, JSON, LaTeX, progress bars, badges, status messages,
expanders, tabs, columns, code blocks, and more — all rendering to clean Markdown.

### Graceful Degradation
Missing pandas? Tables show a friendly fallback. Missing matplotlib? Charts emit data
summaries instead. Your agent never crashes due to a missing optional dependency.

### Artifact Management
Figures, CSVs, and data exports are automatically saved to an `assets/` directory with
deduplication, relative path linking, and an auto-generated artifact index in the report.

---

## Installation

```bash
# Core package (zero dependencies)
pip install notebookmd

# With pandas support — tables, DataFrames, CSV export, data summaries
pip install "notebookmd[pandas]"

# With matplotlib support — chart image generation
pip install "notebookmd[plotting]"

# With Plotly interactive charts
pip install "notebookmd[plotly]"

# With Altair/Vega-Lite charts
pip install "notebookmd[altair]"

# Everything included
pip install "notebookmd[all]"

# Development (includes pytest, pandas, matplotlib)
pip install "notebookmd[dev]"
```

**Requirements:** Python 3.11+

---

## Quick Start

### Basic Report

```python
from notebookmd import nb

st = nb("dist/report.md", title="Sales Dashboard")

st.header("Key Metrics")
st.metric("Total Revenue", "$1,234,567", delta="+12.3%")
st.metric("Active Users", "34,521", delta="+2,100")

st.header("Analysis")
st.write("Revenue grew **12.3%** quarter-over-quarter driven by enterprise expansion.")
st.success("All KPIs on track!")

st.save()
```

### Data Analysis with pandas

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/analysis.md", title="Stock Analysis")

df = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=30),
    "close": [95 + i * 0.5 for i in range(30)],
    "volume": [1_000_000 + i * 50_000 for i in range(30)],
})

st.section("Price Data")
st.dataframe(df.head(10), name="Recent Prices")
st.summary(df, title="Statistical Summary")

st.section("Trend")
st.line_chart(df, x="date", y="close", title="30-Day Price Trend")
st.bar_chart(df.tail(7), x="date", y="volume", title="Weekly Volume")

st.section("Export")
st.export_csv(df, "prices.csv", name="Full price data")
st.save()
```

### AI Agent Pattern

```python
from notebookmd import nb

def analyze(query: str, data: dict) -> str:
    """Agent tool: generate a structured analysis report."""
    st = nb("dist/agent_report.md", title=query)

    st.section("Data Overview")
    st.kv(data["metadata"], title="Dataset Info")
    st.table(data["df"].head(), name="Sample Data")

    st.section("Key Findings")
    st.metric_row([
        {"label": "Mean", "value": f"{data['df']['value'].mean():.2f}"},
        {"label": "Std", "value": f"{data['df']['value'].std():.2f}"},
        {"label": "N", "value": f"{len(data['df']):,}"},
    ])
    st.stats([
        {"label": "Min", "value": data["df"]["value"].min(), "fmt": ".2f"},
        {"label": "Max", "value": data["df"]["value"].max(), "fmt": ".2f"},
    ])

    st.section("Conclusion")
    st.badge("BULLISH", style="success")
    st.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f")

    st.save()
    return st.to_markdown()
```

### Sections and Layout

```python
from notebookmd import nb

st = nb("dist/layout_demo.md", title="Structured Report")

# Sections as context managers (add dividers on exit)
with st.section("Setup", "Initialize data sources"):
    st.kv({"Database": "Connected", "API": "Ready"}, title="Status")

# Collapsible sections
with st.expander("Methodology", expanded=True):
    st.write("Multi-factor model combining value, momentum, and quality.")

with st.expander("Raw Data"):
    st.dataframe(df)

# Tab groups
tabs = st.tabs(["Overview", "Technical", "Fundamental"])
with tabs.tab("Overview"):
    st.metric("Price", "$95.40", delta="+1.2%")
with tabs.tab("Technical"):
    st.kv({"RSI": "62.3", "MACD": "Bullish"}, title="Indicators")
with tabs.tab("Fundamental"):
    st.kv({"P/E": "15.2x", "ROE": "22.1%"}, title="Ratios")

st.save()
```

---

## Full API Reference

### Factory

| Function | Description |
|----------|-------------|
| `nb(out_md, title, assets_dir, cfg)` | Create a new Notebook report builder |
| `NotebookConfig(max_table_rows, float_format)` | Configure rendering behavior |

### Text Elements

| Method | Streamlit Equivalent | Description |
|--------|---------------------|-------------|
| `st.title(text)` | `st.title` | Top-level `# heading` |
| `st.header(text, divider)` | `st.header` | Section `## heading` |
| `st.subheader(text, divider)` | `st.subheader` | Subsection `### heading` |
| `st.caption(text)` | `st.caption` | Small italic caption |
| `st.text(body)` | `st.text` | Preformatted monospace text |
| `st.latex(body)` | `st.latex` | LaTeX math expression |
| `st.md(text)` | `st.markdown` | Raw Markdown passthrough |
| `st.code(source, lang)` | `st.code` | Fenced code block |
| `st.divider()` | `st.divider` | Horizontal rule |
| `st.write(*args)` | `st.write` | Auto-format any value type |

### Data Display

| Method | Description |
|--------|-------------|
| `st.metric(label, value, delta, delta_color)` | Single metric card with optional delta arrow |
| `st.metric_row(metrics)` | Multiple metrics side-by-side in one table |
| `st.table(df, name, max_rows)` | DataFrame as Markdown table with truncation |
| `st.dataframe(df, name, max_rows)` | DataFrame display (Streamlit API compat) |
| `st.json(data, expanded)` | Formatted JSON code block |
| `st.kv(data, title)` | Key-value dictionary as Markdown table |
| `st.summary(df, title)` | Auto-generated DataFrame summary (shape, nulls, stats) |

### Charts and Visualization

| Method | Description |
|--------|-------------|
| `st.line_chart(data, x, y, title)` | Line chart — saves PNG if matplotlib available |
| `st.bar_chart(data, x, y, horizontal)` | Bar chart with optional horizontal mode |
| `st.area_chart(data, x, y, title)` | Area chart with fill |
| `st.figure(fig, filename, caption)` | Save any matplotlib figure as PNG |
| `st.plotly_chart(fig, filename)` | Save Plotly figure (PNG or HTML fallback) |
| `st.altair_chart(chart, filename)` | Save Altair/Vega-Lite chart |
| `st.image(source, caption, width)` | Display image from path, URL, PIL, or numpy |

### Status and Feedback

| Method | Description |
|--------|-------------|
| `st.success(body)` | Green success blockquote |
| `st.error(body)` | Red error blockquote |
| `st.warning(body)` | Yellow warning blockquote |
| `st.info(body)` | Blue info blockquote |
| `st.exception(exc)` | Exception display with type and message |
| `st.progress(value, text)` | Text-based progress bar (0.0-1.0) |
| `st.toast(body)` | Toast notification message |
| `st.balloons()` | Celebration marker |
| `st.snow()` | Snow celebration marker |

### Layout and Structure

| Method | Description |
|--------|-------------|
| `st.section(title, description)` | Semantic section (plain call or context manager) |
| `st.expander(label, expanded)` | Collapsible `<details>` section |
| `st.tabs(labels)` | Tab group — iterate with `tabs.tab(label)` |
| `st.columns(spec)` | Column layout — iterate with `cols.col(index)` |
| `st.container(border)` | Visual container with optional border |

### Analytics and Finance Helpers

| Method | Description |
|--------|-------------|
| `st.stat(label, value, description, fmt)` | Single-line statistic with bold value |
| `st.stats(stats, separator)` | Multiple inline stats on one line |
| `st.badge(text, style)` | Inline badge/pill (success, warning, error, info) |
| `st.change(label, current, previous, fmt, pct)` | Value with absolute and percentage change |
| `st.ranking(label, value, rank, total, percentile)` | Value with rank/percentile context |

### Output and Export

| Method | Description |
|--------|-------------|
| `st.save()` | Write report Markdown to disk, returns `Path` |
| `st.to_markdown()` | Get report as string without saving to disk |
| `st.export_csv(df, filename, name)` | Save DataFrame as CSV artifact |

---

## Use Cases

### AI Agent Data Analysis
LLM-powered agents (Claude Code, AutoGPT, CrewAI, LangChain agents) can generate
structured reports during autonomous data analysis workflows. The agent calls notebookmd
functions as tools, producing human-readable output that can be reviewed, shared, or fed
to downstream agents.

### Automated Reporting Pipelines
Replace Jupyter notebooks in CI/CD pipelines. Run a Python script that fetches data,
computes metrics, generates charts, and saves a Markdown report — no notebook kernel needed.

### Financial and Quantitative Analysis
Built-in helpers for metrics, deltas, rankings, percentiles, change indicators, and badges
make notebookmd ideal for stock analysis, portfolio reporting, and financial dashboards.

### Data Science Report Generation
Generate reproducible analysis reports from Python scripts. Export DataFrames as tables,
save matplotlib/plotly/altair charts as images, and create self-contained Markdown documents.

### Multi-Agent Research Systems
In multi-agent architectures, notebookmd serves as the standard output format. One agent
writes the analysis, another reads the structured Markdown to validate or extend findings.

---

## Comparison

| Feature | notebookmd | Jupyter | Streamlit | Plain Markdown |
|---------|-----------|---------|-----------|----------------|
| No kernel needed | Yes | No | No | Yes |
| Agent-friendly API | Yes | No | Partial | No |
| Zero dependencies | Yes | No | No | Yes |
| Rich widgets | 40+ | Unlimited | Unlimited | Manual |
| Structured output | Yes | JSON | HTML | Manual |
| Chart generation | Yes | Yes | Yes | No |
| Artifact management | Built-in | Manual | N/A | Manual |
| CI/CD friendly | Yes | Needs nbconvert | Needs server | Yes |
| Version control friendly | Yes | Difficult | N/A | Yes |

---

## Architecture

```
notebookmd/
├── __init__.py      # Public API: nb() factory, Notebook, NotebookConfig
├── core.py          # Notebook class — full Streamlit-compatible method surface
├── widgets.py       # 40+ widget renderers (metrics, charts, layout, status)
├── emitters.py      # Low-level Markdown emitters (table, figure, code, kv)
├── capture.py       # Stdout/stderr capture utilities for cell execution
├── assets.py        # AssetManager — saves figures, CSVs, tracks artifacts
└── py.typed         # PEP 561 marker for type checking support
```

**Design Principles:**
- **Familiar API** — if you know Streamlit, you know notebookmd
- **Sequential calls** — no cells, no contexts, just function calls in order
- **Structured output** — clean Markdown parseable by humans and LLMs alike
- **Optional everything** — core works with zero dependencies
- **Fail gracefully** — missing deps produce fallback messages, never crashes

---

## Configuration

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(
    max_table_rows=50,      # Max rows before table truncation (default: 30)
    float_format="{:.2f}",  # Number format for floats (default: "{:.4f}")
)

st = nb("report.md", title="Report", cfg=cfg)
```

---

## FAQ

### What is notebookmd?
notebookmd is a Python library that provides a Streamlit-like API (`st.metric()`, `st.table()`,
`st.line_chart()`, etc.) for generating structured Markdown reports. It is designed for
AI agents and automated pipelines that need to produce human-readable data analysis output
without running a Jupyter kernel or Streamlit server.

### How is notebookmd different from Jupyter Notebooks?
Jupyter notebooks require a running kernel and are designed for interactive, human-driven
exploration. notebookmd is a pure Python library that outputs static Markdown files — ideal
for AI agents, CI/CD pipelines, and automated reporting where no GUI or interactivity is needed.

### How is notebookmd different from Streamlit?
Streamlit renders to a live web application and requires a running server. notebookmd uses
the same familiar `st.*` API but renders to Markdown files that can be committed to git,
read by other LLMs, or published anywhere Markdown is supported.

### Can I use notebookmd with AI agents like Claude, GPT, or LangChain?
Yes. notebookmd is specifically designed for AI agent workflows. Agents call functions like
`st.metric()`, `st.table()`, and `st.line_chart()` sequentially — exactly how an LLM
generates tool calls. The structured Markdown output can then be read by humans or parsed
by downstream agents.

### Does notebookmd require pandas or matplotlib?
No. The core package has zero dependencies. pandas adds table and DataFrame support.
matplotlib adds chart image generation. Both are optional — install only what you need
with `pip install "notebookmd[pandas]"` or `pip install "notebookmd[all]"`.

### What chart libraries does notebookmd support?
notebookmd supports **matplotlib**, **Plotly**, and **Altair/Vega-Lite**. When a chart
library is not installed, chart methods emit a text-based data summary instead of crashing.

### Can I use notebookmd in CI/CD pipelines?
Yes. notebookmd is a regular Python library with no server, no kernel, and no GUI.
Run `python generate_report.py` in any CI/CD step and commit the output Markdown.

### What Python versions are supported?
Python 3.11 and above.

### Is notebookmd type-safe?
Yes. The package includes a `py.typed` marker for PEP 561 and works with mypy,
pyright, and other type checkers.

### How do I export data alongside the report?
Use `st.export_csv(df, "data.csv")` to save a DataFrame as a CSV file in the assets
directory. The file is automatically linked in the report's artifact index.

---

## Examples

See the [`examples/`](examples/) directory:

- **[`analysis.py`](examples/analysis.py)** — Financial analysis report with data loading,
  aggregation, charting, and CSV export
- **[`streamlit_widgets.py`](examples/streamlit_widgets.py)** — Comprehensive demo of all
  40+ widgets: metrics, charts, tables, expanders, tabs, badges, and more

Run from the package root:

```bash
python examples/analysis.py
python examples/streamlit_widgets.py
```

---

## Contributing

```bash
# Clone and install in dev mode
git clone https://github.com/minhlucvan/notebookmd.git
cd notebookmd
pip install -e ".[dev]"

# Run tests (128 tests)
pytest tests/ -v

# Run examples
python examples/analysis.py
python examples/streamlit_widgets.py
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Keywords:** python markdown report generator, AI agent data analysis, streamlit alternative,
jupyter notebook alternative, automated reporting python, LLM agent tools, programmatic
markdown, data analysis report, python report builder, agent-readable output, structured
markdown output, zero dependency python, financial analysis python, pandas markdown table,
matplotlib report, plotly markdown, CI/CD reporting, python data visualization to markdown
