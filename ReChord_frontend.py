"""ReChord_frontend.py construct a flask app and calls on search.py for searching"""
# pylint: disable=invalid-name

import os
import tempfile
from io import BytesIO
from flask import Flask, request, render_template, flash, redirect, abort
from werkzeug.utils import secure_filename
from lxml import etree
from search import text_box_search_folder, snippet_search_folder, prepare_tree

ALLOWED_EXTENSIONS = {'xml', 'mei'}

# initiate the app
app = Flask(__name__)  # pylint: disable=invalid-name
app.secret_key = '\x82\xebT\x17\x07\xbbx\xd9\xe1dxR\x11\x8b\x0ci\xe1\xb7\xa8\x97\n\xd6\x01\x99'


def allowed_file(filename):
    """check the file name to avoid possible hack
    Arguments: uploaded file's name
    Return: rendered result page 'ReChord_result.html'
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def my_form():
    """render front page template
    Return: rendered front page 'index.html'
    """
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    """render front page template
    Return: rendered front page 'index.html'
    """
    return render_template('documentation.html')


@app.route('/', methods=['POST'])
def my_form_post():   # pylint: disable=too-many-return-statements
    """the view function which return the result page by using the input pass to the back end
    Arguments: forms submitted in index.html
    Return: rendered result page 'ReChord_result.html' by call on helper functions
    """

    # Snippet search in ReChord Database
    if request.form['submit'] == 'Search Snippet In Our Database':
        path = 'database/MEI_Complete_examples'
        return search_snippet(path, request.form['text'])

    # Terms search in ReChord Database
    elif request.form['submit'] == 'Search Terms In Our Database':
        tag = request.form['term']
        para = request.form['parameter']
        path = 'database/MEI_Complete_examples'
        return search_terms(path, tag, para)

    # Snippet search using user submitted library
    elif request.form['submit'] == 'Upload and Search Your Snippet':
        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                path = upload_file("base_file", tmpdirname)
                return search_snippet(path, request.form['text'])
            except NameError as error_msg:
                return render_template('ReChord_result.html', errors=str(error_msg))

    # Terms search with user submitted library
    elif request.form['submit'] == 'Upload and Search Parameter':
        tag = request.form['term']
        para = request.form['parameter']
        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                path = upload_file("base_file", tmpdirname)
                return search_terms(path, tag, para)
            except NameError as error_msg:
                return render_template('ReChord_result.html', errors=str(error_msg))
    else:
        abort(404)
        return None


# Helper functions

def get_mei_from_folder(path):
    """gets a list of MEI files from a given folder path
    Arguments: path [string]: absolute or relative path to folder
    Returns: all_mei_files: List<file>: list of mei files in path
    """
    return [path + "/" + filename for filename in os.listdir(path) if
            filename.endswith('.mei') or filename.endswith('.xml')]


def search_snippet(path, snippet):
    """search the snippet from the given database
    Arguments:
        snippet of xml that want to search for
        tree of xml base that needed to be searched in
    Return: rendered result page 'ReChord_result.html'
    """
    xml = BytesIO(snippet.encode())
    error_msg = ""
    try:
        input_xml_tree, _ = prepare_tree(xml)  # pylint: disable=c-extension-no-member

        named_tuples_ls = snippet_search_folder(path, input_xml_tree)
        if named_tuples_ls:
            return render_template('ReChord_result.html', origins=named_tuples_ls)
        else:
            error_msg = "No matched snippet found, maybe try something else?"
            return render_template('ReChord_result.html', nomatch=error_msg)
    except (etree.XMLSyntaxError, ValueError):
        error_msg = "Invalid MEI snippet inputs. Please double check the source and try it again!"
    except KeyError:
        error_msg = "Invalid upload file. Please double check the source and try it again!"
    return render_template('ReChord_result.html', errors=error_msg)


def search_terms(path, tag, para):
    """ search terms in the database
    Arguments:
        tags of term that want to search for
        para(meters) of tags that want to search for
        tree of xml base that needed to be searched in
    Return: rendered result page 'ReChord_result.html'
    """
    error_msg = ""
    try:
        named_tuples_ls = text_box_search_folder(path, tag, para)
        if named_tuples_ls:
            return render_template('ReChord_result.html', origins=named_tuples_ls)
        else:
            error_msg = "No matched term found, maybe try something else?"
            return render_template('ReChord_result.html', nomatch=error_msg)
    except KeyError:
        error_msg = "Invalid upload file. Please double check the source and try it again!"
    return render_template('ReChord_result.html', errors=error_msg)


def upload_file(name_tag, tmpdirname):
    """pass the upload files and store them in uploads folder's unique sub-folder
    Arguments: name_tag that used in html
    Return: upload path name
    """
    # check if the post request has the file part
    if 'base_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    else:
        files = request.files.getlist(name_tag)

        for file in files:
            # if user does not select file, browser also submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            # if properly uploaded
            elif file:
                if allowed_file(file.filename):
                    file.save(os.path.join(tmpdirname, secure_filename(file.filename)))
                else:
                    raise NameError(file.filename + ' is not a allowed name or the file extension is not .mei or .xml.')
        return tmpdirname


if __name__ == "__main__":
    app.run()
