# LaTeX

`sphinx-hextra` does not ship a math renderer of its own. Math support in a
Sphinx project comes from the built-in `sphinx.ext.mathjax` or
`sphinx.ext.imgmath` extensions, plus the MyST `dollarmath` and `amsmath`
extensions for `$`-delimited syntax. This page walks through the full setup.

## Enable the extensions

Start by adding the Sphinx math extension to your `conf.py`. For web output,
MathJax is almost always what you want — it renders client-side and looks
sharp at any zoom level:

```python
extensions = [
    "myst_parser",
    "sphinx_hextra",
    "sphinx.ext.mathjax",
]
```

Then enable the MyST dollar-math syntax so you can write `$…$` and `$$…$$`
the same way you would in a LaTeX document:

```python
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "amsmath",
]
```

`dollarmath` turns on inline and block `$` math. `amsmath` additionally
enables AMS environments (`align`, `gather`, `multline`, `equation`, and
friends).

## Inline math

Wrap inline math in single dollar signs:

```markdown
The area of a circle is $A = \pi r^2$.
```

Which renders as: The area of a circle is $A = \pi r^2$.

If you have a page that uses a lot of shell variables and you are worried
about accidental math triggers, you can disable inline dollar math and still
keep block math by passing the option to `dollarmath`:

```python
myst_dmath_allow_labels = True
myst_dmath_allow_space = True
myst_dmath_double_inline = True
```

See the
[MyST dollarmath documentation](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#dollar-delimited-math)
for the full list of tuning knobs.

## Block math

Double dollar signs produce a centred display equation:

```markdown
$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

Which renders as:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

For AMS environments, drop the dollar signs and use the environment
directly once `amsmath` is enabled:

```markdown
\begin{align}
(a + b)^2 &= a^2 + 2ab + b^2 \\
(a - b)^2 &= a^2 - 2ab + b^2
\end{align}
```

## The `{math}` role and directive

The classic docutils way still works and does not need `dollarmath`:

```markdown
Inline: {math}`e^{i\pi} + 1 = 0`

Block:

```{math}
\int_0^1 x^2 \, dx = \frac{1}{3}
```
```

Pick whichever style reads more naturally. Most projects use dollar math for
everyday expressions and the `{math}` directive only when they need to label
an equation for cross-referencing.

## Labelled equations

With `amsmath` you can label an equation and reference it with `{eq}`:

```markdown
$$
e^{i\pi} + 1 = 0
$$ (eq:euler)

Equation {eq}`eq:euler` is often called "the most beautiful equation in
mathematics".
```

## Backends

There are two Sphinx math backends to pick from:

- **`sphinx.ext.mathjax`** (recommended) — loads MathJax from a CDN and
  renders math in the browser. Crisp at any zoom, searchable, selectable,
  accessible. Slightly slower initial page load.
- **`sphinx.ext.imgmath`** — renders every equation to a PNG or SVG at build
  time using a local LaTeX install. No runtime JS, but you now have a LaTeX
  dependency in your build environment and the images don't scale as
  gracefully.

Unless you have a hard "no client-side JavaScript" constraint, use MathJax.

## Example: the quadratic formula, end-to-end

Full example combining the pieces above. Put this in a `.md` file with
MathJax and `dollarmath` enabled:

```markdown
# Roots of a quadratic

The quadratic formula gives the roots of $ax^2 + bx + c = 0$ as

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$ (eq:quadratic)

Equation {eq}`eq:quadratic` is real-valued when the discriminant
$\Delta = b^2 - 4ac$ is non-negative.
```

The rendered page shows the inline `$ax^2 + bx + c = 0$` in-line with the
prose, a centred display equation below, and a live cross-reference that
Sphinx will turn into a link.
