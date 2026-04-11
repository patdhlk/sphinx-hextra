from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="cards")
def test_cards_container(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    container = soup.select_one("div.hx-cards")
    assert container is not None
    assert "hx-cards--cols-3" in container.get("class", [])


@pytest.mark.sphinx("html", testroot="cards")
def test_cards_items(app):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    items = soup.select("a.hx-cards__item")
    assert len(items) == 2
    assert items[0].get("href") == "quickstart.html"
    assert "Getting Started" in items[0].get_text()
