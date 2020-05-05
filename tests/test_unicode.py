# -*- coding: utf-8 -*-

"""Test reading unicode characters."""

import bibpy
import bibpy.entry


def test_unicode_string():
    bibpy.read_string('@article{keåy, author = {荡 襡}, title = "â"}')


def test_unicode_file():
    bibpy.read_file('tests/data/unicode.bib')
