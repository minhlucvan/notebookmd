# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CI/CD pipeline with GitHub Actions (test matrix, code quality, release automation)
- Contributing guide, Code of Conduct, and Security policy
- Issue and PR templates
- Makefile for common development tasks
- Ruff configuration for linting and formatting

## [0.3.0] - 2026-02-21

### Added
- Core + plugin architecture with `PluginSpec` base class
- 8 built-in plugins: Text, Data, Charts, Status, Layout, Media, Analytics, Utility
- 40+ widget methods mirroring Streamlit's API
- Community plugin discovery via `entry_points`
- `register_plugin()` for global plugin registration
- `Notebook.use()` for per-instance plugin loading
- `NotebookConfig` for customizing rendering behavior

### Changed
- Replaced monolithic `Notebook` class with plugin-based method dispatch
- `section()` replaces old `cell()` API as the primary organizational unit

## [0.2.0] - 2026-02-20

### Added
- Example demos with sample output
- Restructured examples directory

## [0.1.0] - 2026-02-19

### Added
- Initial release
- `Notebook` class with markdown buffering and asset management
- Basic widgets: metric, table, chart, header, text
- Zero-dependency core with optional pandas/matplotlib support
- Asset manager for figures and CSV export

[Unreleased]: https://github.com/minhlucvan/notebookmd/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/minhlucvan/notebookmd/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/minhlucvan/notebookmd/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/minhlucvan/notebookmd/releases/tag/v0.1.0
