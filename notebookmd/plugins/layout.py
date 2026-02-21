"""Layout elements plugin: expander, container, tabs, columns."""

from __future__ import annotations

from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import Any

from ._base import PluginSpec


class LayoutPlugin(PluginSpec):
    """Layout elements: expander, container, tabs, columns, section."""

    name = "layout"
    version = "0.3.0"

    @contextmanager
    def expander(self, label: str, expanded: bool = False) -> Generator[None, None, None]:
        """Create a collapsible section (like st.expander).

        Args:
            label: The expander heading.
            expanded: If True, section is open by default.
        """
        from ..widgets import render_expander_end, render_expander_start

        self._w(render_expander_start(label, expanded=expanded))
        yield
        self._w(render_expander_end())

    @contextmanager
    def container(self, border: bool = False) -> Generator[None, None, None]:
        """Create a visual container (like st.container).

        Args:
            border: If True, add a border (rendered as blockquote).
        """
        from ..widgets import render_container_end, render_container_start

        self._w(render_container_start(border=border))
        yield
        self._w(render_container_end(border=border))

    def tabs(self, labels: Sequence[str]) -> Any:
        """Create a tab group (like st.tabs).

        Returns a _TabGroup that yields tab context managers.

        Args:
            labels: List of tab labels.
        """
        from ..widgets import render_tabs_header

        self._w(render_tabs_header(labels))
        # Import here to avoid circular references
        from ..core import _TabGroup

        return _TabGroup(self, labels)

    def columns(self, spec: int | Sequence[float] = 2) -> Any:
        """Create a column layout (like st.columns).

        Args:
            spec: Number of columns or list of relative widths.
        """
        from ..widgets import render_columns_start

        self._w(render_columns_start(spec))
        n = spec if isinstance(spec, int) else len(spec)
        from ..core import _ColumnGroup

        return _ColumnGroup(self, n)
