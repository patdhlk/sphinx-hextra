# Hero & Feature Grid

The landing-page directives are a set of three: `hextra-hero` for the
full-bleed banner at the top of a marketing page, `hextra-feature-grid`
for the container that lays out features in a responsive grid, and
`hextra-feature` for each individual feature card inside the grid.
Together they reproduce the layout used on Hextra's own landing page,
and on the front page of the documentation you are reading.

## `hextra-hero`

The hero is a centred, padded block intended to sit at the very top of
a page. It takes the page's width, so it works best on pages that
suppress the right-hand table of contents with a `hide-toc: true` front
matter field.

### Options

- **`:title:`** (required) — the hero's main headline. Renders in a
  large display font, bolder than surrounding content.
- **`:tagline:`** — a single line of supporting copy shown directly
  below the title. Optional but almost always desired.
- **`:cta-text:`** — text for the call-to-action button. If you set
  `cta-text`, you should also set `cta-link`.
- **`:cta-link:`** — URL the CTA button points at. Internal
  paths (`guide/index.html`) and external URLs both work.

### Example

````markdown
```{hextra-hero}
:title: Build modern documentation with Sphinx and Markdown
:tagline: Fast, batteries-included Sphinx theme inspired by Hextra.
:cta-text: Get Started
:cta-link: getting-started.html
```
````

### Rendered behaviour

The hero is a centred block with 5rem of vertical padding. The
background is a large radial gradient seeded from `--hx-accent`, so the
hue automatically tracks your theme colour. The title is 3rem / 48px
with tight line-height, the tagline sits directly underneath at 1.25rem
and 75% opacity, and the CTA button is a filled accent-coloured
rectangle with rounded corners. On a narrow viewport the padding
shrinks proportionally and the title scales down.

## `hextra-feature-grid`

The feature grid is a container for `hextra-feature` blocks. It takes
no options — the layout adapts to the number of features inside. Two
features get a 2-column grid, three get a 3-column grid, four get a
2x2 grid on desktop that collapses to a single column on mobile.

### Fence nesting

Because `hextra-feature` is nested inside `hextra-feature-grid`, the
outer fence needs more backticks than the inner. The usual
configuration is four outside, three inside:

````markdown
`````markdown
````{hextra-feature-grid}

```{hextra-feature} Beautiful by default
:subtitle: Hextra typography and dark mode out of the box.
No configuration required.
```

```{hextra-feature} Component directives
:subtitle: Callouts, cards, tabs, steps, filetrees.
Drop a directive, get the Hextra look.
```
````
`````
````

## `hextra-feature`

Each feature is one tile in the grid. The first argument after the
directive name is the feature's title.

### Options

- **`:subtitle:`** — a single line of supporting copy under the title.
- **`:image:`** — a path to an image (SVG or raster) rendered
  full-width at the top of the feature.
- **`:link:`** — optional URL the whole feature tile links to.
- **`:style:`** — inline CSS applied to the tile's root element. This
  is the escape hatch for per-feature visual tweaks: gradient
  backgrounds, accent tints, custom borders.

### Example: matching the landing page

Here is the directive source for the feature grid on the
[front page of this site](../../index.md). It sets a different radial
gradient per tile to give each feature its own colour accent:

````markdown
`````markdown
````{hextra-feature-grid}

```{hextra-feature} Beautiful by default
:subtitle: Hextra-inspired typography, layout, and dark mode.
:image: _static/features/design.svg
:style: background: radial-gradient(ellipse at 60% 80%, rgba(129,140,248,0.18), transparent 60%);
No configuration required.
```

```{hextra-feature} Sphinx-needs ready
:subtitle: First-class styling for requirements and tables.
:image: _static/features/needs.svg
:style: background: radial-gradient(ellipse at 50% 80%, rgba(34,211,238,0.18), transparent 60%);
Requirements, specs, and tests match the theme.
```

```{hextra-feature} Component directives
:subtitle: Callouts, cards, tabs, steps, filetrees.
:image: _static/features/components.svg
:style: background: radial-gradient(ellipse at 50% 80%, rgba(251,191,36,0.18), transparent 60%);
Drop a directive, get the Hextra look.
```
````
`````
````

## Tips

- Put illustrations for `:image:` in `_static/` (for example,
  `_static/features/design.svg`) and make sure `html_static_path =
  ["_static"]` in `conf.py`. SVGs render crisply at every size and keep
  dark and light backgrounds happy.
- Use `:style:` gradients sparingly — one per feature, matching the
  tile's semantic meaning, rather than different gradients on every
  page. The visual effect reads as deliberate only when it is
  consistent.
- Hide the right-hand TOC on landing pages that use a hero, either by
  setting `show_toc = False` globally or adding `hide-toc: true` to
  the page's front matter. A centred hero next to a right-hand TOC
  column looks unbalanced.
