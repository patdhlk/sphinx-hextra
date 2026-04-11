# Directives

`sphinx-hextra` ships seven component directives that give your pages the
Hextra-inspired look: callouts, a card grid, tabs, a step list, a filetree
renderer, a hero banner, and a feature grid. Every directive is a native
Sphinx directive that emits semantic HTML with stable class names, so the
output is searchable, accessible, and survives being converted to other
builders (ePub, LaTeX, manpage) with graceful degradation.

The directives have no runtime dependency beyond Sphinx itself — they
do not pull in Tailwind, Lucide, or any JavaScript framework. The visual
styling comes from the theme's CSS; if you disable `sphinx-hextra` as the
theme but keep it as an extension, the directives still render, just
without the chrome.

## Overview

````{hextra-cards}
:columns: 2

```{hextra-card} Callout
:link: callout.html
Boxed notes with four semantic types and optional custom emoji.
```

```{hextra-card} Cards
:link: cards.html
A responsive grid of clickable cards with icons, images, and links.
```

```{hextra-card} Tabs
:link: tabs.html
Tabbed content sections that persist the active tab to sessionStorage.
```

```{hextra-card} Steps
:link: steps.html
Numbered step list for walkthroughs and onboarding flows.
```

```{hextra-card} FileTree
:link: filetree.html
Render a directory layout from a nested bullet list.
```

```{hextra-card} Hero & Feature Grid
:link: landing.html
Full-bleed hero banner and multi-column feature grid for landing pages.
```
````

## Quick reference

| Directive              | Kind       | Key options                                  |
| ---------------------- | ---------- | -------------------------------------------- |
| `hextra-callout`       | block      | type arg, `:emoji:`                          |
| `hextra-cards`         | container  | `:columns:` (1–4, default 2)                 |
| `hextra-card`          | block      | title arg, `:link:`, `:icon:`, `:image:`     |
| `hextra-tabs`          | container  | none (H3-split)                              |
| `hextra-steps`         | container  | none (H3-split)                              |
| `hextra-filetree`      | block      | none (nested bullets)                        |
| `hextra-hero`          | block      | `:title:`, `:tagline:`, `:cta-text:`, `:cta-link:` |
| `hextra-feature-grid`  | container  | none                                         |
| `hextra-feature`       | block      | title arg, `:subtitle:`, `:image:`, `:link:`, `:style:` |

Every container directive can hold other directives, Markdown prose, and
arbitrary Sphinx content. When you nest fences, the outer fence must use
more backticks than the inner — four outside, three inside for a normal
nesting, or enable `colon_fence` in `myst_enable_extensions` and use `:::`
for the outer block to sidestep the backtick count entirely.
