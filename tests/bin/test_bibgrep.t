Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibgrep --version
    bibgrep v0.1.0

    $ $TESTDIR/../../bin/bibgrep --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:4

    $ $TESTDIR/../../bin/bibgrep --abbreviate-filenames $TESTDIR/../data/small1.bib
    @ARTICLE{Meyer2000,
        AUTHOR="Bernd Meyer",
        TITLE="A constraint-based framework for diagrammatic reasoning",
        JOURNAL="Applied Artificial Intelligence",
        VOLUME= "14",
        ISSUE = "4",
        PAGES= "327--344",
        YEAR=2000
    }

    @ARTICLE{Codishetal2000,
        AUTHOR="M. Codish and K. Marriott and C.K. Taboch",
        TITLE="Improving program analyses by structure untupling",
        JOURNAL="Journal of Logic Programming",
        VOLUME= "43",
        ISSUE = "3",
        PAGES= "251--263",
        YEAR=2000
    }

    @inproceedings{Huetal2000,
        author = "J. Hu, and H.R. Wu and A. Jennings and X. Wang",
        title = "Fast and robust equalization: A case study",
        booktitle = "Proceedings of the World Multiconference on Systemics, Cybernetics and Informatics, (SCI 2000), Florida, USA, 23-26 July 2000",
        publisher = "International Institute of Informatics and Systemics",
        address = "FL, USA",
        pages = "398--403",
        year = "2000"
    }

    @Book{Conway2000,
        author = {Damian Conway},
        title = {Object {O}riented {P}erl: {A} comprehensive guide to concepts and programming techniques},
        publisher = {Manning Publications Co.},
        year = {2000},
        address = {Connecticut, USA}
    }

Test ignoring case

    $ $TESTDIR/../../bin/bibgrep --field="journal~logic" --ignore-case $TESTDIR/../data/small1.bib
    @article{Codishetal2000,
        author  = {M. Codish and K. Marriott and C.K. Taboch},
        title   = {Improving program analyses by structure untupling},
        journal = {Journal of Logic Programming},
        volume  = {43},
        issue   = {3},
        pages   = {251--263},
        year    = {2000}
    }

    $ $TESTDIR/../../bin/bibgrep --field="journal~logic" $TESTDIR/../data/small1.bib

Test counting

    $ $TESTDIR/../../bin/bibgrep --entry="book" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --entry="book,inproceedings" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

    $ $TESTDIR/../../bin/bibgrep --field="issue=3" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --field="journal~Logic" $TESTDIR/../data/small1.bib
    small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --key="~Co" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

    $ $TESTDIR/../../bin/bibgrep --ignore-case --key="~Co" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

Test piping

    $ $TESTDIR/../../bin/bibgrep --entry="book" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count --no-filenames
    1

    $ $TESTDIR/../../bin/bibgrep --entry="book,inproceedings" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count --no-filenames
    2

Test multiple files

    $ $TESTDIR/../../bin/bibgrep --entry="article" --count --no-filenames $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
    3

    $ $TESTDIR/../../bin/bibgrep --entry="article" $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
    @article{Meyer2000,
        author  = {Bernd Meyer},
        title   = {A constraint-based framework for diagrammatic reasoning},
        journal = {Applied Artificial Intelligence},
        volume  = {14},
        issue   = {4},
        pages   = {327--344},
        year    = {2000}
    }

    @article{Codishetal2000,
        author  = {M. Codish and K. Marriott and C.K. Taboch},
        title   = {Improving program analyses by structure untupling},
        journal = {Journal of Logic Programming},
        volume  = {43},
        issue   = {3},
        pages   = {251--263},
        year    = {2000}
    }

    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test removing duplicate

    $ $TESTDIR/../../bin/bibgrep --unique $TESTDIR/../data/duplicates.bib
    @article{key,
        year      = {2001},
        eventdate = {2008-07-02},
        month     = {4},
        foreword  = {Louis Clarkson and Jeremy Willard},
        xdata     = {key1, key2, key3}
    }

Test single comparison

    $ $TESTDIR/../../bin/bibgrep --field="year>=2000" $TESTDIR/../data/simple_1.bib
    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test interval comparison

    $ $TESTDIR/../../bin/bibgrep --field="year=2007-2011" $TESTDIR/../data/simple_1.bib
    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test range comparison

    $ $TESTDIR/../../bin/bibgrep --field="2007<=year<2011" $TESTDIR/../data/simple_1.bib
    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test single comparison failure

    $ $TESTDIR/../../bin/bibgrep --field="author>=2000" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare '2000' with 'Bernd Meyer'

Test interval comparison failure

    $ $TESTDIR/../../bin/bibgrep --field="author=2007-2011" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare 'Bernd Meyer' with interval [2007, 2011]

Test range comparison failure

    $ $TESTDIR/../../bin/bibgrep --field="2007<=author<2011" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare 'Bernd Meyer' with range 2007 <= field < 2011
