# sphinx-needs Integration

sphinx-hextra automatically styles [sphinx-needs](https://github.com/useblocks/sphinx-needs) output whenever the extension is enabled. Tables, need blocks, status and type badges all pick up the theme's colors and rounded corners in both light and dark mode — no configuration required.

The sphinx-needs configuration for this site lives in [`ubproject.toml`](https://github.com/patdhlk/sphinx-hextra/blob/main/docs/ubproject.toml) and is loaded via `needs_from_toml = "ubproject.toml"` in `conf.py`.

## Requirements

```{req} Beautiful by default
:id: R_DESIGN_001
:status: closed
:tags: theme

The theme must be visually recognisable as "Hextra on Sphinx" out of the box — no user configuration required beyond `html_theme = "sphinx_hextra"`.
```

```{req} Component directives
:id: R_CORE_002
:status: closed
:tags: directive

Users must be able to drop Hextra-style components (callouts, cards, tabs, steps, filetrees) into their pages using native Sphinx / MyST syntax.
```

```{req} sphinx-needs compatibility
:id: R_NEEDS_003
:status: closed
:tags: theme

The theme must render sphinx-needs output (tables, need blocks, badges) in a visual style consistent with the rest of the theme.
```

## Specifications

```{spec} Hextra layout chrome
:id: S_LAYOUT_001
:status: closed
:links: R_DESIGN_001
:tags: theme

Ship a full custom `layout.html` with navbar, sidebar, right-hand TOC, and footer, styled after the Hextra Hugo theme.
```

```{spec} Five core directives
:id: S_DIRECTIVES_002
:status: closed
:links: R_CORE_002
:tags: directive

Implement `hextra-callout`, `hextra-cards`/`hextra-card`, `hextra-tabs`, `hextra-steps`, and `hextra-filetree` as Sphinx directives emitting semantic HTML with stable BEM classnames.
```

```{spec} Scoped needs stylesheet
:id: S_NEEDS_CSS_003
:status: closed
:links: R_NEEDS_003
:tags: css

Inject a scoped `sphinx-hextra-needs.css` on pages where `sphinx_needs` is loaded. The stylesheet restyles `needs_table`, `needs_status`, `needs_type`, and `.need` blocks using the theme's CSS variables.
```

## Test cases

```{test} Theme builds with zero warnings
:id: T_BUILD_001
:status: closed
:links: S_LAYOUT_001

Integration test `tests/integration/test_theme_loads.py::test_theme_builds_without_errors` asserts the minimal Sphinx project using `html_theme = "sphinx_hextra"` builds with an empty warning buffer.
```

```{test} Every directive renders semantic HTML
:id: T_DIRECTIVES_002
:status: closed
:links: S_DIRECTIVES_002

Integration tests under `tests/integration/test_callout.py`, `test_cards.py`, `test_tabs.py`, `test_steps.py`, `test_filetree.py` assert that each directive emits the expected classnames and DOM structure via BeautifulSoup.
```

```{test} Needs CSS is loaded only when needed
:id: T_NEEDS_003
:status: closed
:links: S_NEEDS_CSS_003

`tests/integration/test_needs_integration.py` verifies `sphinx-hextra-needs.css` is present in pages built against a project with `sphinx_needs`, and absent otherwise.
```

## Traceability

The `needtable` directive renders a live overview of every need defined on this page:

```{needtable}
:columns: id;title;type;status;tags;outgoing
:style: table
```
