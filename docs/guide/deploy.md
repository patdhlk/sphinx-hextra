# Deploy

A `sphinx-hextra` build produces a directory of static HTML files. There
is no server-side component, no database, no runtime Python. That means
you can host the result on anything that serves static files — GitHub
Pages, Read the Docs, Netlify, Cloudflare Pages, Vercel, S3 + CloudFront,
a single-host nginx container. This page shows the most common targets.

## GitHub Pages

The easiest CI-driven option if your source already lives on GitHub. A
workflow that runs on push to `main`, builds with `-W` (warnings as
errors), and deploys to the `gh-pages` environment:

```yaml
name: Deploy docs

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run sphinx-build -W docs docs/_build/html
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs/_build/html

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

There is a working copy of this workflow in the `sphinx-hextra` repo at
`.github/workflows/docs-deploy.yml` you can crib from.

You also need to enable GitHub Pages for the repository under
**Settings → Pages → Source → GitHub Actions**.

## Read the Docs

Read the Docs (RTD) builds your documentation in a sandbox and hosts
it at `<project>.readthedocs.io`. It supports pull-request previews,
multiple versions, and search out of the box. Add a `.readthedocs.yaml`
at the repo root:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"
  jobs:
    post_create_environment:
      - pip install uv
    post_install:
      - uv pip install --system -r requirements.txt

sphinx:
  configuration: docs/conf.py
  fail_on_warning: true

formats:
  - htmlzip
```

RTD needs a `requirements.txt` (or `pyproject.toml` it can install
from) listing `sphinx`, `sphinx-hextra`, and any extensions you use:

```text
sphinx>=7.0
sphinx-hextra>=0.1
myst-parser>=3.0
```

## Netlify

Netlify runs arbitrary build commands and uploads the result. Add a
`netlify.toml` at the repo root:

```toml
[build]
  command = "uv sync && uv run sphinx-build -W docs docs/_build/html"
  publish = "docs/_build/html"

[build.environment]
  PYTHON_VERSION = "3.12"
```

Netlify's Python version is controlled by `PYTHON_VERSION`; 3.12 is a
good baseline. If you want uv to be available without a separate
install step, add the uv installer as the first part of `command`:

```toml
command = "curl -LsSf https://astral.sh/uv/install.sh | sh && . $HOME/.local/bin/env && uv sync && uv run sphinx-build -W docs docs/_build/html"
```

Netlify's preview-deploy-per-PR flow works without further
configuration.

## Cloudflare Pages

Cloudflare Pages is similar to Netlify. In the dashboard, point the
project at your repo and set:

- **Build command:** `pip install uv && uv sync && uv run sphinx-build -W docs docs/_build/html`
- **Build output directory:** `docs/_build/html`
- **Environment variable:** `PYTHON_VERSION=3.12`

Cloudflare's build image comes with Python but not uv; the install
step above is a single line because `pip install uv` is pre-cached.

## Anywhere else

Because the output is plain HTML, any static host works. The shape of
the command you run is always the same:

```bash
uv run sphinx-build -W docs docs/_build/html
```

Then copy the contents of `docs/_build/html/` to wherever you serve
files from. If you build into an image, a minimal Dockerfile looks
like:

```dockerfile
FROM python:3.12-slim AS build
WORKDIR /app
COPY . .
RUN pip install uv && uv sync && uv run sphinx-build -W docs docs/_build/html

FROM nginx:alpine
COPY --from=build /app/docs/_build/html /usr/share/nginx/html
```

Always build with `-W` in CI. Warnings are almost always either a
broken cross-reference, a typo in a directive option, or a page that
slipped out of your toctree — all of which you want to catch before
deployment, not after.
