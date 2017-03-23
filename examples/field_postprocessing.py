"""Example of postprocessing fields."""

from __future__ import print_function

import bibpy
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


def print_entries(entries):
    for entry in entries:
        for field, value in entry:
            print("    {0} = {1} ({2})".format(field, value, type(value)))

        print()

if __name__ == '__main__':
    entries =\
        bibpy.read_file(get_path_for('../tests/data/field_processing.bib'),
                        format='relaxed').entries

    print("Before postprocessing:")
    print_entries(entries)

    entries =\
        bibpy.read_file(get_path_for('../tests/data/field_processing.bib'),
                        format='relaxed', postprocess=True).entries

    print("After postprocessing:")
    print_entries(entries)

    # We can also choose to postprocess only a subset of fields
    print("Postprocess a subset of fields ('xdata' and 'month'):")
    entries =\
        bibpy.read_file(get_path_for('../tests/data/field_processing.bib'),
                        format='relaxed',
                        postprocess=['xdata', 'month']).entries
    print_entries(entries)
