# notebookmd

**A Streamlit-like API for generating structured Markdown reports.**

notebookmd lets you build rich, readable Markdown reports using a familiar API. Call `n.metric()`, `n.table()`, `n.line_chart()`, and 40+ other methods to produce clean, structured output -- no browser or notebook server required.

Designed for AI agents doing data analysis, automated pipelines, and anyone who needs programmatic report generation.

## Key Features

- **Streamlit-compatible API** -- methods like `metric()`, `table()`, `bar_chart()`, `expander()` work the way you expect
- **Zero-dependency core** -- text and Markdown output works with no external packages
- **Optional integrations** -- pandas for DataFrames, matplotlib for chart images, Plotly and Altair support
- **Plugin architecture** -- extend with custom widgets via a simple base class
- **Asset management** -- figures, CSVs, and other artifacts are saved and indexed automatically

## Quick Example

```python
from notebookmd import nb

n = nb("output/report.md", title="Sales Report")

n.section("Key Metrics")
n.metric("Revenue", "$1.2M", delta="+12%")
n.metric("Customers", "8,421", delta="+3.2%")

n.section("Monthly Trend")
n.table(monthly_df, name="Monthly Revenue")
n.line_chart(monthly_df, x="month", y="revenue", title="Revenue Over Time")

n.save()
```

This produces a complete Markdown file with formatted metrics, tables, and chart images.

## Documentation

| Page | Description |
|------|-------------|
| [Getting Started](getting-started.md) | Installation, first report, core concepts |
| [Widgets Reference](widgets.md) | All 48 widget methods organized by category |
| [Configuration](configuration.md) | NotebookConfig options and asset management |
| [Plugin System](plugins.md) | Custom plugins, registration, and entry points |
| [API Reference](api-reference.md) | Core classes: Notebook, NotebookConfig, AssetManager |
| [Examples](examples.md) | End-to-end report examples |

## Install

```bash
# Core (zero dependencies)
pip install notebookmd

# With pandas support
pip install "notebookmd[pandas]"

# With chart image rendering
pip install "notebookmd[plotting]"

# Everything
pip install "notebookmd[all]"
```

## Architecture

```
notebookmd/
├── __init__.py          # Public API: nb(), Notebook, NotebookConfig, PluginSpec, register_plugin
├── core.py              # Notebook class -- core engine + plugin loading
├── plugins.py           # PluginSpec base class, global registry, entry-point discovery
├── plugins_builtin.py   # 8 built-in plugins (text, data, charts, status, layout, media, analytics, utility)
├── widgets.py           # 40+ widget renderers (metrics, charts, layout, status)
├── emitters.py          # Low-level Markdown emitters (table, figure, code, kv)
├── capture.py           # Stdout/stderr capture utilities
├── assets.py            # AssetManager -- saves figures, CSVs, tracks artifacts
└── py.typed             # PEP 561 type checking marker
```

The package uses a **core + plugin** architecture. The `Notebook` class is a thin core that handles markdown buffering, asset management, and report lifecycle. All widget methods are provided by 8 built-in plugins that are auto-loaded on import.
