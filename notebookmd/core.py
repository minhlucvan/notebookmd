"""Core Notebook (Streamlit-like report builder) implementation.

The Notebook class is the central hub. All widget methods (metric, table,
line_chart, etc.) are provided by plugins that are automatically loaded.
Built-in plugins cover the full Streamlit-compatible API. Community plugins
can add new methods via entry points or ``Notebook.use()``.
"""

from __future__ import annotations

import types
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Sequence

from .assets import AssetManager
from .widgets import render_column_separator, render_columns_end, render_tab_end, render_tab_start


@dataclass
class NotebookConfig:
    """Configuration for report rendering behavior."""

    max_table_rows: int = 30
    float_format: str = "{:.4f}"


class Notebook:
    """Streamlit-like report builder that renders to markdown.

    Designed for AI agents to generate data analysis reports with a familiar
    ``n.*``-style API.  Just call methods sequentially — no cells, no
    execution contexts, no stdout capture.

    Methods like ``metric()``, ``table()``, ``line_chart()`` etc. are provided
    by plugins (see ``notebookmd.plugins``). All built-in plugins are loaded
    automatically, so the API works out of the box.

    Usage::

        n = Notebook("dist/report.md", title="My Analysis")

        n.header("Key Metrics")
        n.metric("Revenue", "$1.2M", delta="+12%")
        n.table(df.head(), name="Preview")

        n.header("Charts")
        n.line_chart(df, x="date", y="close", title="Price Trend")

        n.success("Analysis complete!")
        n.save()

    Custom plugins::

        from notebookmd.plugins import PluginSpec

        class MyPlugin(PluginSpec):
            name = "my_plugin"
            def greet(self, msg: str) -> None:
                self._w(f"> Hello: {msg}\\n\\n")

        n.use(MyPlugin)
        n.greet("world")
    """

    def __init__(
        self,
        out_md: str,
        title: str = "Report",
        assets_dir: str | None = None,
        cfg: NotebookConfig | None = None,
    ):
        self.out_path = Path(out_md)
        self.assets_path = Path(assets_dir) if assets_dir else self.out_path.parent / "assets"
        self._title = title
        self.cfg = cfg or NotebookConfig()

        self._asset_mgr = AssetManager(self.assets_path, self.out_path.parent)
        self._started = False
        self._counter = 0  # General-purpose counter for unique filenames
        self._chunks: list[str] = []
        self._plugins: dict[str, Any] = {}  # name -> PluginSpec instance

        # Load all globally registered plugins
        self._load_default_plugins()

    def _load_default_plugins(self) -> None:
        """Load all globally registered plugins onto this notebook instance."""
        from .plugins import get_registered_plugins

        for name, plugin_cls in get_registered_plugins().items():
            if name not in self._plugins:
                self._apply_plugin(plugin_cls)

    def _apply_plugin(self, plugin_cls: type) -> None:
        """Instantiate a plugin and bind its methods to this Notebook."""
        from .plugins import PluginSpec

        plugin = plugin_cls()
        self._plugins[plugin_cls.name] = plugin

        for method_name, method in plugin.get_methods().items():
            # Bind the unbound plugin method to this Notebook instance
            bound = types.MethodType(method.__func__, self)
            setattr(self, method_name, bound)

    def use(self, plugin_cls: type) -> None:
        """Add a plugin to this Notebook instance.

        The plugin's public methods become available as ``n.method_name()``.
        If a method name conflicts with an existing one, the new plugin
        overwrites it (last-write-wins).

        Args:
            plugin_cls: A PluginSpec subclass.

        Raises:
            TypeError: If plugin_cls is not a PluginSpec subclass.

        Example::

            from notebookmd.plugins import PluginSpec

            class MyPlugin(PluginSpec):
                name = "my_plugin"
                def greet(self, msg: str) -> None:
                    self._w(f"> Hello: {msg}\\n\\n")

            n = nb("report.md")
            n.use(MyPlugin)
            n.greet("world")
        """
        from .plugins import PluginSpec

        if not isinstance(plugin_cls, type) or not issubclass(plugin_cls, PluginSpec):
            raise TypeError(f"Expected a PluginSpec subclass, got {plugin_cls!r}")
        self._apply_plugin(plugin_cls)

    def get_plugins(self) -> dict[str, Any]:
        """Return a dict of loaded plugin names to plugin instances."""
        return dict(self._plugins)

    def _w(self, s: str) -> None:
        """Append a chunk of markdown to the internal buffer."""
        self._chunks.append(s)

    def _ensure_started(self) -> None:
        """Lazily initialize the report header on first use."""
        if self._started:
            return
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self._asset_mgr.ensure_dir()
        self._started = True

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._w(f"# {self._title}\n\n_Generated: {now}_\n\n")
        self._w("## Artifacts\n\n")
        self._w("{{ARTIFACTS_PLACEHOLDER}}\n\n---\n\n")

    def _next_id(self) -> int:
        """Return an auto-incrementing counter for unique asset filenames."""
        self._counter += 1
        return self._counter

    # ── Sections (core functionality, not in a plugin) ──

    def section(self, title: str, description: str = "") -> _SectionContext:
        """Start a new semantic section with a heading and optional description.

        Works both as a plain call and as a context manager::

            # Plain call — just emits the heading, content follows below
            n.section("Key Metrics", "Fundamental indicators for AAPL")
            n.metric("ROE", "22.5%")
            n.kv({"P/E": "15.2x", "P/B": "2.3x"})

            # Context manager — heading emitted on enter, divider on exit
            with n.section("Price Trend"):
                n.line_chart(df, x="date", y="close")

        Args:
            title: Section heading text.
            description: Optional short description rendered as a caption.

        Returns:
            A context manager (also usable as a plain call).
        """
        self._ensure_started()
        self._w(f"## {title}\n\n")
        if description:
            self._w(f"_{description}_\n\n")
        return _SectionContext(self)

    # ── Internal chart helpers ──

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
    ) -> str | None:
        """Try to render a chart using matplotlib. Returns relative path or None."""
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import pandas as pd
        except ImportError:
            return None

        if not isinstance(data, pd.DataFrame):
            try:
                data = pd.DataFrame(data)
            except Exception:
                return None

        fig, ax = plt.subplots(figsize=(10, 4))

        y_cols: list[str] = []
        if y is None:
            y_cols = data.select_dtypes(include="number").columns.tolist()
        elif isinstance(y, str):
            y_cols = [y]
        else:
            y_cols = list(y)

        x_data = data[x] if x else data.index

        for col in y_cols:
            if chart_type == "line":
                ax.plot(x_data, data[col], label=col, linewidth=1.5)
            elif chart_type == "area":
                ax.fill_between(x_data, data[col], alpha=0.4, label=col)
                ax.plot(x_data, data[col], linewidth=1.0)
            elif chart_type == "bar":
                ax.bar(range(len(data[col])), data[col], label=col, alpha=0.7)
            elif chart_type == "barh":
                ax.barh(range(len(data[col])), data[col], label=col, alpha=0.7)

        if title:
            ax.set_title(title)
        if x_label:
            ax.set_xlabel(x_label)
        if y_label:
            ax.set_ylabel(y_label)
        if len(y_cols) > 1:
            ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        fname = filename or f"{chart_type}_{self._next_id()}.png"
        rel = self._asset_mgr.save_figure(fig, fname, dpi=160)
        return rel

    # ── Save / render ──

    def save(self) -> Path:
        """Write the report markdown to disk.

        Returns:
            Path to the saved markdown file.
        """
        self._ensure_started()

        content = "".join(self._chunks)

        # Replace the artifacts placeholder with the actual index
        artifact_index = self._asset_mgr.render_index()
        content = content.replace("{{ARTIFACTS_PLACEHOLDER}}", artifact_index)

        self.out_path.write_text(content, encoding="utf-8")
        return self.out_path

    def to_markdown(self) -> str:
        """Return the report content as a markdown string without saving."""
        self._ensure_started()
        content = "".join(self._chunks)
        artifact_index = self._asset_mgr.render_index()
        return content.replace("{{ARTIFACTS_PLACEHOLDER}}", artifact_index)


