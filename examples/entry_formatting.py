#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of formatting entries for output in different ways."""

import bibpy
from bibpy.tools import get_abspath_for


if __name__ == '__main__':
    filename = get_abspath_for(__file__, '../tests/data/small1.bib')
    entries = [bibpy.read_file(filename, format='relaxed').entries[0]]

    print("* Default formatting")
    print(bibpy.write_string(entries, align=True, indent='    ', order=[],
                             surround='{}'))

    print()
    print("* Use a tab to indent")
    print(bibpy.write_string(entries, align=True, indent='\t', order=[],
                             surround='{}'))

    print()
    print("* Do not align '=' in entries and enclose field values in double "
          "quotes")
    print(bibpy.write_string(entries, align=False, indent='    ', order=[],
                             surround='""'))

    print()
    print("* Put title, author and year as the first fields (if possible)")
    print(bibpy.write_string(entries, align=True, indent='    ',
                             order=['title', 'author', 'year'],
                             surround='{}'))

    print()
    print("* Order fields alphabetically")
    print(bibpy.write_string(entries, align=True, indent='    ', order=True,
                             surround='{}'))
