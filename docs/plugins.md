# Plugin System

notebookmd uses a plugin architecture to provide all widget methods. The core `Notebook` class handles markdown buffering and asset management, while plugins supply the actual widget methods (`metric()`, `table()`, `line_chart()`, etc.).

## Built-in Plugins

Eight plugins are auto-loaded when you import notebookmd:

| Plugin Class | Name | Methods |
|-------------|------|---------|
| `TextPlugin` | `text` | `title`, `header`, `subheader`, `caption`, `md`, `note`, `code`, `text`, `latex`, `divider` |
| `DataPlugin` | `data` | `table`, `dataframe`, `metric`, `metric_row`, `json`, `kv`, `summary` |
| `ChartPlugin` | `charts` | `line_chart`, `area_chart`, `bar_chart`, `figure`, `plotly_chart`, `altair_chart` |
| `StatusPlugin` | `status` | `success`, `error`, `warning`, `info`, `exception`, `progress`, `toast`, `balloons`, `snow` |
| `LayoutPlugin` | `layout` | `expander`, `container`, `tabs`, `columns` |
| `MediaPlugin` | `media` | `image`, `audio`, `video` |
| `AnalyticsPlugin` | `analytics` | `stat`, `stats`, `badge`, `change`, `ranking` |
| `UtilityPlugin` | `utility` | `write`, `echo`, `empty`, `connection_status`, `export_csv` |

You never need to register these manually -- they're loaded automatically during `import notebookmd`.

## Creating a Custom Plugin

### Basic Plugin

A plugin is a class that inherits from `PluginSpec`. All public methods (those without a leading underscore) are automatically bound to the `Notebook` instance:

```python
from notebookmd.plugins import PluginSpec

class FinancePlugin(PluginSpec):
    name = "finance"
    version = "1.0.0"

    def pe_ratio(self, price: float, earnings: float) -> None:
        """Display a P/E ratio metric."""
        ratio = price / earnings if earnings else float("inf")
        self._w(f"**P/E Ratio:** {ratio:.1f}x\n\n")

    def market_cap(self, shares: float, price: float) -> None:
        """Display market capitalization."""
        cap = shares * price
        self._w(f"**Market Cap:** ${cap:,.0f}\n\n")
```

### How Plugin Methods Work

When a plugin is loaded onto a `Notebook`, each public method is bound so that `self` refers to the **Notebook instance** -- not the plugin instance. This means plugin methods can access:

- **`self._w(text)`** -- append markdown to the report buffer
- **`self.cfg`** -- the `NotebookConfig` instance
- **`self._asset_mgr`** -- the `AssetManager` for saving files
- **`self._next_id()`** -- get a unique counter for filenames
- **`self._ensure_started()`** -- lazily initialize the report
- Any other method on the `Notebook`, including other plugin methods

```python
class MyPlugin(PluginSpec):
    name = "my_plugin"

    def custom_summary(self, data: dict) -> None:
        """Use multiple notebook features in one method."""
        self._ensure_started()
        self._w("### Custom Summary\n\n")

        # Call other plugin methods via self
        self.kv(data, title="Overview")
        self.divider()
        self.success("Summary generated")
```

### Private Helper Methods

Methods with a leading underscore are **not** exposed on the Notebook. Use them for internal logic:

```python
class FinancePlugin(PluginSpec):
    name = "finance"

    def _format_currency(self, value: float) -> str:
        """Private helper -- not available on Notebook."""
        if value >= 1_000_000:
            return f"${value / 1_000_000:.1f}M"
        return f"${value:,.0f}"

    def revenue(self, amount: float) -> None:
        """Public method -- available as n.revenue()."""
        formatted = self._format_currency(amount)
        self._w(f"**Revenue:** {formatted}\n\n")
```

## Registering Plugins

### Per-Instance Registration

Use `n.use()` to add a plugin to a single notebook:

```python
from notebookmd import nb

n = nb("report.md", title="Financial Report")
n.use(FinancePlugin)

# Now available:
n.pe_ratio(150.0, 10.0)
n.market_cap(1_000_000, 150.0)
```

### Global Registration

Use `register_plugin()` to make a plugin available on all notebooks created after registration:

```python
from notebookmd.plugins import register_plugin

register_plugin(FinancePlugin)

# All notebooks now have finance methods
n1 = nb("report1.md")
n1.pe_ratio(150.0, 10.0)  # Works

n2 = nb("report2.md")
n2.pe_ratio(200.0, 12.0)  # Also works
```

### Unregistering

```python
from notebookmd.plugins import unregister_plugin

unregister_plugin("finance")
```

### Inspecting the Registry

```python
from notebookmd.plugins import get_registered_plugins

plugins = get_registered_plugins()
for name, cls in plugins.items():
    print(f"{name}: {cls.__name__} v{cls.version}")
```

## Community Plugins via Entry Points

Package authors can distribute plugins that are auto-discovered when installed. Use the `notebookmd.plugins` entry point group in your `pyproject.toml`:

```toml
[project]
name = "notebookmd-finance"
version = "1.0.0"
dependencies = ["notebookmd"]

[project.entry-points."notebookmd.plugins"]
finance = "notebookmd_finance.plugin:FinancePlugin"
```

