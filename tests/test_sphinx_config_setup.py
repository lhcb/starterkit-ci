from pathlib import Path

from starterkit_ci import sphinx_config


class DummyApp:
    def __init__(self, outdir):
        self.outdir = str(outdir)


def test_setup_registers_helpers_and_writes_redirect(monkeypatch, tmp_path):
    calls = []

    def fake_fix_markdown_configure_app(app):
        calls.append(("fix_markdown", app.outdir))

    def fake_panels_configure_app(app):
        calls.append(("panels", app.outdir))

    def extra_setup(app):
        calls.append(("extra", app.outdir))

    monkeypatch.setattr(
        sphinx_config.fix_markdown_file_downloads,
        "configure_app",
        fake_fix_markdown_configure_app,
    )
    monkeypatch.setattr(
        sphinx_config.panels,
        "configure_app",
        fake_panels_configure_app,
    )
    monkeypatch.setattr(
        sphinx_config,
        "starterkit_ci_redirects",
        {"old/page.html": "https://example.org/new/page.html"},
    )
    monkeypatch.setattr(sphinx_config.setup, "extra_setup_funcs", [extra_setup])

    app = DummyApp(tmp_path)
    sphinx_config.setup(app)

    assert calls == [
        ("fix_markdown", str(tmp_path)),
        ("panels", str(tmp_path)),
        ("extra", str(tmp_path)),
    ]

    redirect_path = Path(tmp_path) / "old" / "page.html"
    assert redirect_path.exists()
    content = redirect_path.read_text()
    assert "https://example.org/new/page.html" in content
    assert "refresh" in content
