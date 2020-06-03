#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of expanding and unexpanding string variables in entry fields."""

import bibpy
from bibpy.tools import get_abspath_for
import os


def print_entries(entries):
    print(os.linesep.join(map(str, entries)))
    print()


if __name__ == '__main__':
    filename = get_abspath_for(__file__, '../tests/data/string_variables.bib')
    result = bibpy.read_file(filename, format='relaxed')
    entries, strings = result.entries, result.strings

    print("* String entries:")
    print_entries(strings)

    print("* Without string expansion:")
    print_entries(entries)

    # Expand string variables in-place
    bibpy.expand_strings(entries, strings, ignore_duplicates=False)

    print("* With string expansion:")
    print_entries(entries)

    # Unexpand string variables in-place
    bibpy.unexpand_strings(entries, strings, ignore_duplicates=False)

    print("* And without string expansion again:")
    print_entries(entries)
