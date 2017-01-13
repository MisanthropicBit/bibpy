"""Test bibpy.entry.base."""

import bibpy
import bibpy.entry
import pytest


def test_base_entry():
    be = bibpy.entry.BaseEntry()

    with pytest.raises(NotImplementedError):
        be.format()

    with pytest.raises(NotImplementedError):
        be.entry_type()

    with pytest.raises(NotImplementedError):
        be.entry_key()

    with pytest.raises(NotImplementedError):
        be.fields()

    with pytest.raises(NotImplementedError):
        be.aliases('bibtex')

    with pytest.raises(NotImplementedError):
        be.valid('bibtex')

    with pytest.raises(NotImplementedError):
        be.keys()

    with pytest.raises(NotImplementedError):
        be.values()

    with pytest.raises(NotImplementedError):
        be == be

    with pytest.raises(NotImplementedError):
        be != be

    with pytest.raises(NotImplementedError):
        'lol' in be

    with pytest.raises(NotImplementedError):
        len(be)

    with pytest.raises(NotImplementedError):
        repr(be)

    with pytest.raises(NotImplementedError):
        be.__getitem__('key')

    with pytest.raises(NotImplementedError):
        be.__str__()
