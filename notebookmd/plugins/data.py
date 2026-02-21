"""Data display plugin: table, dataframe, metric, metric_row, json, kv, summary."""

from __future__ import annotations

from typing import Any, Literal

from ._base import PluginSpec


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
        from ..emitters import render_table

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
        from ..widgets import render_dataframe

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
        from ..widgets import render_metric

        self._w(render_metric(label, value, delta=delta, delta_color=delta_color))

    def metric_row(self, metrics: list[dict[str, Any]]) -> None:
        """Display multiple metrics side-by-side in a single row.

        Args:
            metrics: List of dicts with keys: label, value, delta (optional), delta_color (optional).
        """
        from ..widgets import render_metric_row

        self._w(render_metric_row(metrics))

    def json(self, data: Any, expanded: bool = True) -> None:
        """Display data as formatted JSON (like st.json).

        Args:
            data: Any JSON-serializable object.
            expanded: If True, pretty-print with indentation.
        """
        from ..widgets import render_json

        self._w(render_json(data, expanded=expanded))

    def kv(self, data: dict[str, Any], title: str = "Metrics") -> None:
        """Emit a key-value metrics table."""
        from ..emitters import render_kv

        self._w(render_kv(data, title))

    def summary(self, df_obj: Any, title: str = "Data Summary") -> None:
        """Emit an auto-generated DataFrame summary (shape, nulls, stats)."""
        from ..emitters import render_summary

        self._w(render_summary(df_obj, title))
