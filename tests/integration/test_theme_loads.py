import pytest


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_theme_builds_without_errors(app, status, warning):
    app.build()
    assert not warning.getvalue(), warning.getvalue()
    assert (app.outdir / "index.html").exists()


@pytest.mark.sphinx("html", testroot="theme-loads")
def test_theme_css_is_copied(app):
    app.build()
    assert (app.outdir / "_static" / "sphinx-hextra.css").exists()
