# How to release

This project now uses `python-semantic-release`.

## Normal flow

1. Merge conventional commits into `master`
2. Let the `Semantic Release` GitHub Actions workflow determine the next version
3. The workflow updates `datemath/_version.py`, updates `CHANGELOG.md`, creates the tag, and publishes a GitHub release
4. The PyPI publish workflow runs from that GitHub release

## Commit types that affect versioning

- `feat:` bumps the minor version
- `fix:` bumps the patch version
- `perf:` bumps the patch version
- `BREAKING CHANGE:` in the body or footer bumps the major version

Commits like `docs:`, `test:`, `ci:`, and `chore:` are allowed but do not trigger a release by themselves.

## Local checks

```bash
uv sync --group dev
uv run pre-commit run --all-files
uv run semantic-release -c .releaserc.toml version --print
```
