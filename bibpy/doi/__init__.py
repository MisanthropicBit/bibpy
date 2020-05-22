# -*- coding: utf-8 -*-

"""Tools for downloading bibtex files from digital object identifiers."""

import bibpy
from urllib.request import Request, urlopen


def retrieve(doi, source='https://doi.org/{0}', raw=False, **options):
    """Download a bibtex file specified by a digital object identifier.

    The source is a URL containing a single positional format specifier which
    is where the requested doi should appear.

    By default, the data from the doi is parsed by bibpy. If raw is True, the
    raw string is returned instead.

    The options kwargs correspond to the arguments normally passed to
    :py:func:`bibpy.read_string`.

    """
    req = Request(source.format(doi))
    req.add_header('accept', 'application/x-bibtex')
    handle = None

    try:
        handle = urlopen(req)
        contents = handle.read()

        if raw:
            return contents
        else:
            return bibpy.read_string(
                contents.decode('utf-8'),
                **options
            ).entries[0]
    finally:
        if handle:
            handle.close()
