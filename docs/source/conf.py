# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2] / 'src'))

project = 'LIFT Utils'
copyright = '2024, Nate Marti'
author = 'Nate Marti'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'autoapi.extension',
]
autoapi_dirs = ['../../src/lift_utils']
autoapi_options = [
    'members',
    'undoc-members',
    # 'private-members',
    'show-inheritance',
    'show-module-summary',
    # 'special-members',
    'imported-members',
]
autoapi_own_page_level = 'class'
autoapi_member_order = 'groupwise'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'  # default
html_theme = 'haiku'
html_static_path = ['_static']
