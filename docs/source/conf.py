# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys
from pathlib import Path
from shutil import copyfile

# Anchor every path to this file rather than to the working directory, so that
# the documentation builds from any invocation directory (repository root, docs/,
# or the directory Sphinx was started in by a hosting service).
docs_dir = Path(__file__).resolve().parent
repo_dir = docs_dir.parent.parent

sys.path.insert(0, str(repo_dir))

copyfile(repo_dir / "README.md", docs_dir / "readme.md")
copyfile(repo_dir / "CHANGELOG.md", docs_dir / "CHANGELOG.md")
copyfile(repo_dir / "CONTRIBUTING.md", docs_dir / "CONTRIBUTING.md")

# -- Project information -----------------------------------------------------

project = "MSMetaEnhancer"
copyright = "2026, RECETOX"
author = "RECETOX"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "myst_parser"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
