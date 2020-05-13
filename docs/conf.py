# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'bibpy'
copyright = '2020, Alexander Asp Bock'
author = 'Alexander Asp Bock'
master_doc = 'index'

# The full version, including alpha/beta/rc tags
release = '0.1.0-alpha'

# -- General configuration ---------------------------------------------------

html_static_path = ['images']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    'description':     'Python library for reading, writing and manipulating '
                       'Bib(la)tex data',
    'github_user':     'MisanthropicBit',
    'github_repo':     'bibpy',
    'github_banner':   'true',
    'github_button':   'true',
    'extra_nav_links': {
        'Issues':        'https://github.com/MisanthropicBit/bibpy/issues',
        'Pull Requests': 'https://github.com/MisanthropicBit/bibpy/pulls',
    },
}

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}
