"""Built-in plugins that ship with notebookmd.

These plugins implement the core Streamlit-compatible API. They are loaded
automatically so existing code works without changes.

Plugin categories:
- TextPlugin: text, headings, markdown, code, latex, divider
- DataPlugin: table, dataframe, metric, metric_row, json, kv, summary
- ChartPlugin: line_chart, area_chart, bar_chart, figure, plotly_chart, altair_chart
- StatusPlugin: success, error, warning, info, exception, progress, toast, balloons, snow
- LayoutPlugin: expander, container, tabs, columns
- MediaPlugin: image, audio, video
- AnalyticsPlugin: stat, stats, badge, change, ranking
- UtilityPlugin: write, echo, empty, connection_status, export_csv
"""

from __future__ import annotations

from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import Any, ClassVar, Literal

from .plugins import PluginSpec

# ── Text Elements ─────────────────────────────────────────────────────────────


class TextPlugin(PluginSpec):
    """Text elements: title, header, subheader, caption, md, note, code, text, latex, divider."""

    name = "text"
    version = "0.3.0"

    def title(self, text: str, anchor: str | None = None) -> None:
        """Emit a title heading (like st.title).

        Args:
            text: Title text.
            anchor: Optional HTML anchor ID.
        """
        from .widgets import render_title

        self._ensure_started()
        self._w(render_title(text, anchor=anchor))

    def header(self, text: str, anchor: str | None = None, divider: bool = False) -> None:
        """Emit a section header (like st.header).

        Args:
            text: Header text.
            anchor: Optional HTML anchor ID.
            divider: If True, add a horizontal rule below.
        """
        from .widgets import render_header

        self._ensure_started()
        self._w(render_header(text, anchor=anchor, divider=divider))

    def subheader(self, text: str, anchor: str | None = None, divider: bool = False) -> None:
        """Emit a subheader (like st.subheader).

        Args:
            text: Subheader text.
            anchor: Optional HTML anchor ID.
            divider: If True, add a horizontal rule below.
        """
        from .widgets import render_subheader

        self._ensure_started()
        self._w(render_subheader(text, anchor=anchor, divider=divider))

    def caption(self, text: str) -> None:
        """Emit small caption text (like st.caption).

        Args:
            text: Caption text.
        """
        from .widgets import render_caption

        self._w(render_caption(text))

    def md(self, text: str) -> None:
        """Emit raw markdown text."""
        from .emitters import render_md

        self._w(render_md(text))

    def note(self, text: str) -> None:
        """Emit a callout / note blockquote."""
        from .emitters import render_note

        self._w(render_note(text))

    def code(self, source: str, lang: str = "python") -> None:
        """Emit a fenced code block."""
        from .emitters import render_code

        self._w(render_code(source, lang))

    def text(self, body: str) -> None:
        """Emit fixed-width preformatted text (like st.text).

        Args:
            body: Plain text to render in monospace.
        """
        from .widgets import render_text

        self._w(render_text(body))

    def latex(self, body: str) -> None:
        """Emit a LaTeX math expression (like st.latex).

        Args:
            body: LaTeX expression string.
        """
        from .widgets import render_latex

        self._w(render_latex(body))

    def divider(self) -> None:
        """Emit a horizontal divider (like st.divider)."""
        from .widgets import render_divider

        self._w(render_divider())


# ── Data Display ──────────────────────────────────────────────────────────────


