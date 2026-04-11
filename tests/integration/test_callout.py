from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="callout")
def test_callout_renders(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    el = soup.select_one("div.hx-callout.hx-callout--warning")
    assert el is not None
    assert "This is a warning" in el.get_text()


@pytest.mark.sphinx("html", testroot="callout")
def test_callout_default_type_is_info(app, tmp_path):
    (app.srcdir / "index.md").write_text(
        "# Test\n\n```{hextra-callout}\nPlain note.\n```\n"
    )
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    assert soup.select_one("div.hx-callout.hx-callout--info") is not None
