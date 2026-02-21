"""Example analysis script demonstrating notebookmd Streamlit-like API.

This pattern is used by the vnstock multi-agent research system.
See: ../../analyses/samples/VCB_notebookmd_example/

Run from the notebookmd package root:
    python examples/analysis.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from the package root without install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notebookmd import nb, NotebookConfig

# Optional imports — graceful fallback
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
    n = nb("dist/notebook.md", title="Sample Financial Analysis", cfg=cfg)

    # ── Setup ──
    n.section("Setup")
    n.write("This report demonstrates `notebookmd` features for financial analysis.")
    n.kv(
        {
            "pandas": "available" if HAS_PANDAS else "missing",
            "matplotlib": "available" if HAS_MPL else "missing",
        },
        title="Environment",
    )

    if HAS_PANDAS:
        # ── Load data ──
        n.section("Load sample data")
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=30, freq="D"),
                "symbol": ["VCB"] * 30,
                "close": [95 + i * 0.5 + (i % 7) * 0.3 for i in range(30)],
                "volume": [1_000_000 + i * 50_000 for i in range(30)],
            }
        )
        n.table(df.head(10), name="Price data (first 10)")

        # ── Summary stats ──
        n.section("Data Summary")
        n.summary(df, title="VCB Price Data Summary")

        # ── Aggregate ──
        n.section("Weekly Aggregation")
        weekly = df.set_index("date").resample("W")["close"].agg(["mean", "min", "max"]).reset_index()
        weekly.columns = ["week", "avg_close", "min_close", "max_close"]
        n.table(weekly, name="Weekly price stats")
        n.kv(
            {
                "Weeks": len(weekly),
                "Avg Close": f"{weekly['avg_close'].mean():.2f}",
                "Range": f"{df['close'].min():.2f} – {df['close'].max():.2f}",
            },
            title="Quick Metrics",
        )

        # ── Plot ──
        if HAS_MPL:
            n.section("Price Chart")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df["date"], df["close"], linewidth=1.5, color="#2563eb")
            ax.set_title("VCB Daily Close Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (VND thousands)")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            n.figure(fig, "vcb_price.png", caption="VCB daily closing price (Jan 2026)")

        # ── Export ──
        n.section("Export Data")
        n.export_csv(df, "vcb_prices.csv", name="VCB price data")
        n.note("CSV exported for downstream analysis.")

    # ── Interpretation ──
    n.section("Interpretation")
    n.write("""
- VCB shows a **steady upward trend** over the sample period.
- Weekly aggregation reveals consistent mean-reversion within weeks.
- Volume increases suggest **growing institutional interest**.

### Next steps

1. Compare against sector peers (TCB, VPB, ACB)
2. Run factor analysis using the `factor` agent
3. Check macro regime for timing signals
""")

    out = n.save()
    print(f"\nReport saved to: {out}")


if __name__ == "__main__":
    main()
