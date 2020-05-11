#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of formatting bibliographic entries."""


import bibpy
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


if __name__ == '__main__':
    bibdata = get_path_for('../tests/data/small1.bib')
    entries = bibpy.read_file(bibdata, format='relaxed').entries
    entry = entries[0]

    print("Unaligned:")
    print(entry.format(align=False))

    print("Aligned:")
    print(entry.format(align=True))

    print("Aligned with 2 space indent:")
    print(entry.format(align=True, indent='  '))

    print("Aligned with double quotes surrounding values:")
    print(entry.format(align=True, surround='""'))

    print("Prefer year and title fields before remaining fields")
    print(entry.format(order=['year', 'title']))
