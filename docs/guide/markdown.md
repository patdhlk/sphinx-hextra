# Markdown

`sphinx-hextra` does not ship its own Markdown parser. It relies on
[MyST](https://myst-parser.readthedocs.io/), the de-facto Markdown flavour
for Sphinx, which you install as a separate extension:

```bash
uv add myst-parser
# or
pip install myst-parser
```

Then add `"myst_parser"` to the `extensions` list in `conf.py`. Once that is
in place, any file ending in `.md` goes through MyST on its way to Sphinx.

MyST is a strict superset of [CommonMark](https://commonmark.org/) with
additions that map Markdown constructs onto docutils roles and directives —
the underlying building blocks Sphinx is built on. Everything Sphinx can do,
MyST can express; you are not locked out of any Sphinx feature because you
chose Markdown.

## The basics

Headings use `#` through `######`. Every page should start with exactly one
H1:

```markdown
# Page title

## A section

### A subsection
```

Paragraphs are separated by blank lines. Emphasis uses `*italic*` and
`**bold**`. Inline code uses backticks. Links use `[text](url)` and images
use `![alt](url)`.

Unordered lists use `-` or `*`, ordered lists use `1.` (the numbers do not
have to be sequential — Markdown renumbers them on render).

Tables use pipes and dashes:

```markdown
| Column A | Column B |
| -------- | -------- |
| cell     | cell     |
```

Blockquotes use `>`:

```markdown
> "Documentation is a love letter that you write to your future self."
> — Damian Conway
```

## Fenced code

Triple backticks with a language tag produce syntax-highlighted code blocks:

````markdown
```python
def hello():
    print("hi")
```
````

More on that in [Syntax Highlighting](syntax-highlighting.md).

## Directives

Directives are where MyST stops looking like plain Markdown. The syntax is a
fenced block whose language tag is a directive name in curly braces:

````markdown
```{note}
This is a rendered note box.
```
````

All seven `sphinx-hextra` component directives
([callout](directives/callout.md), [cards](directives/cards.md),
[tabs](directives/tabs.md), [steps](directives/steps.md),
[filetree](directives/filetree.md), [hero and feature
grid](directives/landing.md)) use exactly this syntax.

### colon fences vs backtick fences

When you need to nest a directive inside another directive, the outer fence
must use **more** backticks than the inner, which quickly becomes a
book-keeping exercise. MyST offers an alternative with `colon_fence` enabled:

```python
myst_enable_extensions = ["colon_fence"]
```

Now you can use `:::` instead of backticks, which keeps the total backtick
budget for actual code samples:

```markdown
:::{note}
You can freely embed `inline code` without counting backticks.
:::
```

## Roles

Roles are the inline equivalent of directives. They are written as
`` {role}`content` ``:

```markdown
See the {doc}`configuration` page, or jump to the {ref}`install-section`.
```

Useful built-in roles: `{doc}`, `{ref}`, `{math}`, `{kbd}`, `{file}`,
`{command}`. See the
[MyST roles documentation](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html)
for the complete list.

## Substitutions

If you find yourself repeating the same string — a version number, a URL, a
product name — define a substitution in the `myst_substitutions` dict in
`conf.py`:

```python
myst_substitutions = {"version": "0.1.0"}
```

Then reference it in any page:

```markdown
You are reading the docs for version {{ version }}.
```

## Extensions worth enabling

MyST has a handful of optional syntax extensions that most projects end up
using:

- `colon_fence` — write `:::` fenced directives.
- `deflist` — definition lists (`term\n: definition`).
- `tasklist` — GitHub-style `- [ ]` and `- [x]` checkboxes.
- `attrs_inline` — inline `{#id .class}` attributes on spans, links, images.
- `linkify` — bare URLs automatically become links.
- `dollarmath` — `$inline$` and `$$block$$` math syntax. See [LaTeX](latex.md).
- `amsmath` — AMS LaTeX environments (`\begin{align}…\end{align}`).

Enable any combination of these in `conf.py`:

```python
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "attrs_inline",
    "dollarmath",
]
```

For the complete reference — every directive, role, and extension — see the
[MyST documentation](https://myst-parser.readthedocs.io/).
