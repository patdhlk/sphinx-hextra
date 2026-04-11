from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="tabs")
def test_tabs_structure(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    container = soup.select_one("div.hx-tabs")
    assert container is not None
    labels = [b.get_text().strip() for b in container.select("button.hx-tabs__label")]
    assert labels == ["macOS", "Linux", "Windows"]
    panels = container.select("div.hx-tabs__panel")
    assert len(panels) == 3
    assert "Apple" in panels[0].get_text()