class DataPlugin(PluginSpec):
    """Data display: table, dataframe, metric, metric_row, json, kv, summary."""

    name = "data"
    version = "0.3.0"

    def table(
        self,
        data: Any,
        name: str = "Table",
        max_rows: int | None = None,
        columns: list[str] | None = None,
    ) -> None:
        """Emit tabular data as a markdown table with truncation.

        Accepts plain-Python structures (list of dicts, list of lists,
        column-oriented dict) with zero dependencies, or a pandas DataFrame
        when pandas is installed.

        Args:
            data: Tabular data or a pandas DataFrame.
            name: Section heading for the table.
            max_rows: Maximum rows to display before truncation.
            columns: Explicit column headers (overrides auto-detected headers).
        """
        from .emitters import render_table

        n = max_rows if max_rows is not None else self.cfg.max_table_rows
        self._w(render_table(data, name=name, max_rows=n, columns=columns))

    def dataframe(
        self, df_obj: Any, name: str = "", max_rows: int | None = None, use_container_width: bool = False
    ) -> None:
        """Display a DataFrame (like st.dataframe).

        Args:
            df_obj: A pandas DataFrame.
            name: Optional heading for the table.
            max_rows: Maximum rows to display.
            use_container_width: Ignored (API compat with Streamlit).
        """
        from .widgets import render_dataframe

        n = max_rows if max_rows is not None else self.cfg.max_table_rows
        self._w(render_dataframe(df_obj, name=name, max_rows=n, use_container_width=use_container_width))

    def metric(
        self,
        label: str,
        value: Any,
        delta: Any | None = None,
        delta_color: Literal["normal", "inverse", "off"] = "normal",
    ) -> None:
        """Display a metric card with optional delta indicator (like st.metric).

        Args:
            label: Short description of the metric.
            value: The primary metric value.
            delta: Optional change from previous value.
            delta_color: "normal" (green up / red down), "inverse", or "off".
        """
        from .widgets import render_metric

        self._w(render_metric(label, value, delta=delta, delta_color=delta_color))

    def metric_row(self, metrics: list[dict[str, Any]]) -> None:
        """Display multiple metrics side-by-side in a single row.

        Args:
            metrics: List of dicts with keys: label, value, delta (optional), delta_color (optional).
        """
        from .widgets import render_metric_row

        self._w(render_metric_row(metrics))

    def json(self, data: Any, expanded: bool = True) -> None:
        """Display data as formatted JSON (like st.json).

        Args:
            data: Any JSON-serializable object.
            expanded: If True, pretty-print with indentation.
        """
        from .widgets import render_json

        self._w(render_json(data, expanded=expanded))

    def kv(self, data: dict[str, Any], title: str = "Metrics") -> None:
        """Emit a key-value metrics table."""
        from .emitters import render_kv

        self._w(render_kv(data, title))

    def summary(self, df_obj: Any, title: str = "Data Summary") -> None:
        """Emit an auto-generated DataFrame summary (shape, nulls, stats)."""
        from .emitters import render_summary

        self._w(render_summary(df_obj, title))


# ── Chart Widgets ─────────────────────────────────────────────────────────────


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
        from .emitters import render_figure
        from .widgets import render_line_chart

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
        from .emitters import render_figure
        from .widgets import render_area_chart

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
        from .emitters import render_figure
        from .widgets import render_bar_chart

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
        from .emitters import render_figure

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
        from .widgets import render_plotly_chart

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
        from .widgets import render_altair_chart

        fname = filename or f"altair_{self._next_id()}.png"
        rel = self._asset_mgr.save_altair(chart, fname)
        self._w(render_altair_chart(rel, caption=caption, use_container_width=use_container_width))
        return rel


# ── Status Elements ───────────────────────────────────────────────────────────


class StatusPlugin(PluginSpec):
    """Status elements: success, error, warning, info, exception, progress, toast, balloons, snow."""

    name = "status"
    version = "0.3.0"

    def success(self, body: str, icon: str = "\u2705") -> None:
        """Emit a success message (like st.success)."""
        from .widgets import render_success

        self._w(render_success(body, icon=icon))

    def error(self, body: str, icon: str = "\u274c") -> None:
        """Emit an error message (like st.error)."""
        from .widgets import render_error

        self._w(render_error(body, icon=icon))

    def warning(self, body: str, icon: str = "\u26a0\ufe0f") -> None:
        """Emit a warning message (like st.warning)."""
        from .widgets import render_warning

        self._w(render_warning(body, icon=icon))

    def info(self, body: str, icon: str = "\u2139\ufe0f") -> None:
        """Emit an info message (like st.info)."""
        from .widgets import render_info

        self._w(render_info(body, icon=icon))

    def exception(self, exc: Exception) -> None:
        """Display an exception (like st.exception).

        Args:
            exc: The exception to display.
        """
        from .widgets import render_exception

        self._w(render_exception(exc))

    def progress(self, value: float, text: str = "") -> None:
        """Emit a progress bar (like st.progress).

        Args:
            value: Progress from 0.0 to 1.0.
            text: Optional label text.
        """
        from .widgets import render_progress

        self._w(render_progress(value, text=text))

    def toast(self, body: str, icon: str = "\U0001f514") -> None:
        """Emit a toast notification (like st.toast)."""
        from .widgets import render_toast

        self._w(render_toast(body, icon=icon))

    def balloons(self) -> None:
        """Emit a balloons celebration marker (like st.balloons)."""
        from .widgets import render_balloons

        self._w(render_balloons())

    def snow(self) -> None:
        """Emit a snow celebration marker (like st.snow)."""
        from .widgets import render_snow

        self._w(render_snow())


