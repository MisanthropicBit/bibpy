# -*- coding: utf-8 -*-

"""Test field preprocessing."""

import bibpy
from bibpy.preprocess import preprocess,\
    preprocess_namelist,\
    preprocess_keywords,\
    preprocess_int,\
    preprocess_date,\
    preprocess_month,\
    preprocess_keylist,\
    preprocess_pages,\
    preprocess_functions
import calendar
import pytest


def test_preprocess_namelist():
    assert preprocess_namelist(['A. B. Cidric', 'D. E. Fraser']) ==\
        'A. B. Cidric and D. E. Fraser'

    assert preprocess_namelist('string') == 'string'
    t = tuple()
    assert preprocess_namelist(t) is t

    assert preprocess_namelist([
        bibpy.name.Name(first='A. B.', last='Cidric'),
        bibpy.name.Name(first='D. E.', last='Fraser')
    ]) == 'A. B. Cidric and D. E. Fraser'

    assert preprocess_namelist([
        bibpy.name.Name(first='A. B.', last='Cidric'),
        bibpy.name.Name(first='D. E.', last='Fraser')
    ], name_style='last-first') == 'Cidric, A. B. and Fraser, D. E.'


def test_preprocess_keywords():
    assert preprocess_keywords(['java', 'c++', 'haskell', 'python']) ==\
        'java;c++;haskell;python'

    assert preprocess_keywords('string') == 'string'
    t = tuple()
    assert preprocess_keywords(t) is t


def test_preprocess_date():
    d = bibpy.date.DateRange.fromstring('1998-05-02')
    assert preprocess_date(d) == '1998-05-02'


def test_preprocess_month():
    for func in [str.capitalize, str.lower, str.upper]:
        for i, m in enumerate(list(calendar.month_name)[1:]):
            assert preprocess_month(func(m)) == i + 1

    for m in ['gibberish', 'not_a_month', 'fail']:
        assert preprocess_month(m) == m


def test_preproces_int():
    assert preprocess_int(20) == '20'
    assert preprocess_int('abc') == 'abc'


def test_keylist():
    keylist = ['key1', 'key2', 'key3']

    assert preprocess_keylist(keylist) == 'key1, key2, key3'
    assert preprocess_keylist("abc") == "abc"


def test_pages():
    assert preprocess_pages((1, 200)) == '1--200'
    assert preprocess_pages((1, 200)) == '1--200'
    assert preprocess_pages('1/200') == '1/200'
    assert preprocess_pages('--200') == '--200'
    assert preprocess_pages('1--') == '1--'


def test_preprocess():
    entry = bibpy.read_file('tests/data/preprocess.bib', 'relaxed').entries[0]

    expected = {
        'address':       'Arthur Cunnings and Michelle Toulouse',
        'afterword':     'Arthur Cunnings and Michelle Toulouse',
        'author':        'Arthur Cunnings and Michelle Toulouse',
        'bookauthor':    'Arthur Cunnings and Michelle Toulouse',
        'chapter':       '97',
        'commentator':   'Arthur Cunnings and Michelle Toulouse',
        'date':          '1999-03-21',
        'editor':        'Arthur Cunnings and Michelle Toulouse',
        'editora':       'Arthur Cunnings and Michelle Toulouse',
        'editorb':       'Arthur Cunnings and Michelle Toulouse',
        'editorc':       'Arthur Cunnings and Michelle Toulouse',
        'edition':       '2',
        'eventdate':     '2008-12-07/',
        'foreword':      'Arthur Cunnings and Michelle Toulouse',
        'holder':        'Arthur Cunnings and Michelle Toulouse',
        'institution':   'Arthur Cunnings and Michelle Toulouse',
        'introduction':  'Arthur Cunnings and Michelle Toulouse',
        'keywords':      'information;data;communications',
        'location':      'Arthur Cunnings and Michelle Toulouse',
        'language':      'Arthur Cunnings and Michelle Toulouse',
        'month':         '10',
        'number':        '28',
        'organization':  'Arthur Cunnings and Michelle Toulouse',
        'origdate':      '2016-10-19',
        'origlocation':  'Arthur Cunnings and Michelle Toulouse',
        'origpublisher': 'Arthur Cunnings and Michelle Toulouse',
        'pages':         '11-20',
        'pagetotal':     '205',
        'part':          '24',
        'publisher':     'Arthur Cunnings and Michelle Toulouse',
        'related':       'key1, key2, key3',
        'school':        'Arthur Cunnings and Michelle Toulouse',
        'series':        '23',
        'shortauthor':   'Arthur Cunnings and Michelle Toulouse',
        'shorteditor':   'Arthur Cunnings and Michelle Toulouse',
        'translator':    'Arthur Cunnings and Michelle Toulouse',
        'organization':  'Arthur Cunnings and Michelle Toulouse',
        'urldate':       '2016-10-19/2016-10-27',
        'xdata':         ',    key1, key2, key3,   ',
        'volume':        '83',
        'year':          '2016',
    }

    # Ensure that there are no duplicates
    assert len(expected.keys()) == len(set(expected.keys()))
    assert len(preprocess_functions.keys()) ==\
        len(set(preprocess_functions.keys()))

    assert set(expected.keys()) == set(preprocess_functions.keys())

    for field, value in preprocess(entry, expected.keys()):
        assert value == expected.get(field, value)


def test_no_postprocess():
    entry = bibpy.entry.Entry(
        'techreport',
        'ula22',
        **{
            'random_field': 23,
            'nopreprocess': "OK!, OK!, OK!"
        },
    )

    preprocessed = preprocess(entry, ['random_field', 'nopreprocess'])

    assert next(preprocessed) == ('random_field', 23)
    assert next(preprocessed) == ('nopreprocess', "OK!, OK!, OK!")


def test_no_preprocess_of_and_in_names():
    assert preprocess_namelist(['Alexander Ericson']) == 'Alexander Ericson'


def test_preprocess_skip_none_values():
    entry = bibpy.entry.Entry(
        'techreport',
        'ula22',
        **{'author': None},
    )

    preprocessed = preprocess(entry, ['author'])

    # None fields should be skipped by preprocessing and be left unchanged
    assert next(preprocessed, 'no changes') == 'no changes'
