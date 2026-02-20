from pathlib import Path

import pytest
from docutils import nodes
from docutils.utils import new_document
from sphinx.addnodes import download_reference, pending_xref

from starterkit_ci.sphinx_config.fix_markdown_file_downloads import FixMarkdownDownloads
from starterkit_ci.sphinx_config.panels import AddPanels


def test_fix_markdown_downloads_rewrites_existing_local_targets(tmp_path):
    source_path = tmp_path / "page.md"
    source_path.write_text("content")
    (tmp_path / "slides.pdf").write_text("pdf")

    doc = new_document(str(source_path))
    para = nodes.paragraph()

    xref = pending_xref("", reftarget="slides.pdf")
    xref.source = str(source_path)
    xref += nodes.reference("", "", nodes.literal("", "slides.pdf"))
    para += xref
    doc += para

    FixMarkdownDownloads(doc).apply()

    replaced = para[0]
    assert isinstance(replaced, download_reference)
    literal = replaced[0]
    assert isinstance(literal, nodes.literal)
    assert "download" in literal["classes"]
    assert "xref" in literal["classes"]


def test_add_panels_turns_block_markup_into_panel_container():
    doc = new_document("index.md")

    start = nodes.paragraph()
    start.rawsource = '{% callout "Important Title" %}'
    start.source = "index.md"

    body = nodes.paragraph("", "Body text")
    body.rawsource = "Body text"

    end = nodes.paragraph()
    end.rawsource = "{% endcallout %}"

    doc += start
    doc += body
    doc += end

    AddPanels(doc).apply()

    assert len(doc.children) == 1
    panel = doc[0]
    assert isinstance(panel, nodes.container)
    assert "panel" in panel["classes"]
    assert "panel-callout" in panel["classes"]

    header = panel[0]
    body_container = panel[1]
    assert "panel-header" in header["classes"]
    assert "open" in header["classes"]
    assert "panel-body" in body_container["classes"]
    assert body_container[0].astext() == "Body text"


def test_add_panels_raises_for_unknown_panel_type():
    doc = new_document("index.md")

    start = nodes.paragraph()
    start.rawsource = '{% unknown "Title" %}'
    start.source = "index.md"
    doc += start

    with pytest.raises(ValueError, match="Unrecognised panel type"):
        AddPanels(doc).apply()


def test_fix_markdown_downloads_skips_nodes_without_children(tmp_path):
    source_path = tmp_path / "page.md"
    source_path.write_text("content")
    (tmp_path / "slides.pdf").write_text("pdf")

    doc = new_document(str(source_path))
    para = nodes.paragraph()
    xref = pending_xref("", reftarget="slides.pdf")
    xref.source = str(source_path)
    para += xref
    doc += para

    FixMarkdownDownloads(doc).apply()

    assert para[0] is xref
