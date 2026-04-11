# Getting Started

`sphinx-hextra` is a [Sphinx](https://www.sphinx-doc.org/) theme and extension
package inspired by the [Hextra](https://imfing.github.io/hextra/) Hugo theme.
It gives you the visual language of a modern developer documentation site —
sticky navbar, sidebar tree, right-hand table of contents, dark mode, and a
hero landing page — without leaving the Sphinx ecosystem. Because you stay on
Sphinx, you keep every tool the ecosystem ships: reStructuredText, MyST
Markdown, autodoc, intersphinx, internationalisation, `sphinx-needs`, and so
on.

By the end of this page you will have a minimal documentation project that
builds a themed HTML site on your machine. From there you can work through the
[Guide](guide/index.md) to learn how each directive and configuration option
works, or jump straight into [Customization](advanced/customization.md) if you
want to start branding the site immediately.

## Install

`sphinx-hextra` is published to PyPI. Pick the installer that matches your
workflow. The package pulls in `sphinx` and `docutils` as runtime dependencies;
everything else (MyST, sphinx-needs, Mermaid, math) is opt-in, so you only
install what you actually use.

With [uv](https://github.com/astral-sh/uv) — recommended if you are starting a
fresh project:

```bash
uv init my-docs
cd my-docs
uv add sphinx-hextra myst-parser
```

With pip in an existing virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install sphinx-hextra myst-parser
```

`myst-parser` is optional — if you prefer reStructuredText you can skip it —
but every example in these docs is written in Markdown, so the rest of this
page assumes you installed it.

## Configure

Create a `docs/` directory with a `conf.py` file. The minimal configuration
needed to load the theme and enable Markdown support is eight lines:

```python
project = "My Docs"
author = "Your Name"
copyright = "2026, Your Name"

extensions = ["myst_parser", "sphinx_hextra"]
html_theme = "sphinx_hextra"
myst_enable_extensions = ["colon_fence"]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
```

The `colon_fence` extension lets you write directives with `:::` fences when
backticks get in the way, which is handy once you start nesting
`hextra-cards` inside other directives.

## Add content

Create `docs/index.md` with an H1 and a hero directive. The hero is a
full-bleed banner with a headline, tagline, and call-to-action button — the
same thing you see on the [landing page](index.md) of this site.

````markdown
# My Docs

```{hextra-hero}
:title: Welcome to My Docs
:tagline: Everything you need to get productive, in one place.
:cta-text: Get Started
:cta-link: guide/index.html
```

```{toctree}
:hidden:
guide/index
```
````

The `toctree` at the bottom is what builds the sidebar. Sphinx does not scan
your filesystem automatically — every page has to be reachable from the root
`toctree` to show up in the navigation.

## Build

Run `sphinx-build` against the `docs/` directory. The `-W` flag promotes
warnings to errors, which is the setting you want in CI:

```bash
sphinx-build -W docs docs/_build/html
```

Then open the result in your browser:

```bash
open docs/_build/html/index.html
```

You should see your hero, a themed navbar, and the dark-mode toggle in the top
right corner.

## Next steps

````{hextra-cards}
:columns: 3

```{hextra-card} Directives
:link: guide/directives/index.html
Learn every component directive — callouts, cards, tabs, steps, filetree, hero.
```

```{hextra-card} Configuration
:link: guide/configuration.html
Every `html_theme_options` key explained with examples.
```

```{hextra-card} Customization
:link: advanced/customization.html
Override the CSS palette and ship your own brand colours.
```
````
