from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="needs")
def test_needs_css_injected(app, warning):
    app.build()
    for line in warning.getvalue().splitlines():
        assert "sphinx_hextra" not in line, line
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    hrefs = [l.get("href", "") for l in soup.find_all("link", rel="stylesheet")]
    assert any("sphinx-hextra-needs.css" in h for h in hrefs), hrefs


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_needs_css_not_injected_without_needs(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    hrefs = [l.get("href", "") for l in soup.find_all("link", rel="stylesheet")]
    assert not any("sphinx-hextra-needs.css" in h for h in hrefs), hrefs
