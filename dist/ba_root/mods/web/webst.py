
import asyncio
import threading
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("stats/stats_page.html")

def run():
    threading.Thread(target=app.run(False)).start()

