from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_navbar(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("nav.hx-navbar"), "navbar missing"


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_sidebar(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("aside.hx-sidebar"), "sidebar missing"


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_theme_toggle(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("button.hx-theme-toggle"), "theme toggle missing"


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_layout_has_footer(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("footer.hx-footer"), "footer missing"
