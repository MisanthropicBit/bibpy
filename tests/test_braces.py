"""Test that extra braces in fields are handled properly."""

import bibpy


def test_braces():
    entries, _, _, _, _ = bibpy.read_file('tests/data/braces.bib', 'relaxed')

    assert len(entries) == 3
    assert entries[0].editor == 'value'
    assert entries[1].editor == '{THIS IS ALL UPPERCASE}'
    assert entries[2].editor == 'Communications {and} Data'

    entries, _, _, _, _ = bibpy.read_file('tests/data/braces.bib', 'relaxed',
                                          postprocess=True)

    assert len(entries) == 3
    assert entries[0].editor == ['value']
    assert entries[1].editor == ['THIS IS ALL UPPERCASE']
    assert entries[2].editor == ['Communications and Data']
