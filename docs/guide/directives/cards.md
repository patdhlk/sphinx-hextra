# Cards

The card grid is two directives working together: `hextra-cards` is the
container that lays out its children in a responsive grid, and
`hextra-card` is the individual clickable card. You will reach for this
combination on section landing pages, on a "next steps" block at the
bottom of a tutorial, and any time you have a handful of equally-weighted
destinations you want to present side-by-side.

## Syntax

Because `hextra-card` is nested inside `hextra-cards`, the outer fence
needs more backticks than the inner. The normal convention is four
backticks outside and three inside:

````markdown
`````markdown
````{hextra-cards}
:columns: 3

```{hextra-card} Getting Started
:link: ../../getting-started.html
Install, configure, and build your first themed Sphinx site.
```

```{hextra-card} Guide
:link: ../index.html
Learn every directive and configuration option.
```

```{hextra-card} Advanced
:link: ../../advanced/index.html
Customization, additional pages, i18n, comments.
```
````
`````
````

If you prefer to avoid counting backticks, enable `colon_fence` in
`myst_enable_extensions` and use `:::` for the outer block.

## `hextra-cards` options

### `:columns:`

Number of columns in the grid. Accepts integers from 1 to 4. Default is
2. On a narrow viewport the grid collapses to a single column
automatically.

```markdown
:columns: 3
```

## `hextra-card` options

### Title (positional argument)

The first word-after-the-directive-name is the card title. It renders as
the card's heading:

```markdown
```{hextra-card} My Card Title
```
```

### `:link:`

Optional URL the card links to. If set, the entire card becomes a
clickable anchor:

```markdown
:link: configuration.html
```

You can use external URLs (`https://example.com`) or internal paths
(`guide/configuration.html`). Cross-references via `{doc}` are not
currently supported in this option; use the resolved HTML filename.

### `:icon:`

A short string shown to the left of the title. This can be an emoji, a
Unicode glyph, or a single character:

```markdown
:icon: 📖
```

As of v0.1 icons are plain strings — there is no SVG icon bundle and
`:icon:` does not resolve named icons like `lucide:book`. A proper
Lucide icon bundle is planned for v0.2. If you need SVG icons today, put
them in `_static/` and use `:image:` instead.

### `:image:`

A path to an image to render as the card's header. The image fills the
top of the card edge-to-edge:

```markdown
:image: _static/features/components.svg
```

## Three-column example with icons

````markdown
```markdown
````{hextra-cards}
:columns: 3

```{hextra-card} Fast
:icon: ⚡
Builds your documentation in seconds, not minutes.
```

```{hextra-card} Themed
:icon: 🎨
Dark mode and Hextra-inspired layout out of the box.
```

```{hextra-card} Hackable
:icon: 🔧
Override any CSS variable to match your brand.
```
````
```
````

## Two-column example with images

````markdown
```markdown
````{hextra-cards}
:columns: 2

```{hextra-card} Design system
:image: _static/features/design.svg
:link: ../../advanced/customization.html
Hextra typography, layout, and dark mode, themable via CSS variables.
```

```{hextra-card} Components
:image: _static/features/components.svg
:link: index.html
Seven directives for callouts, cards, tabs, steps, filetree, and heroes.
```
````
```
````

## Rendered behaviour

Each card is a 1px-bordered rounded rectangle that lifts slightly on
hover — the border colour tweens from `--hx-border` to `--hx-accent` and
the cursor switches to pointer if `:link:` is set. The grid uses CSS
grid, so cards in the same row always have the same height regardless of
body length. On a viewport narrower than ~640px, all cards stack into a
single column.

Cards are intentionally plain — they are a layout primitive, not a full
widget. If you need a card with a badge, a rating, or a price, build it
in your own template and drop the resulting HTML in via `html_additional_pages`
or a raw-HTML block.
