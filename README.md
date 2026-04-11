# sphinx-hextra

A Sphinx HTML theme and component directive set that brings the aesthetic of the [Hextra](https://github.com/imfing/hextra) Hugo theme to the Sphinx documentation ecosystem, with first-class styling for [sphinx-needs](https://github.com/useblocks/sphinx-needs).

**sphinx-hextra is a derivative work.** Visual design, component concepts, and CSS structure are ported from Hextra (MIT, © Imfing and contributors). The upstream LICENSE is preserved verbatim at [`licenses/HEXTRA-LICENSE`](licenses/HEXTRA-LICENSE). See [`CREDITS.md`](CREDITS.md) for full attribution.

## Install

```bash
uv add sphinx-hextra
```

## Use

In your `conf.py`:

```python
extensions = ["myst_parser", "sphinx_hextra"]
html_theme = "sphinx_hextra"
```

## Features (v0.1)

- Hextra-inspired layout, typography, and dark mode
- Directives: `hextra-callout`, `hextra-cards` + `hextra-card`, `hextra-tabs`, `hextra-steps`, `hextra-filetree`
- Landing-page directives: `hextra-hero`, `hextra-feature-grid`, `hextra-feature`
- Automatic sphinx-needs integration styling (when `sphinx_needs` is enabled)
- Zero Node.js dependency for end users — CSS is precompiled

## Credits

This project stands on the shoulders of [Hextra](https://github.com/imfing/hextra). Every design decision traces back to their work. Bugs here are ours; beauty is theirs.

## License

MIT. See [`LICENSE`](LICENSE) (sphinx-hextra) and [`licenses/HEXTRA-LICENSE`](licenses/HEXTRA-LICENSE) (upstream Hextra).
