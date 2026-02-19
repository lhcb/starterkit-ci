import os
from os.path import dirname, join

from . import fix_markdown_file_downloads, panels

extensions = [
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinx.ext.mathjax",
    "nbsphinx",
]


templates_path = [
    "_templates",
]


html_theme = "sphinx_rtd_theme"
html_show_sourcelink = True
html_theme_options = {
    "collapse_navigation": False,
}


exclude_patterns = [
    "**.ipynb_checkpoints",
]


html_context = {
    "display_github": True,
    "github_user": "lhcb",
    "github_repo": "starterkit-lessons",
    "github_version": "master",
    "conf_py_path": "/source/",
}


highlight_language = "none"


html_static_path = [
    f"{dirname(__file__)}/_static",
]


linkcheck_ignore = [
    # Certificate verification fails (CERTIFICATE_VERIFY_FAILED)
    r"https://lhcb-portal-dirac\.cern\.ch/DIRAC/",
    r"https://lhcb-nightlies\.cern\.ch.*",
    # Returns 404 for /merge_requests/new URLs
    r"https://gitlab\.cern\.ch/.*/merge_requests/new",
    # GitLab line anchors are not in the HTML source
    r"https://gitlab\.cern\.ch/.*/blob/.+#L\d+",
    # PDG Live returns 500s to linkcheck requests
    r"https?://pdg.*\.lbl\.gov/.*",
]


linkcheck_workers = 8
linkcheck_timeout = 60
linkcheck_retries = 2


starterkit_ci_redirects = {}


source_suffix = {
    ".md": "markdown",
}


myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "linkify",
    "substitution",
]


def setup(app):
    fix_markdown_file_downloads.configure_app(app)
    panels.configure_app(app)
    for extra_setup_func in setup.extra_setup_funcs:
        extra_setup_func(app)

    # Create redirects
    for origin, target in starterkit_ci_redirects.items():
        origin = join(app.outdir, origin)
        print("Creating redirect from", origin, "to", target)
        os.makedirs(dirname(origin), exist_ok=True)
        with open(origin, "wt") as fp:
            fp.write(f'<meta http-equiv="refresh" content="0; url={target}">\n')
            fp.write(f'<link rel="canonical" href="{target}" />\n')


# Allow additional setup functions to be defined in projects
setup.extra_setup_funcs = []
