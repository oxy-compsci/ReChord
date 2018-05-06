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
└── static
|   └── css
|   └── fonts
|   └── js
|   └── sass
└── templates
|   └── index.html
|   └── result.html
└── ReChord_frontend.py
└── search.py
└── tests.py
└── terms_dict.txt

```

# Project ReChord Back-End Essential Files and Structures

The back-end of this project uses Python to develop its search.
This project uses lxml in order to parse the MEI file and develop a tree of elements which is used for our search methods. It is necessary to install lxml to run the back-end. It is also encouraged to get familiar with lxml and its capabilities before jumping into the back-end. All methods for the back-end can be found in 'search.py' with test cases in 'tests.py'.

The following are notes to keep in mind when working on the 'search.py' methods:
 - lxml allows the developer to parse an MEI (or xml) document into a tree of elements (or 'etree')
 - MEI has a specific namespace which is imperative for a developer to search through tags of elements in the tree: `'{http://www.music-encoding.org/ns/mei}'`
 - We use 'element' and 'root' which are objects outlined in the lxml API. These objects allow us to extract data from the etree.
 - We mainly utilized the 'attrib', 'tag', and 'text' properties of an element to compare to our desired criteria, which generally took the form of a string: `creators_list = [element.text for element in children if element.attrib['role'] == "creator"]`
 - Terms dictionary file ('terms_dict.txt') allows the user to search by shorthands for a term and the full term interchangeably.
	 -  e.g. 'cresc.' and 'crescendo' will produce the same output in expressive term search.
 - Tuples are used for the output of 'text_box_search_folder' and 'snippet_search_folder' and allow the front-end to display the output much more intuitively.
	 - Tuple creation: `result = namedtuple('result', ['file_name', 'title', 'creator', 'measure_numbers', 'appearance'])`

	 - Using tuple to declare a match: `result_list.append(result(file_name, title, creator, str(measure_numbers)[1:-1], appearance))`



# Project ReChord Front-end integration

The existing Project ReChord website is built upon Flask and Jinja. Before you start, it's good to get your hands on how [Flask](http://flask.pocoo.org/) and [Jinja](http://jinja.pocoo.org/) work. You may certainly have your own search interface, so let's get started!

# Essential Files and Structures
Flask has its own rules to setup the web structure. In our project (and many other standard flask projects), the heirarchy and naming are:

 - **static**
	 - css
	 - fonts
	 - js
	 - sass
 - **templates**
	 - index.html
	 - result.html
 - **ReChord_frontend.py**

All of your local css or javascript should go into the static folder. Once done, to call specific javascript or css in header, please follow the format down below:
To call a javascript with file name **js/ie/html5shiv.js**

    <script src="{{url_for('static', filename='js/ie/html5shiv.js')}}"></script>
To call a css file with name **css/main.css**

    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/main.css') }}">

# Setup Flask
To setup your flask, first you need to setup a python file and call flask.

    app = Flask(__name__)
After you build your homepage (generally named index.html), specify a [route](http://flask.pocoo.org/docs/0.12/quickstart/#routing) in a function and use [render_template](http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates) to display your index.html. In our example. Here is how we return the homepage and the homepage routing is defaulted by "/"

    @app.route('/')
    def my_form():
	    return render_template('index.html')

# Passing data from HTML to Flask
In our current development, we pass text and dropdown choices to the backend search algorithms.
In the snippet search, we retrieve snippets using textarea. The snippet input will be passed as "*text"* and the submission value will be passed as *"Search Snippet In Our Database"*.

**Snippet search in index.html**

    <form method="POST">
	    <textarea name="text" rows="7" cols="80" placeholder="Paste your MEI snippet here" required </textarea>
	    <input type="submit" name="submit" value="Search Snippet In Our Database" style="background-color: black;">
    </form>

**Snippet search in ReChord_frontend.py**

    if request.form['submit'] == 'Search Snippet In Our Database':
	    path = 'database/MEI_Complete_examples'
	    return search_snippet(path, request.form['text'])

In the term search, we pass two values to the backend: *tag* and *para*
**Term search in index.html**

    <div style="padding: 20px 0 40px 0;">
	    <select name="term">
		    <option value="">Select your term</option>
		    <option value="Expressive Terms">Expressive Terms</option>
		    <option value="Tempo Marking">Tempo Marking</option>
		    <option value="Articulation">Articulation</option>
		    <option value="Dynamic Markings">Dynamic Markings</option>
		    <option value="Piano Fingerings">Piano Fingerings</option>
		    <option value="Pedal Marking">Pedal Marking</option>
		    <option value="Hairpin">Hairpin</option>
	    </select>
	    <input type="text" class="terms" name="parameter" placeholder="Enter your parameter here">
    </div>
    <input type="submit" name="submit" value="Upload and Search Parameter">
**Term search in ReChord_frontend.py**

    elif request.form['submit'] == 'Search Terms In Our Database':
	    tag = request.form['term']
	    para = request.form['parameter']
	    path = 'database/MEI_Complete_examples'
	    return search_terms(path, tag, para)
All parameters will then be passed to the front-end search function: **search_snippet** and **search_terms**. These two functions will communicate with the backend search algorithm, retrieving necessary information