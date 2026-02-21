"""PluginSpec — base class for all notebookmd plugins.

Subclass this and define methods that will be bound onto ``Notebook``
instances. Inside plugin methods, ``self`` refers to the Notebook
instance, so you can call ``self._w()``, ``self._ensure_started()``,
``self._asset_mgr``, ``self.cfg``, etc.

Example::

    from notebookmd.plugins import PluginSpec

    class MyPlugin(PluginSpec):
        name = "my_plugin"

        def hello(self, message: str) -> None:
            \"\"\"Emit a greeting.\"\"\"
            self._w(f"> Hello: {message}\\n\\n")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..assets import AssetManager
    from ..core import NotebookConfig


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

    # -- Type stubs for the Notebook interface --
    # At runtime, plugin methods are bound to Notebook instances via
    # types.MethodType, so ``self`` is actually a Notebook.  These stubs
    # let mypy see the Notebook attributes that plugins use.
    if TYPE_CHECKING:
        cfg: NotebookConfig
        _asset_mgr: AssetManager

        def _w(self, s: str) -> None: ...
        def _ensure_started(self) -> None: ...
        def _next_id(self) -> int: ...
        def _try_render_mpl_chart(
            self,
            chart_type: str,
            data: Any,
            x: str | None,
            y: str | Sequence[str] | None,
            title: str,
            x_label: str,
            y_label: str,
            filename: str | None,
        ) -> str | None: ...

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
