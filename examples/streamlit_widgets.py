"""Example demonstrating all Streamlit-style widgets in notebookmd.

Run from the notebookmd package root:
    python examples/streamlit_widgets.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from the package root without install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notebookmd import nb, NotebookConfig

# Optional imports
try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def main():
    cfg = NotebookConfig(max_table_rows=20)
    n = nb("dist/streamlit_demo.md", title="Streamlit Widgets Demo", cfg=cfg)

    # ── Text Elements ──
    n.section("Text Elements")
    n.title("Dashboard Title")
    n.header("Section Header", divider=True)
    n.subheader("Subsection")
    n.caption("This is a small caption text")
    n.text("Fixed-width preformatted text output")
    n.latex(r"\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i")
    n.divider()
    n.md("Regular **markdown** with `inline code`.")

    # ── Metrics ──
    n.section("Metric Cards")
    n.metric("Total Revenue", "$1,234,567", delta="+12.3%")
    n.metric("Active Users", "34,521", delta="+2,100")
    n.metric("Churn Rate", "2.1%", delta="-0.3%", delta_color="inverse")

    n.subheader("Metrics in a Row")
    n.metric_row([
        {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
        {"label": "Profit", "value": "$340K", "delta": "+8%"},
        {"label": "Users", "value": "3,400", "delta": "+200"},
        {"label": "Churn", "value": "2.1%", "delta": "-0.3%", "delta_color": "inverse"},
    ])

    # ── JSON Display ──
    n.section("JSON Display")
    n.json({
        "symbol": "VCB",
        "exchange": "HOSE",
        "metrics": {
            "pe_ratio": 15.2,
            "pb_ratio": 2.8,
            "dividend_yield": 0.012,
        },
        "sector": "Banking",
        "tags": ["blue-chip", "state-owned", "dividend"],
    })

    n.json({"compact": True, "value": 42}, expanded=False)

    # ── Status Elements ──
    n.section("Status Elements")
    n.success("Data loaded successfully! 1,234 rows processed.")
    n.info("Processing will use cached data from the last 24 hours.")
    n.warning("Missing data detected for 3 trading days.")
    n.error("Failed to fetch real-time quotes. Using last known prices.")
    n.progress(0.75, "Loading data...")
    n.progress(1.0, "Complete!")
    n.toast("New data available for VCB")

    # ── Layout: Expander ──
    n.section("Collapsible Sections")
    n.write("Click to expand the sections below:")

    with n.expander("Methodology", expanded=True):
        n.write("""
The analysis uses a multi-factor model combining:
- **Value**: P/E, P/B ratios relative to sector median
- **Momentum**: 6-month and 12-month price returns
- **Quality**: ROE, debt-to-equity, earnings stability
""")

    with n.expander("Data Sources"):
        n.write("""
- HOSE/HNX market data via vnstock API
- Financial statements from company filings
- Macro indicators from GSO/SBV
""")

    # ── Layout: Tabs ──
    n.section("Tabbed Sections")
    tabs = n.tabs(["Overview", "Technical", "Fundamental"])

    with tabs.tab("Overview"):
        n.metric_row([
            {"label": "Price", "value": "95,400"},
            {"label": "Change", "value": "+1.2%", "delta": "+1.2%"},
            {"label": "Volume", "value": "1.5M"},
        ])

    with tabs.tab("Technical"):
        n.kv({
            "RSI (14)": "62.3",
            "MACD": "Bullish crossover",
            "EMA 20": "94,200",
            "Support": "93,000",
            "Resistance": "97,500",
        }, title="Technical Indicators")

    with tabs.tab("Fundamental"):
        n.kv({
            "P/E": "15.2x",
            "P/B": "2.8x",
            "ROE": "22.1%",
            "Dividend Yield": "1.2%",
            "NPL Ratio": "0.8%",
        }, title="Fundamental Metrics")

    # ── Code Display ──
    n.section("Code Display")
    n.echo(
        'df = fetch_quote("VCB", start="2025-01-01")\nprint(f"Rows: {len(df)}")',
        "Rows: 280",
    )

    # ── DataFrame & Charts (requires pandas) ──
    if HAS_PANDAS:
        df = pd.DataFrame({
            "date": pd.date_range("2026-01-01", periods=30, freq="D"),
            "close": [95 + i * 0.5 + (i % 7) * 0.3 for i in range(30)],
            "volume": [1_000_000 + i * 50_000 for i in range(30)],
            "rsi": [45 + i * 0.8 - (i % 5) * 2 for i in range(30)],
        })

        n.section("DataFrame Display")
        n.dataframe(df, name="VCB Price Data")
        n.summary(df, title="Data Summary")

        if HAS_MPL:
            n.section("Convenience Charts")
            n.line_chart(df, x="date", y="close", title="VCB Close Price")
            n.bar_chart(df.tail(10), x="date", y="volume", title="Recent Volume")
            n.area_chart(df, x="date", y="rsi", title="RSI Trend")

        n.section("Export & Wrap-up")
        n.export_csv(df, "vcb_demo.csv", name="VCB demo data")
        n.connection_status("vnstock API", status="connected", details="v3.1.0")
        n.success("Demo report complete!")
        n.balloons()

    out = n.save()
    print(f"\nReport saved to: {out}")


if __name__ == "__main__":
    main()
