# FileTree

`hextra-filetree` renders a directory layout from a nested bullet list.
It is the right tool for "here is what your project looks like after
the tutorial" snippets, for documenting the layout of a scaffold, or
for showing where a config file lives in relation to the rest of a
project.

## Syntax

The body of the directive is a plain Markdown bullet list. Folders are
signalled by a trailing slash on the item text. Nesting uses standard
Markdown two-space indentation. The directive has no arguments and no
options — everything you control is in the list itself.

````markdown
```{hextra-filetree}
- my-project/
  - docs/
    - _static/
      - logo.svg
    - conf.py
    - index.md
    - guide/
      - index.md
      - configuration.md
  - pyproject.toml
  - README.md
```
````

Any item without a trailing slash is rendered as a file. Items with a
trailing slash are rendered as folders, regardless of whether they
have nested children. An empty folder is written as `name/` with no
sub-bullets.

## Rendered behaviour

The filetree renders in a monospace font (`JetBrains Mono` falling back
to the system monospace stack) with a 1px border and rounded corners,
sitting inline with the surrounding prose the way a code block would.
Each folder line shows a folder glyph to the left of its name; each
file line shows a file glyph. The glyphs are Unicode characters from
the theme stylesheet — they do not require any external icon font.

Nested items are indented relative to their parent with a subtle guide
line, so it is visually obvious where a subtree ends. The container is
horizontally scrollable for very deep trees on narrow viewports, so
deeply nested structures don't break the page layout.

## A larger example

````markdown
```{hextra-filetree}
- sphinx-hextra/
  - src/
    - sphinx_hextra/
      - __init__.py
      - directives/
        - __init__.py
        - callout.py
        - cards.py
        - tabs.py
        - steps.py
        - filetree.py
        - hero.py
      - theme/
        - sphinx_hextra/
          - layout.html
          - theme.toml
          - static/
            - sphinx-hextra.css
            - theme-toggle.js
  - tests/
    - integration/
      - test_callout.py
      - test_cards.py
  - docs/
    - index.md
    - conf.py
  - pyproject.toml
  - README.md
```
````

## When not to use filetree

If you need to annotate individual files with long explanations, a
filetree gets awkward fast — the monospace rendering is not built for
paragraph-length captions. In that case, use a regular definition list
or a table with a "path" column and a "purpose" column, which
`sphinx-hextra` styles with the same accent palette.

If you want to render a *live* filetree of the user's actual project
(e.g., scanning a directory at build time), that is outside the scope
of this directive. Use the [sphinx-filetree](https://pypi.org/project/sphinx-filetree/)
extension or generate the bullet list from a script during your build
step.
