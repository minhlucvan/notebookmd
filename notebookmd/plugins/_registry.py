"""Global plugin registry and entry-point discovery for notebookmd."""

from __future__ import annotations

import importlib.metadata
import logging

from ._base import PluginSpec

logger = logging.getLogger(__name__)

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
            plugin_eps = eps.get("notebookmd.plugins", [])  # type: ignore[union-attr, arg-type]

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
    from . import BUILTIN_PLUGINS

    for plugin_cls in BUILTIN_PLUGINS:
        if plugin_cls.name not in _global_registry:
            register_plugin(plugin_cls)

    # Discover and register community plugins from entry points
    for plugin_cls in discover_entry_point_plugins():
        if plugin_cls.name not in _global_registry:
            register_plugin(plugin_cls)
