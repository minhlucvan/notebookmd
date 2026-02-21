# Financial Analysis Demo

A realistic stock analysis workflow using notebookmd, demonstrating how AI agents
can produce structured financial reports.

## What This Demo Shows

- Loading CSV data into pandas DataFrames
- Price tables with summary statistics
- Weekly aggregation with key-value metrics
- Metric cards for KPIs (return, range, volume)
- Matplotlib price chart with high-low band
- Volume bar chart with color-coded up/down days
- CSV export for downstream pipelines

## Files

```
financial-analysis/
├── README.md           # This file
├── data/
│   └── stock_prices.csv  # 30 days of VCB trading data
├── run.py              # Analysis script
└── output/             # Generated report + chart assets
```

## Requirements

```bash
pip install "notebookmd[all]"   # pandas + matplotlib
```

## Run

```bash
cd examples/financial-analysis
python run.py
```

## Output

The script generates `output/notebook.md` with embedded chart images and
exported CSV files in the `output/assets/` directory.
