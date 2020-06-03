#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of importing and exporting to and from various formats.

Loads a bibtexml file and prints out the data converted to json.

"""

import bibpy
import bibpy.formats
from bibpy.tools import get_abspath_for
import os


def print_entries(entries):
    print(os.linesep.join(map(str, entries)))
    print()


if __name__ == '__main__':
    # Load just the entries of the file
    path = get_abspath_for(__file__, '../tests/data/crossreferences.bib')
    entries = bibpy.formats.read_xml_file(path, format='relaxed').entries

    print_entries(bibpy.formats.write_json(entries))
