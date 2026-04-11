# sphinx-hextra v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `sphinx-hextra` v0.1 — a Sphinx HTML theme plus directive set that brings the Hextra Hugo theme aesthetic to Sphinx, with integration styling for sphinx-needs.

**Architecture:** Single Python package (`src/sphinx_hextra/`) managed with `uv`, built with Hatchling, registered via the `sphinx.html_themes` entry point. Tailwind CSS compiles dev-side only; compiled CSS ships inside the wheel. Five content directives + landing-page directives emit semantic HTML from docutils nodes. End users never install Node.

**Tech Stack:** Python 3.10+, Sphinx 7+, uv, Hatchling, Tailwind CSS 3.x, pytest, pytest-sphinx (via `sphinx.testing.fixtures`), GitHub Actions, MyST-Parser.

**Spec:** `docs/superpowers/specs/2026-04-11-sphinx-hextra-design.md`

---

## Background: key conventions for all tasks

- **Test runner:** `uv run pytest` for Python tests. All Python commands go through `uv run`.
- **Test location:** `tests/unit/` for directive unit tests (docutils-only), `tests/integration/` for full `sphinx-build` tests using `tests/roots/`.
- **Commit style:** Conventional Commits (`feat:`, `test:`, `docs:`, `chore:`, `ci:`, `build:`).
- **Every task ends in a commit.** Frequent commits are required.
- **HTML classname prefix:** `hx-` for all directive output. BEM-style (`hx-callout`, `hx-callout--warning`, `hx-cards__item`).
- **Branch:** work on `main` directly — this is a greenfield repo. No PR review gate in v0.1.

---

## Task 1: Project scaffolding — pyproject.toml, uv, src layout

**Files:**
- Create: `pyproject.toml`
- Create: `src/sphinx_hextra/__init__.py`
- Create: `.gitignore`
- Create: `.python-version`

- [ ] **Step 1: Create `.gitignore`**

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
dist/
build/

# Node
node_modules/

# Sphinx build output
_build/

# IDE
.idea/
.vscode/
.DS_Store

# uv
.python-version.local
```

- [ ] **Step 2: Create `.python-version`**

```
3.12
```

- [ ] **Step 3: Create `pyproject.toml`**

```toml
[project]
name = "sphinx-hextra"
version = "0.1.0.dev0"
description = "A Sphinx theme and directive set bringing the Hextra aesthetic to Sphinx, with sphinx-needs integration."
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.10"
authors = [{ name = "Patrick Dahlke" }]
keywords = ["sphinx", "theme", "documentation", "hextra", "sphinx-needs"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Framework :: Sphinx",
    "Framework :: Sphinx :: Theme",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Documentation :: Sphinx",
]
dependencies = [
    "sphinx>=7",
    "docutils>=0.19",
]

[project.urls]
Homepage = "https://github.com/patdhlk/sphinx-hextra"
Repository = "https://github.com/patdhlk/sphinx-hextra"
Issues = "https://github.com/patdhlk/sphinx-hextra/issues"

[project.entry-points."sphinx.html_themes"]
sphinx_hextra = "sphinx_hextra"

