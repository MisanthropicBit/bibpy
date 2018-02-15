#!/usr/bin/env python

import bibpy
import pytest


def test_incorrect_format():
    with pytest.raises(KeyError):
        bibpy.read_string('', 'gibberish')

    # with pytest.raises(ValueError):
    #     bibpy.read_string('@article{key,author={temp}}', 'biblatex',
    #                       postprocess='string')
