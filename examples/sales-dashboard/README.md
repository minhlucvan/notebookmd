# Sales Dashboard Demo

A KPI-driven sales dashboard built from regional sales data, demonstrating
how notebookmd can generate executive-ready reports.

## What This Demo Shows

- Executive summary with metric cards and badges
- Week-over-week change indicators
- Regional performance rankings
- Product comparison with tabbed views
- Horizontal bar charts for regional breakdown
- Dual-axis weekly trend charts
- Margin analysis with expander insights
- Multi-table CSV export

## Files

```
sales-dashboard/
├── README.md           # This file
├── data/
│   └── sales.csv       # 5 weeks × 4 regions × 2 products
├── run.py              # Dashboard script
└── output/             # Generated report + chart assets
```

## Requirements

```bash
pip install "notebookmd[all]"   # pandas + matplotlib
```

## Run

```bash
cd examples/sales-dashboard
python run.py
```

## Output

Generates `output/notebook.md` with KPI cards, ranking tables, trend charts,
and exported CSVs in `output/assets/`.
