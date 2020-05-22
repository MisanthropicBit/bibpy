# -*- coding: utf-8 -*-

import bibpy
import pytest


def test_incorrect_format():
    with pytest.raises(KeyError):
        bibpy.read_string('', 'gibberish')
