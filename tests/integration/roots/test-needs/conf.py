project = "test"
extensions = ["sphinx_needs", "sphinx_hextra"]
html_theme = "sphinx_hextra"
master_doc = "index"
exclude_patterns = ["_build"]
needs_types = [
    {"directive": "req", "title": "Requirement", "prefix": "R_", "color": "#BFD8D2", "style": "node"},
]
