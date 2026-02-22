# notebookmd Examples

Self-contained demos showcasing different notebookmd features. Each folder
includes sample data, a run script, and a generated README.md report with assets.

## Demos

| Demo | Description | Key Features |
|------|-------------|--------------|
| [basic](basic/) | Hello world example | Minimal API demonstration, core widgets |
| [financial-analysis](financial-analysis/) | Stock price analysis for AAPL | Tables, summary stats, weekly aggregation, price/volume charts, CSV export |
| [widget-showcase](widget-showcase/) | Tour of all 40+ widgets | Text, metrics, status, layout, charts, analytics helpers, celebration |
| [sales-dashboard](sales-dashboard/) | KPI dashboard from regional sales data | Metric cards, rankings, change indicators, tabs, margin analysis |
| [project-status](project-status/) | Sprint status report from task tracker | Badges, progress bars, team workload, estimation accuracy, risk callouts |
| [data-exploration](data-exploration/) | Employee dataset exploration | Summary stats, department tabs, salary box plots, scatter plots, crosstabs |

## Quick Start

```bash
# Install all optional dependencies
pip install "notebookmd[all]"

# Run any demo
cd examples/financial-analysis
python run.py

# Or run from the project root
python examples/financial-analysis/run.py
```

## Structure

Each demo follows the same layout:

```
demo-name/
├── README.md       # Generated report (output of run.py)
├── assets/         # Generated charts + exported CSVs
├── data/           # Sample input data (if needed)
└── run.py          # Self-contained script
```

Running `python run.py` regenerates `README.md` and `assets/` in place.

## Requirements

- **Minimal**: `pip install notebookmd` — text-only widgets work without extras
- **Full**: `pip install "notebookmd[all]"` — adds pandas tables and matplotlib charts
