
import ba
import _ba
import _thread
from flask import Flask, render_template, make_response

app = Flask(__name__)

html_file = os.path.join(_ba.env()['python_directory_user'], "web" + os.sep) + "templates/stats_page.html"



@app.route("/")
def index():
    with open(html_file, 'r' as file:
        contents = file.read()
    
    html = str(contents)
    # return render_template("stats_page.html")
    return make_response(html)

def run():
    _thread.start_new_thread(app.run, ("0.0.0.0", 5000, False))

