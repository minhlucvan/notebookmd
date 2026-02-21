# Contributing to notebookmd

Thank you for your interest in contributing to notebookmd! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git

### Getting Started

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/notebookmd.git
   cd notebookmd
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or .venv\Scripts\activate on Windows
   ```

3. **Install in development mode:**

   ```bash
   pip install -e ".[all,dev]"
   pip install ruff mypy
   ```

4. **Verify your setup:**

   ```bash
   make test
   make lint
   ```

## Development Workflow

### Branch Naming

- `feat/description` — new features
- `fix/description` — bug fixes
- `docs/description` — documentation changes
- `refactor/description` — code refactoring

### Making Changes

1. Create a branch from `main`
2. Make your changes
3. Add or update tests as needed
4. Run the full quality check: `make check`
5. Commit with a clear message
6. Open a pull request

### Running Tests

```bash
# Run all tests
make test

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run tests without optional dependencies (verifies zero-dep core)
pip install -e .
pytest tests/ -v
```

### Code Quality

```bash
# Run linter
make lint

# Auto-fix lint issues
make fix

# Type checking
make typecheck

# Run everything
make check
```

## Architecture

notebookmd uses a **core + plugin** architecture:

- **`core.py`** — `Notebook` class handles markdown buffering, asset management, and report lifecycle
- **`plugins/`** — Plugin system package: base class (`PluginSpec`), registry, entry-point discovery, and 8 built-in plugins (one module per plugin)
- **`widgets.py`** — Widget rendering functions
- **`emitters.py`** — Low-level Markdown emitters
- **`assets.py`** — Asset file management
- **`capture.py`** — Stdout/stderr capture

### Key Principles

- **Zero-dependency core.** The core package must never require pandas, matplotlib, or any other dependency. Optional deps use `try/except` with graceful fallback messages.
- **Streamlit-compatible API.** Widget methods should mirror Streamlit's API as closely as possible.
- **Plugin-first.** New widgets belong in built-in plugins (or new plugins), not in the core.

### Adding a New Widget

1. Identify which built-in plugin it belongs to (or create a new one)
2. Add the method to the plugin class in its module under `plugins/` (e.g. `plugins/data.py`)
3. Add rendering logic to `widgets.py` if needed
4. Add tests in `tests/unit/`
5. Update the plugin table in `CLAUDE.md` if adding a new plugin

### Creating a Plugin

See the [Plugin System](#plugin-system) section in the README or:

```python
from notebookmd.plugins import PluginSpec, register_plugin

class MyPlugin(PluginSpec):
    name = "my_plugin"

    def my_widget(self, value: str) -> None:
        self._w(f"**{value}**\n\n")

register_plugin(MyPlugin)
```

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Include tests for new functionality
- Update documentation if adding public API methods
- Ensure all CI checks pass before requesting review
- Write a clear PR description explaining *what* and *why*

## Reporting Issues

- Use the [bug report template](https://github.com/minhlucvan/notebookmd/issues/new?template=bug_report.yml) for bugs
- Use the [feature request template](https://github.com/minhlucvan/notebookmd/issues/new?template=feature_request.yml) for ideas
- Check existing issues before creating a new one

## Code Style

- **Formatter:** Ruff (line length 120)
- **Linter:** Ruff
- **Type checker:** mypy with `disallow_untyped_defs`
- **Docstrings:** Required on all public methods
- **Type hints:** Required everywhere

## License

By contributing to notebookmd, you agree that your contributions will be licensed under the [MIT License](LICENSE).
