# Widget Showcase Demo

A comprehensive tour of every widget available in notebookmd — the full
Streamlit-compatible API rendered as clean Markdown.

## What This Demo Shows

- **Text**: title, header, subheader, caption, text, latex, md, code, echo
- **Metrics**: metric cards, metric rows with deltas
- **Analytics**: stat, stats, badge, change, ranking
- **JSON**: expanded and compact display
- **Status**: success, info, warning, error, progress, toast, connection_status
- **Layout**: expanders, tabs, columns, containers
- **Data**: dataframe, summary, key-value tables
- **Charts**: line_chart, bar_chart, area_chart
- **Export**: CSV export, balloons, snow

## Files

```
widget-showcase/
├── README.md       # This file
├── run.py          # Showcase script
└── output/         # Generated report + assets
```

## Requirements

```bash
pip install "notebookmd[all]"   # Full feature set
# Or minimal (text-only widgets still work):
pip install notebookmd
```

## Run

```bash
cd examples/widget-showcase
python run.py
```

## Sample Output

The script generates `output/notebook.md` demonstrating every widget.
Charts and exported CSVs are saved to `output/assets/`.

---

<!-- BEGIN SAMPLE OUTPUT -->

A comprehensive tour of every widget available in `notebookmd`.

# Widget Showcase

_Generated: 2026-02-21_

## Artifacts

- [line_1.png](assets/line_1.png)
- [bar_2.png](assets/bar_2.png)
- [area_3.png](assets/area_3.png)
- [sample_data.csv](assets/sample_data.csv)


---

## Text Elements

# Dashboard Title

## Section Header

---

### Subsection Header

_This is a small caption — useful for footnotes and attributions._

```text
Fixed-width preformatted text block
  preserves spacing and indentation
```

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

---

