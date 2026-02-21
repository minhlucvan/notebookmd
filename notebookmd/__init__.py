"""notebookmd — The notebook for AI agents.

Generates structured Markdown reports from sequential Python function calls.
Designed for AI agents doing data analysis — just call functions sequentially,
no cells, no kernel, no execution context needed.

Usage::

    from notebookmd import nb

    n = nb("dist/report.md", title="VCB Investment Analysis")

    n.header("Key Metrics")
    n.metric("ROE", "22.5%", delta="+4.5%")
    n.metric_row([
        {"label": "P/E", "value": "15.2x"},
        {"label": "P/B", "value": "2.3x"},
        {"label": "Dividend", "value": "1.2%"},
    ])

    n.header("Price Trend")
    n.line_chart(df, x="date", y="close", title="VCB Close Price")
    n.dataframe(df.head(), name="Recent Prices")

    n.header("Analysis")
    n.write("VCB shows **strong fundamentals** with best-in-class ROE.")
    n.success("Analysis complete!")

    with n.expander("Raw Data"):
        n.dataframe(df)

    n.save()
"""

from .core import Notebook, NotebookConfig

__version__ = "0.3.0"
__all__ = ["nb", "Notebook", "NotebookConfig"]


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
