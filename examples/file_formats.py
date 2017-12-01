"""Example of importing and exporting to and from various formats.

Loads a bibtexml file and prints out the data converted to json.

"""

from __future__ import print_function

import bibpy
import bibpy.formats
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


def print_entries(entries):
    print(os.linesep.join(map(str, entries)))
    print()


if __name__ == '__main__':
    # Load just the entries of the file
    path = get_path_for('../tests/data/crossreferences.bib')
    entries = bibpy.formats.read_xml_file(path, format='relaxed').entries

    print_entries(bibpy.formats.write_json(entries))
