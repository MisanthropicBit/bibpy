#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of postprocessing fields."""

import bibpy
from bibpy.tools import get_abspath_for


def print_entry_fields(entries):
    for entry in entries:
        for field, value in entry:
            print("    {0} = {1} ({2})".format(field, value, type(value)))

        print()


if __name__ == '__main__':
    testfile_path = get_abspath_for(
        __file__,
        '../tests/data/field_processing.bib'
    )

    entries = bibpy.read_file(testfile_path, format='relaxed').entries

    print("Before postprocessing:")
    print_entry_fields(entries)

    entries = bibpy.read_file(
        testfile_path,
        format='relaxed',
        postprocess=True
    ).entries

    print("After postprocessing:")
    print_entry_fields(entries)

    # We can also choose to postprocess only a subset of fields
    print("Postprocess a subset of fields ('xdata' and 'month'):")
    entries = bibpy.read_file(
        testfile_path,
        format='relaxed',
        postprocess=['xdata', 'month']
    ).entries

    print_entry_fields(entries)
