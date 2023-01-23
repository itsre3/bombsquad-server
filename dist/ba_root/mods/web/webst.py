
import ba
import _ba
import _thread, os
from flask import Flask, render_template, make_response

app = Flask(__name__)

html_file = os.path.join(_ba.env()['python_directory_user'], "web" + os.sep) + "templates/stats_page.html"

contents = ""

def reload_file():
    with open(html_file, 'r') as file:
        content = file.read()
    
    contents = str(content)

def tr():
    ba.timer(10, reload_file(), True)


@app.route("/")
def index():
    
    html = contents
    # return render_template("stats_page.html")
    return make_response(html)

def run():
    _thread.start_new_thread(app.run, ("0.0.0.0", 5000, False))
    
    _thread.start_new_thread(tr, ())

