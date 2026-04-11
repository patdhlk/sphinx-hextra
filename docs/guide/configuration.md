# Configuration

This page covers every knob `sphinx-hextra` exposes via
`html_theme_options`, plus the `conf.py` keys you are most likely to touch
when setting up a new site. For the full universe of Sphinx configuration
options, see the
[official Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html).

## Theme options

All theme-specific options go inside the `html_theme_options` dictionary in
`conf.py`:

```python
html_theme = "sphinx_hextra"
html_theme_options = {
    "navbar_title": "My Project",
    "navbar_logo": "logo.svg",
    "github_url": "https://github.com/me/my-project",
    "show_toc": True,
}
```

### `navbar_title`

- **Type:** string
- **Default:** `""` (falls back to the Sphinx `project` value)
- **Effect:** The text shown next to the logo in the top navbar. Set this
  when your `project` name is too long or contains characters you don't want
  in the chrome.

```python
html_theme_options = {"navbar_title": "My Docs"}
```

### `navbar_logo`

- **Type:** string
- **Default:** `""` (no logo)
- **Effect:** Filename of an image under `html_static_path[0]` (usually
  `_static/`) to render as the navbar logo. A 32px SVG works best. Both the
  light and dark themes use the same file, so pick something that reads
  against both backgrounds.

```python
html_static_path = ["_static"]
html_theme_options = {"navbar_logo": "logo.svg"}
```

### `github_url`

- **Type:** string
- **Default:** `""` (no link)
- **Effect:** When set, renders a GitHub icon link in the navbar that
  points at the URL.

```python
html_theme_options = {"github_url": "https://github.com/patdhlk/sphinx-hextra"}
```

### `edit_page_url_template`

- **Type:** string
- **Default:** `""`
- **Effect:** Reserved for a future "Edit this page" link above the right
  TOC. As of v0.1 it is not wired up; setting it does nothing. It is listed
  in `theme.toml` so that when support lands in v0.2 your existing
  configuration keeps working.

### `show_toc`

- **Type:** bool
- **Default:** `True`
- **Effect:** Controls the right-hand "On this page" table of contents. Set
  it to `False` globally if you prefer a two-column layout. You can also
  hide it per-page by adding a `hide-toc: true` front matter field — see
  the landing page in `docs/index.md` for an example.

```python
html_theme_options = {"show_toc": False}
```

## Other useful `conf.py` keys

Beyond the theme options, there are a handful of top-level settings in
`conf.py` that every project ends up touching.

```python
project = "My Docs"
author = "Your Name"
copyright = "2026, Your Name"

extensions = [
    "myst_parser",
    "sphinx_hextra",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "dollarmath",
]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
root_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_hextra"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]
```

`html_static_path` must be set to a list containing `"_static"` before
`html_css_files` or `html_js_files` have any effect — Sphinx will not find
your assets otherwise. Both lists are appended to whatever the theme already
ships, so you are always additive.

## A minimal configuration

The shortest `conf.py` that builds a usable themed site:

```python
project = "My Docs"
author = "Me"
extensions = ["myst_parser", "sphinx_hextra"]
html_theme = "sphinx_hextra"
```

## A real-world configuration

What you are more likely to end up with once the project has grown:

```python
project = "My Docs"
author = "Example Team"
copyright = "2026, Example Team"

extensions = [
    "myst_parser",
    "sphinx_hextra",
    "sphinx.ext.mathjax",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "attrs_inline",
    "dollarmath",
]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
exclude_patterns = ["_build", ".DS_Store", "drafts/**"]

html_theme = "sphinx_hextra"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "navbar_title": "My Docs",
    "navbar_logo": "logo.svg",
    "github_url": "https://github.com/example/docs",
    "show_toc": True,
}
```

This is roughly what the `conf.py` for `sphinx-hextra`'s own documentation
looks like — take a look at `docs/conf.py` in this repository for the
canonical reference.
