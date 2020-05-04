Test version number

    $ bibformat --version
    bibformat v0.1.0

Test alphabetic ordering

    $ bibformat --order=true $TESTDIR/../data/all_bibpy_entry_types.bib
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }
    
    @unpublished{unpubkey,
        author = {Somebody McPerson},
        title = {How To Parse BibTex},
        year = {2011}
    }

Test specific ordering

    $ bibformat --order=year,author,title $TESTDIR/../data/all_bibpy_entry_types.bib
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }
    
    @unpublished{unpubkey,
        year = {2011},
        author = {Somebody McPerson},
        title = {How To Parse BibTex}
    }

Test ordering without align

    $ bibformat --order=title,author,year $TESTDIR/../data/all_bibpy_entry_types.bib
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }
    
    @unpublished{unpubkey,
        title = {How To Parse BibTex},
        author = {Somebody McPerson},
        year = {2011}
    }

Test ordering with align

    $ bibformat --order=title,author,year --align $TESTDIR/../data/all_bibpy_entry_types.bib
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }
    
    @unpublished{unpubkey,
        title  = {How To Parse BibTex},
        author = {Somebody McPerson},
        year   = {2011}
    }

Test xdata inheritance

    $ bibformat --inherit-xdata $TESTDIR/../data/xdata_inheritance.bib
    @xdata{macmillan:name,
        publisher = {Macmillan}
    }
    
    @xdata{macmillan:place,
        location = {New York and London}
    }
    
    @xdata{macmillan,
        xdata = {macmillan:name, macmillan:place},
        publisher = {Macmillan},
        location = {New York and London}
    }
    
    @book{key,
        author = {Author},
        title = {Title},
        date = {2016-11-29},
        xdata = {macmillan},
        publisher = {Macmillan},
        location = {New York and London}
    }

Test string expansion

    $ bibformat --expand-string-vars $TESTDIR/../data/string_variables.bib
    @string{month = "March"}
    
    @string{var = "less"}
    
    @string{last_name = "Cook"}
    
    @string{var1 = "should"}
    
    @string{var2 = "multiple"}
    
    @conference{key,
        title = {March Report}
    }
    
    @article{key,
        author = {Charles Xavier},
        title = {Merciless Animals}
    }
    
    @book{key,
        author = {Andre Cook},
        title = {b}
    }
    
    @techreport{key,
        institution = {This should expand multiple variables}
    }
    
    @article{no_expand,
        author = {Regular Author},
        title = {Regular Title}
    }

Test indentation

    $ bibformat --indent='____' $TESTDIR/../data/all_bibpy_entry_types.bib
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }
    
    @unpublished{unpubkey,
    ____author = {Somebody McPerson},
    ____title = {How To Parse BibTex},
    ____year = {2011}
    }

Test surrounding characters

    $ bibformat --surround=@@ $TESTDIR/../data/all_bibpy_entry_types.bib
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }
    
    @unpublished{unpubkey,
        author = @Somebody McPerson@,
        title = @How To Parse BibTex@,
        year = @2011@
    }

Test grouping

    $ bibformat --group $TESTDIR/../data/all_entry_types.bib $TESTDIR/../data/crossreferences.bib
    @article{test1,
        author = {ksjbgr},
        title = {kj srgr},
        journaltitle = {kj srgr},
        year = {2016}
    }
    
    @book{test2,
        author = {ksjbgr},
        title = {kj srgr},
        year = {2016}
    }
    
    @book{key2,
        subtitle = {Booksubtitle},
        title = {Booktitle},
        author = {Author2},
        date = {1995},
        publisher = {Publisher},
        location = {Location}
    }
    
    @inbook{key1,
        crossref = {key2},
        title = {Title},
        author = {Author},
        pages = {5--25}
    }
