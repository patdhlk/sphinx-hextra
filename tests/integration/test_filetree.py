from bs4 import BeautifulSoup
import pytest


@pytest.mark.sphinx("html", testroot="filetree")
def test_filetree_structure(app, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "lxml")
    root = soup.select_one("ul.hx-filetree")
    assert root is not None
    folders = root.select("li.hx-filetree__folder")
    files = root.select("li.hx-filetree__file")
    folder_names = {f.select_one(".hx-filetree__name").get_text() for f in folders}
    file_names = {f.select_one(".hx-filetree__name").get_text() for f in files}
    assert folder_names == {"content/", "docs/"}
    assert file_names == {"_index.md", "intro.md", "conf.py"}
