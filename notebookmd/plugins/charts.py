"""Chart widgets plugin: line_chart, area_chart, bar_chart, figure, plotly_chart, altair_chart."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, ClassVar

from ._base import PluginSpec


class ChartPlugin(PluginSpec):
    """Chart widgets: line_chart, area_chart, bar_chart, figure, plotly_chart, altair_chart."""

    name = "charts"
    version = "0.3.0"
    requires: ClassVar[list[str]] = ["matplotlib"]

    def line_chart(
        self,
        data: Any,
        x: str | None = None,
        y: str | Sequence[str] | None = None,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        filename: str | None = None,
    ) -> str | None:
        """Display a line chart (like st.line_chart).

        Returns:
            Relative path to saved chart image, or None if no image was saved.
        """
        from ..emitters import render_figure
        from ..widgets import render_line_chart

        rel = self._try_render_mpl_chart("line", data, x, y, title, x_label, y_label, filename)
        if rel:
            self._w(render_figure(rel, caption=title, filename=rel))
            return rel
        self._w(render_line_chart(data, x=x, y=y, title=title, x_label=x_label, y_label=y_label))
        return None

    def area_chart(
        self,
        data: Any,
        x: str | None = None,
        y: str | Sequence[str] | None = None,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        filename: str | None = None,
    ) -> str | None:
        """Display an area chart (like st.area_chart).

        Returns:
            Relative path to saved chart image, or None.
        """
        from ..emitters import render_figure
        from ..widgets import render_area_chart

        rel = self._try_render_mpl_chart("area", data, x, y, title, x_label, y_label, filename)
        if rel:
            self._w(render_figure(rel, caption=title, filename=rel))
            return rel
        self._w(render_area_chart(data, x=x, y=y, title=title, x_label=x_label, y_label=y_label))
        return None

    def bar_chart(
        self,
        data: Any,
        x: str | None = None,
        y: str | Sequence[str] | None = None,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        horizontal: bool = False,
        filename: str | None = None,
    ) -> str | None:
        """Display a bar chart (like st.bar_chart).

        Returns:
            Relative path to saved chart image, or None.
        """
        from ..emitters import render_figure
        from ..widgets import render_bar_chart

        rel = self._try_render_mpl_chart("barh" if horizontal else "bar", data, x, y, title, x_label, y_label, filename)
        if rel:
            self._w(render_figure(rel, caption=title, filename=rel))
            return rel
        self._w(render_bar_chart(data, x=x, y=y, title=title, x_label=x_label, y_label=y_label, horizontal=horizontal))
        return None

    def figure(self, fig: Any, filename: str, caption: str = "", dpi: int = 160) -> str:
        """Save a matplotlib figure and emit its markdown link.

        Returns:
            Relative path to the saved figure.
        """
        from ..emitters import render_figure

        rel = self._asset_mgr.save_figure(fig, filename, dpi=dpi)
        self._w(render_figure(rel, caption=caption, filename=filename))
        return rel

    def plotly_chart(
        self,
        fig: Any,
        filename: str | None = None,
        caption: str = "",
        use_container_width: bool = True,
    ) -> str:
        """Save and display a Plotly figure (like st.plotly_chart).

        Returns:
            Relative path to the saved chart image.
        """
        from ..widgets import render_plotly_chart

        fname = filename or f"plotly_{self._next_id()}.png"
        rel = self._asset_mgr.save_plotly(fig, fname)
        self._w(render_plotly_chart(rel, caption=caption, use_container_width=use_container_width))
        return rel

    def altair_chart(
        self,
        chart: Any,
        filename: str | None = None,
        caption: str = "",
        use_container_width: bool = True,
    ) -> str:
        """Save and display an Altair/Vega-Lite chart (like st.altair_chart).

        Returns:
            Relative path to the saved chart image.
        """
        from ..widgets import render_altair_chart

        fname = filename or f"altair_{self._next_id()}.png"
        rel = self._asset_mgr.save_altair(chart, fname)
        self._w(render_altair_chart(rel, caption=caption, use_container_width=use_container_width))
        return rel
