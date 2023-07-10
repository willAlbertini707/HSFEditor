from flask import Flask, render_template, request
from utils.create_subsystem import CreateSubsystem
from threading import Timer
import webbrowser

app = Flask(__name__, template_folder='templates', static_folder='static')
SUBSYSTEM_TEMPLATES = ["subsystem_template", "ADCS_template", "Comm_template"]
PREBUILT_SUBSYSTEMS = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", defaults={"var": ""})
@app.route("/result/<var>")
def result(var):
    if var in SUBSYSTEM_TEMPLATES:

        if var == "subsystem_template":
            var = "\n"
            var += CreateSubsystem().build_template()
            var += "\n"
        else:
            subsystem = var.replace("_template", "")
            var = "\n"
            var += CreateSubsystem(subsystem).build_template()
            var += "\n"
    else:
        var = ""

    return render_template("model.html", variable = var)


def open_browser():
  webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()