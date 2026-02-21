# Publish notebookmd to PyPI

Publish a new version of the notebookmd package. Follow these steps exactly:

## 1. Pre-flight checks

- Run the full test suite: `pytest tests/ -v`
- Run lint: `ruff check .`
- Run format check: `ruff format --check .`
- If any checks fail, fix the issues before proceeding.

## 2. Determine the new version

- Read the current version from `notebookmd/__init__.py` (`__version__`)
- Ask the user what the new version should be, suggesting the next patch/minor/major based on the current version.

## 3. Bump the version

Update the version string in **both** files (they must stay in sync):
- `pyproject.toml` → `version = "X.Y.Z"`
- `notebookmd/__init__.py` → `__version__ = "X.Y.Z"`

## 4. Update CHANGELOG.md

- Add a new section at the top for the new version with today's date
- Ask the user for a summary of changes, or generate one from recent commits since the last tag
- Follow the existing changelog format

## 5. Commit, tag, and push

```
git add pyproject.toml notebookmd/__init__.py CHANGELOG.md
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

The `v*` tag push triggers `.github/workflows/release.yml` which automatically:
1. Builds the package
2. Tests it on Python 3.11/3.12/3.13
3. Publishes to PyPI (via trusted publishing)
4. Creates a GitHub Release with auto-generated notes

## 6. Verify

After pushing, tell the user to check:
- GitHub Actions: `https://github.com/minhlucvan/notebookmd/actions/workflows/release.yml`
- PyPI: `https://pypi.org/project/notebookmd/`

Remind the user that trusted publishing must be configured on PyPI for the first release (owner: `minhlucvan`, repo: `notebookmd`, workflow: `release.yml`, environment: `pypi`).
