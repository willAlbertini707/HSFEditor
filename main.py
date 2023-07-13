from flask import Flask, render_template, request
from utils.create_subsystem import SubsystemBuilder
from threading import Timer
import webbrowser

app = Flask(__name__, template_folder='templates', static_folder='static')
PREBUILT_SUBSYSTEMS = ["aeolus_adcs", "aeolus_Comm"]
current_subsystem = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", defaults={"var": ""}, methods=["POST", "GET"])
@app.route("/result/<var>", methods=["POST", "GET"])
def result(var: str):
    # add current_subsystem to scope to keep track of state/current subsystem in editor
    global current_subsystem
    
    if request.method == "GET":
        # handle a get request to render a pre-existing subsystem

        if var in PREBUILT_SUBSYSTEMS:

            sub_name = var.split("_")[1]
            current_subsystem = SubsystemBuilder(sub_name)
            path = "subsystem_templates/" + var + ".txt"
            subsystem_class = current_subsystem.build_template(file_path=path) + "\n"

        else:
            subsystem_class = ""

        return render_template("model.html", variable = subsystem_class)
    
    if request.method == "POST" and "input_sub" in request.form:
        # handle a user entering input into template generator

        # use data from post request
        subsystem = request.form["input_sub"]
        current_subsystem = SubsystemBuilder(subsystem)
        subsystem_class = current_subsystem.build_template() + "\n"

        return render_template("model.html", variable = subsystem_class)


    if request.method == "POST" and "code" in request.form:
        # handle a user saving the code in the editor

        # strip/replace JSON.stringify output from editor
        subsystem_class = request.form['code'].strip('"').replace("\\n", "\n").replace("\\\"", '"')

        # if subsystem exists, save it
        if current_subsystem:
            current_subsystem.save_subsystem(subsystem_class)

        return render_template("model.html", variable = subsystem_class)


def open_browser():
  # open a window in default browser with connection to the local server
  webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()