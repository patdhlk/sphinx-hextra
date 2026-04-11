# Advanced

The advanced section covers the topics you reach for after you have a
working site and want to push it further: brand colours, custom HTML
pages, translations, comments, and deep integration with
`sphinx-needs`. None of these are strictly necessary to get a
`sphinx-hextra` site online, but every one of them comes up eventually.

If you are still setting up, start with [Getting
Started](../getting-started.md) and the [Guide](../guide/index.md); if
you are looking for how a specific directive works, jump to the
[Directives](../guide/directives/index.md) section. Come back here once
your documentation has outgrown the default look.

## In this section

````{hextra-cards}
:columns: 2

```{hextra-card} Customization
:link: customization.html
Override the CSS palette, add custom styles, and brand the theme.
```

```{hextra-card} Additional Pages
:link: additional-pages.html
Orphan pages, `html_additional_pages`, and content outside the toctree.
```

```{hextra-card} Multi-Language
:link: multi-language.html
Sphinx's gettext-based internationalisation, and what is still English.
```

```{hextra-card} Comments
:link: comments.html
Add Giscus, Utterances, or Disqus to your pages.
```

```{hextra-card} sphinx-needs
:link: sphinx-needs.html
First-class styling for requirements, specifications, and traceability.
```
````

## What counts as "advanced"

Roughly, a topic lands here when it involves one of the following:

- **Overriding defaults.** Customization lives here because you need to
  understand the theme's CSS variable palette to change it cleanly.
- **Leaving the toctree.** Additional pages and orphans are advanced
  because they break Sphinx's default "everything is in the tree"
  invariant and you have to know why.
- **Adding a dependency.** Multi-language, comments, and `sphinx-needs`
  all pull in extensions or tooling `sphinx-hextra` does not ship by
  itself.
- **Tooling integration.** `sphinx-needs` styling is the one topic
  where `sphinx-hextra` has first-class code — a scoped stylesheet that
  restyles needs tables to match the theme — so it gets its own page.

Everything else is in the main [Guide](../guide/index.md).
