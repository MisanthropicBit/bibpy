"""Example of expanding and unexpanding string variables in entry fields."""

from __future__ import print_function

import bibpy
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


def print_entries(entries):
    print(os.linesep.join(map(str, entries)))
    print()


if __name__ == '__main__':
    filename = get_path_for('../tests/data/string_variables.bib')
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
