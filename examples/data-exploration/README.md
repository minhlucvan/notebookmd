# Data Exploration Demo

An interactive-style exploration of a sample employee dataset, demonstrating
how notebookmd handles tabular data, summary statistics, and drill-down analysis.

## What This Demo Shows

- Dataset overview with shape and summary statistics
- Department analysis with tabbed team views
- Salary distribution box plots and comparison tables
- Performance ranking with scatter plot visualization
- Remote work analysis with crosstab tables
- City breakdown with aggregated metrics
- Collapsible deep-dives using expanders
- Multi-table CSV export

## Files

```
data-exploration/
├── README.md           # This file
├── data/
│   └── employees.csv   # 20 employees across 7 departments
├── run.py              # Exploration script
└── output/             # Generated report + chart assets
```

## Requirements

```bash
pip install "notebookmd[all]"   # pandas + matplotlib
```

## Run

```bash
cd examples/data-exploration
python run.py
```

## Output

Generates `output/notebook.md` with tables, summary statistics, charts,
and exported CSVs in `output/assets/`.
