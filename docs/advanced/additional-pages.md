# Additional Pages

Most of the time you want every page to live inside the toctree so it
shows up in the sidebar and participates in previous/next navigation.
Sometimes, though, you want a page that is published as HTML but
deliberately *not* in the tree: a 404 page, a marketing splash, a
standalone changelog linked only from the navbar, an HTML redirect.
This page covers the three mechanisms Sphinx exposes for that.

## Orphan pages

The simplest case: a Markdown page that lives in your source tree and
is built like every other page, but is not listed in any toctree.
Normally Sphinx warns about this ("document isn't included in any
toctree") because it usually means you forgot to wire up the page.

If you want the warning suppressed for a specific page, mark it as an
orphan. In a MyST file, add the `:orphan:` metadata at the very top,
before the H1:

```markdown
---
orphan: true
---

# Standalone page

This page exists but is not in the sidebar.
```

The page builds normally, is reachable at its usual URL, and Sphinx
does not complain. Use orphan pages for things you link to from other
places — a landing page linked from your navbar, an internal cheat
sheet linked from a blog post — but do not want cluttering the main
navigation.

You can also set `hide-toc: true` as part of the same front matter if
the orphan page should suppress the right-hand table of contents:

```markdown
---
orphan: true
hide-toc: true
---

# Landing
```

## `html_additional_pages`

When you need to ship arbitrary HTML — not Markdown, not RST — use the
`html_additional_pages` mapping in `conf.py`. The keys are output
paths (without the `.html` extension), and the values are Jinja2
template names that Sphinx renders to produce the page.

```python
html_additional_pages = {
    "404": "404.html",
    "robots": "robots.txt",
}
```

With this, Sphinx renders `_templates/404.html` into the build output
as `404.html`, and `_templates/robots.txt` into `robots.txt`. The
templates have access to the full Jinja context Sphinx provides to
layout templates, so you can extend the base theme to get the navbar
and footer for free:

```jinja
{% extends "layout.html" %}
{% set title = "Page not found" %}

{% block body %}
  <div class="hx-content">
    <h1>Page not found</h1>
    <p>The page you were looking for does not exist.</p>
    <p><a href="{{ pathto(master_doc) }}">Return home</a>.</p>
  </div>
{% endblock %}
```

Make sure `templates_path = ["_templates"]` is set in `conf.py` so
Sphinx can find the template file.

## HTML redirects

A common special case of `html_additional_pages` is a redirect. When
you rename a page, you want URLs that used to point at the old name
to still work. Create a small redirect template:

```jinja
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url={{ target }}">
    <link rel="canonical" href="{{ target }}">
  </head>
  <body>
    <p>Redirecting to <a href="{{ target }}">{{ target }}</a>.</p>
  </body>
</html>
```

Then register the redirects in `conf.py`. You will need to pass the
target through to the template, which means either a wrapper function
or using `html_context`:

```python
html_additional_pages = {
    "old-name": "redirect.html",
}
html_context = {"target": "new-name.html"}
```

For a more complete solution, install
[`sphinx-reredirects`](https://pypi.org/project/sphinx-reredirects/)
which wraps this pattern in a friendlier config:

```python
extensions = [..., "sphinx_reredirects"]
redirects = {
    "old-name": "new-name.html",
}
```

## Raw HTML inside a page

If you want arbitrary HTML embedded *inside* an otherwise normal
Markdown page, you do not need `html_additional_pages` at all — just
use a MyST raw-HTML block:

````markdown
```{raw} html
<div class="my-custom-widget">
  <iframe src="https://example.com/embed" loading="lazy"></iframe>
</div>
```
````

The raw block is emitted verbatim into the HTML output and skipped by
other builders. Use it sparingly — anything you embed this way will
not be picked up by search, by the intersphinx inventory, or by
`sphinx-build -b epub`.
