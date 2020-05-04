bibpy
=====

.. image:: https://travis-ci.org/MisanthropicBit/bibpy.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/MisanthropicBit/bibpy

.. image:: https://img.shields.io/github/license/MisanthropicBit/bibpy.svg
   :alt: License
   :target: https://img.shields.io/github/license/MisanthropicBit/bibpy.svg

.. image:: https://img.shields.io/pypi/pyversions/bibpy.svg
   :alt: Python Versions
   :target: https://pypi.python.org/pypi/bibpy/

.. image:: https://img.shields.io/pypi/wheel/bibpy
   :alt: Wheel support
   :target: https://img.shields.io/pypi/wheel/bibpy

.. toctree::
   :maxdepth: 2
   :hidden:

   tutorial
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
