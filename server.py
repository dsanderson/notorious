from flask import Flask
from flask import request, redirect
import os
app = Flask(__name__)

PYTHON_PATH = '/home/dsa/Projects/notorious-app/bin/python2'
ROOT_DIR = '/home/dsa/Projects/notorious-app/notorious/data/'

@app.route("/")
def hello():
    return "Hello World!"

##Stuff for reading notes
@app.route("/read/<path:loc>", methods=['GET'])
def read_note(loc):
    txt = read_note_raw(loc)
    #placeholder for now, in future will add proper templating
    return txt

def read_note_raw(loc):
    path = os.path.join(ROOT_DIR,loc)
    print loc, path
    try:
        f = open(path,'r')
        txt = f.read()
        f.close()
    except:
        txt = "No page, please make one :)"
    return txt


##Stuff for making notes
@app.route("/write/<path:loc>", methods=['GET','POST'])
def write_note(loc):
    print loc
    if request.method == 'GET':
        return write_note_input_page(loc)
    if request.method == 'POST':
        txt = request.form['note']
        loc2 = os.path.join(ROOT_DIR, loc)
        path, fname = os.path.split(loc2)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(loc2, 'w')
        f.write(txt)
        f.close()
        print loc, path
        return redirect('/read/'+loc)


def write_note_input_page(loc):
    txt = read_note_raw(loc)
    page_header = """<!DOCTYPE html>\n<html>\n<body>\n<textarea rows="40" cols="80" name="note" form="note_form">\n"""
    page_footer = """</textarea>\n<p>\n<form action="""+loc+""" method="POST" id="note_form">\n
    <input type="submit" value="Write Note">\n</form>\n</body>\n</html>"""
    page = page_header+txt+page_footer
    return page


##stuff for executing notes
@app.route("/run/<path:loc>", methods=['GET'])
def run_note(loc):
    command = [PYTHON_PATH, loc]
    txt = subprocess.check_output(command)
    #placeholder, will use templates in future
    return txt

if __name__ == "__main__":
    app.debug = True
    app.run()
