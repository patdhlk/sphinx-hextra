# Organize Files

Sphinx does not scan your filesystem for content. Every page has to be
reachable from the root document (`index.md` by default) via a `toctree`
directive, either directly or through another page that is itself in a
toctree. This is different from static-site generators like Hugo or Jekyll,
and it is the single most common source of confusion when you come to Sphinx
from another tool.

This page shows the directory layout `sphinx-hextra` expects, explains how
the toctree works, and covers the cross-referencing syntax you will reach for
most often.

## Recommended layout

A typical project looks like this:

```
my-docs/
├── docs/
│   ├── _static/
│   │   ├── custom.css
│   │   └── logo.svg
│   ├── _templates/
│   ├── conf.py
│   ├── index.md
│   ├── getting-started.md
│   ├── guide/
│   │   ├── index.md
│   │   └── configuration.md
│   └── advanced/
│       ├── index.md
│       └── customization.md
├── pyproject.toml
└── README.md
```

`_static/` holds assets that Sphinx copies verbatim to the build output —
stylesheets, images, fonts, JavaScript. `_templates/` holds Jinja templates
that override theme templates; most projects leave it empty. Everything else
is content, organised into subdirectories that match the sections in your
sidebar.

## The root document

Sphinx's entry point is controlled by the `root_doc` option in `conf.py`
(older projects used `master_doc`, which is still accepted as an alias). The
default is `"index"`, which maps to `docs/index.md`. You rarely need to
change this.

```python
root_doc = "index"
```

## The toctree directive

`toctree` builds the navigation tree. Inside a MyST file it looks like this:

````markdown
```{toctree}
:caption: Guide
:maxdepth: 2

guide/index
guide/configuration
guide/directives/index
```
````

Each non-empty line is a document path relative to the source directory,
**without** the `.md` extension. The `:caption:` option labels the section in
the sidebar. `:maxdepth:` controls how deep the sidebar expands by default.

The most important option is `:hidden:`. A hidden toctree still contributes to
the sidebar and next/previous links, but does not render an inline list of
links on the page itself. That is what you want on your landing page:

````markdown
```{toctree}
:hidden:
:caption: Getting Started

getting-started
```
````

You can have multiple toctrees on the same page, each with its own caption.
`sphinx-hextra`'s sidebar groups them by caption, which is how the docs you
are reading right now produce the "Getting Started", "Guide", and "Advanced"
headings.

## Cross-references

MyST gives you three ways to link between pages. Use whichever reads best.

A plain relative Markdown link works and is the easiest to write:

```markdown
See the [configuration guide](configuration.md) for details.
```

The `{doc}` role links to a document by its Sphinx path (no extension) and
uses the target page's title as the link text by default:

```markdown
See {doc}`configuration` for details.
```

The `{ref}` role links to a labelled target anywhere in the project. Define
the label with a `(label-name)=` line above the heading you want to target,
then link to it:

```markdown
(advanced-css)=
## Advanced CSS tricks

Jump to {ref}`advanced-css` from anywhere.
```

`{ref}` is the only option that survives a file being renamed without
updating every caller, so prefer it for targets that get referenced many
times.

## Excluding files

`exclude_patterns` in `conf.py` tells Sphinx to ignore matching paths. The
default already excludes `_build`, `Thumbs.db`, and `.DS_Store`. Add anything
else you don't want Sphinx parsing — drafts, templates, configuration files
that happen to sit in the source tree:

```python
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "drafts/**",
    "ubproject.toml",
]
```

If you get a "document isn't included in any toctree" warning, the fix is
either to add the page to a toctree or to add it to `exclude_patterns`.
