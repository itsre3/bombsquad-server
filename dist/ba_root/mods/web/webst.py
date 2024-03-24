
import ba
import _ba
import _thread, os
import logging
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
logging.getLogger('werkzurg').disabled = True

@app.route("/")
def index():
    return render_template("stats_page.html")

def run():
    _thread.start_new_thread(app.run, ("0.0.0.0", 5000, False))

