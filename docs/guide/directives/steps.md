# Steps

`hextra-steps` renders a numbered walkthrough with a vertical rail on
the left and a filled circle for each step marker. Use it for any
sequence the reader follows in order: an install flow, a tutorial, a
migration guide.

Unlike an ordered list, the steps directive gives each item a heading
and a body, and it reserves vertical space so adjacent steps read as
distinct milestones rather than list items blurred together. The result
reads like Hugo Hextra's steps widget because that is what it is
modelled on.

## Syntax

Inside `hextra-steps`, each H3 (`###`) heading starts a new step. The
heading text becomes the step title, and everything between this H3 and
the next becomes the step body. Steps are auto-numbered in the rendered
output, so you do not write the numbers yourself.

````markdown
```{hextra-steps}
### Install
Run `uv add sphinx-hextra` (or `pip install sphinx-hextra`) in your
documentation project.

### Configure
Add `"sphinx_hextra"` to `extensions` and set
`html_theme = "sphinx_hextra"` in `docs/conf.py`.

### Build
Run `sphinx-build -W docs docs/_build/html` and open the resulting
`index.html` in a browser.
```
````

## Rendered behaviour

Steps render as a vertical stack with a 1px rail running down the left.
Each step has a filled circle marker at the same height as its heading,
containing the step's 1-indexed number in white text on a background of
`--hx-accent`. The rail colour is `--hx-border`, the step heading uses
the default `--hx-fg` foreground, and the step body is indented so it
lines up cleanly with the heading.

The marker geometry is fixed — 20px diameter — so very long step numbers
(more than 2 digits) will look cramped. If you have more than 99 steps
in a single block, the right answer is almost always to split the flow
across multiple pages instead.

## A three-step example

````markdown
```{hextra-steps}
### Create a branch
```bash
git checkout -b docs/update-guide
```

### Write and preview
```bash
sphinx-build -W docs docs/_build/html
open docs/_build/html/index.html
```

### Commit and open a PR
```bash
git add docs && git commit -m "docs: expand guide"
git push -u origin HEAD
gh pr create
```
```
````

Inside a step body you can freely use nested directives — code blocks,
callouts, tabs, even another card grid — provided you get the fence
nesting right. Four backticks outside, three inside is the usual
configuration; jump to five outside and four inside if you genuinely
need a triply-nested directive.

## H1 + H3 and `suppress_warnings`

Just like [tabs](tabs.md), the steps directive splits on H3 headings,
which means a page with a single H1 followed by a `hextra-steps` block
will trip MyST's "non-consecutive header level increase" warning unless
you suppress it. Add the following to `conf.py`:

```python
suppress_warnings = ["myst.header", "config.cache"]
```

This is already set in `sphinx-hextra`'s own docs and is the
recommended default for any project that uses `hextra-tabs` or
`hextra-steps` on titled pages.
