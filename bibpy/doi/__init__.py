# -*- coding: utf-8 -*-

"""Tools for downloading bibtex files from digital object identifiers."""

import bibpy

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen


def download(doi, source='http://dx.doi.org/{0}', raw=False):
    """Download a bibtex file specified by a digital object identifier.

    The source is a URL containing a single format specifier which is where the
    requested doi should appear.

    By default, the bibtex string from the doi is parsed by bibpy. Specify
    raw=True to get the raw bibtex string instead.

    """
    req = Request(source.format(doi))
    req.add_header('accept', 'application/x-bibtex')

    try:
        handle = urlopen(req)
        contents = handle.read()

        return contents if raw else bibpy.read_string(contents).entries[0]
    finally:
        handle.close()
