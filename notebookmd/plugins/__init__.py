"""Plugin system for notebookmd — enables built-in and community extensions.

Plugins add methods to the Notebook class at runtime. Each plugin declares
a set of methods that get bound to Notebook instances when the plugin is
loaded via ``Notebook.use()`` or auto-discovered through entry points.

Built-in plugins are loaded automatically. Community plugins can be
installed as packages that declare the ``notebookmd.plugins`` entry point.

Example — creating a custom plugin::

    from notebookmd.plugins import PluginSpec

    class MyPlugin(PluginSpec):
        name = "my_plugin"

        def hello(self, message: str) -> None:
            \"\"\"Emit a greeting.\"\"\"
            self._w(f"> Hello: {message}\\n\\n")

    # Register globally so all notebooks get it:
    register_plugin(MyPlugin)

    # Or per-instance:
    n = nb("report.md")
    n.use(MyPlugin)
    n.hello("world")
"""

from ._base import PluginSpec
from ._registry import (
    clear_registry,
    discover_entry_point_plugins,
    get_registered_plugins,
    load_default_plugins,
    register_plugin,
    unregister_plugin,
)
from .analytics import AnalyticsPlugin
from .charts import ChartPlugin
from .data import DataPlugin
from .layout import LayoutPlugin
from .media import MediaPlugin
from .status import StatusPlugin
from .text import TextPlugin
from .utility import UtilityPlugin

BUILTIN_PLUGINS: list[type[PluginSpec]] = [
    TextPlugin,
    DataPlugin,
    ChartPlugin,
    StatusPlugin,
    LayoutPlugin,
    MediaPlugin,
    AnalyticsPlugin,
    UtilityPlugin,
]

__all__ = [
    "AnalyticsPlugin",
    "BUILTIN_PLUGINS",
    "ChartPlugin",
    "DataPlugin",
    "LayoutPlugin",
    "MediaPlugin",
    "PluginSpec",
    "StatusPlugin",
    "TextPlugin",
    "UtilityPlugin",
    "clear_registry",
    "discover_entry_point_plugins",
    "get_registered_plugins",
    "load_default_plugins",
    "register_plugin",
    "unregister_plugin",
]
