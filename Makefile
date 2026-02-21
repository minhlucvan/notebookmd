.PHONY: help install dev test test-unit test-integration lint fix format typecheck check clean build publish

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e ".[all,dev]"

dev: install ## Install with dev + quality tools
	pip install ruff mypy pandas-stubs

test: ## Run all tests
	python -m pytest tests/ -v

test-unit: ## Run unit tests only
	python -m pytest tests/unit/ -v

test-integration: ## Run integration tests only
	python -m pytest tests/integration/ -v

test-core: ## Run tests with zero dependencies (core only)
	pip install -e .
	python -m pytest tests/ -v

lint: ## Run linter and format check
	ruff check .
	ruff format --check .

fix: ## Auto-fix lint issues and format code
	ruff check --fix .
	ruff format .

format: fix ## Alias for fix

typecheck: ## Run type checker
	mypy notebookmd/ --ignore-missing-imports

check: lint typecheck test ## Run all quality checks (lint + typecheck + test)

clean: ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean ## Build distribution packages
	python -m build

publish: build ## Publish to PyPI (use with caution)
	python -m twine upload dist/*