# ── Layout Elements ───────────────────────────────────────────────────────────


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
        from .widgets import render_expander_end, render_expander_start

        self._w(render_expander_start(label, expanded=expanded))
        yield
        self._w(render_expander_end())

    @contextmanager
    def container(self, border: bool = False) -> Generator[None, None, None]:
        """Create a visual container (like st.container).

        Args:
            border: If True, add a border (rendered as blockquote).
        """
        from .widgets import render_container_end, render_container_start

        self._w(render_container_start(border=border))
        yield
        self._w(render_container_end(border=border))

    def tabs(self, labels: Sequence[str]) -> Any:
        """Create a tab group (like st.tabs).

        Returns a _TabGroup that yields tab context managers.

        Args:
            labels: List of tab labels.
        """
        from .widgets import render_tabs_header

        self._w(render_tabs_header(labels))
        # Import here to avoid circular references
        from .core import _TabGroup

        return _TabGroup(self, labels)

    def columns(self, spec: int | Sequence[float] = 2) -> Any:
        """Create a column layout (like st.columns).

        Args:
            spec: Number of columns or list of relative widths.
        """
        from .widgets import render_columns_start

        self._w(render_columns_start(spec))
        n = spec if isinstance(spec, int) else len(spec)
        from .core import _ColumnGroup

        return _ColumnGroup(self, n)


# ── Media Elements ────────────────────────────────────────────────────────────


class MediaPlugin(PluginSpec):
    """Media elements: image, audio, video."""

    name = "media"
    version = "0.3.0"

    def image(
        self,
        source: Any,
        caption: str = "",
        width: int | None = None,
        filename: str | None = None,
    ) -> str:
        """Display an image (like st.image).

        Supports file paths, URLs, or raw image data (PIL/numpy).

        Returns:
            Path or URL to the image.
        """
        from .widgets import render_image

        if isinstance(source, str):
            self._w(render_image(source, caption=caption, width=width))
            return source

        fname = filename or f"image_{self._next_id()}.png"
        rel = self._asset_mgr.save_image(source, fname)
        self._w(render_image(rel, caption=caption, width=width))
        return rel

    def audio(self, source: str, caption: str = "") -> None:
        """Display an audio player link (like st.audio)."""
        from .widgets import render_audio

        self._w(render_audio(source, caption=caption))

    def video(self, source: str, caption: str = "") -> None:
        """Display a video link (like st.video)."""
        from .widgets import render_video

        self._w(render_video(source, caption=caption))


# ── Analytics Helpers ─────────────────────────────────────────────────────────


class AnalyticsPlugin(PluginSpec):
    """Analytics-oriented helpers: stat, stats, badge, change, ranking."""

    name = "analytics"
    version = "0.3.0"

    def stat(
        self,
        label: str,
        value: Any,
        description: str = "",
        fmt: str | None = None,
    ) -> None:
        """Display a single-line statistic with bold value and optional context."""
        from .widgets import render_stat

        self._w(render_stat(label, value, description=description, fmt=fmt))

    def stats(
        self,
        stats: list[dict[str, Any]],
        separator: str = " \u00b7 ",
    ) -> None:
        """Display multiple inline stats on one line."""
        from .widgets import render_stats

        self._w(render_stats(stats, separator=separator))

    def badge(self, text: str, style: str = "default") -> None:
        """Display an inline badge/pill label.

        Args:
            text: Badge text.
            style: One of "default", "success", "warning", "error", "info".
        """
        from .widgets import render_badge

        self._w(render_badge(text, style=style))

    def change(
        self,
        label: str,
        current: float,
        previous: float,
        fmt: str = ".2f",
        pct: bool = True,
        invert: bool = False,
    ) -> None:
        """Display a value with absolute and percentage change."""
        from .widgets import render_change

        self._w(render_change(label, current, previous, fmt=fmt, pct=pct, invert=invert))

    def ranking(
        self,
        label: str,
        value: Any,
        rank: int | None = None,
        total: int | None = None,
        percentile: float | None = None,
        fmt: str | None = None,
    ) -> None:
        """Display a value with rank/percentile context."""
        from .widgets import render_ranking

        self._w(render_ranking(label, value, rank=rank, total=total, percentile=percentile, fmt=fmt))


# ── Utility Widgets ───────────────────────────────────────────────────────────


class UtilityPlugin(PluginSpec):
    """Utility widgets: write, echo, empty, connection_status, export_csv."""

    name = "utility"
    version = "0.3.0"

    def write(self, *args: Any) -> None:
        """Auto-format and display any combination of values (like st.write)."""
        from .widgets import render_write

        self._w(render_write(*args))

    def echo(self, source: str, output: str = "") -> None:
        """Display code and its output together (like st.echo)."""
        from .widgets import render_echo

        self._w(render_echo(source, output=output))

    def empty(self) -> None:
        """Emit an empty placeholder (like st.empty)."""
        from .widgets import render_empty

        self._w(render_empty())

    def connection_status(
        self,
        name: str,
        status: Literal["connected", "disconnected", "error"] = "connected",
        details: str = "",
    ) -> None:
        """Display a data connection status indicator."""
        from .widgets import render_connection_status

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


# ── Registry of all built-in plugins ─────────────────────────────────────────

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
