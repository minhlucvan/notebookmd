# notebookmd — Project Instructions

## Overview

notebookmd is a Python package that provides a **Streamlit-like API** for generating structured
Markdown reports. It is designed for AI agents doing data analysis — agents call `n.metric()`,
`n.table()`, `n.line_chart()` etc. and get clean, structured Markdown output.

## Architecture

The package uses a **core + plugin** architecture. The `Notebook` class is a thin core that
handles markdown buffering, asset management, and report lifecycle. All widget methods
(`metric()`, `table()`, `line_chart()`, etc.) are provided by plugins that are auto-loaded.

```
notebookmd/
├── __init__.py          # Public API: nb(), Notebook, NotebookConfig, PluginSpec, register_plugin
├── core.py              # Notebook class — core engine + plugin loading
├── plugins.py           # PluginSpec base class, global registry, entry-point discovery
├── plugins_builtin.py   # 8 built-in plugins (text, data, charts, status, layout, media, analytics, utility)
├── widgets.py           # 40+ widget renderers (metrics, charts, layout, status)
├── emitters.py          # Low-level Markdown emitters (table, figure, code, kv)
├── capture.py           # Stdout/stderr capture utilities
├── assets.py            # AssetManager — saves figures, CSVs, tracks artifacts
└── py.typed             # PEP 561 type checking marker
```

### Built-in Plugins

| Plugin | Name | Methods |
|--------|------|---------|
| TextPlugin | `text` | title, header, subheader, caption, md, note, code, text, latex, divider |
| DataPlugin | `data` | table, dataframe, metric, metric_row, json, kv, summary |
| ChartPlugin | `charts` | line_chart, area_chart, bar_chart, figure, plotly_chart, altair_chart |
| StatusPlugin | `status` | success, error, warning, info, exception, progress, toast, balloons, snow |
| LayoutPlugin | `layout` | expander, container, tabs, columns |
| MediaPlugin | `media` | image, audio, video |
| AnalyticsPlugin | `analytics` | stat, stats, badge, change, ranking |
| UtilityPlugin | `utility` | write, echo, empty, connection_status, export_csv |

## Key Patterns

### Creating a report
```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(max_table_rows=30)
n = nb("output/report.md", title="My Report", cfg=cfg)

n.section("Section Name")
n.metric("Label", "Value", delta="+10%")
n.table(df, name="Data Table")
n.line_chart(df, x="date", y="value", title="Trend")
n.save()
```

### The `n` variable convention
Always name the Notebook instance `n` (from `nb()`). This keeps code concise and
distinguishes notebookmd from Streamlit's `st` convention.

### Creating a custom plugin
```python
from notebookmd.plugins import PluginSpec, register_plugin

class FinancePlugin(PluginSpec):
    name = "finance"

    def pe_ratio(self, price: float, earnings: float) -> None:
        ratio = price / earnings if earnings else float("inf")
        self._w(f"**P/E Ratio:** {ratio:.1f}x\n\n")

# Global registration (all notebooks get it):
register_plugin(FinancePlugin)

# Or per-instance:
n = nb("report.md")
n.use(FinancePlugin)
n.pe_ratio(150.0, 10.0)
```

### Community plugins via entry points
Package authors can register plugins in their `pyproject.toml`:
```toml
[project.entry-points."notebookmd.plugins"]
my_plugin = "my_package.plugin:MyPlugin"
```

## Dependencies

- **Core**: Zero dependencies (text/markdown only)
- **pandas**: `pip install "notebookmd[pandas]"` — tables, DataFrames, CSV export
- **matplotlib**: `pip install "notebookmd[plotting]"` — chart images
- **All**: `pip install "notebookmd[all]"`

## Testing

```bash
pytest tests/ -v                    # Run all 167 tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests only
```

## Code Style

- Python 3.11+, type hints everywhere
- Black formatting (120 char line length)
- isort with black profile
- Docstrings on all public methods

## Important Rules

- Never break the zero-dependency core — pandas/matplotlib must stay optional
- All optional deps use try/except with graceful fallback messages
- Tests must pass with AND without optional dependencies
- Widget methods should mirror Streamlit's API as closely as possible
- The `section()` method is the primary organizational unit (replaces old `cell()` API)
- Plugin methods receive `self` as the Notebook instance — they can use `self._w()`, `self.cfg`, `self._asset_mgr`, etc.
- Built-in plugins are auto-loaded; community plugins are discovered via `notebookmd.plugins` entry points
- New widgets should be added as methods in the appropriate built-in plugin (or a new plugin)
