# Project Status Report Demo

A sprint status report built from task tracking data, demonstrating
status elements, progress bars, badges, and team analytics.

## What This Demo Shows

- Sprint health badges and progress bars
- Task breakdown by status and priority (pie + bar charts)
- Team workload table with completion percentages
- Estimation accuracy analysis with status callouts
- Estimated vs actual hours comparison chart
- Risk and blocker highlighting
- Connection status indicators
- Multi-table CSV export

## Files

```
project-status/
├── README.md           # This file
├── data/
│   └── tasks.csv       # 16 tasks across 3 sprints
├── run.py              # Report script
└── output/             # Generated report + chart assets
```

## Requirements

```bash
pip install "notebookmd[all]"   # pandas + matplotlib
```

## Run

```bash
cd examples/project-status
python run.py
```

## Output

Generates `output/notebook.md` with sprint breakdowns, team metrics,
risk callouts, and charts in `output/assets/`.
