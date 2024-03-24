
import ba
import _ba
import asyncio, threading
import logging
from flask import Flask, render_template

app = Flask(__name__)
logging.getLogger('werkzurg').disabled = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    return render_template("stats_page.html")

def run():
    loop = asyncio.get_event_loop()
    loop.create_task(app.run(debug=False))
    threading.Thread(target=loop.run_forever).start()

