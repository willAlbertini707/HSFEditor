from flask import Flask, render_template, request
from threading import Timer
import webbrowser

app = Flask(__name__, template_folder='templates', static_folder='styling')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    return render_template("model.html")

def open_browser():
  webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()