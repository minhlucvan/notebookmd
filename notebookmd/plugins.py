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

from __future__ import annotations

import importlib.metadata
import logging
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


class PluginSpec:
    """Base class for notebookmd plugins.

    Subclass this and define methods that will be bound onto ``Notebook``
    instances. Inside plugin methods, ``self`` refers to the Notebook
    instance, so you can call ``self._w()``, ``self._ensure_started()``,
    ``self._asset_mgr``, ``self.cfg``, etc.

    Class attributes:
        name: Unique plugin identifier (required).
        version: Optional version string.
        requires: Optional list of pip extras this plugin needs (informational).

    Example::

        class DataPlugin(PluginSpec):
            name = "data"
            requires = ["pandas"]

            def table(self, df_obj, name="Table", max_rows=None):
                ...
    """

    name: ClassVar[str] = ""
    version: ClassVar[str] = "0.1.0"
    requires: ClassVar[list[str]] = []

    def get_methods(self) -> dict[str, Any]:
        """Return a mapping of method_name -> callable for this plugin.

        By default, collects all public methods (no leading underscore) that
        are not inherited from PluginSpec itself.
        """
        base_attrs = set(dir(PluginSpec))
        methods: dict[str, Any] = {}
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue
            if attr_name in base_attrs:
                continue
            val = getattr(self, attr_name)
            if callable(val):
                methods[attr_name] = val
        return methods


# ── Global Plugin Registry ────────────────────────────────────────────────────

_global_registry: dict[str, type[PluginSpec]] = {}


def register_plugin(plugin_cls: type[PluginSpec]) -> None:
    """Register a plugin class globally.

    All Notebook instances created after registration will have the
    plugin's methods available.

    Args:
        plugin_cls: A PluginSpec subclass.

    Raises:
        TypeError: If plugin_cls is not a PluginSpec subclass.
        ValueError: If the plugin has no name.
    """
    if not isinstance(plugin_cls, type) or not issubclass(plugin_cls, PluginSpec):
        raise TypeError(f"Expected a PluginSpec subclass, got {plugin_cls!r}")
    if not plugin_cls.name:
        raise ValueError(f"Plugin {plugin_cls!r} must have a non-empty 'name' class attribute.")
    _global_registry[plugin_cls.name] = plugin_cls


def unregister_plugin(name: str) -> None:
    """Remove a plugin from the global registry.

    Args:
        name: The plugin name to unregister.
    """
    _global_registry.pop(name, None)


def get_registered_plugins() -> dict[str, type[PluginSpec]]:
    """Return a copy of the global plugin registry."""
    return dict(_global_registry)


def clear_registry() -> None:
    """Clear all globally registered plugins. Mainly useful for testing."""
    _global_registry.clear()


def discover_entry_point_plugins() -> list[type[PluginSpec]]:
    """Discover plugins declared via the ``notebookmd.plugins`` entry point group.

    Package authors can register plugins in their pyproject.toml::

        [project.entry-points."notebookmd.plugins"]
        my_plugin = "my_package.plugin:MyPlugin"

    Returns:
        List of discovered PluginSpec subclasses.
    """
    discovered: list[type[PluginSpec]] = []
    try:
        eps = importlib.metadata.entry_points()
        # Python 3.12+ returns a SelectableGroups / dict-like, 3.9+ has .select()
        if hasattr(eps, "select"):
            plugin_eps = eps.select(group="notebookmd.plugins")
        else:
            plugin_eps = eps.get("notebookmd.plugins", [])  # type: ignore[union-attr]

        for ep in plugin_eps:
            try:
                cls = ep.load()
                if isinstance(cls, type) and issubclass(cls, PluginSpec) and cls is not PluginSpec:
                    discovered.append(cls)
                else:
                    logger.warning("Entry point %r did not resolve to a PluginSpec subclass.", ep.name)
            except Exception:
                logger.warning("Failed to load plugin entry point %r.", ep.name, exc_info=True)
    except Exception:
        logger.debug("Entry point discovery unavailable.", exc_info=True)

    return discovered


def load_default_plugins() -> None:
    """Register all built-in plugins and discover entry-point plugins.

    Called automatically during package import. Safe to call multiple times.
    """
    from .plugins_builtin import BUILTIN_PLUGINS

    for plugin_cls in BUILTIN_PLUGINS:
        if plugin_cls.name not in _global_registry:
            register_plugin(plugin_cls)

    # Discover and register community plugins from entry points
    for plugin_cls in discover_entry_point_plugins():
        if plugin_cls.name not in _global_registry:
            register_plugin(plugin_cls)
