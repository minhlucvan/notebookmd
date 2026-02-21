"""Financial Analysis Demo — notebookmd

Demonstrates a realistic stock analysis workflow:
- Loading CSV data into pandas DataFrames
- Displaying price tables and summary statistics
- Weekly aggregation with key-value metrics
- Matplotlib price and volume charts
- CSV export for downstream pipelines

Run:
    cd examples/financial-analysis
    python run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from any location without install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from notebookmd import NotebookConfig, nb

# Optional imports — graceful fallback
try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    HAS_MPL = True
except ImportError:
    HAS_MPL = False

HERE = Path(__file__).resolve().parent


def main():
    cfg = NotebookConfig(max_table_rows=20)
    n = nb(HERE / "README.md", title="AAPL Stock Analysis", cfg=cfg)

    # ── Overview ──
    n.section("Overview")
    n.write(
        "This report analyzes **AAPL (Apple Inc.)** daily trading data "
        "for January–February 2026, covering price trends, volume patterns, "
        "and weekly aggregation."
    )
    n.kv(
        {
            "Symbol": "AAPL",
            "Exchange": "NASDAQ",
            "Period": "Jan 2 – Feb 17, 2026",
            "Frequency": "Daily",
        },
        title="Report Parameters",
    )

    if not HAS_PANDAS:
        n.warning("pandas is not installed. Install with: `pip install 'notebookmd[pandas]'`")
        n.save()
        return

    # ── Load Data ──
    n.section("Raw Data")
    df = pd.read_csv(HERE / "data" / "stock_prices.csv", parse_dates=["date"])
    n.table(df.head(10), name="Price data (first 10 rows)")
    n.caption(f"Showing 10 of {len(df)} trading days")

    # ── Summary Statistics ──
    n.section("Summary Statistics")
    n.summary(df[["close", "volume", "high", "low"]], title="AAPL Trading Data Summary")

    price_range = df["close"].max() - df["close"].min()
    total_return = (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100
    avg_volume = df["volume"].mean()

    n.metric_row(
        [
            {"label": "Latest Close", "value": f"${df['close'].iloc[-1]:.2f}"},
            {"label": "Total Return", "value": f"{total_return:+.1f}%", "delta": f"{total_return:+.1f}%"},
            {"label": "Price Range", "value": f"${price_range:.2f}"},
            {"label": "Avg Volume", "value": f"{avg_volume:,.0f}"},
        ]
    )

    # ── Weekly Aggregation ──
    n.section("Weekly Aggregation")
    weekly = df.set_index("date").resample("W")["close"].agg(["mean", "min", "max", "count"]).reset_index()
    weekly.columns = ["week", "avg_close", "min_close", "max_close", "trading_days"]
    n.table(weekly, name="Weekly price statistics")

    n.kv(
        {
            "Weeks Covered": str(len(weekly)),
            "Best Week Avg": f"${weekly['avg_close'].max():.2f}",
            "Worst Week Avg": f"${weekly['avg_close'].min():.2f}",
            "Overall Range": f"${df['close'].min():.2f} – ${df['close'].max():.2f}",
        },
        title="Aggregation Summary",
    )

    # ── Charts ──
    if HAS_MPL:
        n.section("Price Chart")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["date"], df["close"], linewidth=1.5, color="#2563eb", label="Close")
        ax.fill_between(df["date"], df["low"], df["high"], alpha=0.15, color="#2563eb", label="High–Low range")
        ax.set_title("AAPL Daily Close Price with High-Low Band")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        fig.autofmt_xdate()
        fig.tight_layout()
        n.figure(fig, "aapl_price_band.png", caption="AAPL daily closing price with high-low range")
        plt.close(fig)

        n.section("Volume Chart")
        fig, ax = plt.subplots(figsize=(10, 3))
        colors = ["#22c55e" if c >= o else "#ef4444" for c, o in zip(df["close"], df["open"], strict=True)]
        ax.bar(df["date"], df["volume"], color=colors, width=0.8)
        ax.set_title("AAPL Daily Trading Volume")
        ax.set_xlabel("Date")
        ax.set_ylabel("Volume")
        ax.grid(True, alpha=0.3, axis="y")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        fig.autofmt_xdate()
        fig.tight_layout()
        n.figure(fig, "aapl_volume.png", caption="Green = close >= open, Red = close < open")
        plt.close(fig)

    # ── Export ──
    n.section("Data Export")
    n.export_csv(df, "aapl_prices.csv", name="AAPL price data")
    n.export_csv(weekly, "aapl_weekly.csv", name="AAPL weekly aggregation")
    n.success("All data exported for downstream analysis.")

    # ── Interpretation ──
    n.section("Interpretation")
    n.write(
        f"""
- AAPL shows a **steady upward trend** over the sample period, gaining **{total_return:.1f}%**.
- The high-low band remains narrow, indicating **low intraday volatility**.
- Volume increases in the latter half suggest **growing institutional interest**.
- Weekly aggregation confirms consistent upward drift with no significant pullbacks.

### Next Steps

1. Compare against sector peers (MSFT, GOOGL, AMZN)
2. Overlay technical indicators (RSI, MACD, Bollinger Bands)
3. Check macro regime alignment for timing signals
"""
    )

    out = n.save()
    print(f"Report saved to: {out}")


if __name__ == "__main__":
    main()
