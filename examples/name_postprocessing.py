#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of name splitting specific fields and filtering entries."""

import bibpy
from bibpy.tools import get_abspath_for


if __name__ == '__main__':
    # Load just the entries of the file and split names only for 'author'
    # fields
    entries = bibpy.read_file(
        get_abspath_for(__file__, '../tests/data/graphs.bib'),
        postprocess=True,
        split_names=True
    ).entries

    # Print the key of each entry that has an author whose last name is
    # 'Fujisawa' (2: KashiwabaraF79 and OhtsukiMKF81)
    for entry in entries:
        if entry.author:
            if any(name.last == 'Fujisawa' for name in entry.author if name):
                print(entry.bibkey)
