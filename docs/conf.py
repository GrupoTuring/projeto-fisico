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
import os
import sys
from typing import List
from sphinx.application import Sphinx
from sphinx.ext import autodoc

sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(1, os.path.abspath('.'))


autodoc_type_aliases = {
    'Value': 'car_env.config_side_channel.ConfigSideChannel.Value',
}
autodoc_typehints_format = 'short'


# -- Project information -----------------------------------------------------

project = 'Projeto Fisico'
copyright = '2021, Turing USP'
author = 'Turing USP'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'pt_BR'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Handlers ----------------------------------------------------------------

def remove_duplicate_members(app: 'Sphinx', what: str, name: str, obj: object,
                             options: autodoc.Options, lines: List[str]):
    """Avoid duplicated documentation when using autodoc with ``undoc-members``.

    Autodoc's ``undoc-members`` option causes documentation to be generated for all
    (public) attributes which do not have a docstring. This includes attributes
    which are documented only in the enclosing class' docstring (and therefore do not have
    a docstring of their own). In this case, each attribute will be documented twice:
    once from the class' docstring and once from the ``undoc-members`` option.

    This function avoids this duplication by preventing the ``undoc-members``
    option from generating documentation for attributes which have already
    been documented in the enclosing class' docstring.

    See also:
        Autodoc's documentation of the ``autodoc-process-docstring`` event
        for a description of this function's arguments.
    """
    if what != 'class' or not options.undoc_members:
        # We only care about class docstrings, and the duplication only happens when
        # the option ``undoc-members`` is active.
        return

    for line in lines:
        # The docstring is always converted to .rst format by napoleon,
        # so any class attributes are documented as ".. attribute:: ATTRIBUTE_NAME"
        prefix = '.. attribute:: '
        if line.startswith(prefix):
            attr = line[len(prefix):]
            try:
                # If the current line documents an attribute,
                # remove the corresponding attribute from obj.__annotations__.
                # This is enough to prevent autodoc from documenting this attribute.
                del obj.__annotations__[attr]
            except KeyError:
                pass


def setup(app: 'Sphinx'):
    app.connect('autodoc-process-docstring', remove_duplicate_members)
