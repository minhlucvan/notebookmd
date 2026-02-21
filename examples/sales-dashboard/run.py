"""Sales Dashboard Demo — notebookmd

Builds a KPI dashboard from regional sales data:
- Executive summary with metric cards
- Revenue breakdown by region and product
- Trend analysis with charts
- Rankings and change indicators
- Tabbed views for different perspectives

Run:
    cd examples/sales-dashboard
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
    import matplotlib.pyplot as plt

    HAS_MPL = True
except ImportError:
    HAS_MPL = False

HERE = Path(__file__).resolve().parent


def main():
    cfg = NotebookConfig(max_table_rows=25)
    n = nb(HERE / "README.md", title="Sales Dashboard — January 2026", cfg=cfg)

    if not HAS_PANDAS:
        n.warning("pandas is required for this demo. Install with: `pip install 'notebookmd[pandas]'`")
        n.save()
        return

    # ── Load Data ──
    df = pd.read_csv(HERE / "data" / "sales.csv", parse_dates=["date"])
    df["profit"] = df["revenue"] - df["cost"]
    df["margin"] = df["profit"] / df["revenue"]

    # ══════════════════════════════════════════════════════════════
    # EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════
    n.section("Executive Summary")
    n.badge("LIVE", style="success")
    n.write("Monthly performance overview for all regions and products.")

    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    total_units = df["units"].sum()
    avg_margin = df["margin"].mean()

    n.metric_row(
        [
            {"label": "Total Revenue", "value": f"${total_revenue:,.0f}"},
            {"label": "Total Profit", "value": f"${total_profit:,.0f}"},
            {"label": "Units Sold", "value": f"{total_units:,}"},
            {"label": "Avg Margin", "value": f"{avg_margin:.1%}"},
        ]
    )

    # Week-over-week change (last week vs first week)
    weekly_rev = df.groupby("date")["revenue"].sum().reset_index()
    first_week_rev = weekly_rev.iloc[0]["revenue"]
    last_week_rev = weekly_rev.iloc[-1]["revenue"]
    n.change("Weekly Revenue", last_week_rev, first_week_rev, fmt=",.0f", pct=True)

    # ══════════════════════════════════════════════════════════════
    # REGIONAL BREAKDOWN
    # ══════════════════════════════════════════════════════════════
    n.section("Regional Performance")

    region_summary = (
        df.groupby("region")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("units", "sum"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    region_summary["margin"] = (region_summary["profit"] / region_summary["revenue"] * 100).round(1)
    n.table(region_summary, name="Revenue by Region")

    # Rank the regions
    for i, row in region_summary.iterrows():
        n.ranking(
            row["region"],
            row["revenue"],
            rank=i + 1,
            total=len(region_summary),
            fmt=",.0f",
        )

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(region_summary["region"], region_summary["revenue"], color=["#2563eb", "#7c3aed", "#059669", "#dc2626"])
        ax.set_xlabel("Revenue ($)")
        ax.set_title("Revenue by Region")
        ax.grid(True, alpha=0.3, axis="x")
        for i, v in enumerate(region_summary["revenue"]):
            ax.text(v + 1000, i, f"${v:,.0f}", va="center", fontsize=9)
        fig.tight_layout()
        n.figure(fig, "revenue_by_region.png", caption="Regional revenue comparison")
        plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # PRODUCT ANALYSIS
    # ══════════════════════════════════════════════════════════════
    n.section("Product Analysis")

    tabs = n.tabs(["Widget A", "Widget B", "Comparison"])

    product_a = df[df["product"] == "Widget A"]
    product_b = df[df["product"] == "Widget B"]

    with tabs.tab("Widget A"):
        a_rev = product_a["revenue"].sum()
        a_units = product_a["units"].sum()
        a_margin = product_a["margin"].mean()
        n.metric_row(
            [
                {"label": "Revenue", "value": f"${a_rev:,.0f}"},
                {"label": "Units", "value": f"{a_units:,}"},
                {"label": "Avg Margin", "value": f"{a_margin:.1%}"},
            ]
        )

    with tabs.tab("Widget B"):
        b_rev = product_b["revenue"].sum()
        b_units = product_b["units"].sum()
        b_margin = product_b["margin"].mean()
        n.metric_row(
            [
                {"label": "Revenue", "value": f"${b_rev:,.0f}"},
                {"label": "Units", "value": f"{b_units:,}"},
                {"label": "Avg Margin", "value": f"{b_margin:.1%}"},
            ]
        )

    with tabs.tab("Comparison"):
        comparison = (
            df.groupby("product")
            .agg(revenue=("revenue", "sum"), units=("units", "sum"), profit=("profit", "sum"))
            .reset_index()
        )
        comparison["margin"] = (comparison["profit"] / comparison["revenue"] * 100).round(1)
        n.table(comparison, name="Product Comparison")

    # ══════════════════════════════════════════════════════════════
    # WEEKLY TRENDS
    # ══════════════════════════════════════════════════════════════
    n.section("Weekly Trends")

    weekly = (
        df.groupby("date")
        .agg(revenue=("revenue", "sum"), units=("units", "sum"), profit=("profit", "sum"))
        .reset_index()
    )
    n.table(weekly, name="Weekly totals")

    if HAS_MPL:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

        ax1.plot(weekly["date"], weekly["revenue"], marker="o", color="#2563eb", linewidth=2)
        ax1.set_ylabel("Revenue ($)")
        ax1.set_title("Weekly Revenue & Units Trend")
        ax1.grid(True, alpha=0.3)

        ax2.bar(weekly["date"], weekly["units"], color="#7c3aed", width=3)
        ax2.set_ylabel("Units Sold")
        ax2.set_xlabel("Week")
        ax2.grid(True, alpha=0.3, axis="y")

        fig.tight_layout()
        n.figure(fig, "weekly_trends.png", caption="Revenue and unit trends over 5 weeks")
        plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # MARGIN ANALYSIS
    # ══════════════════════════════════════════════════════════════
    n.section("Margin Analysis")

    margin_by_region_product = (
        df.groupby(["region", "product"]).agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    )
    margin_by_region_product["margin"] = (
        margin_by_region_product["profit"] / margin_by_region_product["revenue"] * 100
    ).round(1)
    n.table(margin_by_region_product, name="Margin by Region × Product")

    best = margin_by_region_product.loc[margin_by_region_product["margin"].idxmax()]
    worst = margin_by_region_product.loc[margin_by_region_product["margin"].idxmin()]

    with n.expander("Margin Insights", expanded=True):
        n.success(f"Highest margin: **{best['region']} / {best['product']}** at {best['margin']}%")
        n.warning(f"Lowest margin: **{worst['region']} / {worst['product']}** at {worst['margin']}%")

    # ══════════════════════════════════════════════════════════════
    # DATA EXPORT
    # ══════════════════════════════════════════════════════════════
    n.section("Data Export")
    n.export_csv(df, "sales_full.csv", name="Full sales data")
    n.export_csv(region_summary, "region_summary.csv", name="Regional summary")
    n.export_csv(weekly, "weekly_trends.csv", name="Weekly trends")
    n.success("Dashboard generation complete.")

    out = n.save()
    print(f"Report saved to: {out}")


if __name__ == "__main__":
    main()
