"""Test getting entries from a doi."""

import bibpy
import bibpy.doi
import os
import pytest
import vcr

not_on_travis = pytest.mark.skipif(os.environ.get('TRAVIS') is not None,
                                   reason='Do not test web requests on Travis')


@not_on_travis
def test_doi():
    with vcr.use_cassette('fixtures/vcr_cassettes/doi.yaml'):
        doi = '10.1145/1015530.1015557'
        entry = bibpy.doi.retrieve(doi)

        assert len(entry.fields) == 11
        assert entry.bibtype == 'article'
        assert entry.bibkey == 'Hancock_2004'
        assert entry.author == 'Jeffrey T. Hancock'
        assert entry.title == '{LOL}'
        assert entry.journal == 'interactions'
        assert entry.volume == '11'
        assert entry.number == '5'
        assert entry.month == 'sep'
        assert entry.year == '2004'
        assert entry.pages == '57'
        assert entry.url == 'https://doi.org/10.1145%2F1015530.1015557'
        assert entry.publisher == 'Association for Computing Machinery ({ACM})'
        assert entry.doi == doi


@not_on_travis
def test_doi_postprocess():
    with vcr.use_cassette('fixtures/vcr_cassettes/doi.yaml'):
        doi = '10.1145/1015530.1015557'
        entry = bibpy.doi.retrieve(doi, postprocess=True)

        assert len(entry.fields) == 11
        assert entry.bibtype == 'article'
        assert entry.bibkey == 'Hancock_2004'
        assert entry.author == ['Jeffrey T. Hancock']
        assert entry.title == '{LOL}'
        assert entry.journal == 'interactions'
        assert entry.volume == 11
        assert entry.number == 5
        assert entry.month == 'September'
        assert entry.year == 2004
        assert entry.pages == '57'
        assert entry.url == 'https://doi.org/10.1145%2F1015530.1015557'
        assert entry.publisher ==\
            ['Association for Computing Machinery ({ACM})']
        assert entry.doi == doi


@not_on_travis
def test_doi_raw():
    with vcr.use_cassette('fixtures/vcr_cassettes/doi.yaml'):
        doi = '10.1145/1015530.1015557'
        entry = bibpy.doi.retrieve(doi, raw=True)

        assert entry == b"""@article{Hancock_2004,
\tdoi = {10.1145/1015530.1015557},
\turl = {https://doi.org/10.1145%2F1015530.1015557},
\tyear = 2004,
\tmonth = {sep},
\tpublisher = {Association for Computing Machinery ({ACM})},
\tvolume = {11},
\tnumber = {5},
\tpages = {57},
\tauthor = {Jeffrey T. Hancock},
\ttitle = {{LOL}},
\tjournal = {interactions}
}"""
