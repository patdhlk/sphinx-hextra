project = "sphinx-hextra"
copyright = "2026, Patrick Dahlke"
author = "Patrick Dahlke"

extensions = ["myst_parser", "sphinx_needs", "sphinx_hextra"]
myst_enable_extensions = ["colon_fence"]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
master_doc = "index"
html_theme = "sphinx_hextra"
html_theme_options = {
    "navbar_title": "sphinx-hextra",
    "github_url": "https://github.com/patdhlk/sphinx-hextra",
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "superpowers", "ubproject.toml"]
suppress_warnings = ["myst.header", "config.cache"]

# sphinx-needs configuration lives in ./ubproject.toml
needs_from_toml = "ubproject.toml"
