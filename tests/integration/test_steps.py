from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="steps")
def test_steps_structure(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    container = soup.select_one("ol.hx-steps")
    assert container is not None
    items = container.select("li.hx-steps__item")
    assert len(items) == 2
    titles = [i.select_one(".hx-steps__title").get_text() for i in items]
    assert titles == ["Install", "Run"]
