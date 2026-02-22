"""Hello World — notebookmd

Simplest possible example.

Run:
    cd examples/basic
    python run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from any location without install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from notebookmd import nb

HERE = Path(__file__).resolve().parent


def main():
    n = nb(HERE / "README.md", title="Hello World")

    n.write("Hello, world!")
    n.success("It works!")

    out = n.save()
    print(f"Report saved to: {out}")


if __name__ == "__main__":
    main()