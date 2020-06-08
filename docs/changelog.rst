Changelog
=========

.. 'new' is for new, planned modifications
.. 'fix' is for bugfixes
.. 'feature' is for features added via pull requests
.. 'refactor' is for code refactors
.. 'docs' is for anything related to documentation
.. 'tests' is for anything related to tests
.. 'tools' is for anything related to bibpy's tools

.. raw:: html

    <style> .new      { color:#329932 } </style>
    <style> .fix      { color:#e50000 } </style>
    <style> .feature  { color:#a64ca6 } </style>
    <style> .refactor { color:#ffa500 } </style>
    <style> .docs     { color:#0376ee } </style>
    <style> .tests    { color:#49b6bf } </style>
    <style> .tools    { color:#c68278 } </style>

.. role:: new
.. role:: fix
.. role:: feature
.. role:: refactor
.. role:: docs
.. role:: tests
.. role:: tools

Version numbers follow `Semantic Versioning <https://semver.org/>`__ (i.e. <major>.<minor>.<patch>).

`1.0.0 <https://github.com/MisanthropicBit/bibpy/releases/tag/v1.0.0>`_
-----------------------------------------------------------------------

.. warning::

    Version 1.0.0 only supports Python 3.5+ and PyPy3.

- :new:`[new]` Port everything to Python 3.5+
- :new:`[new]` Changed license
- :new:`[new]` :docs:`[docs]` Add readthedocs documentation
- :refactor:`[refactor]` General code overhaul:
    - Added utf-8 encoding declarations to all files
    - Better formatting for more readable code
    - Eliminated duplicate code
    - Eliminated unused code
    - Eliminated unused imports
    - Eliminated some pytest warnings
    - Cleaned up lexer classes
    - Prefer single-quoted strings to double-quoted
    - Improved docstrings and added missing ones
- :feature:`[feature]` Added setter for values (and variable for @string) for
  @comment, @string and @preamble entries
- :tests:`[tests]` Extended some tests and completed missing ones
- :fix:`[fix]` Improved main bib lexer slightly by removing a call to the
  :py:func:`~bibpy.lexers.remove_whitespace_tokens` function since the lexer
  already removes whitespace in entries and combines whitespace as part of
  comments outside of entries
- :fix:`[fix]` Fixed minor errors:
    - Date fields follow ISO8601-2 Extended Format specification level 1 which
      does not allow for single digit numbers for days, i.e '2008-12-7' is not
      allowed but '2008-12-07' is
    - Preprocess pagetotal field
- :tools:`[tools]` Cleaned up tools and moved them from the top-level directory
  into bibpy/scripts to use setuptools' `entry_points
  <https://packaging.python.org/guides/distributing-packages-using-setuptools/?highlight=scripts#entry-points>`__
  feature and `improve portability
  <https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation>`__

`0.1.0-alpha <https://github.com/MisanthropicBit/bibpy/releases/tag/v0.1.0-alpha>`_
-----------------------------------------------------------------------------------

- :new:`[new]` Initial alpha version
