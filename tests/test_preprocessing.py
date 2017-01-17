"""Test field preprocessing."""

import bibpy.preprocess
import calendar
import pytest


def test_preprocess_namelist():
    assert bibpy.preprocess.preprocess_namelist(['A. B. Cidric',
                                                 'D. E. Fraser']) ==\
        'A. B. Cidric and D. E. Fraser'

    assert bibpy.preprocess.preprocess_namelist('string') == 'string'
    t = tuple()
    assert bibpy.preprocess.preprocess_namelist(t) is t


def test_preprocess_keywords():
    assert bibpy.preprocess.preprocess_keywords(['java', 'c++',
                                                 'haskell', 'python']) ==\
        'java;c++;haskell;python'

    assert bibpy.preprocess.preprocess_keywords('string') == 'string'
    t = tuple()
    assert bibpy.preprocess.preprocess_keywords(t) is t


def test_preprocess_date():
    d = bibpy.date.DateRange.fromstring('1998-05-02')
    assert bibpy.preprocess.preprocess_date(d) == '1998-05-02'


def test_preprocess_month():
    for func in [str.capitalize, str.lower, str.upper]:
        for i, m in enumerate(list(calendar.month_name)[1:]):
            assert bibpy.preprocess.preprocess_month(func(m)) == i + 1

    for m in ['gibberish', 'not_a_month', 'fail']:
        assert bibpy.preprocess.preprocess_month(m) == m


@pytest.mark.randomize(i=int, ncalls=100)
def test_preproces_int(i):
    assert bibpy.preprocess.preprocess_int(i) == str(i)


# @pytest.mark.skip
def test_preprocess():
    entry = bibpy.read_file('tests/data/preprocess.bib', 'relaxed')[0][0]

    expected = {
        'address': 'Arthur Cunnings and Michelle Toulouse',
        'afterword': 'Arthur Cunnings and Michelle Toulouse',
        'author': 'Arthur Cunnings and Michelle Toulouse',
        'bookauthor': 'Arthur Cunnings and Michelle Toulouse',
        'chapter': '97',
        'commentator': 'Arthur Cunnings and Michelle Toulouse',
        'date': '1999-03-21',
        'editor': 'Arthur Cunnings and Michelle Toulouse',
        'editora': 'Arthur Cunnings and Michelle Toulouse',
        'editorb': 'Arthur Cunnings and Michelle Toulouse',
        'editorc': 'Arthur Cunnings and Michelle Toulouse',
        'edition': '2',
        'eventdate': '2008-12-7/',
        'foreword': 'Arthur Cunnings and Michelle Toulouse',
        'holder': 'Arthur Cunnings and Michelle Toulouse',
        'institution': 'Arthur Cunnings and Michelle Toulouse',
        'introduction': 'Arthur Cunnings and Michelle Toulouse',
        'keywords': 'information;data;communications',
        'location': 'Arthur Cunnings and Michelle Toulouse',
        'language': 'Arthur Cunnings and Michelle Toulouse',
        'month': '10',
        'number': '28',
        'organization': 'Arthur Cunnings and Michelle Toulouse',
        'origdate': '2016-10-19',
        'origlocation': 'Arthur Cunnings and Michelle Toulouse',
        'origpublisher': 'Arthur Cunnings and Michelle Toulouse',
        'part': '24',
        'publisher': 'Arthur Cunnings and Michelle Toulouse',
        'related': 'key1, key2, key3',
        'school': 'Arthur Cunnings and Michelle Toulouse',
        'series': '23',
        'shortauthor': 'Arthur Cunnings and Michelle Toulouse',
        'shorteditor': 'Arthur Cunnings and Michelle Toulouse',
        'translator': 'Arthur Cunnings and Michelle Toulouse',
        'organization': 'Arthur Cunnings and Michelle Toulouse',
        'urldate': '2016-10-19/2016-10-27',
        'xdata': ',    key1, key2, key3,   ',
        'volume': '83',
        'year': '2016'
    }

    # Ensure that there are no duplicates
    assert len(expected.keys()) == len(set(expected.keys()))
    assert len(bibpy.preprocess.preprocess_functions.keys()) ==\
        len(set(bibpy.preprocess.preprocess_functions.keys()))

    assert set(expected.keys()) ==\
        set(bibpy.preprocess.preprocess_functions.keys())

    for field, value in bibpy.preprocess.preprocess(entry, expected.keys()):
        assert value == expected.get(field, value)


def test_no_postprocess():
    entry = bibpy.entry.Entry('techreport', 'ula22',
                              **{'random_field': 23,
                                 'nopreprocess': "OK!, OK!, OK!"})

    preprocessed = bibpy.preprocess.preprocess(entry, ['random_field',
                                                       'nopreprocess'])

    assert next(preprocessed) == ('random_field', 23)
    assert next(preprocessed) == ('nopreprocess', "OK!, OK!, OK!")
