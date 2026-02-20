__all__ = [
    "configure_app",
    "FixMarkdownDownloads",
]

from os.path import isfile, join, dirname

from docutils import nodes
from sphinx.addnodes import download_reference, pending_xref
from sphinx.transforms import SphinxTransform


def configure_app(app):
    app.add_transform(FixMarkdownDownloads)


class FixMarkdownDownloads(SphinxTransform):
    default_priority = 5

    def apply(self, **kwargs):
        for old_node in list(self.document.findall(pending_xref)):
            source = getattr(old_node, "source", None)
            reftarget = old_node.get("reftarget")
            if not source or not reftarget:
                continue
            if not old_node.children or not old_node.children[0].children:
                continue
            if not isfile(join(dirname(source), reftarget)):
                continue
            node1 = nodes.literal(
                "", "", *old_node.children[0].children, classes=["xref", "download"]
            )
            old_node.replace(old_node.children[0], node1)
            new_node = download_reference(
                old_node.rawsource, "", *old_node.children, **old_node.attributes
            )
            old_node.parent.replace(old_node, new_node)
