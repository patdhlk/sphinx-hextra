# Multi-Language

Sphinx ships a full internationalisation pipeline based on GNU
gettext, the same toolchain that translates the Python interpreter,
the GNU coreutils, and most of the Linux desktop. It is not opt-in
per theme; you get it for free the moment you install Sphinx, and
`sphinx-hextra` inherits it without needing any theme-specific
configuration. This page walks through the workflow.

A caveat up front: `sphinx-hextra`'s own UI chrome — the "On this
page" heading above the right-hand TOC, the light/dark toggle button
label, the search box placeholder — is currently hard-coded in
English. The *content* you author gets translated end-to-end; the
surrounding theme chrome does not. If this is a blocker, please open
an issue or a pull request at
[github.com/patdhlk/sphinx-hextra](https://github.com/patdhlk/sphinx-hextra)
— translating the theme is a finite amount of work we are happy to
accept contributions for.

## The gettext workflow

Translation has three phases: **extraction**, **translation**, and
**building**. Extraction scans your Sphinx source for translatable
strings and writes them into `.pot` template files. Translators
create a `.po` file per target language from each `.pot`. At build
time, Sphinx reads the `.po` files and emits a fully translated HTML
tree.

### Step 1 — Extract

Tell Sphinx to extract strings from your source:

```bash
sphinx-build -b gettext docs docs/_build/gettext
```

This produces one `.pot` file per `.md` or `.rst` source file under
`docs/_build/gettext/`. A `.pot` is the untranslated template — think
of it as the schema for a translation.

### Step 2 — Initialise or update translations

Install `sphinx-intl` once (`uv add sphinx-intl` or `pip install
sphinx-intl`) and use it to create `.po` files per locale:

```bash
sphinx-intl update -p docs/_build/gettext -l de -l fr -l ja
```

This creates `docs/locale/de/LC_MESSAGES/`, `docs/locale/fr/…`, and
`docs/locale/ja/…`, each containing one `.po` per source file.
Re-running the same command after a content update merges new strings
into existing `.po` files without discarding already-translated
entries.

### Step 3 — Translate

A `.po` file is plain text with blocks of this shape:

```
#: ../../getting-started.md:15
msgid "Install"
msgstr ""
```

Fill in `msgstr` with the translation. Translators usually use an
editor like [Poedit](https://poedit.net/) or
[Lokalize](https://apps.kde.org/lokalize/) which wraps the same files
in a friendlier UI, but a plain text editor works too.

### Step 4 — Build per language

Point `sphinx-build` at a locale by passing the `language` config:

```bash
sphinx-build -b html -D language=de docs docs/_build/de
sphinx-build -b html -D language=fr docs docs/_build/fr
sphinx-build -b html -D language=ja docs docs/_build/ja
```

Each build produces a fully translated HTML tree. The usual deployment
pattern is to publish each locale under its own path prefix:
`/de/…`, `/fr/…`, `/ja/…`, with the default English build at the
root.

## `conf.py` settings

The two settings you want in `conf.py`:

```python
language = "en"
locale_dirs = ["locale/"]
gettext_compact = False
```

- `language` is the source language of the `.md` files. Sphinx uses
  this to pick the right date formats and to select the `.po`
  directory when building translated output. You override it per build
  with `-D language=…`.
- `locale_dirs` lists directories to search for `.po` files. `locale/`
  is the convention and matches what `sphinx-intl update` produces.
- `gettext_compact = False` tells Sphinx to produce one `.pot` per
  source file instead of collapsing them into per-directory bundles —
  which makes diffs clearer and lets you split translation work per
  file.

## Localising URLs and file names

By default, translated pages keep the original file names — an
English `getting-started.md` is still `getting-started.html` in
German. If you want the URLs themselves translated (`premiers-pas.html`
for French), look at
[`sphinx-polyglot`](https://pypi.org/project/sphinx-polyglot/) or build
a post-processing step. Sphinx itself does not rename files based on
language, because doing so breaks cross-references and search
indexing.

## Theme chrome translation

The strings `sphinx-hextra` puts into the rendered HTML — "On this
page", "Search", "Edit this page" (reserved), the theme toggle aria
labels — live inside `layout.html` and its partials as plain text. In
v0.1 they are not wrapped in `{% trans %}` blocks, which means even if
you have translated all your content, the surrounding chrome stays in
English. The roadmap for v0.2 is to wrap every chrome string in a
`{% trans %}` block and ship a default `en.po`, at which point
translating the chrome becomes a matter of dropping a `de.po` next to
it. Until then, the workaround is to override `layout.html` via
`_templates/layout.html` (see the template-overriding section in
[Customization](customization.md)) and hard-code
the strings in your target language.
