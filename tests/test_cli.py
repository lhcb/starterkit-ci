import sys

import starterkit_ci


def test_parse_args_dispatches_to_command(monkeypatch):
    calls = []

    def fake_clean_docs(source_dir, allow_warnings=False):
        calls.append((source_dir, allow_warnings))

    monkeypatch.setattr(starterkit_ci, "clean_docs", fake_clean_docs)
    monkeypatch.setattr(
        sys,
        "argv",
        ["starterkit_ci", "clean", "--source-dir", "/tmp/docs", "--allow-warnings"],
    )

    starterkit_ci.parse_args()

    assert calls == [("/tmp/docs", True)]


def test_sphinx_build_adds_warnings_flag_by_default(monkeypatch):
    captured = {}

    def fake_check_call(cmd, cwd):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        return 0

    monkeypatch.setattr(starterkit_ci, "check_call", fake_check_call)

    starterkit_ci._sphinx_build("html", "/tmp/docs", allow_warnings=False)

    assert captured["cmd"] == ["sphinx-build", "-M", "html", ".", "build", "-W"]
    assert captured["cwd"] == "/tmp/docs"


def test_sphinx_build_allows_warnings_when_requested(monkeypatch):
    captured = {}

    def fake_check_call(cmd, cwd):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        return 0

    monkeypatch.setattr(starterkit_ci, "check_call", fake_check_call)

    starterkit_ci._sphinx_build("linkcheck", "/tmp/docs", allow_warnings=True)

    assert captured["cmd"] == ["sphinx-build", "-M", "linkcheck", ".", "build"]
    assert captured["cwd"] == "/tmp/docs"
