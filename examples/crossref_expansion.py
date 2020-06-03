#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of expanding and unexpanding crossreferences."""

import bibpy
from bibpy.tools import get_abspath_for
import os


def print_entries(entries):
    print(os.linesep.join(map(str, entries)))
    print()


if __name__ == '__main__':
    # Load just the entries of the file
    entries = bibpy.read_file(
        get_abspath_for(__file__, '../tests/data/crossreferences.bib'),
        format='relaxed'
    ).entries

    print("Before inheriting crossreferences")
    print_entries(entries)

    # Inherit crossreferences in-place
    bibpy.inherit_crossrefs(entries, inherit=True, override=False,
                            exceptions={})

    print("After inheriting crossreferences")
    print_entries(entries)

    # Uninherit crossreferences again
    bibpy.uninherit_crossrefs(entries, inherit=True, override=False,
                              exceptions={})

    # The entries should now be the same as before they inherited
    # crossreferences
    print("After uninheriting crossreferences")
    print_entries(entries)
