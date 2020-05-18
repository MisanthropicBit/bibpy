**bibpy**
=========

.. image:: https://img.shields.io/pypi/v/bibpy
   :alt: PyPI
   :target: https://pypi.org/project/bibpy/

.. image:: https://travis-ci.org/MisanthropicBit/bibpy.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/github/MisanthropicBit/bibpy

.. image:: https://img.shields.io/readthedocs/bibpy
   :alt: Docs build status
   :target: https://readthedocs.org/projects/bibpy/

.. image:: https://coveralls.io/repos/github/MisanthropicBit/bibpy/badge.svg?branch=master
   :alt: Coverage percentage
   :target: https://coveralls.io/github/MisanthropicBit/bibpy?branch=master

.. image:: https://img.shields.io/github/license/MisanthropicBit/bibpy.svg
   :alt: License
   :target: https://github.com/MisanthropicBit/bibpy/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/bibpy.svg
   :alt: Python Versions
   :target: https://pypi.org/project/bibpy/

.. image:: https://img.shields.io/pypi/wheel/bibpy
   :alt: Wheel support

.. toctree::
   :maxdepth: 2
   :hidden:

   tutorial
   faq
   changelog

bibpy allows you to parse bib(la)tex files and easily manipulate bibliographic
entries.

Install with pip:

.. code:: bash

    pip install bibpy

Simple usage:

.. code:: python

    >>> import bibpy
    >>> result = bibpy.read_file('references.bib', 'relaxed')
    >>> entries = result.entries
    >>> entries[0].bibkey
    'key4'
    >>> entries[0].bibtype
    'article'
    >>> entries[0].author
    'Archer Sterling'
    >>> entries[0].title
    'A Practical Guide To Getting Ants'

View the `tutorial <tutorial.html>`__ for a more comprehensive guide.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
