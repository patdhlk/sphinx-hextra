from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_theme_toggle_js_loaded(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    scripts = [s.get("src", "") for s in soup.find_all("script")]
    assert any("theme-toggle.js" in s for s in scripts), scripts
