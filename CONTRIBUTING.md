# Contributing to sphinx-hextra

Thanks for considering a contribution! This project is small, so the process is simple.

## Development setup

```bash
uv sync --group dev
```

If you plan to touch CSS or JS:

```bash
npm install
```

## Running the test suite

```bash
uv run pytest
```

## Building the demo docs site

```bash
uv run sphinx-build -W --keep-going docs docs/_build/html
open docs/_build/html/index.html
```

## Touching CSS or JS

After changing anything under `assets/`, rebuild the compiled CSS:

```bash
npm run build:css
```

and commit the updated files under `src/sphinx_hextra/theme/sphinx_hextra/static/`. CI will reject PRs where the committed CSS is stale.

## Commit style

Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `test:`, `build:`).

## Credit

If you port additional concepts from upstream Hextra, note it in your PR description and keep a comment reference in the ported code. Upstream is MIT; we honour attribution.
