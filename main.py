from flask import Flask, render_template, request
from utils.create_subsystem import CreateSubsystem
from threading import Timer
import webbrowser

app = Flask(__name__, template_folder='templates', static_folder='static')
SUBSYSTEM_TEMPLATES = ["subsystem_template", "ADCS_template", "Comm_template"]
PREBUILT_SUBSYSTEMS = ["aeolus_adcs", "aeolus_Comm"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", defaults={"var": ""}, methods=["POST", "GET"])
@app.route("/result/<var>", methods=["POST", "GET"])
def result(var):
    
    if request.method == "GET":
        if var in SUBSYSTEM_TEMPLATES:

            if var == "subsystem_template":
                subsystem_class = "\n" + CreateSubsystem().build_template() + "\n"
            else:
                subsystem = var.replace("_template", "")
                subsystem_class = "\n" + CreateSubsystem(subsystem).build_template() + "\n"

        elif var in PREBUILT_SUBSYSTEMS:
            path = "subsystem_templates/" + var + ".txt"
            subsystem_class = "\n" + CreateSubsystem().build_template(path) + "\n"

        else:
            subsystem_class = ""

        return render_template("model.html", variable = subsystem_class)
    
    if request.method == "POST":
        subsystem = request.form["input_sub"]
        subsystem_class = "\n" + CreateSubsystem(subsystem).build_template() + "\n"

        return render_template("model.html", variable = subsystem_class)



def open_browser():
  webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()