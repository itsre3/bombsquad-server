
import ba
import _ba
import os
import _thread
from flask import Flask, render_template

app = Flask(__name__)

stats_dir = os.path.join(_ba.env()['python_directory_user'], "stats" + os.sep

stats_file = stats_dir + "stats_page.html"

@app.route("/")
def index():
    return render_template(stats_file)

def run():
    _thread.start_new_thread(app.run, ("0.0.0.0", 5000, False))