[dependency-groups]
dev = [
    "pytest>=8",
    "pytest-xdist>=3",
    "myst-parser>=3",
    "sphinx-needs>=3",
    "beautifulsoup4>=4.12",
    "lxml>=5",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/sphinx_hextra"]

[tool.hatch.build.targets.wheel.force-include]
"src/sphinx_hextra/theme" = "sphinx_hextra/theme"

[tool.hatch.build]
exclude = [
    "assets/",
    "package.json",
    "package-lock.json",
    "tailwind.config.js",
    "node_modules/",
    "tests/",
    "docs/",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"
```

- [ ] **Step 4: Create `src/sphinx_hextra/__init__.py`**

```python
"""sphinx-hextra: Hextra-inspired Sphinx theme with component directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__version__ = "0.1.0.dev0"

_THEME_PATH = Path(__file__).resolve().parent / "theme"


def setup(app: Any) -> dict[str, Any]:
    app.add_html_theme("sphinx_hextra", str(_THEME_PATH / "sphinx_hextra"))
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```

- [ ] **Step 5: Run `uv sync` and verify it resolves**

Run: `uv sync`
Expected: creates `.venv/`, resolves all deps, writes `uv.lock`.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/sphinx_hextra/__init__.py .gitignore .python-version uv.lock
git commit -m "feat: scaffold sphinx-hextra package with uv and hatchling"
```

---

## Task 2: Minimal theme skeleton — theme.toml and layout.html that builds

**Files:**
- Create: `src/sphinx_hextra/theme/sphinx_hextra/theme.toml`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/layout.html`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css`
- Create: `tests/integration/roots/test-theme-loads/conf.py`
- Create: `tests/integration/roots/test-theme-loads/index.rst`
- Create: `tests/integration/test_theme_loads.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write failing integration test for theme loading**

`tests/conftest.py`:
```python
from __future__ import annotations

from pathlib import Path

import pytest

pytest_plugins = ["sphinx.testing.fixtures"]


@pytest.fixture(scope="session")
def rootdir() -> Path:
    return Path(__file__).parent / "integration" / "roots"
```

`tests/integration/roots/test-theme-loads/conf.py`:
```python
project = "test"
extensions = []
html_theme = "sphinx_hextra"
exclude_patterns = ["_build"]
```

`tests/integration/roots/test-theme-loads/index.rst`:
```rst
Test
====

Hello world.
```

`tests/integration/test_theme_loads.py`:
```python
import pytest


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_theme_builds_without_errors(app, status, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    assert (app.outdir / "index.html").exists()


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_theme_css_is_copied(app):
    app.build()
    assert (app.outdir / "_static" / "sphinx-hextra.css").exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/integration/test_theme_loads.py -v`
Expected: FAIL — theme directory is missing required files.

- [ ] **Step 3: Create `theme.toml`**

`src/sphinx_hextra/theme/sphinx_hextra/theme.toml`:
```toml
[theme]
inherit = "basic"
stylesheets = ["sphinx-hextra.css"]
pygments_style = { default = "friendly", dark = "monokai" }

[options]
navbar_title = ""
navbar_logo = ""
github_url = ""
edit_page_url_template = ""
show_toc = true
```

- [ ] **Step 4: Create minimal `layout.html`**

`src/sphinx_hextra/theme/sphinx_hextra/layout.html`:
```html
{%- extends "basic/layout.html" %}

{% block extrahead %}
  {{ super() }}
  <meta name="generator" content="sphinx-hextra {{ sphinx_hextra_version|default('') }}">
{% endblock %}
```

- [ ] **Step 5: Create empty compiled CSS placeholder**

`src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css`:
```css
/* Compiled by Tailwind. See Task 4. This placeholder is replaced in Task 4. */
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest tests/integration/test_theme_loads.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/sphinx_hextra/theme tests/conftest.py tests/integration
git commit -m "feat: minimal theme skeleton inheriting from basic"
```

---

## Task 3: Node toolchain — package.json, Tailwind config, empty source CSS

**Files:**
- Create: `package.json`
- Create: `tailwind.config.js`
- Create: `assets/css/main.css`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "sphinx-hextra-build",
  "private": true,
  "version": "0.0.0",
  "description": "Build tooling for sphinx-hextra CSS assets. Not published.",
  "scripts": {
    "build:css": "tailwindcss -i ./assets/css/main.css -o ./src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css --minify",
    "watch:css": "tailwindcss -i ./assets/css/main.css -o ./src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css --watch"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",
    "@tailwindcss/typography": "^0.5.10"
  }
}
```

- [ ] **Step 2: Create `tailwind.config.js`**

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/sphinx_hextra/theme/**/*.html",
    "./assets/**/*.{css,js}",
    "./src/sphinx_hextra/directives/**/*.py",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        hextra: {
          primary: "#6366f1",
          "primary-dark": "#818cf8",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
```

- [ ] **Step 3: Create `assets/css/main.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --hx-bg: #ffffff;
    --hx-fg: #1f2937;
    --hx-border: #e5e7eb;
    --hx-muted: #6b7280;
    --hx-accent: #6366f1;
  }

  html.dark {
    --hx-bg: #0b0f19;
    --hx-fg: #e5e7eb;
    --hx-border: #1f2937;
    --hx-muted: #9ca3af;
    --hx-accent: #818cf8;
  }

  body {
    background: var(--hx-bg);
    color: var(--hx-fg);
    font-family: theme("fontFamily.sans");
  }
}
```

- [ ] **Step 4: Install Node deps and run build**

Run:
```bash
npm install
npm run build:css
```
Expected: produces `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css` with real Tailwind output.

- [ ] **Step 5: Commit**

```bash
git add package.json package-lock.json tailwind.config.js assets/css/main.css \
        src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css
git commit -m "build: add Tailwind CSS toolchain and base styles"
```

---

## Task 4: Theme partials — navbar, sidebar, toc, footer, theme-toggle

**Files:**
- Create: `src/sphinx_hextra/theme/sphinx_hextra/partials/navbar.html`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/partials/sidebar.html`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/partials/toc.html`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/partials/footer.html`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/partials/theme-toggle.html`
- Modify: `src/sphinx_hextra/theme/sphinx_hextra/layout.html`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/page.html`
- Create: `tests/integration/test_layout_structure.py`

- [ ] **Step 1: Write failing test asserting layout structure**

`tests/integration/test_layout_structure.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_navbar(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("nav.hx-navbar"), "navbar missing"


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_sidebar(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("aside.hx-sidebar"), "sidebar missing"


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_theme_toggle(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("button.hx-theme-toggle"), "theme toggle missing"


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_footer(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("footer.hx-footer"), "footer missing"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_layout_structure.py -v`
Expected: FAIL — no custom layout yet.

- [ ] **Step 3: Create `partials/navbar.html`**

```html
<nav class="hx-navbar">
  <div class="hx-navbar__inner">
    <a class="hx-navbar__brand" href="{{ pathto(master_doc) }}">
      {%- if theme_navbar_logo %}
        <img src="{{ pathto('_static/' ~ theme_navbar_logo, 1) }}" alt="logo">
      {%- endif %}
      <span>{{ theme_navbar_title or project }}</span>
    </a>
    <div class="hx-navbar__actions">
      {%- if theme_github_url %}
        <a class="hx-navbar__github" href="{{ theme_github_url }}" aria-label="GitHub">GitHub</a>
      {%- endif %}
      {%- include "sphinx_hextra/partials/theme-toggle.html" %}
    </div>
  </div>
</nav>
```

- [ ] **Step 4: Create `partials/sidebar.html`**

```html
<aside class="hx-sidebar">
  <div class="hx-sidebar__inner">
    {{ toctree(maxdepth=3, collapse=False, includehidden=True, titles_only=False) }}
  </div>
</aside>
```

- [ ] **Step 5: Create `partials/toc.html`**

```html
{%- if theme_show_toc and display_toc %}
<aside class="hx-toc">
  <div class="hx-toc__title">On this page</div>
  {{ toc }}
</aside>
{%- endif %}
```

- [ ] **Step 6: Create `partials/footer.html`**

```html
<footer class="hx-footer">
  <div class="hx-footer__inner">
    <span>Built with <a href="https://github.com/patdhlk/sphinx-hextra">sphinx-hextra</a>, inspired by <a href="https://github.com/imfing/hextra">Hextra</a>.</span>
    {%- if copyright %}
      <span>&copy; {{ copyright }}</span>
    {%- endif %}
  </div>
</footer>
```

- [ ] **Step 7: Create `partials/theme-toggle.html`**

```html
<button type="button" class="hx-theme-toggle" aria-label="Toggle color theme">
  <span class="hx-theme-toggle__sun" aria-hidden="true">☀</span>
  <span class="hx-theme-toggle__moon" aria-hidden="true">☾</span>
</button>
```

- [ ] **Step 8: Replace `layout.html` with full layout**

`src/sphinx_hextra/theme/sphinx_hextra/layout.html`:
```html
<!DOCTYPE html>
<html lang="{{ language or 'en' }}" class="hx-html">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title|striptags|e }} — {{ project|e }}</title>
  {%- block css %}
    {%- for css in css_files %}
      {%- if css|attr("filename") %}
        {{ css_tag(css) }}
      {%- else %}
        <link rel="stylesheet" href="{{ pathto(css, 1)|e }}" type="text/css">
      {%- endif %}
    {%- endfor %}
  {%- endblock %}
  {%- block extrahead %}{% endblock %}
</head>
<body class="hx-body">
  {%- include "sphinx_hextra/partials/navbar.html" %}
  <div class="hx-shell">
    {%- include "sphinx_hextra/partials/sidebar.html" %}
    <main class="hx-main">
      <article class="hx-content">
        {% block body %}{% endblock %}
      </article>
      {%- include "sphinx_hextra/partials/toc.html" %}
    </main>
  </div>
  {%- include "sphinx_hextra/partials/footer.html" %}
  {%- block scripts %}
    {%- for scriptfile in script_files %}
      {{ js_tag(scriptfile) }}
    {%- endfor %}
  {%- endblock %}
</body>
</html>
```

- [ ] **Step 9: Create `page.html`**

```html
{%- extends "sphinx_hextra/layout.html" %}
{%- block body %}
  {{ body }}
{%- endblock %}
```

- [ ] **Step 10: Run tests to verify they pass**

Run: `uv run pytest tests/integration/test_layout_structure.py -v`
Expected: PASS.

- [ ] **Step 11: Commit**

```bash
git add src/sphinx_hextra/theme tests/integration/test_layout_structure.py
git commit -m "feat: layout partials for navbar, sidebar, toc, footer, theme toggle"
```

---

## Task 5: Theme toggle JavaScript and JS registration

**Files:**
- Create: `assets/js/theme-toggle.js`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/static/theme-toggle.js`
- Modify: `src/sphinx_hextra/__init__.py`
- Create: `tests/integration/test_js_assets.py`

- [ ] **Step 1: Write failing test for JS asset registration**

`tests/integration/test_js_assets.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_theme_toggle_js_loaded(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    scripts = [s.get("src", "") for s in soup.find_all("script")]
    assert any("theme-toggle.js" in s for s in scripts), scripts
```

- [ ] **Step 2: Run test — should fail**

Run: `uv run pytest tests/integration/test_js_assets.py -v`
Expected: FAIL — no theme-toggle.js registered.

- [ ] **Step 3: Create `assets/js/theme-toggle.js`**

```js
(function () {
  "use strict";

  var STORAGE_KEY = "sphinx-hextra:theme";
  var root = document.documentElement;

  function apply(theme) {
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }

  function resolveInitial() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored === "dark" || stored === "light") return stored;
    } catch (e) { /* ignore */ }
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }

  apply(resolveInitial());

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".hx-theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var next = root.classList.contains("dark") ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* ignore */ }
    });
  });
})();
```

- [ ] **Step 4: Copy the file to the theme static dir (build step placeholder)**

For now, commit the file into both `assets/js/` and `src/sphinx_hextra/theme/sphinx_hextra/static/theme-toggle.js` — we'll add automation in Task 18 (release workflow). Copy verbatim.

- [ ] **Step 5: Register JS in `setup()`**

Modify `src/sphinx_hextra/__init__.py`:
```python
"""sphinx-hextra: Hextra-inspired Sphinx theme with component directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__version__ = "0.1.0.dev0"

_THEME_PATH = Path(__file__).resolve().parent / "theme"


def setup(app: Any) -> dict[str, Any]:
    app.add_html_theme("sphinx_hextra", str(_THEME_PATH / "sphinx_hextra"))
    app.add_js_file("theme-toggle.js")
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```

- [ ] **Step 6: Run tests — should pass**

Run: `uv run pytest tests/integration/test_js_assets.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add assets/js/theme-toggle.js \
        src/sphinx_hextra/theme/sphinx_hextra/static/theme-toggle.js \
        src/sphinx_hextra/__init__.py \
        tests/integration/test_js_assets.py
git commit -m "feat: theme toggle script with localStorage persistence"
```

---

## Task 6: Directive infrastructure — shared base, node types, registration hook

**Files:**
- Create: `src/sphinx_hextra/directives/__init__.py`
- Create: `src/sphinx_hextra/directives/_base.py`
- Create: `src/sphinx_hextra/nodes.py`
- Modify: `src/sphinx_hextra/__init__.py`

- [ ] **Step 1: Create `src/sphinx_hextra/nodes.py`**

```python
"""Custom docutils node types used by sphinx-hextra directives."""

from __future__ import annotations

from docutils import nodes


class HextraNode(nodes.General, nodes.Element):
    """Base class for all sphinx-hextra custom nodes."""


class CalloutNode(HextraNode):
    pass


class CardsNode(HextraNode):
    pass


class CardNode(HextraNode):
    pass


class TabsNode(HextraNode):
    pass


class TabNode(HextraNode):
    pass


class StepsNode(HextraNode):
    pass


class StepNode(HextraNode):
    pass


class FileTreeNode(HextraNode):
    pass


class FileTreeEntryNode(HextraNode):
    pass


class HeroNode(HextraNode):
    pass


class FeatureGridNode(HextraNode):
    pass


class FeatureNode(HextraNode):
    pass
```

- [ ] **Step 2: Create `src/sphinx_hextra/directives/_base.py`**

```python
"""Shared helpers for sphinx-hextra directives."""

from __future__ import annotations

from docutils.parsers.rst import Directive


class HextraDirective(Directive):
    """Base class. Each concrete directive sets its own spec."""

    has_content = True
    optional_arguments = 0
    required_arguments = 0
    final_argument_whitespace = False
    option_spec: dict = {}

    def nested_parse(self, node) -> None:
        """Parse `self.content` into `node`."""
        self.state.nested_parse(self.content, self.content_offset, node)
```

- [ ] **Step 3: Create `src/sphinx_hextra/directives/__init__.py`**

```python
"""Directive package — `register()` wires every directive into Sphinx."""

from __future__ import annotations

from typing import Any


def register(app: Any) -> None:
    """Register all sphinx-hextra directives, nodes, and HTML visitors."""
    # Concrete registrations added in each directive's task.
```

- [ ] **Step 4: Wire registration into `setup()`**

Modify `src/sphinx_hextra/__init__.py`:
```python
"""sphinx-hextra: Hextra-inspired Sphinx theme with component directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import directives as _directives

__version__ = "0.1.0.dev0"

_THEME_PATH = Path(__file__).resolve().parent / "theme"


def setup(app: Any) -> dict[str, Any]:
    app.add_html_theme("sphinx_hextra", str(_THEME_PATH / "sphinx_hextra"))
    app.add_js_file("theme-toggle.js")
    _directives.register(app)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```

- [ ] **Step 5: Run existing tests — should still pass**

Run: `uv run pytest tests/integration -v`
Expected: PASS (nothing broken).

- [ ] **Step 6: Commit**

```bash
git add src/sphinx_hextra/nodes.py src/sphinx_hextra/directives src/sphinx_hextra/__init__.py
git commit -m "feat: directive infrastructure and node types"
```

---

## Task 7: `hextra-callout` directive

**Files:**
- Create: `src/sphinx_hextra/directives/callout.py`
- Modify: `src/sphinx_hextra/directives/__init__.py`
- Create: `tests/integration/roots/test-callout/conf.py`
- Create: `tests/integration/roots/test-callout/index.md`
- Create: `tests/integration/test_callout.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-callout/conf.py`:
```python
project = "test"
extensions = ["myst_parser", "sphinx_hextra"]
html_theme = "sphinx_hextra"
master_doc = "index"
exclude_patterns = ["_build"]
```

`tests/integration/roots/test-callout/index.md`:
````markdown
# Test

```{hextra-callout} warning
This is a warning.
```
````

`tests/integration/test_callout.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="callout")
def test_callout_renders(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    el = soup.select_one("div.hx-callout.hx-callout--warning")
    assert el is not None
    assert "This is a warning" in el.get_text()


@pytest.mark.sphinx("html", testroot="callout")
def test_callout_default_type_is_info(app, tmp_path):
    (app.srcdir / "index.md").write_text(
        "# Test\n\n```{hextra-callout}\nPlain note.\n```\n"
    )
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("div.hx-callout.hx-callout--info") is not None
```

- [ ] **Step 2: Run tests — should fail**

Run: `uv run pytest tests/integration/test_callout.py -v`
Expected: FAIL — `hextra-callout` directive not defined.

- [ ] **Step 3: Implement `callout.py`**

`src/sphinx_hextra/directives/callout.py`:
```python
"""The ``hextra-callout`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import CalloutNode
from ._base import HextraDirective

_VALID_TYPES = {"info", "warning", "error", "default"}
_DEFAULT_EMOJI = {
    "info": "ℹ",
    "warning": "⚠",
    "error": "✖",
    "default": "•",
}


class CalloutDirective(HextraDirective):
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {"emoji": str}

    def run(self) -> list[nodes.Node]:
        callout_type = (self.arguments[0] if self.arguments else "info").lower()
        if callout_type not in _VALID_TYPES:
            callout_type = "info"
        emoji = self.options.get("emoji", _DEFAULT_EMOJI[callout_type])
        node = CalloutNode(callout_type=callout_type, emoji=emoji)
        self.nested_parse(node)
        return [node]


def visit_callout_html(self: Any, node: CalloutNode) -> None:
    classes = f"hx-callout hx-callout--{node['callout_type']}"
    self.body.append(
        f'<div class="{classes}">'
        f'<span class="hx-callout__icon" aria-hidden="true">{node["emoji"]}</span>'
        f'<div class="hx-callout__body">'
    )


def depart_callout_html(self: Any, node: CalloutNode) -> None:
    self.body.append("</div></div>")


def register(app: Any) -> None:
    app.add_node(CalloutNode, html=(visit_callout_html, depart_callout_html))
    app.add_directive("hextra-callout", CalloutDirective)
```

- [ ] **Step 4: Wire into `directives/__init__.py`**

```python
"""Directive package — `register()` wires every directive into Sphinx."""

from __future__ import annotations

from typing import Any

from . import callout


def register(app: Any) -> None:
    callout.register(app)
```

- [ ] **Step 5: Run tests — should pass**

Run: `uv run pytest tests/integration/test_callout.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/sphinx_hextra/directives/callout.py \
        src/sphinx_hextra/directives/__init__.py \
        tests/integration/roots/test-callout \
        tests/integration/test_callout.py
git commit -m "feat: hextra-callout directive with info/warning/error variants"
```

---

## Task 8: `hextra-cards` + `hextra-card` directives

**Files:**
- Create: `src/sphinx_hextra/directives/cards.py`
- Modify: `src/sphinx_hextra/directives/__init__.py`
- Create: `tests/integration/roots/test-cards/conf.py`
- Create: `tests/integration/roots/test-cards/index.md`
- Create: `tests/integration/test_cards.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-cards/conf.py`: copy from test-callout's conf.py.

`tests/integration/roots/test-cards/index.md`:
````markdown
# Test

```{hextra-cards}
:columns: 3

```{hextra-card} Getting Started
:link: quickstart.html
:icon: rocket
Intro text.
```

```{hextra-card} API
:link: api.html
Reference material.
```
```
````

`tests/integration/test_cards.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="cards")
def test_cards_container(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    container = soup.select_one("div.hx-cards")
    assert container is not None
    assert "hx-cards--cols-3" in container.get("class", [])


@pytest.mark.sphinx("html", testroot="cards")
def test_cards_items(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    items = soup.select("a.hx-cards__item")
    assert len(items) == 2
    assert items[0].get("href") == "quickstart.html"
    assert "Getting Started" in items[0].get_text()
```

- [ ] **Step 2: Run tests — should fail**

Run: `uv run pytest tests/integration/test_cards.py -v`
Expected: FAIL — directives not defined.

- [ ] **Step 3: Implement `cards.py`**

`src/sphinx_hextra/directives/cards.py`:
```python
"""The ``hextra-cards`` + ``hextra-card`` directives."""

from __future__ import annotations

from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives

from ..nodes import CardNode, CardsNode
from ._base import HextraDirective


def _columns(argument: str) -> int:
    value = int(argument)
    if value < 1 or value > 4:
        raise ValueError("columns must be between 1 and 4")
    return value


class CardsDirective(HextraDirective):
    option_spec = {"columns": _columns}

    def run(self) -> list[nodes.Node]:
        cols = self.options.get("columns", 2)
        node = CardsNode(columns=cols)
        self.nested_parse(node)
        return [node]


class CardDirective(HextraDirective):
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "link": directives.uri,
        "icon": directives.unchanged,
        "image": directives.uri,
    }

    def run(self) -> list[nodes.Node]:
        node = CardNode(
            title=self.arguments[0],
            link=self.options.get("link", ""),
            icon=self.options.get("icon", ""),
            image=self.options.get("image", ""),
        )
        self.nested_parse(node)
        return [node]


def visit_cards_html(self: Any, node: CardsNode) -> None:
    cols = node.get("columns", 2)
    self.body.append(f'<div class="hx-cards hx-cards--cols-{cols}">')


def depart_cards_html(self: Any, node: CardsNode) -> None:
    self.body.append("</div>")


def visit_card_html(self: Any, node: CardNode) -> None:
    href = node["link"] or "#"
    icon_html = (
        f'<span class="hx-cards__icon hx-icon hx-icon--{node["icon"]}" aria-hidden="true"></span>'
        if node["icon"]
        else ""
    )
    image_html = (
        f'<img class="hx-cards__image" src="{node["image"]}" alt="">'
        if node["image"]
        else ""
    )
    self.body.append(
        f'<a class="hx-cards__item" href="{href}">'
        f"{image_html}"
        f'<div class="hx-cards__header">{icon_html}'
        f'<span class="hx-cards__title">{node["title"]}</span>'
        f"</div>"
        f'<div class="hx-cards__body">'
    )


def depart_card_html(self: Any, node: CardNode) -> None:
    self.body.append("</div></a>")


def register(app: Any) -> None:
    app.add_node(CardsNode, html=(visit_cards_html, depart_cards_html))
    app.add_node(CardNode, html=(visit_card_html, depart_card_html))
    app.add_directive("hextra-cards", CardsDirective)
    app.add_directive("hextra-card", CardDirective)
```

- [ ] **Step 4: Wire into `directives/__init__.py`**

```python
from __future__ import annotations

from typing import Any

from . import callout, cards


def register(app: Any) -> None:
    callout.register(app)
    cards.register(app)
```

- [ ] **Step 5: Run tests — should pass**

Run: `uv run pytest tests/integration/test_cards.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/sphinx_hextra/directives/cards.py \
        src/sphinx_hextra/directives/__init__.py \
        tests/integration/roots/test-cards \
        tests/integration/test_cards.py
git commit -m "feat: hextra-cards and hextra-card directives"
```

---

## Task 9: `hextra-tabs` directive

**Files:**
- Create: `src/sphinx_hextra/directives/tabs.py`
- Modify: `src/sphinx_hextra/directives/__init__.py`
- Create: `assets/js/tabs.js`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/static/tabs.js`
- Modify: `src/sphinx_hextra/__init__.py` (register tabs.js)
- Create: `tests/integration/roots/test-tabs/conf.py`
- Create: `tests/integration/roots/test-tabs/index.md`
- Create: `tests/integration/test_tabs.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-tabs/conf.py`: same as test-cards.

`tests/integration/roots/test-tabs/index.md`:
````markdown
# Test

```{hextra-tabs}
### macOS
Apple.

### Linux
Open source.

### Windows
Microsoft.
```
````

`tests/integration/test_tabs.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="tabs")
def test_tabs_structure(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    container = soup.select_one("div.hx-tabs")
    assert container is not None
    labels = [b.get_text().strip() for b in container.select("button.hx-tabs__label")]
    assert labels == ["macOS", "Linux", "Windows"]
    panels = container.select("div.hx-tabs__panel")
    assert len(panels) == 3
    assert "Apple" in panels[0].get_text()
```

- [ ] **Step 2: Run test — should fail**

Run: `uv run pytest tests/integration/test_tabs.py -v`
Expected: FAIL — directive not defined.

- [ ] **Step 3: Implement `tabs.py`**

`src/sphinx_hextra/directives/tabs.py`:
```python
"""The ``hextra-tabs`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import TabNode, TabsNode
from ._base import HextraDirective


class TabsDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        wrapper = nodes.section()
        self.nested_parse(wrapper)

        tabs = TabsNode()
        for section in wrapper.children:
            if not isinstance(section, nodes.section):
                continue
            title_node = section.next_node(nodes.title)
            label = title_node.astext() if title_node else ""
            if title_node is not None:
                title_node.parent.remove(title_node)
            tab = TabNode(label=label)
            for child in list(section.children):
                section.remove(child)
                tab += child
            tabs += tab
        return [tabs]


def visit_tabs_html(self: Any, node: TabsNode) -> None:
    labels = [child["label"] for child in node.children if isinstance(child, TabNode)]
    self.body.append('<div class="hx-tabs" data-hx-tabs>')
    self.body.append('<div class="hx-tabs__labels" role="tablist">')
    for idx, label in enumerate(labels):
        active = "hx-tabs__label--active" if idx == 0 else ""
        self.body.append(
            f'<button type="button" class="hx-tabs__label {active}" '
            f'role="tab" data-hx-tab-index="{idx}">{label}</button>'
        )
    self.body.append("</div>")
    self.body.append('<div class="hx-tabs__panels">')


def depart_tabs_html(self: Any, node: TabsNode) -> None:
    self.body.append("</div></div>")


def visit_tab_html(self: Any, node: TabNode) -> None:
    index = node.parent.index(node)
    active = "hx-tabs__panel--active" if index == 0 else ""
    self.body.append(
        f'<div class="hx-tabs__panel {active}" role="tabpanel" data-hx-tab-index="{index}">'
    )


def depart_tab_html(self: Any, node: TabNode) -> None:
    self.body.append("</div>")


def register(app: Any) -> None:
    app.add_node(TabsNode, html=(visit_tabs_html, depart_tabs_html))
    app.add_node(TabNode, html=(visit_tab_html, depart_tab_html))
    app.add_directive("hextra-tabs", TabsDirective)
```

- [ ] **Step 4: Add `tabs.js`**

`assets/js/tabs.js` (copy same content to `src/sphinx_hextra/theme/sphinx_hextra/static/tabs.js`):
```js
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var containers = document.querySelectorAll("[data-hx-tabs]");
    containers.forEach(function (container) {
      var labels = container.querySelectorAll(".hx-tabs__label");
      var panels = container.querySelectorAll(".hx-tabs__panel");
      labels.forEach(function (label, idx) {
        label.addEventListener("click", function () {
          labels.forEach(function (l) { l.classList.remove("hx-tabs__label--active"); });
          panels.forEach(function (p) { p.classList.remove("hx-tabs__panel--active"); });
          label.classList.add("hx-tabs__label--active");
          if (panels[idx]) panels[idx].classList.add("hx-tabs__panel--active");
        });
      });
    });
  });
})();
```

- [ ] **Step 5: Register tabs.js in `setup()`**

Modify `src/sphinx_hextra/__init__.py`, append one line after the theme-toggle registration:
```python
    app.add_js_file("tabs.js")
```

- [ ] **Step 6: Wire into `directives/__init__.py`**

```python
from __future__ import annotations

from typing import Any

from . import callout, cards, tabs


def register(app: Any) -> None:
    callout.register(app)
    cards.register(app)
    tabs.register(app)
```

- [ ] **Step 7: Run tests — should pass**

Run: `uv run pytest tests/integration/test_tabs.py -v`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/sphinx_hextra/directives/tabs.py \
        src/sphinx_hextra/directives/__init__.py \
        src/sphinx_hextra/__init__.py \
        assets/js/tabs.js \
        src/sphinx_hextra/theme/sphinx_hextra/static/tabs.js \
        tests/integration/roots/test-tabs \
        tests/integration/test_tabs.py
git commit -m "feat: hextra-tabs directive with client-side switching"
```

---

## Task 10: `hextra-steps` directive

**Files:**
- Create: `src/sphinx_hextra/directives/steps.py`
- Modify: `src/sphinx_hextra/directives/__init__.py`
- Create: `tests/integration/roots/test-steps/conf.py`
- Create: `tests/integration/roots/test-steps/index.md`
- Create: `tests/integration/test_steps.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-steps/conf.py`: same pattern as test-tabs.

`tests/integration/roots/test-steps/index.md`:
````markdown
# Test

```{hextra-steps}
### Install
Run `uv sync`.

### Run
Run `sphinx-build docs _build`.
```
````

`tests/integration/test_steps.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="steps")
def test_steps_structure(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    container = soup.select_one("ol.hx-steps")
    assert container is not None
    items = container.select("li.hx-steps__item")
    assert len(items) == 2
    titles = [i.select_one(".hx-steps__title").get_text() for i in items]
    assert titles == ["Install", "Run"]
```

- [ ] **Step 2: Run test — should fail**

Run: `uv run pytest tests/integration/test_steps.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement `steps.py`**

`src/sphinx_hextra/directives/steps.py`:
```python
"""The ``hextra-steps`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import StepNode, StepsNode
from ._base import HextraDirective


class StepsDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        wrapper = nodes.section()
        self.nested_parse(wrapper)

        steps = StepsNode()
        for section in wrapper.children:
            if not isinstance(section, nodes.section):
                continue
            title_node = section.next_node(nodes.title)
            title = title_node.astext() if title_node else ""
            if title_node is not None:
                title_node.parent.remove(title_node)
            step = StepNode(title=title)
            for child in list(section.children):
                section.remove(child)
                step += child
            steps += step
        return [steps]


def visit_steps_html(self: Any, node: StepsNode) -> None:
    self.body.append('<ol class="hx-steps">')


def depart_steps_html(self: Any, node: StepsNode) -> None:
    self.body.append("</ol>")


def visit_step_html(self: Any, node: StepNode) -> None:
    self.body.append(
        '<li class="hx-steps__item">'
        '<span class="hx-steps__marker" aria-hidden="true"></span>'
        '<div class="hx-steps__content">'
        f'<h3 class="hx-steps__title">{node["title"]}</h3>'
        '<div class="hx-steps__body">'
    )


def depart_step_html(self: Any, node: StepNode) -> None:
    self.body.append("</div></div></li>")


def register(app: Any) -> None:
    app.add_node(StepsNode, html=(visit_steps_html, depart_steps_html))
    app.add_node(StepNode, html=(visit_step_html, depart_step_html))
    app.add_directive("hextra-steps", StepsDirective)
```

- [ ] **Step 4: Wire into `directives/__init__.py`**

```python
from __future__ import annotations

from typing import Any

from . import callout, cards, steps, tabs


def register(app: Any) -> None:
    callout.register(app)
    cards.register(app)
    tabs.register(app)
    steps.register(app)
```

- [ ] **Step 5: Run test — should pass**

Run: `uv run pytest tests/integration/test_steps.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/sphinx_hextra/directives/steps.py \
        src/sphinx_hextra/directives/__init__.py \
        tests/integration/roots/test-steps \
        tests/integration/test_steps.py
git commit -m "feat: hextra-steps directive for numbered walkthroughs"
```

---

## Task 11: `hextra-filetree` directive

**Files:**
- Create: `src/sphinx_hextra/directives/filetree.py`
- Modify: `src/sphinx_hextra/directives/__init__.py`
- Create: `tests/integration/roots/test-filetree/conf.py`
- Create: `tests/integration/roots/test-filetree/index.md`
- Create: `tests/integration/test_filetree.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-filetree/index.md`:
````markdown
# Test

```{hextra-filetree}
- content/
  - _index.md
  - docs/
    - intro.md
- conf.py
```
````

`tests/integration/test_filetree.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="filetree")
def test_filetree_structure(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    root = soup.select_one("ul.hx-filetree")
    assert root is not None
    folders = root.select("li.hx-filetree__folder")
    files = root.select("li.hx-filetree__file")
    folder_names = {f.select_one(".hx-filetree__name").get_text() for f in folders}
    file_names = {f.select_one(".hx-filetree__name").get_text() for f in files}
    assert folder_names == {"content/", "docs/"}
    assert file_names == {"_index.md", "intro.md", "conf.py"}
```

- [ ] **Step 2: Run test — should fail**

Run: `uv run pytest tests/integration/test_filetree.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement `filetree.py`**

`src/sphinx_hextra/directives/filetree.py`:
```python
"""The ``hextra-filetree`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import FileTreeEntryNode, FileTreeNode
from ._base import HextraDirective


def _parse_tree(lines: list[str]) -> list[dict]:
    """Parse an indented bullet list into a nested entry tree.

    Each entry is a dict: {"name": str, "is_folder": bool, "children": [...]}.
    """
    stack: list[tuple[int, list[dict]]] = [(-1, [])]
    for raw in lines:
        stripped = raw.rstrip()
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.strip()
        if content.startswith("- "):
            content = content[2:]
        name = content.strip()
        is_folder = name.endswith("/")
        entry = {"name": name, "is_folder": is_folder, "children": []}
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack[-1][1].append(entry)
        if is_folder:
            stack.append((indent, entry["children"]))
    return stack[0][1]


class FileTreeDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        tree = _parse_tree(list(self.content))
        root = FileTreeNode(tree=tree)
        return [root]


def _render_entries(entries: list[dict], body: list[str]) -> None:
    for entry in entries:
        cls = "hx-filetree__folder" if entry["is_folder"] else "hx-filetree__file"
        body.append(f'<li class="{cls}">')
        body.append(f'<span class="hx-filetree__name">{entry["name"]}</span>')
        if entry["is_folder"] and entry["children"]:
            body.append('<ul class="hx-filetree__children">')
            _render_entries(entry["children"], body)
            body.append("</ul>")
        body.append("</li>")


def visit_filetree_html(self: Any, node: FileTreeNode) -> None:
    self.body.append('<ul class="hx-filetree">')
    _render_entries(node["tree"], self.body)


def depart_filetree_html(self: Any, node: FileTreeNode) -> None:
    self.body.append("</ul>")


def register(app: Any) -> None:
    app.add_node(FileTreeNode, html=(visit_filetree_html, depart_filetree_html))
    app.add_node(FileTreeEntryNode, html=(lambda s, n: None, lambda s, n: None))
    app.add_directive("hextra-filetree", FileTreeDirective)
```

- [ ] **Step 4: Wire into `directives/__init__.py`**

```python
from __future__ import annotations

from typing import Any

from . import callout, cards, filetree, steps, tabs


def register(app: Any) -> None:
    callout.register(app)
    cards.register(app)
    tabs.register(app)
    steps.register(app)
    filetree.register(app)
```

- [ ] **Step 5: Run test — should pass**

Run: `uv run pytest tests/integration/test_filetree.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/sphinx_hextra/directives/filetree.py \
        src/sphinx_hextra/directives/__init__.py \
        tests/integration/roots/test-filetree \
        tests/integration/test_filetree.py
git commit -m "feat: hextra-filetree directive with nested bullet parsing"
```

---

## Task 12: Landing-page directives — `hextra-hero`, `hextra-feature-grid`, `hextra-feature`

**Files:**
- Create: `src/sphinx_hextra/directives/landing.py`
- Modify: `src/sphinx_hextra/directives/__init__.py`
- Create: `tests/integration/roots/test-landing/conf.py`
- Create: `tests/integration/roots/test-landing/index.md`
- Create: `tests/integration/test_landing.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-landing/index.md`:
````markdown
# Home

```{hextra-hero}
:title: Welcome
:tagline: Beautiful Sphinx docs.
:cta-text: Start
:cta-link: quickstart.html
```

```{hextra-feature-grid}

```{hextra-feature} Fast
:subtitle: Builds quickly.
Description.
```

```{hextra-feature} Flexible
:subtitle: Many components.
More.
```
```
````

`tests/integration/test_landing.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="landing")
def test_hero_renders(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    hero = soup.select_one("section.hx-hero")
    assert hero is not None
    assert hero.select_one(".hx-hero__title").get_text() == "Welcome"
    assert hero.select_one(".hx-hero__tagline").get_text() == "Beautiful Sphinx docs."
    cta = hero.select_one("a.hx-hero__cta")
    assert cta.get("href") == "quickstart.html"
    assert "Start" in cta.get_text()


@pytest.mark.sphinx("html", testroot="landing")
def test_feature_grid_renders(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    grid = soup.select_one("div.hx-feature-grid")
    assert grid is not None
    features = grid.select("div.hx-feature")
    assert len(features) == 2
    titles = [f.select_one(".hx-feature__title").get_text() for f in features]
    assert titles == ["Fast", "Flexible"]
```

- [ ] **Step 2: Run test — should fail**

Run: `uv run pytest tests/integration/test_landing.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement `landing.py`**

`src/sphinx_hextra/directives/landing.py`:
```python
"""Landing-page directives: hero and feature grid."""

from __future__ import annotations

from html import escape
from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives

from ..nodes import FeatureGridNode, FeatureNode, HeroNode
from ._base import HextraDirective


class HeroDirective(HextraDirective):
    has_content = False
    option_spec = {
        "title": directives.unchanged_required,
        "tagline": directives.unchanged,
        "cta-text": directives.unchanged,
        "cta-link": directives.uri,
    }

    def run(self) -> list[nodes.Node]:
        node = HeroNode(
            title=self.options["title"],
            tagline=self.options.get("tagline", ""),
            cta_text=self.options.get("cta-text", ""),
            cta_link=self.options.get("cta-link", ""),
        )
        return [node]


class FeatureGridDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        node = FeatureGridNode()
        self.nested_parse(node)
        return [node]


class FeatureDirective(HextraDirective):
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "subtitle": directives.unchanged,
        "image": directives.uri,
        "link": directives.uri,
    }

    def run(self) -> list[nodes.Node]:
        node = FeatureNode(
            title=self.arguments[0],
            subtitle=self.options.get("subtitle", ""),
            image=self.options.get("image", ""),
            link=self.options.get("link", ""),
        )
        self.nested_parse(node)
        return [node]


def visit_hero_html(self: Any, node: HeroNode) -> None:
    cta = ""
    if node["cta_text"] and node["cta_link"]:
        cta = (
            f'<a class="hx-hero__cta" href="{escape(node["cta_link"])}">'
            f'{escape(node["cta_text"])}</a>'
        )
    self.body.append(
        '<section class="hx-hero">'
        '<div class="hx-hero__inner">'
        f'<h1 class="hx-hero__title">{escape(node["title"])}</h1>'
        f'<p class="hx-hero__tagline">{escape(node["tagline"])}</p>'
        f"{cta}"
        "</div></section>"
    )
    raise nodes.SkipNode


def visit_feature_grid_html(self: Any, node: FeatureGridNode) -> None:
    self.body.append('<div class="hx-feature-grid">')


def depart_feature_grid_html(self: Any, node: FeatureGridNode) -> None:
    self.body.append("</div>")


def visit_feature_html(self: Any, node: FeatureNode) -> None:
    image = (
        f'<img class="hx-feature__image" src="{escape(node["image"])}" alt="">'
        if node["image"] else ""
    )
    wrapper_open = (
        f'<a class="hx-feature hx-feature--link" href="{escape(node["link"])}">'
        if node["link"] else '<div class="hx-feature">'
    )
    self.body.append(
        f"{wrapper_open}"
        f"{image}"
        f'<h3 class="hx-feature__title">{escape(node["title"])}</h3>'
        f'<p class="hx-feature__subtitle">{escape(node["subtitle"])}</p>'
        f'<div class="hx-feature__body">'
    )


def depart_feature_html(self: Any, node: FeatureNode) -> None:
    close = "</a>" if node["link"] else "</div>"
    self.body.append(f"</div>{close}")


def register(app: Any) -> None:
    app.add_node(HeroNode, html=(visit_hero_html, lambda s, n: None))
    app.add_node(FeatureGridNode, html=(visit_feature_grid_html, depart_feature_grid_html))
    app.add_node(FeatureNode, html=(visit_feature_html, depart_feature_html))
    app.add_directive("hextra-hero", HeroDirective)
    app.add_directive("hextra-feature-grid", FeatureGridDirective)
    app.add_directive("hextra-feature", FeatureDirective)
```

- [ ] **Step 4: Wire into `directives/__init__.py`**

```python
from __future__ import annotations

from typing import Any

from . import callout, cards, filetree, landing, steps, tabs


def register(app: Any) -> None:
    callout.register(app)
    cards.register(app)
    tabs.register(app)
    steps.register(app)
    filetree.register(app)
    landing.register(app)
```

- [ ] **Step 5: Run test — should pass**

Run: `uv run pytest tests/integration/test_landing.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/sphinx_hextra/directives/landing.py \
        src/sphinx_hextra/directives/__init__.py \
        tests/integration/roots/test-landing \
        tests/integration/test_landing.py
git commit -m "feat: landing-page directives (hero, feature-grid, feature)"
```

---

## Task 13: Component CSS — write source styles for all directives and rebuild

**Files:**
- Create: `assets/css/components/callout.css`
- Create: `assets/css/components/cards.css`
- Create: `assets/css/components/tabs.css`
- Create: `assets/css/components/steps.css`
- Create: `assets/css/components/filetree.css`
- Create: `assets/css/landing.css`
- Modify: `assets/css/main.css` (import all component files)
- Regenerate: `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css`

- [ ] **Step 1: Write `assets/css/components/callout.css`**

```css
@layer components {
  .hx-callout {
    @apply flex gap-3 rounded-lg border p-4 my-4;
    border-color: var(--hx-border);
    background: color-mix(in srgb, var(--hx-accent) 6%, transparent);
  }
  .hx-callout__icon { @apply flex-shrink-0 text-xl leading-none; }
  .hx-callout__body { @apply flex-1; }
  .hx-callout--info    { border-left: 4px solid #3b82f6; }
  .hx-callout--warning { border-left: 4px solid #f59e0b; }
  .hx-callout--error   { border-left: 4px solid #ef4444; }
  .hx-callout--default { border-left: 4px solid var(--hx-muted); }
}
```

- [ ] **Step 2: Write `assets/css/components/cards.css`**

```css
@layer components {
  .hx-cards { @apply grid gap-4 my-6; }
  .hx-cards--cols-1 { @apply grid-cols-1; }
  .hx-cards--cols-2 { @apply grid-cols-1 md:grid-cols-2; }
  .hx-cards--cols-3 { @apply grid-cols-1 md:grid-cols-2 lg:grid-cols-3; }
  .hx-cards--cols-4 { @apply grid-cols-1 md:grid-cols-2 lg:grid-cols-4; }
  .hx-cards__item {
    @apply block rounded-lg border p-4 transition hover:shadow-md no-underline;
    border-color: var(--hx-border);
    color: var(--hx-fg);
  }
  .hx-cards__item:hover { border-color: var(--hx-accent); }
  .hx-cards__header { @apply flex items-center gap-2 mb-2; }
  .hx-cards__title  { @apply font-semibold; }
  .hx-cards__body   { @apply text-sm opacity-80; }
}
```

- [ ] **Step 3: Write `assets/css/components/tabs.css`**

```css
@layer components {
  .hx-tabs { @apply my-4; }
  .hx-tabs__labels { @apply flex gap-2 border-b; border-color: var(--hx-border); }
  .hx-tabs__label {
    @apply px-4 py-2 border-b-2 border-transparent font-medium opacity-70 hover:opacity-100;
  }
  .hx-tabs__label--active {
    @apply opacity-100;
    border-color: var(--hx-accent);
  }
  .hx-tabs__panels { @apply pt-4; }
  .hx-tabs__panel { display: none; }
  .hx-tabs__panel--active { display: block; }
}
```

- [ ] **Step 4: Write `assets/css/components/steps.css`**

```css
@layer components {
  .hx-steps { @apply relative my-6 pl-6 list-none; }
  .hx-steps::before {
    content: "";
    @apply absolute left-2 top-2 bottom-2 w-px;
    background: var(--hx-border);
  }
  .hx-steps__item { @apply relative pl-4 pb-6; counter-increment: step; }
  .hx-steps__marker {
    @apply absolute -left-0.5 top-0 flex h-5 w-5 items-center justify-center rounded-full text-xs text-white;
    background: var(--hx-accent);
  }
  .hx-steps__marker::before { content: counter(step); }
  .hx-steps__title { @apply font-semibold text-base m-0; }
  .hx-steps__body  { @apply mt-1; }
  .hx-steps { counter-reset: step; }
}
```

- [ ] **Step 5: Write `assets/css/components/filetree.css`**

```css
@layer components {
  .hx-filetree, .hx-filetree__children {
    @apply list-none pl-4 font-mono text-sm;
  }
  .hx-filetree { @apply pl-0 my-4; }
  .hx-filetree__folder, .hx-filetree__file { @apply py-0.5; }
  .hx-filetree__folder > .hx-filetree__name::before { content: "▸ "; }
  .hx-filetree__file   > .hx-filetree__name::before { content: "· "; opacity: 0.5; }
}
```

- [ ] **Step 6: Write `assets/css/landing.css`**

```css
@layer components {
  .hx-hero {
    @apply py-20 text-center;
    background: radial-gradient(ellipse at 50% 50%, color-mix(in srgb, var(--hx-accent) 15%, transparent), transparent);
  }
  .hx-hero__title   { @apply text-5xl font-bold mb-4; }
  .hx-hero__tagline { @apply text-xl opacity-80 mb-8; }
  .hx-hero__cta {
    @apply inline-block px-6 py-3 rounded-lg font-medium text-white no-underline;
    background: var(--hx-accent);
  }

  .hx-feature-grid { @apply grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 my-10; }
  .hx-feature {
    @apply rounded-xl border p-6 block no-underline;
    border-color: var(--hx-border);
    color: var(--hx-fg);
  }
  .hx-feature__title    { @apply text-xl font-semibold mb-2 mt-0; }
  .hx-feature__subtitle { @apply text-sm opacity-70 mb-4; }
  .hx-feature__image    { @apply w-full rounded-lg mb-4; }
}
```

- [ ] **Step 7: Update `assets/css/main.css` to import components**

Replace the file contents with:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --hx-bg: #ffffff;
    --hx-fg: #1f2937;
    --hx-border: #e5e7eb;
    --hx-muted: #6b7280;
    --hx-accent: #6366f1;
  }

  html.dark {
    --hx-bg: #0b0f19;
    --hx-fg: #e5e7eb;
    --hx-border: #1f2937;
    --hx-muted: #9ca3af;
    --hx-accent: #818cf8;
  }

  body {
    background: var(--hx-bg);
    color: var(--hx-fg);
    font-family: theme("fontFamily.sans");
  }
}

@import "./components/callout.css";
@import "./components/cards.css";
@import "./components/tabs.css";
@import "./components/steps.css";
@import "./components/filetree.css";
@import "./landing.css";
```

- [ ] **Step 8: Rebuild CSS**

Run:
```bash
npm run build:css
```
Expected: `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css` is regenerated with component styles.

- [ ] **Step 9: Run all integration tests — should still pass**

Run: `uv run pytest tests/integration -v`
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add assets/css \
        src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css
git commit -m "feat: component and landing-page styles"
```

---

## Task 14: sphinx-needs integration — scoped CSS and conditional load

**Files:**
- Create: `assets/css/sphinx-needs.css`
- Create: `src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra-needs.css`
- Create: `src/sphinx_hextra/needs_integration.py`
- Modify: `src/sphinx_hextra/__init__.py`
- Create: `tests/integration/roots/test-needs/conf.py`
- Create: `tests/integration/roots/test-needs/index.rst`
- Create: `tests/integration/test_needs_integration.py`

- [ ] **Step 1: Write failing test**

`tests/integration/roots/test-needs/conf.py`:
```python
project = "test"
extensions = ["sphinx_needs", "sphinx_hextra"]
html_theme = "sphinx_hextra"
master_doc = "index"
exclude_patterns = ["_build"]
needs_types = [
    {"directive": "req", "title": "Requirement", "prefix": "R_", "color": "#BFD8D2", "style": "node"},
]
```

`tests/integration/roots/test-needs/index.rst`:
```rst
Test
====

.. req:: A requirement
   :id: R_001

   Body.

.. needtable::
```

`tests/integration/test_needs_integration.py`:
```python
from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="needs")
def test_needs_css_injected(app, warning):
    app.build()
    for line in warning.getvalue().splitlines():
        assert "sphinx_hextra" not in line, line
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    hrefs = [l.get("href", "") for l in soup.find_all("link", rel="stylesheet")]
    assert any("sphinx-hextra-needs.css" in h for h in hrefs), hrefs


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_needs_css_not_injected_without_needs(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    hrefs = [l.get("href", "") for l in soup.find_all("link", rel="stylesheet")]
    assert not any("sphinx-hextra-needs.css" in h for h in hrefs), hrefs
```

- [ ] **Step 2: Run — should fail**

Run: `uv run pytest tests/integration/test_needs_integration.py -v`
Expected: FAIL.

- [ ] **Step 3: Write `assets/css/sphinx-needs.css`**

```css
@layer components {
  table.needs_table,
  table.NEEDS_TABLE {
    @apply rounded-lg border overflow-hidden;
    border-color: var(--hx-border);
  }
  table.needs_table th,
  table.NEEDS_TABLE th {
    background: color-mix(in srgb, var(--hx-accent) 10%, transparent);
    color: var(--hx-fg);
  }
  table.needs_table td,
  table.NEEDS_TABLE td { border-color: var(--hx-border); }

  .need {
    @apply rounded-lg border px-3 py-2 my-2;
    border-color: var(--hx-border);
    background: color-mix(in srgb, var(--hx-accent) 4%, transparent);
  }
  .needs_status,
  .needs_type {
    @apply inline-block rounded-full px-2 py-0.5 text-xs font-medium;
    background: var(--hx-accent);
    color: white;
  }
}
```

- [ ] **Step 4: Create `src/sphinx_hextra/needs_integration.py`**

```python
"""Conditional sphinx-needs CSS injection."""

from __future__ import annotations

from typing import Any

_NEEDS_CSS = "sphinx-hextra-needs.css"


def _on_builder_inited(app: Any) -> None:
    if "sphinx_needs" in app.extensions:
        app.add_css_file(_NEEDS_CSS)


def register(app: Any) -> None:
    app.connect("builder-inited", _on_builder_inited)
```

- [ ] **Step 5: Wire into `setup()`**

Modify `src/sphinx_hextra/__init__.py` to call `_needs_integration.register(app)`:
```python
from . import directives as _directives
from . import needs_integration as _needs_integration

# ...in setup():
    _directives.register(app)
    _needs_integration.register(app)
```

- [ ] **Step 6: Build the needs CSS separately**

The needs CSS needs to compile into its own file so it's only loaded conditionally. Add a second Tailwind build to `package.json` scripts:

```json
"scripts": {
  "build:css": "npm run build:css:main && npm run build:css:needs",
  "build:css:main": "tailwindcss -i ./assets/css/main.css -o ./src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css --minify",
  "build:css:needs": "tailwindcss -i ./assets/css/sphinx-needs.css -o ./src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra-needs.css --minify",
  "watch:css": "tailwindcss -i ./assets/css/main.css -o ./src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css --watch"
}
```

Run:
```bash
npm run build:css
```
Expected: both CSS files exist in `src/sphinx_hextra/theme/sphinx_hextra/static/`.

- [ ] **Step 7: Run tests — should pass**

Run: `uv run pytest tests/integration/test_needs_integration.py -v`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add assets/css/sphinx-needs.css \
        src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra-needs.css \
        src/sphinx_hextra/needs_integration.py \
        src/sphinx_hextra/__init__.py \
        package.json package-lock.json \
        tests/integration/roots/test-needs \
        tests/integration/test_needs_integration.py
git commit -m "feat: conditional sphinx-needs styling integration"
```

---

## Task 15: Demo / docs site — uses every directive, self-hosts

**Files:**
- Create: `docs/conf.py`
- Create: `docs/index.md`
- Create: `docs/quickstart.md`
- Create: `docs/components/callout.md`
- Create: `docs/components/cards.md`
- Create: `docs/components/tabs.md`
- Create: `docs/components/steps.md`
- Create: `docs/components/filetree.md`
- Create: `docs/sphinx-needs.md`

- [ ] **Step 1: Create `docs/conf.py`**

```python
project = "sphinx-hextra"
copyright = "2026, Patrick Dahlke"
author = "Patrick Dahlke"

extensions = ["myst_parser", "sphinx_hextra"]
myst_enable_extensions = ["colon_fence"]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
master_doc = "index"
html_theme = "sphinx_hextra"
html_theme_options = {
    "navbar_title": "sphinx-hextra",
    "github_url": "https://github.com/patdhlk/sphinx-hextra",
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
```

- [ ] **Step 2: Create `docs/index.md` using hero + feature grid**

````markdown
---
hide-toc: true
---

```{hextra-hero}
:title: sphinx-hextra
:tagline: The Hextra aesthetic, on Sphinx.
:cta-text: Get Started
:cta-link: quickstart.html
```

```{hextra-feature-grid}

```{hextra-feature} Beautiful by default
:subtitle: Hextra-inspired typography, layout, and dark mode.
No configuration required.
```

```{hextra-feature} Sphinx-needs ready
:subtitle: First-class integration styling.
Requirements, specs, and tests match the theme.
```

```{hextra-feature} Component directives
:subtitle: Callouts, cards, tabs, steps, filetrees.
Pure Sphinx / MyST syntax.
```
```

```{toctree}
:hidden:
quickstart
components/callout
components/cards
components/tabs
components/steps
components/filetree
sphinx-needs
```
````

- [ ] **Step 3: Create `docs/quickstart.md`**

````markdown
# Quickstart

```{hextra-steps}

### Install
Run `uv add sphinx-hextra` in your project.

### Configure
Set `html_theme = "sphinx_hextra"` and add `"sphinx_hextra"` to your extensions list in `conf.py`.

### Build
Run `sphinx-build docs _build/html` and open the output.
```
````

- [ ] **Step 4: Create each component doc page**

`docs/components/callout.md`:
````markdown
# Callout

```{hextra-callout} info
This is an info callout.
```

```{hextra-callout} warning
This is a warning.
```

```{hextra-callout} error
This is an error.
```
````

`docs/components/cards.md`:
````markdown
# Cards

```{hextra-cards}
:columns: 2

```{hextra-card} Callout
:link: callout.html
Alert boxes.
```

```{hextra-card} Tabs
:link: tabs.html
Tabbed content.
```
```
````

`docs/components/tabs.md`:
````markdown
# Tabs

```{hextra-tabs}
### macOS
Apple's OS.
### Linux
Open source.
### Windows
Microsoft's OS.
```
````

`docs/components/steps.md`:
````markdown
# Steps

```{hextra-steps}
### First
Do this.
### Second
Then this.
### Third
Finally this.
```
````

`docs/components/filetree.md`:
````markdown
# FileTree

```{hextra-filetree}
- src/
  - sphinx_hextra/
    - __init__.py
    - directives/
- pyproject.toml
```
````

`docs/sphinx-needs.md`:
```markdown
# sphinx-needs Integration

sphinx-hextra automatically styles sphinx-needs output when the extension is present. No configuration required.
```

- [ ] **Step 5: Verify the docs build with `-W`**

Run: `uv run sphinx-build -W --keep-going docs docs/_build/html`
Expected: clean build, no warnings, all pages rendered.

- [ ] **Step 6: Commit**

```bash
git add docs/
git commit -m "docs: self-hosted demo site exercising every directive"
```

---

## Task 16: GitHub Actions — `ci.yml` (test matrix + docs build)

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python: ["3.10", "3.11", "3.12", "3.13"]
        sphinx: ["7.*", "8.*"]
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          enable-cache: true
      - name: Set up Python
        run: uv python install ${{ matrix.python }}
      - name: Sync dependencies
        run: uv sync --group dev
      - name: Pin Sphinx version
        run: uv pip install "sphinx==${{ matrix.sphinx }}"
      - name: Run tests
        run: uv run pytest -n auto
      - name: Build docs
        run: uv run sphinx-build -W --keep-going docs docs/_build/html
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: test matrix for Python 3.10-3.13 and Sphinx 7-8"
```

---

## Task 17: GitHub Actions — `css-build.yml` (guard compiled CSS freshness)

**Files:**
- Create: `.github/workflows/css-build.yml`

- [ ] **Step 1: Create `.github/workflows/css-build.yml`**

```yaml
name: CSS freshness

on:
  pull_request:
    paths:
      - "assets/**"
      - "tailwind.config.js"
      - "package.json"
      - "package-lock.json"

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm run build:css
      - name: Fail if compiled CSS is stale
        run: |
          if ! git diff --quiet src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra.css \
                                src/sphinx_hextra/theme/sphinx_hextra/static/sphinx-hextra-needs.css; then
            echo "::error::Compiled CSS is stale. Run 'npm run build:css' locally and commit the result."
            git diff --stat src/sphinx_hextra/theme/sphinx_hextra/static/
            exit 1
          fi
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/css-build.yml
git commit -m "ci: guard that compiled CSS is committed fresh on asset changes"
```

---

## Task 18: GitHub Actions — `release.yml` (PyPI Trusted Publishing)

**Files:**
- Create: `.github/workflows/release.yml`

- [ ] **Step 1: Create `.github/workflows/release.yml`**

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write
  id-token: write

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    environment: release
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - name: Rebuild CSS from source
        run: |
          npm ci
          npm run build:css
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      - name: Build wheel and sdist
        run: uv build
      - name: Verify wheel contains compiled CSS
        run: |
          python -m zipfile -l dist/*.whl | grep "sphinx-hextra.css"
          python -m zipfile -l dist/*.whl | grep "sphinx-hextra-needs.css"
      - name: Verify wheel excludes dev assets
        run: |
          if python -m zipfile -l dist/*.whl | grep -q "tailwind.config"; then
            echo "dev asset leaked into wheel"
            exit 1
          fi
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
      - name: Create GitHub release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/release.yml
git commit -m "ci: release workflow with Trusted Publishing and wheel verification"
```

---

## Task 19: GitHub Actions — `docs-deploy.yml` (GitHub Pages)

**Files:**
- Create: `.github/workflows/docs-deploy.yml`

- [ ] **Step 1: Create `.github/workflows/docs-deploy.yml`**

```yaml
name: Deploy docs

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --group dev
      - run: uv run sphinx-build -W --keep-going docs docs/_build/html
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
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/docs-deploy.yml
git commit -m "ci: deploy docs site to GitHub Pages on main"
```

---

## Task 20: Licensing, attribution, README, CREDITS, CHANGELOG, CONTRIBUTING

**Files:**
- Create: `LICENSE`
- Create: `licenses/HEXTRA-LICENSE`
- Create: `README.md`
- Create: `CREDITS.md`
- Create: `CHANGELOG.md`
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Create `LICENSE` (our MIT)**

```
MIT License

Copyright (c) 2026 Patrick Dahlke and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Fetch and store the upstream Hextra LICENSE**

Run:
```bash
mkdir -p licenses
curl -sSL https://raw.githubusercontent.com/imfing/hextra/main/LICENSE -o licenses/HEXTRA-LICENSE
```
Expected: the file exists and contains Hextra's MIT notice (Copyright (c) Imfing).

- [ ] **Step 3: Create `README.md`**

```markdown
# sphinx-hextra

A Sphinx HTML theme and component directive set that brings the aesthetic of the [Hextra](https://github.com/imfing/hextra) Hugo theme to the Sphinx documentation ecosystem, with first-class styling for [sphinx-needs](https://github.com/useblocks/sphinx-needs).

**sphinx-hextra is a derivative work.** Visual design, component concepts, and CSS structure are ported from Hextra (MIT, © Imfing and contributors). The upstream LICENSE is preserved verbatim at [`licenses/HEXTRA-LICENSE`](licenses/HEXTRA-LICENSE). See [`CREDITS.md`](CREDITS.md) for full attribution.

## Install

```bash
uv add sphinx-hextra
```

## Use

In your `conf.py`:

```python
extensions = ["myst_parser", "sphinx_hextra"]
html_theme = "sphinx_hextra"
```

## Features (v0.1)

- Hextra-inspired layout, typography, and dark mode
- Directives: `hextra-callout`, `hextra-cards` + `hextra-card`, `hextra-tabs`, `hextra-steps`, `hextra-filetree`
- Landing-page directives: `hextra-hero`, `hextra-feature-grid`, `hextra-feature`
- Automatic sphinx-needs integration styling (when `sphinx_needs` is enabled)
- Zero Node.js dependency for end users — CSS is precompiled

## Credits

This project stands on the shoulders of [Hextra](https://github.com/imfing/hextra). Every design decision traces back to their work. Bugs here are ours; beauty is theirs.

## License

MIT. See [`LICENSE`](LICENSE) (sphinx-hextra) and [`licenses/HEXTRA-LICENSE`](licenses/HEXTRA-LICENSE) (upstream Hextra).
```

- [ ] **Step 4: Create `CREDITS.md`**

```markdown
# Credits

## Upstream: Hextra

`sphinx-hextra` is a derivative work of the [Hextra](https://github.com/imfing/hextra) Hugo theme.

- **Upstream repository:** https://github.com/imfing/hextra
- **Upstream license:** MIT — preserved verbatim at [`licenses/HEXTRA-LICENSE`](licenses/HEXTRA-LICENSE)
- **Upstream maintainer:** [@imfing](https://github.com/imfing)
- **Full contributor list:** https://github.com/imfing/hextra/graphs/contributors

Every design decision in this project — the layout, the colour palette, the component set, the typography, the dark mode strategy — originates with Hextra. We ported the ideas into a Sphinx-native form.

## This package

- **Maintainer:** Patrick Dahlke

Contributions welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
```

- [ ] **Step 5: Create `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to this project will be documented in this file.
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Initial release: Hextra-inspired Sphinx theme.
- Directives: `hextra-callout`, `hextra-cards`, `hextra-card`, `hextra-tabs`,
  `hextra-steps`, `hextra-filetree`.
- Landing directives: `hextra-hero`, `hextra-feature-grid`, `hextra-feature`.
- Conditional sphinx-needs integration styling.
- Dark mode with `localStorage` persistence.
```

- [ ] **Step 6: Create `CONTRIBUTING.md`**

```markdown
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
```

- [ ] **Step 7: Commit**

```bash
git add LICENSE licenses/HEXTRA-LICENSE README.md CREDITS.md CHANGELOG.md CONTRIBUTING.md
git commit -m "docs: licensing, attribution, README, CREDITS, contributing guide"
```

---

## Task 21: Final smoke — run everything, tag v0.1.0

**Files:** none

- [ ] **Step 1: Run the full test suite**

Run: `uv run pytest -v`
Expected: all tests PASS, no warnings.

- [ ] **Step 2: Build the demo site with warnings-as-errors**

Run: `uv run sphinx-build -W --keep-going docs docs/_build/html`
Expected: clean build.

- [ ] **Step 3: Build the wheel and inspect**

Run:
```bash
uv build
python -m zipfile -l dist/*.whl | grep -E "(sphinx-hextra.css|sphinx-hextra-needs.css|theme.toml|layout.html)"
```
Expected: all four files present. No `tailwind.config` or `assets/` in wheel.

- [ ] **Step 4: Install the wheel into a fresh venv and build a trivial site**

Run:
```bash
uv venv /tmp/hextra-check
source /tmp/hextra-check/bin/activate
uv pip install dist/*.whl sphinx myst-parser
mkdir -p /tmp/hextra-site
cat > /tmp/hextra-site/conf.py <<'EOF'
project = "smoke"
extensions = ["myst_parser", "sphinx_hextra"]
html_theme = "sphinx_hextra"
master_doc = "index"
EOF
echo "# Hello" > /tmp/hextra-site/index.md
sphinx-build /tmp/hextra-site /tmp/hextra-site/_build
deactivate
```
Expected: build succeeds.

- [ ] **Step 5: Tag and push**

```bash
git tag v0.1.0
git push origin main --tags
```

The release workflow will take it from there: rebuild CSS, build wheel, publish to PyPI, create GitHub Release.

---

## Self-Review Notes (author)

**Spec coverage:**
- Goals §2.1 — all seven bullets are covered (theme: T2/T4; directives: T7–T12; sphinx-needs: T14; no-Node UX: T3/T13/T17/T18; Python/Sphinx matrix: T1/T16).
- Non-goals §2.2 — no tasks implement them. ✓
- Architecture §3 — T1/T2/T3/T4/T5/T6 together construct the two build axes.
- Repo layout §4 — every file in the spec's tree gets created. Cross-checked line by line.
- Directive API §5 — each directive has a dedicated task (T7–T12) that matches the spec's syntax; the `hextra-tabs` clarification from spec §5.3 is honoured (H3s carry labels, no `:items:` option).
- sphinx-needs §6 — T14.
- Testing §7 — T2/T4/T5/T7–T12/T14 each add unit and/or integration tests; docs smoke test is part of T15/T21 and CI.
- CI/release §8 — T16 (ci.yml), T17 (css-build.yml), T18 (release.yml), T19 (docs-deploy.yml).
- Licensing §9 — T20.

**Placeholders:** none. Every code block is complete.

**Type/name consistency:** class names (`CalloutNode`, `CardsNode`, etc.) are defined in T6's `nodes.py` and used unchanged in T7–T12. HTML classnames (`hx-callout`, `hx-cards__item`, `hx-tabs__panel--active`) match between the directive output and CSS under T13. JS selectors (`[data-hx-tabs]`, `.hx-theme-toggle`) match between templates, directive output, and JS modules.

**One thing engineers will hit:** Task 3 ships an almost-empty CSS file, and Task 13 regenerates it. The intermediate commits (Tasks 4–12) reference CSS classes that aren't yet styled — this is intentional: tests assert structure, not visual output. Don't panic if the demo looks unstyled until Task 13.
