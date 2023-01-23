
import asyncio
import threading
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("stats/stats_page.html")

def run():
    loop = asyncio.get_event_loop()
    loop.create_task(app.run(debug=False))
    threading.Thread(target=loop.run_forever).start()