When `notebookmd` is imported, it calls `discover_entry_point_plugins()` which scans for all packages that declare this entry point and registers them automatically.

### Package Structure

```
notebookmd-finance/
├── pyproject.toml
└── notebookmd_finance/
    ├── __init__.py
    └── plugin.py          # Contains FinancePlugin(PluginSpec)
```

### `plugin.py`

```python
from notebookmd.plugins import PluginSpec

class FinancePlugin(PluginSpec):
    name = "finance"
    version = "1.0.0"
    requires = ["yfinance"]  # Optional: declare pip extras needed

    def pe_ratio(self, price: float, earnings: float) -> None:
        ratio = price / earnings if earnings else float("inf")
        self._w(f"**P/E Ratio:** {ratio:.1f}x\n\n")
```

Users install your package and the plugin is available immediately:

```bash
pip install notebookmd-finance
```

```python
from notebookmd import nb

n = nb("report.md")
n.pe_ratio(150.0, 10.0)  # Available automatically
```

## PluginSpec API Reference

### Class Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `ClassVar[str]` | `""` | Unique plugin identifier (required) |
| `version` | `ClassVar[str]` | `"0.1.0"` | Plugin version |
| `requires` | `ClassVar[list[str]]` | `[]` | Pip extras needed by this plugin |

### Methods

#### `get_methods() -> dict[str, Any]`

Returns a mapping of method names to callables. By default, collects all public methods (no leading underscore) that are not inherited from `PluginSpec` itself.

Override this if you need custom method selection logic:

```python
class SelectivePlugin(PluginSpec):
    name = "selective"

    def get_methods(self):
        # Only expose specific methods
        return {
            "custom_metric": self.custom_metric,
        }

    def custom_metric(self, label, value):
        self._w(f"**{label}:** {value}\n\n")

    def internal_helper(self):
        # This won't be exposed even though it's public
        pass
```

## Plugin Registry Functions

```python
from notebookmd.plugins import (
    register_plugin,       # Register a plugin globally
    unregister_plugin,     # Remove a plugin by name
    get_registered_plugins, # Get all registered plugins
    clear_registry,        # Clear all plugins (for testing)
    discover_entry_point_plugins,  # Scan for entry-point plugins
    load_default_plugins,  # Register built-ins + discover entry points
)
```

### `register_plugin(plugin_cls)`

Register a `PluginSpec` subclass globally.

**Raises:**
- `TypeError` if `plugin_cls` is not a `PluginSpec` subclass
- `ValueError` if the plugin has no `name`

### `unregister_plugin(name)`

Remove a plugin by its name string.

### `get_registered_plugins() -> dict[str, type[PluginSpec]]`

Returns a copy of the global registry (name -> class).

### `clear_registry()`

Clears all registered plugins. Primarily useful in tests.

### `discover_entry_point_plugins() -> list[type[PluginSpec]]`

Scans for plugins declared via the `notebookmd.plugins` entry point group. Returns a list of discovered classes.

### `load_default_plugins()`

Registers all built-in plugins and discovers entry-point plugins. Called automatically on `import notebookmd`. Safe to call multiple times.

## Full Example: Healthcare Plugin

```python
from notebookmd.plugins import PluginSpec, register_plugin

class HealthcarePlugin(PluginSpec):
    name = "healthcare"
    version = "1.0.0"

    def vital_signs(self, heart_rate: int, bp_sys: int, bp_dia: int, temp: float) -> None:
        """Display patient vital signs as a metric row."""
        self.metric_row([
            {"label": "Heart Rate", "value": f"{heart_rate} bpm"},
            {"label": "Blood Pressure", "value": f"{bp_sys}/{bp_dia}"},
            {"label": "Temperature", "value": f"{temp:.1f}°F"},
        ])

    def diagnosis(self, condition: str, confidence: float, icd_code: str = "") -> None:
        """Display a diagnosis with confidence level."""
        self._ensure_started()
        style = "success" if confidence >= 0.8 else "warning" if confidence >= 0.5 else "error"
        self.badge(condition.upper(), style=style)
        self.stat("Confidence", confidence, fmt=".1%")
        if icd_code:
            self._w(f"ICD-10: `{icd_code}`\n\n")

    def lab_results(self, results: dict[str, tuple[float, str, str]]) -> None:
        """Display lab results with values, units, and reference ranges.

        Args:
            results: Dict mapping test name to (value, unit, reference_range)
        """
        self._w("### Lab Results\n\n")
        self._w("| Test | Value | Unit | Reference |\n")
        self._w("|------|-------|------|-----------|\n")
        for test, (value, unit, ref) in results.items():
            self._w(f"| {test} | {value} | {unit} | {ref} |\n")
        self._w("\n")


# Register globally
register_plugin(HealthcarePlugin)
```

Usage:

```python
from notebookmd import nb

n = nb("output/patient_report.md", title="Patient Report")

n.section("Vital Signs")
n.vital_signs(72, 120, 80, 98.6)

n.section("Diagnosis")
n.diagnosis("Type 2 Diabetes", confidence=0.92, icd_code="E11.9")

n.section("Lab Work")
n.lab_results({
    "Glucose": (126, "mg/dL", "70-100"),
    "HbA1c": (7.2, "%", "<5.7"),
    "Cholesterol": (195, "mg/dL", "<200"),
})

n.save()
```
