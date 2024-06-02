# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the
# documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from typing import List

project = "{{ project_name }}"
copyright = "2024, {{ project_author_name }}"
author = "{{ project_author_name }}"
release = "v0.0.0"

# -- General configuration ------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html

extensions: List[str] = []

templates_path: List[str] = ["_templates"]
exclude_patterns: List[str] = []

language = "en"

# -- Options for HTML output ----------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html

html_theme = "alabaster"
html_static_path = ["_static"]
