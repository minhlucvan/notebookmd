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

## Output

The script generates `output/notebook.md` demonstrating every widget.
Charts and exported CSVs are saved to `output/assets/`.
