# Comments

`sphinx-hextra` does not bundle a comments system. Comments are
deliberately an opt-in feature because every project has different
constraints: some use Giscus for GitHub-backed discussions, some use
Utterances for the same but with issues instead of discussions, some
use Disqus, some run a self-hosted Commento instance, and many
projects have no comments at all. Rather than picking one for you,
the theme stays out of the way and lets you drop any third-party
comments widget into your template.

This page covers the three most common choices.

## Giscus

[Giscus](https://giscus.app/) is a comments widget backed by GitHub
Discussions. It is free, requires no server, and the comments live
alongside your repository on GitHub — which is the right fit for
most open-source documentation sites.

Setup is four steps: enable Discussions on your repo, install the
Giscus GitHub App and grant it access, generate a script tag on
<https://giscus.app/>, and drop that script tag into a Sphinx
template.

The simplest way to inject the Giscus script is via `html_js_files`:

```python
html_js_files = [
    (
        "https://giscus.app/client.js",
        {
            "data-repo": "you/your-repo",
            "data-repo-id": "R_xxxxxxxx",
            "data-category": "Announcements",
            "data-category-id": "DIC_xxxxxxxx",
            "data-mapping": "pathname",
            "data-reactions-enabled": "1",
            "data-emit-metadata": "0",
            "data-input-position": "bottom",
            "data-theme": "preferred_color_scheme",
            "data-lang": "en",
            "crossorigin": "anonymous",
            "async": "async",
        },
    ),
]
```

Sphinx's `html_js_files` accepts a tuple of `(url, attributes_dict)`,
which it expands into a `<script>` tag with all the attributes set.
The Giscus client reads its config from `data-*` attributes on its
own script tag, so this is exactly the shape Giscus expects.

The one issue with this approach is that Giscus loads on every page,
including your landing page and 404 page, which you probably do not
want. For per-page control, create `_templates/layout.html` that
extends the theme and appends a Giscus container inside the content
block. See the template-overriding section in
[Customization](customization.md) for the pattern.

`data-theme: preferred_color_scheme` makes Giscus track the user's
system preference automatically. If you want Giscus to follow
`sphinx-hextra`'s dark-mode toggle instead, set
`data-theme: light` as the default and add a short script that posts
a theme message to the Giscus iframe whenever the toggle fires. The
theme-toggle script in `static/theme-toggle.js` dispatches a
`hx:theme` custom event on `document` you can listen for.

## Utterances

[Utterances](https://utteranc.es/) is similar to Giscus but backed
by GitHub Issues instead of Discussions, and with a much smaller
feature set (no reactions, no threading). The advantage is that any
public repo can use it without enabling Discussions first.

Configuration looks the same:

```python
html_js_files = [
    (
        "https://utteranc.es/client.js",
        {
            "repo": "you/your-repo",
            "issue-term": "pathname",
            "theme": "preferred-color-scheme",
            "crossorigin": "anonymous",
            "async": "async",
        },
    ),
]
```

Utterances creates one GitHub issue per page on first visit.

## Disqus

The [`sphinxcontrib-disqus`](https://pypi.org/project/sphinxcontrib-disqus/)
extension wraps the Disqus embed in a Sphinx directive, which lets
you place the thread exactly where you want it on a page:

```python
extensions = [
    "myst_parser",
    "sphinx_hextra",
    "sphinxcontrib.disqus",
]
disqus_shortname = "your-disqus-shortname"
```

Then in any page where you want a thread:

````markdown
```{disqus}
```
````

Disqus is closed-source, ad-supported, and has a long history of
data-privacy controversy. It is listed here for completeness but is
not what we would recommend for a new project in 2026.

## A note on privacy and GDPR

Every third-party comments widget loads JavaScript from someone else's
server, which means tracking pixels, cookies, and GDPR obligations.
Giscus and Utterances are the least invasive of the three — they only
load after the user scrolls to the comments section and they do not
set cookies for unauthenticated readers — but the safest choice is
still to make comments opt-in per page and to disclose the integration
in your privacy policy.
