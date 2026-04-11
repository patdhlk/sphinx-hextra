# Callout

`hextra-callout` produces a boxed note — the Hextra equivalent of a
docutils admonition. Callouts are the right tool for information that
needs to catch the reader's eye without interrupting the flow of the
surrounding prose: tips, warnings about footguns, links to related
pages, hints about upcoming changes.

## Syntax

A callout is a fenced directive with an optional positional argument that
controls the colour and default icon. Valid type arguments are `info`,
`warning`, `error`, and `default`. If you omit the type, it defaults to
`info`.

````markdown
```{hextra-callout} info
This is an info callout. Use it for neutral, on-topic asides.
```
````

The body of the directive is regular MyST content: paragraphs, inline
code, links, lists, even nested directives if you really want.

## Options

### `:emoji:`

Override the default leading icon with an arbitrary string — usually an
emoji or a single character. This is useful when you want a callout to
stand out from its neighbours visually, or when your site has a strong
emoji vocabulary (a rocket for "release notes", a wrench for "breaking
change", and so on):

````markdown
```{hextra-callout} info
:emoji: 🚀

Version 0.1.0 is out. See the changelog for details.
```
````

The emoji sits in the same position as the default type icon and takes
over entirely — the type argument still controls the colour scheme, but
the icon is now whatever you passed.

## All four types

An **info** callout, used for neutral asides and cross-references:

````markdown
```{hextra-callout} info
`sphinx-hextra` only depends on `sphinx` and `docutils`. Everything else
is opt-in.
```
````

A **warning** callout, used for footguns and things that surprise
readers:

````markdown
```{hextra-callout} warning
The `edit_page_url_template` option is reserved for v0.2 and has no
effect in the current release.
```
````

An **error** callout, used for "this will break your build" level
problems:

````markdown
```{hextra-callout} error
Nested fences must use more backticks on the outside than the inside.
Four outside, three inside is the normal configuration.
```
````

A **default** callout, used when you want the shape of a callout but
without committing to a semantic colour:

````markdown
```{hextra-callout} default
A neutral callout. Good for "by the way" content that does not fit any
of the other three buckets.
```
````

## Rendered behaviour

A callout renders as a rounded rectangle with a 1px border, a 4px
coloured accent strip on the left, and a gently tinted background whose
hue matches the type. The leading icon sits in a fixed column on the
left at the same height as the first line of body text. On a narrow
viewport the callout stretches to fill the available width; there is no
explicit mobile breakpoint because the layout is already fluid.

Callouts use the CSS variables `--hx-accent`, `--hx-border`, and
`--hx-fg` from the theme palette. Overriding any of these in your
`custom.css` (see [Customization](../../advanced/customization.md))
changes how every callout on the site looks without touching individual
pages.

Semantically, the output is a `<aside>` element with an ARIA role that
screen readers announce as a note. If you build the same source as ePub
or LaTeX, the callout falls back to the nearest equivalent structure in
that format instead of breaking.
