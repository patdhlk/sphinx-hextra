# Syntax Highlighting

Sphinx highlights code using [Pygments](https://pygments.org/), a
Python-based syntax highlighter that supports several hundred languages out
of the box. `sphinx-hextra` ships a paired light/dark Pygments configuration
in its `theme.toml`, so code blocks look right in both themes with no extra
work from you.

## Fenced code blocks

The simplest way to get a highlighted code block is a Markdown fence with a
language tag:

````markdown
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
````

Pygments recognises the language tag and renders tokens accordingly. A
short, non-exhaustive list of tags you can use: `python`, `javascript`,
`typescript`, `jsx`, `tsx`, `rust`, `go`, `java`, `c`, `cpp`, `sh`, `bash`,
`zsh`, `powershell`, `html`, `css`, `scss`, `yaml`, `json`, `toml`, `ini`,
`sql`, `dockerfile`, `nginx`, `diff`, `text`.

If you leave the tag off, the block renders as plain preformatted text
without highlighting. If you want to be explicit about that, use `text`.

## The `code-block` directive

When you need more control than a plain fence allows — line numbers, caption,
emphasised lines — switch to the `code-block` directive:

````markdown
```{code-block} python
:linenos:
:emphasize-lines: 2,3
:caption: greet.py

def greet(name: str) -> str:
    message = f"Hello, {name}!"
    return message
```
````

The useful options are:

- `:linenos:` — show line numbers down the left side.
- `:emphasize-lines:` — comma-separated list of line numbers to highlight.
  Accepts ranges: `3-5,8`.
- `:caption:` — a caption rendered above the block, useful for "this is
  `app/main.py`" style pointers.
- `:name:` — a label you can cross-reference with `{ref}`.
- `:lineno-start:` — start numbering at a value other than 1.

## Light and dark styles

The `theme.toml` that ships with `sphinx-hextra` configures two Pygments
styles — `friendly` for the light theme, `monokai` for the dark theme — and
the dark-mode toggle swaps between them automatically. Both styles are part
of Pygments itself, so there is no extra install step.

If you want a different pair, you can override `pygments_style` in your
`conf.py`. Sphinx's Pygments handling is single-style by default, so
overriding it means you lose the automatic dark-theme swap:

```python
pygments_style = "tango"
```

See the [Pygments style gallery](https://pygments.org/styles/) for a
complete list. Good light-theme candidates: `friendly`, `tango`, `perldoc`.
Good dark-theme candidates: `monokai`, `dracula`, `one-dark`, `nord`.

## Examples

A Python example:

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str

    def display_name(self) -> str:
        return self.email.split("@")[0]
```

A JavaScript example:

```javascript
export async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to load user ${id}`);
  }
  return response.json();
}
```

A Rust example:

```rust
#[derive(Debug)]
struct Point {
    x: f64,
    y: f64,
}

impl Point {
    fn distance(&self, other: &Self) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}
```

A shell example with emphasised lines:

````markdown
```{code-block} bash
:linenos:
:emphasize-lines: 2

sphinx-build -W docs docs/_build/html
open docs/_build/html/index.html
```
````

## Inline code

Single backticks produce inline code that picks up the theme accent tint in
the background — useful for pointing at things like `html_theme_options` or
`_static/`. If you want inline code with syntax highlighting, use the
`{code}` role with a language:

```markdown
Use the {code}`python:def greet():` constructor to define a function.
```

The rendered output in `sphinx-hextra` wraps code blocks in a bordered
container with a rounded corner and a subtle accent tint on the background,
matching the rest of the theme chrome. Long lines scroll horizontally inside
the container rather than breaking the page layout.
