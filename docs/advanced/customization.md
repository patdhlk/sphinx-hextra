# Customization

Out of the box, `sphinx-hextra` looks like the Hextra Hugo theme: a
muted indigo accent on a near-white background in light mode, and a
lighter indigo on near-black in dark mode. Most projects eventually want
to change at least the accent colour to match their brand. This page
shows how to do that cleanly — by overriding a handful of CSS variables
rather than rewriting the stylesheet.

## The CSS variable palette

Every colour in `sphinx-hextra`'s stylesheet is defined in terms of a
small set of CSS variables declared on `:root` and `html.dark`. The
full palette is:

| Variable       | Light default | Dark default  | Purpose                                    |
| -------------- | ------------- | ------------- | ------------------------------------------ |
| `--hx-bg`      | `#ffffff`     | `#0b0f19`     | Page background                            |
| `--hx-fg`      | `#1f2937`     | `#e5e7eb`     | Default foreground text                    |
| `--hx-border`  | `#e5e7eb`     | `#1f2937`     | Borders, dividers, 1px outlines            |
| `--hx-muted`   | `#6b7280`     | `#9ca3af`     | Secondary text (metadata, captions)        |
| `--hx-accent`  | `#6366f1`     | `#818cf8`     | Links, buttons, active states, highlights  |

Every visible border, every link colour, every hover state ultimately
resolves to one of these five variables or a `color-mix()` of them
with the background. That means a one-line override in a custom
stylesheet rethemes the entire site at once.

## Overriding the palette

Create a `_static/custom.css` file in your project. Inside it, redefine
whichever variables you want to change, once for light mode on
`:root` and once for dark mode on `html.dark`:

```css
:root {
  --hx-accent: #ec4899;
}

html.dark {
  --hx-accent: #f472b6;
}
```

Then tell Sphinx to load it by adding two entries to `conf.py`:

```python
html_static_path = ["_static"]
html_css_files = ["custom.css"]
```

`html_static_path` points at the directory containing your static
assets. `html_css_files` lists stylesheets to inject into every page.
Both are additive — `sphinx-hextra`'s own stylesheet still loads, your
override simply comes after it and wins.

After rebuilding, every link, button, callout accent strip, active
sidebar item, and focus outline now uses pink instead of indigo,
because they all resolve to `var(--hx-accent)`.

## Brand-colour example

A complete example theming everything towards a warm orange:

```css
:root {
  --hx-bg: #fffbf5;
  --hx-fg: #1a1208;
  --hx-border: #f3e6d1;
  --hx-muted: #7c6a55;
  --hx-accent: #ea580c;
}

html.dark {
  --hx-bg: #14110c;
  --hx-fg: #f3e6d1;
  --hx-border: #2b2418;
  --hx-muted: #a68a6a;
  --hx-accent: #fb923c;
}
```

Drop this into `_static/custom.css`, rebuild, and the whole site — navbar,
sidebar, code blocks, callouts, hero gradient — shifts to the new
palette. Because `color-mix(in srgb, var(--hx-accent) …)` is used for
tints throughout the stylesheet, even subtle things like the hover tint
on sidebar links inherit the new colour automatically.

## Adding custom JavaScript

Exactly the same pattern with `html_js_files`:

```python
html_static_path = ["_static"]
html_js_files = ["custom.js"]
```

Drop your script in `_static/custom.js`. Every page loads it after the
theme's own scripts (theme toggle, tab persistence), so you can safely
reference any DOM they set up.

A common use case is a pageview counter or an analytics snippet:

```javascript
(function () {
  if (!window.plausible) return;
  window.plausible("Docs view", { props: { page: location.pathname } });
})();
```

## Overriding templates

If CSS is not enough — say you want to add a banner across every page,
or change the footer copy — point Sphinx at a `_templates/` directory
in `conf.py`:

```python
templates_path = ["_templates"]
```

Inside `_templates/`, create a file with the same name as the theme
template you want to override. Sphinx looks for templates in
`templates_path` before falling back to the theme, so
`_templates/layout.html` shadows `sphinx-hextra`'s `layout.html`.

In practice you almost never want to replace `layout.html` wholesale.
Instead, extend it with Jinja blocks so you inherit most of the
upstream layout and only change the bits you care about:

```jinja
{% extends "!layout.html" %}

{% block extrahead %}
  {{ super() }}
  <link rel="icon" href="{{ pathto('_static/favicon.svg', 1) }}">
{% endblock %}
```

The leading `!` in `extends "!layout.html"` tells Sphinx "extend the
same-named template from the underlying theme, not from this
directory", which is what you want when you are shadowing a template.

## Fully custom HTML pages

For pages that fall outside Sphinx entirely — a 404, a custom
marketing page, an HTML redirect — use `html_additional_pages`. See
[Additional Pages](additional-pages.md) for the details.
