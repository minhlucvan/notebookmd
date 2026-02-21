# notebookmd Documentation

This directory contains the full documentation for notebookmd.

## Contents

| Document | Description |
|----------|-------------|
| [index.md](index.md) | Landing page — features overview and architecture |
| [getting-started.md](getting-started.md) | Installation, first report, core concepts |
| [api-reference.md](api-reference.md) | Core classes and functions (`nb()`, `Notebook`, `NotebookConfig`, `AssetManager`, `Runner`) |
| [widgets.md](widgets.md) | Complete catalog of 48+ widget methods across 8 plugin categories |
| [plugins.md](plugins.md) | Plugin system — built-in plugins, custom plugins, entry-point discovery |
| [cli.md](cli.md) | CLI reference — `notebookmd run`, `notebookmd cache`, variable injection |
| [configuration.md](configuration.md) | `NotebookConfig` options, output paths, optional dependencies, environment patterns |
| [caching.md](caching.md) | `@cache_data` and `@cache_resource` decorators, cache management |
| [examples.md](examples.md) | 8+ complete runnable examples (sales report, data quality, ML evaluation, and more) |
| [community-launch-plan.md](community-launch-plan.md) | Community launch strategy and marketing plan |

## Reading Order

If you're new to notebookmd, read the docs in this order:

1. **[getting-started.md](getting-started.md)** — Install, write your first report
2. **[widgets.md](widgets.md)** — Browse available widgets
3. **[configuration.md](configuration.md)** — Customize output behavior
4. **[plugins.md](plugins.md)** — Extend with custom plugins
5. **[cli.md](cli.md)** — Run scripts from the command line
6. **[caching.md](caching.md)** — Speed up repeated computations
7. **[api-reference.md](api-reference.md)** — Deep dive into internals
8. **[examples.md](examples.md)** — Full end-to-end examples

## Building Docs

The documentation is plain Markdown and can be read directly on GitHub or rendered with any static site generator (MkDocs, Sphinx, etc.).

To serve locally with MkDocs:

```bash
pip install mkdocs
mkdocs serve
```
