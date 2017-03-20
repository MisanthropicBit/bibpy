Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibgrep --version
    bibgrep v0.1.0

    $ $TESTDIR/../../bin/bibgrep --count $TESTDIR/../data/small1.bib
    Found 4 entries

Test counting

    $ $TESTDIR/../../bin/bibgrep --entries="book" --count $TESTDIR/../data/small1.bib
    Found 1 entries

    $ $TESTDIR/../../bin/bibgrep --entries="book,inproceedings" --count $TESTDIR/../data/small1.bib
    Found 2 entries

Test entry type filtering

    $ $TESTDIR/../../bin/bibgrep --entries="book" $TESTDIR/../data/small1.bib
    @book{Conway2000,
        title     = {Object {O}riented {P}erl: {A} comprehensive guide to concepts and programming techniques},
        address   = {Connecticut, USA},
        year      = {2000},
        author    = {Damian Conway},
        publisher = {Manning Publications Co.}
    }

    $ $TESTDIR/../../bin/bibgrep --entries="inproceedings, book" $TESTDIR/../data/small1.bib
    @inproceedings{Huetal2000,
        title     = {Fast and robust equalization: A case study},
        booktitle = {Proceedings of the World Multiconference on Systemics, Cybernetics and Informatics, (SCI 2000), Florida, USA, 23-26 July 2000},
        address   = {FL, USA},
        year      = {2000},
        author    = {J. Hu, and H.R. Wu and A. Jennings and X. Wang},
        pages     = {398--403},
        publisher = {International Institute of Informatics and Systemics}
    }
    
    @book{Conway2000,
        title     = {Object {O}riented {P}erl: {A} comprehensive guide to concepts and programming techniques},
        address   = {Connecticut, USA},
        year      = {2000},
        author    = {Damian Conway},
        publisher = {Manning Publications Co.}
    }

    $ $TESTDIR/../../bin/bibgrep --entries="inproceedings" --entries="book" $TESTDIR/../data/small1.bib
    @inproceedings{Huetal2000,
        title     = {Fast and robust equalization: A case study},
        booktitle = {Proceedings of the World Multiconference on Systemics, Cybernetics and Informatics, (SCI 2000), Florida, USA, 23-26 July 2000},
        address   = {FL, USA},
        year      = {2000},
        author    = {J. Hu, and H.R. Wu and A. Jennings and X. Wang},
        pages     = {398--403},
        publisher = {International Institute of Informatics and Systemics}
    }
    
    @book{Conway2000,
        title     = {Object {O}riented {P}erl: {A} comprehensive guide to concepts and programming techniques},
        address   = {Connecticut, USA},
        year      = {2000},
        author    = {Damian Conway},
        publisher = {Manning Publications Co.}
    }

Test key filtering

    $ $TESTDIR/../../bin/bibgrep --key="Conway2000" $TESTDIR/../data/small1.bib
    @book{Conway2000,
        title     = {Object {O}riented {P}erl: {A} comprehensive guide to concepts and programming techniques},
        address   = {Connecticut, USA},
        year      = {2000},
        author    = {Damian Conway},
        publisher = {Manning Publications Co.}
    }
