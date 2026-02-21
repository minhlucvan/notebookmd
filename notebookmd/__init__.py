"""notebookmd — The notebook for AI agents.

Generates structured Markdown reports from sequential Python function calls.
Designed for AI agents doing data analysis — just call functions sequentially,
no cells, no kernel, no execution context needed.

Usage::

    from notebookmd import nb

    n = nb("dist/report.md", title="AAPL Investment Analysis")

    n.header("Key Metrics")
    n.metric("ROE", "157%", delta="+12%")
    n.metric_row([
        {"label": "P/E", "value": "32.5x"},
        {"label": "P/B", "value": "48.1x"},
        {"label": "Dividend", "value": "0.5%"},
    ])

    n.header("Price Trend")
    n.line_chart(df, x="date", y="close", title="AAPL Close Price")
    n.dataframe(df.head(), name="Recent Prices")

    n.header("Analysis")
    n.write("AAPL shows **strong fundamentals** with consistent growth.")
    n.success("Analysis complete!")

    with n.expander("Raw Data"):
        n.dataframe(df)

    n.save()

Plugin system::

    from notebookmd.plugins import PluginSpec, register_plugin

    class MyPlugin(PluginSpec):
        name = "my_plugin"

        def greet(self, message: str) -> None:
            self._w(f"> Hello: {message}\\n\\n")

    # Global registration (all notebooks get it):
    register_plugin(MyPlugin)

    # Or per-instance:
    n = nb("report.md")
    n.use(MyPlugin)
    n.greet("world")
"""

from .core import Notebook, NotebookConfig
from .plugins import PluginSpec, register_plugin

__version__ = "0.3.0"
__all__ = ["nb", "Notebook", "NotebookConfig", "PluginSpec", "register_plugin"]

# Load built-in plugins and discover community plugins via entry points.
# This must happen after imports but before any Notebook is created.
from .plugins import load_default_plugins as _load_default_plugins

_load_default_plugins()


def nb(
    out_md: str,
    title: str = "Report",
    assets_dir: str | None = None,
    cfg: NotebookConfig | None = None,
) -> Notebook:
    """Create a new report builder (convenience factory).

    Args:
        out_md: Path to the output markdown file (e.g. "dist/report.md").
        title: Title for the report.
        assets_dir: Directory for saving figures/assets. Defaults to ``<out_md_dir>/assets/``.
        cfg: Optional NotebookConfig for customizing rendering behavior.

    Returns:
        A configured Notebook instance ready for sequential method calls.

    Example::

        n = nb("dist/report.md", title="My Analysis")
        n.header("Overview")
        n.metric("Revenue", "$1.2M", delta="+12%")
        n.save()
    """
    return Notebook(out_md=out_md, title=title, assets_dir=assets_dir, cfg=cfg)
