Test version number

    $ bibgrep --version
    bibgrep v0.1.0

    $ bibgrep --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:4

    $ bibgrep --abbreviate-filenames $TESTDIR/../data/small1.bib
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
    
    @inproceedings{Huetal2000,
        author    = {J. Hu, and H.R. Wu and A. Jennings and X. Wang},
        title     = {Fast and robust equalization: A case study},
        booktitle = {Proceedings of the World Multiconference on Systemics, Cybernetics and Informatics, (SCI 2000), Florida, USA, 23-26 July 2000},
        publisher = {International Institute of Informatics and Systemics},
        address   = {FL, USA},
        pages     = {398--403},
        year      = {2000}
    }
    
    @book{Conway2000,
        author    = {Damian Conway},
        title     = {Object {O}riented {P}erl: {A} comprehensive guide to concepts and programming techniques},
        publisher = {Manning Publications Co.},
        year      = {2000},
        address   = {Connecticut, USA}
    }

Test ignoring case

    $ bibgrep --field="journal~logic" --ignore-case $TESTDIR/../data/small1.bib
    @article{Codishetal2000,
        author  = {M. Codish and K. Marriott and C.K. Taboch},
        title   = {Improving program analyses by structure untupling},
        journal = {Journal of Logic Programming},
        volume  = {43},
        issue   = {3},
        pages   = {251--263},
        year    = {2000}
    }

    $ bibgrep --field="journal~logic" $TESTDIR/../data/small1.bib

Test counting

    $ bibgrep --entry="book" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ bibgrep --entry="book,inproceedings" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

    $ bibgrep --field="issue=3" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ bibgrep --field="journal~Logic" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:1

    $ bibgrep --key="~Co" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

    $ bibgrep --ignore-case --key="~Co" --count --abbreviate-filenames $TESTDIR/../data/small1.bib
    small1.bib:2

Test piping

    $ bibgrep --entry="book" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count --no-filenames
    1

    $ bibgrep --entry="book,inproceedings" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count --no-filenames
    2

Test multiple files

    $ bibgrep --entry="article" --count --no-filenames $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
    3

    $ bibgrep --entry="article" $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
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

    $ bibgrep --unique $TESTDIR/../data/duplicates.bib
    @article{key,
        year      = {2001},
        eventdate = {2008-07-02},
        month     = {4},
        foreword  = {Louis Clarkson and Jeremy Willard},
        xdata     = {key1, key2, key3}
    }

Test single comparison

    $ bibgrep --field="year>=2000" $TESTDIR/../data/simple_1.bib
    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test interval comparison

    $ bibgrep --field="year=2007-2011" $TESTDIR/../data/simple_1.bib
    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test range comparison

    $ bibgrep --field="2007<=year<2011" $TESTDIR/../data/simple_1.bib
    @article{test,
        author      = {James Conway and Archer Sterling},
        title       = {1337 Hacker},
        year        = {2010},
        month       = {4},
        institution = {Office of Information Management {and} Communications}
    }

Test single comparison failure

    $ bibgrep --field="author>=2000" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare '2000' with 'Bernd Meyer'
    [1]

Test interval comparison failure

    $ bibgrep --field="author=2007-2011" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare 'Bernd Meyer' with interval [2007, 2011]
    [1]

Test range comparison failure

    $ bibgrep --field="2007<=author<2011" $TESTDIR/../data/small1.bib
    bibgrep: Cannot compare 'Bernd Meyer' with range 2007 <= field < 2011
    [1]

Test field occurrence

    $ bibgrep --field=booktitle $TESTDIR/../data/small1.bib
    @inproceedings{Huetal2000,
        author    = {J. Hu, and H.R. Wu and A. Jennings and X. Wang},
        title     = {Fast and robust equalization: A case study},
        booktitle = {Proceedings of the World Multiconference on Systemics, Cybernetics and Informatics, (SCI 2000), Florida, USA, 23-26 July 2000},
        publisher = {International Institute of Informatics and Systemics},
        address   = {FL, USA},
        pages     = {398--403},
        year      = {2000}
    }

    $ bibgrep --field="^address" $TESTDIR/../data/small1.bib
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

Test wrong option

    $ bibgrep --idonotexist=nope $TESTDIR/../data/small1.bib
    bibgrep: [Errno 2] No such file or directory: '--idonotexist=nope'
    [1]

Test recursive directory searching

    $ bibgrep --recursive $TESTDIR/../data
    bibgrep: Duplicate field(s) 'year' in entry 'key' with type 'article'
    [1]
