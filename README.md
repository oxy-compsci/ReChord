# ReChord

[![Build Status](https://travis-ci.org/oxy-compsci/ReChord.svg?branch=master)](https://travis-ci.org/oxy-compsci/ReChord)
### Introduction
**ReChord is a web application that seeks to aid the comparative study of musical expressive terms by allowing for text-based search across MEI data.** It serves as the core functionality for what will eventually be a graphical tool that will allow music scholars to view snippets of scores which contain user-specified search terms across editions and corpuses of different composers. By simplifying the examination of the contexts in which expressive terms are used across a large body of musical passages, ReChord will help scholars and performers develop a more nuanced and data-driven understanding of the meanings behind expressive terms, as well as the mutation of those meanings across different works of music.


### Folder Configuration
```
app
└── database
|   └── MEI_Complete_examples (a folder of many mei files)
|   └── test_files
└── js
|   └── main.js
└── static
|   └── css
|   └── fonts
|   └── js
|   └── sass
└── templates
|   └── images
|   └── index.html
|   └── ReChord_front.html
|   └── ReChord_result.html
└── ReChord_frontend.py
└── search.py
└── tests.py
└── terms_dict.txt

```