Regular **markdown** with `inline code` and [links](https://example.com).

## Code Display

```python
import notebookmd
n = notebookmd.nb("report.md")
n.metric("Users", 42)
```

### Echo (Code + Output)

```python
df = fetch_quote("VCB", start="2025-01-01")
print(f"Rows: {len(df)}")
```

```text
Rows: 280
```

## Metric Cards

| **Total Revenue** |
| :---: |
| **$1,234,567** |
| +12.3% |

| **Active Users** |
| :---: |
| **34,521** |
| +2,100 |

| **Churn Rate** |
| :---: |
| **2.1%** |
| -0.3% |

### Metric Row

| **Revenue** | **Profit** | **Users** | **Churn** |
| :---: | :---: | :---: | :---: |
| **$1.2M** | **$340K** | **3,400** | **2.1%** |
| ▲ +12% | ▲ +8% | ▲ +200 | ▲ -0.3% |

## Analytics Helpers

### Stat & Stats

Total Orders: **12450** (Last 30 days)

Revenue: **$1.2M** · Orders: **12,450** · AOV: **$96.40**

### Badges

**`✅ LIVE`**

**`⚠️ BETA`**

**`❌ DEPRECATED`**

**`ℹ️ v2.1.0`**

**`internal`**

### Change Indicator

Monthly Revenue: **1,240,000** (▲ +135,000, +12.2%)

### Ranking

VCB: **104.60** (96th percentile, top 4%, #1 of 27)

## JSON Display

```json
{
  "symbol": "VCB",
  "exchange": "HOSE",
  "metrics": {
    "pe_ratio": 15.2,
    "pb_ratio": 2.8,
    "dividend_yield": 0.012
  },
  "tags": [
    "blue-chip",
    "state-owned",
    "dividend"
  ]
}
```

```json
{"compact": true, "value": 42}
```

## Status Elements

> ✅ **Success:** Data loaded successfully! 1,234 rows processed.

> ℹ️ **Info:** Processing will use cached data from the last 24 hours.

> ⚠️ **Warning:** Missing data detected for 3 trading days.

> ❌ **Error:** Failed to fetch real-time quotes. Using last known prices.

### Progress Bars

`[█████░░░░░░░░░░░░░░░] 25%` Downloading data...

`[██████████░░░░░░░░░░] 50%` Processing...

`[███████████████░░░░░] 75%` Generating charts...

`[████████████████████] 100%` Complete!

### Toast & Connection

> 🔔 New data available for VCB

🟢 **vnstock API**: connected — v3.1.0

🔴 **Redis cache**: disconnected — timeout after 5s

## Expanders (Collapsible Sections)

<details open>
<summary><strong>Methodology</strong></summary>

The analysis uses a multi-factor model combining:
- **Value**: P/E, P/B ratios relative to sector median
- **Momentum**: 6-month and 12-month price returns
- **Quality**: ROE, debt-to-equity, earnings stability

</details>

<details>
<summary><strong>Data Sources</strong></summary>

- HOSE/HNX market data via vnstock API
- Financial statements from company filings
- Macro indicators from GSO/SBV

</details>

## Tabs

[**Overview** | **Technical** | **Fundamental**]

#### Overview

| **Price** | **Change** | **Volume** |
| :---: | :---: | :---: |
| **95,400** | **+1.2%** | **1.5M** |
| — | ▲ +1.2% | — |

---

#### Technical

#### Technical Indicators

| Key | Value |
| --- | --- |
| RSI (14) | 62.3 |
| MACD | Bullish crossover |
| EMA 20 | 94,200 |
| Support | 93,000 |
| Resistance | 97,500 |

---

#### Fundamental

#### Fundamental Metrics

| Key | Value |
| --- | --- |
| P/E | 15.2x |
| P/B | 2.8x |
| ROE | 22.1% |
| Dividend Yield | 1.2% |
| NPL Ratio | 0.8% |

---

## Columns & Containers

<!-- columns: 3 -->

| **Revenue** |
| :---: |
| **$1.2M** |
| +12% |

| | |
| **Profit** |
| :---: |
| **$340K** |
| +8% |

| | |
| **Users** |
| :---: |
| **3,400** |
| ▲ +200 |

<!-- /columns -->

> ---
>
This content is inside a **bordered container**.

#### Metrics

| Key | Value |
| --- | --- |
| Status | Active |
| Last Updated | 2026-02-21 |

>
> ---

## DataFrame Display

#### Sample Trading Data

| date                | close   | volume   | rsi   |
|:--------------------|:--------|:---------|:------|
| 2026-01-01 00:00:00 | 95.0    | 1000000  | 45.0  |
| 2026-01-02 00:00:00 | 95.8    | 1050000  | 43.8  |
| 2026-01-03 00:00:00 | 96.6    | 1100000  | 42.6  |
| …                   | …       | …        | …     |

_shape: 20 rows × 4 cols_

#### Data Summary

- **Shape**: 20 rows × 4 cols
- **Columns**: date, close, volume, rsi

**Numeric stats (top 10):**

|        |        mean |          std |    min |        max |
|:-------|------------:|-------------:|-------:|-----------:|
| close  | 100.605     |      3.15152 | 95     | 106        |
| volume |   1.475e+06 | 295804       |  1e+06 |   1.95e+06 |
| rsi    |  48.6       |      4.90757 | 40.2   |  57        |

## Key-Value Display

#### Company Profile

| Key | Value |
| --- | --- |
| Symbol | VCB |
| Sector | Banking |
| Market Cap | $12.3B |
| Float | 74.2% |
| Dividend Yield | 1.2% |

## Built-in Charts

![Line Chart — Close Price](assets/line_1.png)

*Line Chart — Close Price*

![Bar Chart — Recent Volume](assets/bar_2.png)

*Bar Chart — Recent Volume*

![Area Chart — RSI Trend](assets/area_3.png)

*Area Chart — RSI Trend*

## Export

**Exported:** [Sample trading data](assets/sample_data.csv)

## Celebration

> ✅ **Success:** Widget showcase complete!

> 🎈🎈🎈 **Celebration!**

> ❄️❄️❄️ **Snow!**

<!-- END SAMPLE OUTPUT -->
