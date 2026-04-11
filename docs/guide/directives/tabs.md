# Tabs

`hextra-tabs` groups a set of mutually-exclusive content sections behind
a tab bar. It is the right choice when you have the same instructions
for several operating systems, several languages, or several install
methods, and you want the reader to see one at a time instead of
scrolling past all of them.

## Syntax

Inside a `hextra-tabs` directive, each H3 (`###`) heading becomes a tab.
Everything between one H3 and the next is the tab's body. There are no
options — the directive has no arguments and no fields.

````markdown
```{hextra-tabs}
### macOS
Install with Homebrew:

    brew install sphinx-hextra

### Linux
On Debian/Ubuntu:

    apt install python3-sphinx-hextra

### Windows
On Windows with winget:

    winget install sphinx-hextra
```
````

## Rendered behaviour

A tab bar sits on top, with each H3 title rendered as a button. Clicking
a button shows the corresponding panel and hides the others. The active
tab has a coloured underline matching `--hx-accent`, inactive tabs are
dimmed to 70% opacity.

The active tab is persisted to `sessionStorage` keyed by the group's
position on the page, so if a reader picks "Linux" in one tab group and
scrolls further down the same page, subsequent tab groups also start on
the matching label when possible. This behaviour is scoped to the browser
session — it does not persist across page reloads from a fresh tab, and
it does not sync across tabs.

On keyboards, left/right arrows move focus between tabs once the tab bar
has focus, and `Enter`/`Space` activates the focused tab. The panels are
linked by `aria-controls` / `aria-labelledby` so assistive technology can
navigate them as a tab set.

## Three-tab example for a cross-platform install

````markdown
```{hextra-tabs}
### macOS
```bash
brew tap example/tap
brew install example-cli
```

### Linux
```bash
curl -sSL https://example.com/install.sh | bash
```

### Windows
```powershell
winget install Example.CLI
```
```
````

Inside a tab body you can use any Markdown or directive — including
other `hextra-*` directives — as long as your backtick nesting is
consistent.

## H1 + H3 and the `myst.header` warning

Because tabs split on H3 headings, a page that has an H1 at the top
**and** a `hextra-tabs` block with H3s will produce a MyST header-level
warning ("non-consecutive header level increase") unless you suppress
it. `sphinx-hextra`'s own documentation suppresses this globally in
`conf.py`:

```python
suppress_warnings = ["myst.header", "config.cache"]
```

You want this set in your own project too. It suppresses the one
specific warning that fires on legitimate uses of `hextra-tabs` and
`hextra-steps` inside titled pages, without suppressing anything else.

If you would rather not suppress the warning globally, you can use H2s
in the tabs directive — `sphinx-hextra` splits on H3s specifically, so
H2 content will not be recognised as a tab label. The best current
workaround is to live with the global suppression.
