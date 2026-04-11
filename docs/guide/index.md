# Guide

The guide walks you through every piece of `sphinx-hextra` that you will touch
while authoring a documentation site. It is organised from the outside in:
first how to lay out files and wire up configuration, then how to write
content with Markdown, code blocks, math and diagrams, then the individual
component directives that give the theme its Hextra-like feel, and finally
how to deploy the result to a static host.

If you are brand new, start with [Getting Started](../getting-started.md) for
the shortest path from zero to a running build, then come back here. If you
already have a Sphinx site and are migrating to `sphinx-hextra`, skim
[Configuration](configuration.md) and [Customization](../advanced/customization.md)
first — those are the two pages that change when you swap themes.

## In this section

````{hextra-cards}
:columns: 2

```{hextra-card} Organize Files
:link: organize-files.html
Directory layout, the root toctree, and how to wire pages together.
```

```{hextra-card} Configuration
:link: configuration.html
Every theme option and the common `conf.py` keys you will touch.
```

```{hextra-card} Markdown
:link: markdown.html
MyST syntax, fenced directives, and the extensions worth enabling.
```

```{hextra-card} Syntax Highlighting
:link: syntax-highlighting.html
Fenced code blocks, Pygments, line numbers, and emphasised lines.
```

```{hextra-card} LaTeX
:link: latex.html
Inline and block math via MyST dollar syntax and MathJax.
```

```{hextra-card} Diagrams
:link: diagrams.html
Add Mermaid, Graphviz, or PlantUML via Sphinx extensions.
```

```{hextra-card} Directives
:link: directives/index.html
Callouts, cards, tabs, steps, filetree, hero, feature grid.
```

```{hextra-card} Deploy
:link: deploy.html
Ship your site to GitHub Pages, Read the Docs, Netlify, or Cloudflare.
```
````

## What sphinx-hextra gives you

`sphinx-hextra` is two things stitched into one package. First, it is a
Sphinx HTML theme — a full custom `layout.html` with navbar, sidebar,
right-hand table of contents, dark-mode toggle, and a matching stylesheet.
Second, it is a set of seven Sphinx directives (`hextra-callout`,
`hextra-cards`/`hextra-card`, `hextra-tabs`, `hextra-steps`,
`hextra-filetree`, `hextra-hero`, `hextra-feature-grid`/`hextra-feature`)
that emit semantic HTML with stable class names the theme knows how to style.

What it deliberately does not do: it does not bundle a Markdown parser, a
math renderer, a diagram extension, or a comments system. Those live in their
own Sphinx extensions that you install alongside. Each relevant guide page
below shows the exact extension to add when you need one of those
capabilities.
