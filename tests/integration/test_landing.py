from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="landing")
def test_hero_renders(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    hero = soup.select_one("section.hx-hero")
    assert hero is not None
    assert hero.select_one(".hx-hero__title").get_text() == "Welcome"
    assert hero.select_one(".hx-hero__tagline").get_text() == "Beautiful Sphinx docs."
    cta = hero.select_one("a.hx-hero__cta")
    assert cta.get("href") == "quickstart.html"
    assert "Start" in cta.get_text()


@pytest.mark.sphinx("html", testroot="landing")
def test_feature_grid_renders(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    grid = soup.select_one("div.hx-feature-grid")
    assert grid is not None
    features = grid.select("div.hx-feature")
    assert len(features) == 2
    titles = [f.select_one(".hx-feature__title").get_text() for f in features]
    assert titles == ["Fast", "Flexible"]
