# sphinx-hextra — Design Spec

**Date:** 2026-04-11
**Status:** Approved for planning
**Author:** Patrick Dahlke

## 1. Overview

`sphinx-hextra` is a Sphinx HTML theme and companion directive set that brings the look and feel of the [Hextra](https://github.com/imfing/hextra) Hugo theme (MIT, © Imfing and contributors) to the Sphinx documentation ecosystem.

The motivation is pragmatic: Hextra is one of the most attractive modern documentation themes available, but Sphinx offers capabilities the Hugo ecosystem does not — most importantly [sphinx-needs](https://github.com/useblocks/sphinx-needs) for engineering-as-code requirements management. `sphinx-hextra` lets users adopt the Hextra aesthetic without giving up the Sphinx toolchain.

This is an open-source, derivative-work project published under MIT. Upstream Hextra authorship is preserved in `licenses/HEXTRA-LICENSE` and credited in `README.md` and `CREDITS.md`.

## 2. Goals and Non-Goals

### Goals (v0.1)

- Ship a pip-installable Sphinx HTML theme that is visually recognisable as "Hextra on Sphinx": top nav, left sidebar, right TOC, dark mode, typography, gradients.
- Provide Sphinx-native directives for Hextra's five core content components: Callout, Cards, Tabs, Steps, FileTree.
- Provide landing-page directives (`hextra-hero`, `hextra-feature-grid`, `hextra-feature`) so users can build a Hextra-style home page in `index.md`.
- Provide styled (not deep) integration with sphinx-needs: scoped CSS so `needtable`, `needextract`, and status badges match the Hextra aesthetic in both light and dark mode.
- Install and build with zero Node dependency for end users. CSS is compiled by maintainers in CI and shipped inside the wheel.
- Support Python 3.10+ and Sphinx 7+, managed with `uv`.

### Non-Goals (v0.1)

- Hugo shortcode syntax compatibility. Directives use native Sphinx/MyST syntax.
- A reskinned search UI (Cmd-K command palette). Sphinx's built-in search is used as-is and styled lightly. Reskin deferred to v0.2.
- Visual regression testing infrastructure (Playwright/Percy). Deferred to v0.2.
- Icon, PDF embed, and Jupyter-tabs directives. Deferred.
- `Details`/collapsible directive — users already have `sphinx-design`'s `dropdown`.
- Dark mode support for `needflow` (PlantUML-rendered SVG — out of scope).
- Multi-package split. One package, `sphinx-hextra`, ships theme + directives together.
- Conda-forge distribution at launch. PyPI only; conda-forge may follow once the API stabilizes.

## 3. Architecture

`sphinx-hextra` has two distinct build axes.

### 3.1 Developer-side build (maintainer, CI)

Tailwind CSS compiles source styles under `assets/css/` into a single committed output file at `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css`. This runs in CI on release (and optionally locally via `npm run build:css`). The compiled CSS is the only CSS that ships in the wheel. Tailwind sources are dev-only and excluded from the distribution.

Dark mode uses Tailwind's `class` strategy — a `dark` class on `<html>` flips the whole palette. No runtime CSS compilation.

### 3.2 User-side build (end user's `sphinx-build`)

Pure Python, no Node. The user adds `sphinx_hextra` to `extensions` in `conf.py` and sets `html_theme = "sphinx_hextra"`. The package:

1. Registers the theme directory via the `sphinx.html_themes` entry point and `app.add_html_theme`.
2. Adds the compiled CSS and JS bundles to every page via `app.add_css_file` / `app.add_js_file`.
3. Registers the content directives and the landing-page directives.
4. Detects `sphinx-needs` in `app.extensions` and, if present, adds the scoped needs-integration CSS.

### 3.3 Theme inheritance

`theme.toml` inherits from Sphinx's `basic` theme. We override `layout.html`, `page.html`, and `search.html` entirely but retain `basic`'s search scaffolding (`searchindex.js`, `search.html` integration) unchanged in v0.1.

### 3.4 Dark mode

A small vanilla-JS module (`theme-toggle.js`) toggles a `dark` class on `<html>` and persists the user's choice in `localStorage`. Initial state is resolved from `localStorage` → `prefers-color-scheme` → light. No Python-side state.

## 4. Repository and Package Layout

```
sphinx-hextra/
├── pyproject.toml              # hatchling build, entry point, uv-managed
├── uv.lock
├── README.md                   # credits Hextra prominently
├── CREDITS.md                  # Hextra contributors from their git log
├── LICENSE                     # MIT (our code)
├── licenses/
│   └── HEXTRA-LICENSE          # upstream Hextra MIT license, verbatim
├── package.json                # Tailwind + build tooling (dev only)
├── tailwind.config.js
├── assets/                     # dev-only, excluded from wheel
│   ├── css/
│   │   ├── main.css
│   │   ├── components/
│   │   │   ├── callout.css
│   │   │   ├── cards.css
│   │   │   ├── tabs.css
│   │   │   ├── steps.css
│   │   │   └── filetree.css
│   │   ├── sphinx-needs.css
│   │   └── landing.css
│   └── js/
│       ├── theme-toggle.js
│       ├── sidebar.js
│       └── tabs.js
├── src/sphinx_hextra/
│   ├── __init__.py             # setup(app), __version__
│   ├── directives/
│   │   ├── __init__.py
│   │   ├── callout.py
│   │   ├── cards.py            # hextra-cards + hextra-card
│   │   ├── tabs.py
│   │   ├── steps.py
│   │   ├── filetree.py
│   │   └── landing.py          # hextra-hero + hextra-feature-grid
│   ├── needs_integration.py
│   └── theme/sphinx_hextra/
│       ├── theme.toml
│       ├── layout.html
│       ├── page.html
│       ├── search.html
│       ├── partials/
│       │   ├── navbar.html
│       │   ├── sidebar.html
│       │   ├── toc.html
│       │   ├── footer.html
│       │   └── theme-toggle.html
│       └── static/
│           ├── sphinx-hextra.css    # compiled, committed
│           └── sphinx-hextra.js     # bundled, committed
├── tests/
│   ├── conftest.py
│   ├── test_build.py
│   ├── test_directives/
│   └── roots/                  # minimal Sphinx projects per test
├── docs/                       # self-hosted demo + real docs
│   ├── conf.py
│   ├── index.md                # uses hextra-hero/feature-grid
│   └── ...
└── .github/workflows/
    ├── ci.yml
    ├── css-build.yml
    ├── release.yml
    └── docs-deploy.yml
```

### 4.1 `theme.toml`

```toml
[theme]
inherit = "basic"
stylesheets = ["sphinx-hextra.css"]
sidebars = ["sphinx_hextra/partials/sidebar.html"]
pygments_style = { default = "friendly", dark = "monokai" }

[options]
# Theme-level options surfaced via html_theme_options
navbar_title = ""
navbar_logo = ""
github_url = ""
edit_page_url_template = ""
show_toc = true
```

### 4.2 `pyproject.toml` highlights

```toml
[project]
name = "sphinx-hextra"
requires-python = ">=3.10"
dependencies = ["sphinx>=7", "docutils>=0.19"]

[project.entry-points."sphinx.html_themes"]
sphinx_hextra = "sphinx_hextra"

[tool.hatch.build.targets.wheel]
packages = ["src/sphinx_hextra"]

[tool.hatch.build.targets.wheel.force-include]
"src/sphinx_hextra/theme" = "sphinx_hextra/theme"

[tool.hatch.build]
exclude = ["assets/", "package.json", "tailwind.config.js", "node_modules/"]
```

## 5. Directive API

All directives work in reStructuredText and MyST Markdown. Primary authoring target is MyST. Every directive emits semantic HTML with stable BEM-ish classnames (`hx-callout`, `hx-cards`, `hx-cards__item`) so users can override CSS without inspecting generated structure. No required options — sensible defaults everywhere.

### 5.1 `hextra-callout`

```markdown
```{hextra-callout} warning
This is a warning callout.
```
```

- Positional argument: type (`info` | `warning` | `error` | `default`). Default: `info`.
- Option `:emoji:` — override the default icon.
- Rendered as `<div class="hx-callout hx-callout--warning">` with icon + body.

### 5.2 `hextra-cards` + `hextra-card`

```markdown
```{hextra-cards}
:columns: 3

```{hextra-card} Getting Started
:link: quickstart.html
:icon: rocket
Quick intro to the project.
```
```
```

- `hextra-cards` option `:columns:` — integer 1–4, default 2.
- `hextra-card` positional argument: title.
- `hextra-card` options: `:link:`, `:icon:` (name from bundled Lucide subset), `:image:`.

### 5.3 `hextra-tabs`

```markdown
```{hextra-tabs}
:items: macOS, Linux, Windows

### macOS
Apple's desktop OS.

### Linux
Open-source OS.

### Windows
Microsoft's OS.
```
```

- Option `:items:` — comma-separated tab labels.
- Tab bodies delimited by H3 headings inside the directive. Heading text must match `items` labels in order.
- Active tab state persisted per-page in `sessionStorage`.

### 5.4 `hextra-steps`

```markdown
```{hextra-steps}
### Install dependencies
Run `uv sync`.

### Start the dev server
Run `sphinx-autobuild docs _build/html`.
```
```

- H3 headings become step titles.
- Rendered as vertical list with auto-numbered circular markers.

### 5.5 `hextra-filetree`

```markdown
```{hextra-filetree}
- content/
  - _index.md
  - docs/
    - intro.md
- conf.py
```
```

- Parser walks a bullet list. Items ending in `/` become folders; others become files.
- Emits nested `<ul>` with folder/file icons.

### 5.6 Landing-page directives

**`hextra-hero`**

```markdown
```{hextra-hero}
:title: Sphinx, the Hextra way
:tagline: Beautiful docs with sphinx-needs power.
:cta-text: Get started
:cta-link: quickstart.html
```
```

**`hextra-feature-grid`** + **`hextra-feature`**

Mirror of cards but with heavier styling (gradient backgrounds, larger images, title/subtitle). Used on the home page.

### 5.7 Implementation pattern

Directives are thin. Each directive:
1. Subclasses `docutils.parsers.rst.Directive` (or a small shared base class).
2. Parses options and nested content into docutils nodes.
3. Delegates HTML rendering to `visit_*` / `depart_*` methods registered via `app.add_node(node, html=(visit, depart))`.

This keeps directive logic decoupled from HTML output and makes the node tree inspectable in tests.

## 6. sphinx-needs Integration

`sphinx_hextra.needs_integration` is imported unconditionally but only activates if `sphinx_needs` is present in `app.extensions` at `builder-inited` time. When active, it injects `sphinx-needs.css` — a scoped stylesheet that restyles:

- `needtable` (rounded corners, theme borders, dark-mode table rows)
- Need status/type badges (Hextra callout palette, rounded pills)
- `needextract` blocks (bordered, hover state)
- `need` inline blocks (status dot, subtle background)

No Jinja template overrides. No modification of sphinx-needs output structure. The scoped CSS targets sphinx-needs' stable output classes only.

`needflow` is explicitly out of scope for v0.1 styling.

## 7. Testing Strategy

Three layers:

1. **Unit tests for directives** — pytest + docutils. Each directive has a test that parses a minimal snippet and asserts the generated node tree structure. Fast, no full Sphinx build.

2. **Integration tests** — `sphinx.testing.fixtures`. Each directive gets a minimal Sphinx project under `tests/roots/test-<directive>/` with a `conf.py` using the theme and a single source file. Tests assert built HTML contains expected class names and structure. One root includes `sphinx_needs` and asserts need tables render alongside our CSS without breakage.

3. **Docs build smoke test** — CI runs `sphinx-build -W --keep-going docs/ _build/html` on the real docs site. Warnings are errors. This is the canary for template breakage.

Visual regression testing is deferred to v0.2.

## 8. CI, Release, and Distribution

All via GitHub Actions.

### 8.1 `ci.yml`

- Triggers: push, PR.
- Matrix: Python {3.10, 3.11, 3.12, 3.13} × Sphinx {7.x, 8.x}, Ubuntu only.
- Steps: `uv sync`, `uv run pytest`, `uv run sphinx-build -W docs _build/html`.

### 8.2 `css-build.yml`

- Triggers: PR touching `assets/**`, `tailwind.config.js`, or `package.json`.
- Steps: `npm ci`, `npm run build:css`, diff `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css`.
- Fails if the compiled CSS differs from what's committed, with a message telling the contributor to run `npm run build:css` locally and commit the result.
- Does not auto-commit.

### 8.3 `release.yml`

- Triggers: version tag push (`v*`).
- Steps: checkout → fresh `npm run build:css` → `uv build` → verify wheel contents → publish to PyPI via Trusted Publishing (OIDC, no API tokens) → create GitHub Release with auto-generated notes.

### 8.4 `docs-deploy.yml`

- Triggers: push to `main`.
- Deploys `docs/_build/html` to GitHub Pages. The live site doubles as the demo.

### 8.5 Versioning

Semantic versioning, v0.x.y until API stabilizes. `CHANGELOG.md` in Keep a Changelog format, maintained manually.

## 9. Licensing and Attribution

- Package license: MIT (our own code).
- `licenses/HEXTRA-LICENSE` contains the verbatim upstream Hextra MIT license.
- `README.md` credits Hextra prominently in the intro paragraph, links to the upstream repo, and notes that `sphinx-hextra` is a derivative work.
- `CREDITS.md` lists Hextra contributors extracted from the upstream git log at the time of our initial port, plus a link to the live contributor list.
- `pyproject.toml` `Author` field lists the current maintainer. A `Contributors` section in `CREDITS.md` captures the dual authorship.
- Any CSS or HTML fragment directly ported from Hextra retains a source comment referencing the upstream file path.

## 10. Out of Scope / Deferred

- Hugo shortcode syntax compatibility layer.
- Cmd-K search palette / Pagefind / FlexSearch.
- Visual regression CI (Playwright/Percy).
- `Icon`, `Details`, `PDF`, `Jupyter` directives.
- Conda-forge distribution.
- `needflow` dark-mode support.
- i18n of directive output (we inherit Sphinx's i18n mechanisms for prose, but directive labels are English in v0.1).
- Theme options for radically different layouts (single-page, book-style). v0.1 ships one layout: Hextra's default.

## 11. Open Questions (non-blocking)

None that block planning. Questions likely to surface during implementation:

- Exact Lucide icon subset to bundle with `hextra-card`'s `:icon:` option.
- Whether to ship a small set of built-in colour presets for the gradient hero backgrounds or expose them as CSS variables only.
- Whether to add an `:ref:`-aware variant of `hextra-card`'s `:link:` option so users can reference other Sphinx pages by docname rather than URL.

These are implementation-level decisions and do not block writing the plan.
