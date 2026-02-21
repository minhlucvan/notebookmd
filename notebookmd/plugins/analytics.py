"""Analytics helpers plugin: stat, stats, badge, change, ranking."""

from __future__ import annotations

from typing import Any

from ._base import PluginSpec


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
        from ..widgets import render_stat

        self._w(render_stat(label, value, description=description, fmt=fmt))

    def stats(
        self,
        stats: list[dict[str, Any]],
        separator: str = " \u00b7 ",
    ) -> None:
        """Display multiple inline stats on one line."""
        from ..widgets import render_stats

        self._w(render_stats(stats, separator=separator))

    def badge(self, text: str, style: str = "default") -> None:
        """Display an inline badge/pill label.

        Args:
            text: Badge text.
            style: One of "default", "success", "warning", "error", "info".
        """
        from ..widgets import render_badge

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
        from ..widgets import render_change

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
        from ..widgets import render_ranking

        self._w(render_ranking(label, value, rank=rank, total=total, percentile=percentile, fmt=fmt))
