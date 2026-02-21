"""Widget Showcase Demo — notebookmd

A comprehensive tour of all 40+ Streamlit-style widgets:
- Text elements (title, header, subheader, caption, text, latex, md, code)
- Metric cards and metric rows
- JSON display (expanded and compact)
- Status elements (success, info, warning, error, progress, toast)
- Layout (expanders, tabs, columns, containers)
- Data display (tables, dataframes, summaries, key-value)
- Charts (line, bar, area)
- Analytics helpers (stat, stats, badge, change, ranking)
- Export and celebration

Run:
    cd examples/widget-showcase
    python run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from notebookmd import NotebookConfig, nb

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import matplotlib

    matplotlib.use("Agg")

    HAS_MPL = True
except ImportError:
    HAS_MPL = False

HERE = Path(__file__).resolve().parent


def main():
    cfg = NotebookConfig(max_table_rows=15)
    n = nb(HERE / "README.md", title="Widget Showcase", cfg=cfg)

    n.write("A comprehensive tour of every widget available in `notebookmd`.")

    # ══════════════════════════════════════════════════════════════
    # TEXT ELEMENTS
    # ══════════════════════════════════════════════════════════════
    n.section("Text Elements")
    n.title("Dashboard Title")
    n.header("Section Header", divider=True)
    n.subheader("Subsection Header")
    n.caption("This is a small caption — useful for footnotes and attributions.")
    n.text("Fixed-width preformatted text block\n  preserves spacing and indentation")
    n.latex(r"\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i")
    n.divider()
    n.md("Regular **markdown** with `inline code` and [links](https://example.com).")

    # ══════════════════════════════════════════════════════════════
    # CODE DISPLAY
    # ══════════════════════════════════════════════════════════════
    n.section("Code Display")
    n.code('import notebookmd\nn = notebookmd.nb("report.md")\nn.metric("Users", 42)', lang="python")
    n.subheader("Echo (Code + Output)")
    n.echo(
        'df = fetch_quote("VCB", start="2025-01-01")\nprint(f"Rows: {len(df)}")',
        "Rows: 280",
    )

    # ══════════════════════════════════════════════════════════════
    # METRIC CARDS
    # ══════════════════════════════════════════════════════════════
    n.section("Metric Cards")
    n.metric("Total Revenue", "$1,234,567", delta="+12.3%")
    n.metric("Active Users", "34,521", delta="+2,100")
    n.metric("Churn Rate", "2.1%", delta="-0.3%", delta_color="inverse")

    n.subheader("Metric Row")
    n.metric_row(
        [
            {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
            {"label": "Profit", "value": "$340K", "delta": "+8%"},
            {"label": "Users", "value": "3,400", "delta": "+200"},
            {"label": "Churn", "value": "2.1%", "delta": "-0.3%", "delta_color": "inverse"},
        ]
    )

    # ══════════════════════════════════════════════════════════════
    # ANALYTICS HELPERS
    # ══════════════════════════════════════════════════════════════
    n.section("Analytics Helpers")

    n.subheader("Stat & Stats")
    n.stat("Total Orders", 12_450, description="Last 30 days")
    n.stats(
        [
            {"label": "Revenue", "value": "$1.2M"},
            {"label": "Orders", "value": "12,450"},
            {"label": "AOV", "value": "$96.40"},
        ]
    )

    n.subheader("Badges")
    n.badge("LIVE", style="success")
    n.badge("BETA", style="warning")
    n.badge("DEPRECATED", style="error")
    n.badge("v2.1.0", style="info")
    n.badge("internal", style="default")

    n.subheader("Change Indicator")
    n.change("Monthly Revenue", 1_240_000, 1_105_000, fmt=",.0f", pct=True)

    n.subheader("Ranking")
    n.ranking("VCB", 104.60, rank=1, total=27, percentile=96.3, fmt=",.2f")

    # ══════════════════════════════════════════════════════════════
    # JSON DISPLAY
    # ══════════════════════════════════════════════════════════════
    n.section("JSON Display")
    n.json(
        {
            "symbol": "VCB",
            "exchange": "HOSE",
            "metrics": {"pe_ratio": 15.2, "pb_ratio": 2.8, "dividend_yield": 0.012},
            "tags": ["blue-chip", "state-owned", "dividend"],
        }
    )
    n.json({"compact": True, "value": 42}, expanded=False)

    # ══════════════════════════════════════════════════════════════
    # STATUS ELEMENTS
    # ══════════════════════════════════════════════════════════════
    n.section("Status Elements")
    n.success("Data loaded successfully! 1,234 rows processed.")
    n.info("Processing will use cached data from the last 24 hours.")
    n.warning("Missing data detected for 3 trading days.")
    n.error("Failed to fetch real-time quotes. Using last known prices.")

    n.subheader("Progress Bars")
    n.progress(0.25, "Downloading data...")
    n.progress(0.50, "Processing...")
    n.progress(0.75, "Generating charts...")
    n.progress(1.0, "Complete!")

    n.subheader("Toast & Connection")
    n.toast("New data available for VCB")
    n.connection_status("vnstock API", status="connected", details="v3.1.0")
    n.connection_status("Redis cache", status="disconnected", details="timeout after 5s")

    # ══════════════════════════════════════════════════════════════
    # LAYOUT: EXPANDERS
    # ══════════════════════════════════════════════════════════════
    n.section("Expanders (Collapsible Sections)")
    with n.expander("Methodology", expanded=True):
        n.write(
            "The analysis uses a multi-factor model combining:\n"
            "- **Value**: P/E, P/B ratios relative to sector median\n"
            "- **Momentum**: 6-month and 12-month price returns\n"
            "- **Quality**: ROE, debt-to-equity, earnings stability"
        )

    with n.expander("Data Sources"):
        n.write(
            "- HOSE/HNX market data via vnstock API\n"
            "- Financial statements from company filings\n"
            "- Macro indicators from GSO/SBV"
        )

    # ══════════════════════════════════════════════════════════════
    # LAYOUT: TABS
    # ══════════════════════════════════════════════════════════════
    n.section("Tabs")
    tabs = n.tabs(["Overview", "Technical", "Fundamental"])

    with tabs.tab("Overview"):
        n.metric_row(
            [
                {"label": "Price", "value": "95,400"},
                {"label": "Change", "value": "+1.2%", "delta": "+1.2%"},
                {"label": "Volume", "value": "1.5M"},
            ]
        )

    with tabs.tab("Technical"):
        n.kv(
            {
                "RSI (14)": "62.3",
                "MACD": "Bullish crossover",
                "EMA 20": "94,200",
                "Support": "93,000",
                "Resistance": "97,500",
            },
            title="Technical Indicators",
        )

    with tabs.tab("Fundamental"):
        n.kv(
            {
                "P/E": "15.2x",
                "P/B": "2.8x",
                "ROE": "22.1%",
                "Dividend Yield": "1.2%",
                "NPL Ratio": "0.8%",
            },
            title="Fundamental Metrics",
        )

    # ══════════════════════════════════════════════════════════════
    # LAYOUT: COLUMNS & CONTAINERS
    # ══════════════════════════════════════════════════════════════
    n.section("Columns & Containers")
    cols = n.columns(3)
    with cols.col(0):
        n.metric("Revenue", "$1.2M", delta="+12%")
    with cols.col(1):
        n.metric("Profit", "$340K", delta="+8%")
    with cols.col(2):
        n.metric("Users", "3,400", delta="+200")

    with n.container(border=True):
        n.write("This content is inside a **bordered container**.")
        n.kv({"Status": "Active", "Last Updated": "2026-02-21"})

    # ══════════════════════════════════════════════════════════════
    # DATA DISPLAY (requires pandas)
    # ══════════════════════════════════════════════════════════════
    if HAS_PANDAS:
        n.section("DataFrame Display")
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=20, freq="D"),
                "close": [95 + i * 0.5 + (i % 7) * 0.3 for i in range(20)],
                "volume": [1_000_000 + i * 50_000 for i in range(20)],
                "rsi": [45 + i * 0.8 - (i % 5) * 2 for i in range(20)],
            }
        )
        n.dataframe(df, name="Sample Trading Data")
        n.summary(df, title="Data Summary")

        n.section("Key-Value Display")
        n.kv(
            {
                "Symbol": "VCB",
                "Sector": "Banking",
                "Market Cap": "$12.3B",
                "Float": "74.2%",
                "Dividend Yield": "1.2%",
            },
            title="Company Profile",
        )

        # ── Charts ──
        if HAS_MPL:
            n.section("Built-in Charts")
            n.line_chart(df, x="date", y="close", title="Line Chart — Close Price")
            n.bar_chart(df.tail(10), x="date", y="volume", title="Bar Chart — Recent Volume")
            n.area_chart(df, x="date", y="rsi", title="Area Chart — RSI Trend")

        # ── Export ──
        n.section("Export")
        n.export_csv(df, "sample_data.csv", name="Sample trading data")

    # ══════════════════════════════════════════════════════════════
    # CELEBRATION
    # ══════════════════════════════════════════════════════════════
    n.section("Celebration")
    n.success("Widget showcase complete!")
    n.balloons()
    n.snow()

    out = n.save()
    print(f"Report saved to: {out}")


if __name__ == "__main__":
    main()
