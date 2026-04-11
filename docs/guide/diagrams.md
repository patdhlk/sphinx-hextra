# Diagrams

`sphinx-hextra` does not bundle diagram support. The reasoning is the same
as for math: diagrams are a big dependency surface (PlantUML wants Java,
Graphviz wants a C binary, Mermaid wants a Node toolchain) and most projects
only need one of them. So instead of picking for you, the theme stays out of
the way and lets you add whichever Sphinx extension matches your needs.

The good news is that every popular diagramming extension either ships with
Sphinx already or can be installed in one line. This page walks through the
three most common choices.

## Mermaid

[Mermaid](https://mermaid.js.org/) is a JavaScript diagramming library with
a simple text syntax. The `sphinxcontrib-mermaid` extension adds a
`{mermaid}` directive to Sphinx that renders your source into an SVG at
build time (or defers to the Mermaid runtime in the browser).

Install:

```bash
uv add sphinxcontrib-mermaid
# or
pip install sphinxcontrib-mermaid
```

Enable in `conf.py`:

```python
extensions = [
    "myst_parser",
    "sphinx_hextra",
    "sphinxcontrib.mermaid",
]
```

A flowchart example:

````markdown
```{mermaid}
flowchart LR
    A[Write docs] --> B{Build with -W}
    B -- passes --> C[Deploy]
    B -- fails --> A
```
````

A sequence diagram:

````markdown
```{mermaid}
sequenceDiagram
    participant User
    participant Browser
    participant Server
    User->>Browser: click link
    Browser->>Server: GET /page
    Server-->>Browser: 200 OK
    Browser-->>User: render page
```
````

Mermaid themes itself — setting `mermaid_output_format = "raw"` in `conf.py`
leaves theming to the browser, which means your diagrams pick up whatever
CSS variables are in scope. `sphinx-hextra`'s dark-mode toggle does not
currently re-render Mermaid diagrams on theme change; if this matters to
you, set `mermaid_output_format = "svg"` and style the SVG with CSS
targeting `.mermaid svg` in your `custom.css`.

## Graphviz (built-in)

[Graphviz](https://graphviz.org/) is a venerable C-based graph layout engine
and the `sphinx.ext.graphviz` extension is bundled with Sphinx itself. You
do need the `dot` binary on your `PATH` at build time — on macOS,
`brew install graphviz`; on Debian/Ubuntu, `apt install graphviz`.

Enable:

```python
extensions = [
    "myst_parser",
    "sphinx_hextra",
    "sphinx.ext.graphviz",
]
```

Example:

````markdown
```{graphviz}
digraph example {
    rankdir=LR;
    node [shape=box, style=rounded];
    source -> sphinx -> html;
    sphinx -> latex;
    sphinx -> epub;
}
```
````

Graphviz outputs a static SVG at build time, so there is no JavaScript to
load in the browser.

## PlantUML

[PlantUML](https://plantuml.com/) covers UML in all its flavours — class,
sequence, state, activity, component, deployment. The
`sphinxcontrib-plantuml` extension wraps the PlantUML jar and exposes a
`{uml}` directive.

Install:

```bash
uv add sphinxcontrib-plantuml
```

You also need the `plantuml` command available. On macOS,
`brew install plantuml`; on Linux, grab the jar from
[plantuml.com/download](https://plantuml.com/download) and create a wrapper
script.

Enable:

```python
extensions = [
    "myst_parser",
    "sphinx_hextra",
    "sphinxcontrib.plantuml",
]
plantuml = "plantuml"
```

A class diagram:

````markdown
```{uml}
@startuml
class User {
    +id: int
    +email: string
    +displayName(): string
}
class Session {
    +token: string
    +expiresAt: datetime
}
User "1" -- "*" Session
@enduml
```
````

## A note on `needflow`

If you are using [sphinx-needs](../advanced/sphinx-needs.md), its `needflow`
directive renders a traceability graph across your requirements, specs, and
tests. Under the hood `needflow` uses PlantUML, so the install notes above
apply. Once the `plantuml` binary is reachable, `needflow` "just works" —
you don't need to install `sphinxcontrib-plantuml` separately for it to do
its job.