class _SectionContext:
    """Returned by ``Notebook.section()`` to allow optional context-manager use.

    When used as a plain call the heading is already emitted and this object is
    simply discarded.  When used with ``with``, it emits a divider on exit to
    visually close the section::

        # Both styles are valid:
        n.section("Setup")           # plain call
        with n.section("Analysis"):  # context manager
            n.write("...")
    """

    def __init__(self, notebook: Notebook):
        self._notebook = notebook

    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Add a divider to visually close the section
        self._notebook._w("\n---\n\n")
        return None


class _TabGroup:
    """Helper for creating tab sections within a report.

    Usage::

        tabs = n.tabs(["Overview", "Details"])
        with tabs.tab("Overview"):
            n.md("Overview content")
        with tabs.tab("Details"):
            n.table(df)
    """

    def __init__(self, notebook: Notebook, labels: Sequence[str]):
        self._notebook = notebook
        self._labels = list(labels)

    @contextmanager
    def tab(self, label: str) -> Generator[None, None, None]:
        """Open a tab section by label.

        Args:
            label: Must match one of the labels passed to st.tabs().
        """
        self._notebook._w(render_tab_start(label))
        yield
        self._notebook._w(render_tab_end())


class _ColumnGroup:
    """Helper for column layout within a report.

    Usage::

        cols = n.columns(3)
        with cols.col(0):
            n.metric("A", "100")
        with cols.col(1):
            n.metric("B", "200")
    """

    def __init__(self, notebook: Notebook, n: int):
        self._notebook = notebook
        self._n = n

    @contextmanager
    def col(self, index: int) -> Generator[None, None, None]:
        """Open a column section by index.

        Args:
            index: Zero-based column index.
        """
        if index > 0:
            self._notebook._w(render_column_separator())
        yield
        if index == self._n - 1:
            self._notebook._w(render_columns_end())
