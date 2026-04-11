project = "sphinx-hextra"
copyright = "2026, Patrick Dahlke"
author = "Patrick Dahlke"

extensions = ["myst_parser", "sphinx_hextra"]
myst_enable_extensions = ["colon_fence"]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
master_doc = "index"
html_theme = "sphinx_hextra"
html_theme_options = {
    "navbar_title": "sphinx-hextra",
    "github_url": "https://github.com/patdhlk/sphinx-hextra",
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "superpowers"]
suppress_warnings = ["myst.header"]
