"""Utility widgets plugin: write, echo, empty, connection_status, export_csv."""

from __future__ import annotations

from typing import Any, Literal

from ._base import PluginSpec


class UtilityPlugin(PluginSpec):
    """Utility widgets: write, echo, empty, connection_status, export_csv."""

    name = "utility"
    version = "0.3.0"

    def write(self, *args: Any) -> None:
        """Auto-format and display any combination of values (like st.write)."""
        from ..widgets import render_write

        self._w(render_write(*args))

    def echo(self, source: str, output: str = "") -> None:
        """Display code and its output together (like st.echo)."""
        from ..widgets import render_echo

        self._w(render_echo(source, output=output))

    def empty(self) -> None:
        """Emit an empty placeholder (like st.empty)."""
        from ..widgets import render_empty

        self._w(render_empty())

    def connection_status(
        self,
        name: str,
        status: Literal["connected", "disconnected", "error"] = "connected",
        details: str = "",
    ) -> None:
        """Display a data connection status indicator."""
        from ..widgets import render_connection_status

        self._w(render_connection_status(name, status=status, details=details))

    def export_csv(self, df: Any, filename: str, name: str | None = None) -> str:
        """Save a DataFrame as CSV and link it in the artifacts.

        Returns:
            Relative path to the saved CSV.
        """
        rel = self._asset_mgr.save_csv(df, filename)
        display_name = name or filename
        self._w(f"**Exported:** [{display_name}]({rel})\n\n")
        return rel
