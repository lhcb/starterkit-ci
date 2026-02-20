# starterkit-ci

Helpers and Sphinx configuration for building and checking the LHCb Starterkit lessons documentation.

This package provides:
- A CLI command, `starterkit-ci`, to run Sphinx build/linkcheck in a consistent way.
- Shared Sphinx configuration under `starterkit_ci.sphinx_config`.
- Custom Sphinx transforms used by Starterkit lesson content.

## Installation

With `uv`:

```bash
uv add starterkit-ci
```

With `pip`:

```bash
pip install starterkit-ci
```

For local development in this repository:

```bash
uv sync --frozen --group dev
```

## CLI usage

The package exposes a console script: `starterkit-ci`.
The legacy alias `starterkit_ci` is still available for compatibility.

### Build docs

```bash
starterkit-ci build --source-dir /path/to/docs
```

### Check external links

```bash
starterkit-ci check --source-dir /path/to/docs
```

### Clean Sphinx build output

```bash
starterkit-ci clean --source-dir /path/to/docs
```

By default warnings are treated as errors (`-W`). To allow warnings:

```bash
starterkit-ci build --source-dir /path/to/docs --allow-warnings
```

### Run without installing (uvx)

You can run the tool directly from PyPI without adding it to your environment:

```bash
uvx starterkit-ci build --source-dir /path/to/docs
uvx starterkit-ci check --source-dir /path/to/docs
```

## Using the shared Sphinx config

In a docs project `conf.py`:

```python
from starterkit_ci.sphinx_config import *  # NOQA
```

You can then extend settings in your project, for example:
- `starterkit_ci_redirects` for HTML redirects.
- `setup.extra_setup_funcs` for project-specific setup hooks.

## Development

Run tests:

```bash
uv run pytest
```

Run code quality checks:

```bash
pre-commit run --all-files
```

## CI and releases

- `pre-commit` hooks run in GitHub Actions via `prek`.
- Unit tests run on Python 3.10 to 3.14.
- Integration workflow validates against the real `lhcb/starterkit-lessons` repository.
- Package builds use `uv build`.
- PyPI publishing uses trusted publishing on tags.
