Test version number

    $ bibformat --version
    bibformat v0.1.0

Test alphabetic ordering

    $ bibformat --order=true $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        author = {Somebody McPerson},
        title = {How To Parse BibTex},
        year = {2011}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }

Test specific ordering

    $ bibformat --order=year,author,title $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        year = {2011},
        author = {Somebody McPerson},
        title = {How To Parse BibTex}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }

Test ordering with align

    $ bibformat --order=title,author,year --align $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        title  = {How To Parse BibTex},
        author = {Somebody McPerson},
        year   = {2011}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
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
    
    @string{month = "March"}
    
    @string{var = "less"}
    
    @string{last_name = "Cook"}
    
    @string{var1 = "should"}
    
    @string{var2 = "multiple"}

Test indentation

    $ bibformat --indent='____' $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
    ____author = {Somebody McPerson},
    ____title = {How To Parse BibTex},
    ____year = {2011}
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }

Test surrounding characters

    $ bibformat --surround=@@ $TESTDIR/../data/all_bibpy_entry_types.bib
    @unpublished{unpubkey,
        author = @Somebody McPerson@,
        title = @How To Parse BibTex@,
        year = @2011@
    }
    
    @string{variable = "value"}
    
    @preamble{\textbf{\latex}}
    
    @comment{
        Anything is possible with comments!
    }

Test grouping

    $ bibformat --group $TESTDIR/../data/{all_entry_types,crossreferences}.bib
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
