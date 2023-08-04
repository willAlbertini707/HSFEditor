# external imports
from flask import Flask, render_template, request
from fileinput import filename
from threading import Timer
import webbrowser, os, sys

# internal imports
from utils.create_subsystem import SubsystemBuilder
from utils.file_manager import display_directory, parse_class_from_file, load_object
from tests.dynamic.runner import run_suite

# add .dll files to path
sys.path.append("dlls/")

app = Flask(__name__, template_folder='templates', static_folder='static')
PREBUILT_SUBSYSTEMS = ["aeolus_adcs", "aeolus_Comm"]
current_subsystem = SubsystemBuilder("Unnamed")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", defaults={"var": ""}, methods=["POST", "GET"])
@app.route("/result/<var>", methods=["POST", "GET"])
def result(var: str):
    # add current_subsystem to scope to keep track of state/current subsystem in editor
    global current_subsystem

    # check the subsystems directory for python files to display
    saved_files = [file for file in os.listdir("Subsystems/") if ".py" in file]
    
    if request.method == "GET":
        # handle a get request to render a pre-existing subsystem

        if var in PREBUILT_SUBSYSTEMS:

            sub_name = var.split("_")[1]
            current_subsystem = SubsystemBuilder(sub_name)
            path = "subsystem_templates/" + var + ".txt"
            subsystem_class = current_subsystem.build_template(file_path=path) + "\n"

        else:
            subsystem_class = ""

    
    elif request.method == "POST" and "input_sub" in request.form:
        # handle a user entering input into template generator

        # use data from post request
        subsystem = request.form["input_sub"]
        current_subsystem = SubsystemBuilder(subsystem)
        subsystem_class = current_subsystem.build_template() + "\n"


    elif request.method == "POST" and "code" in request.form:
        # handle a user saving the code in the editor

        # strip/replace JSON.stringify output from editor
        subsystem_class = request.form['code'][1:-1].replace("\\n", "\n").replace('\\"', '"')

        # save subsystem to default directory with chosen file name or default file name
        if request.form["fileName"]:
            current_subsystem.save_subsystem(subsystem_class, file_name = request.form["fileName"])
        else:
            current_subsystem.save_subsystem(subsystem_class)


    elif request.method == "POST" and "file" in request.files:
        # handle the uploading and parsing of files to editor
        file = request.files["file"]
        save_dir = f"subsystems/{file.filename}"
        file.save(save_dir)
        current_subsystem = SubsystemBuilder("Unnamed")
        subsystem_class = current_subsystem.parse_upload(save_dir, file.filename)


    elif request.method == "POST" and "subsystemFile" in request.form:
        # handle the opening/testing/deleting of files in subsystem directory

        file = request.form["subsystemFile"]
        file_dir = f"subsystems/{file}"
        current_subsystem = SubsystemBuilder("Unnamed")

        if request.form["action"] == "open":
            # file is only opened and parsed to editor
            subsystem_class = current_subsystem.parse_upload(file_dir, file)
            

        elif request.form["action"] == "test":
            # file is opened and tested
            subsystem_class = current_subsystem.parse_upload(file_dir, file)

            # try to dynamically instantiate the object
            os.system(f"python tests/test_runner.py {file_dir}")
            

        elif request.form["action"] == "delete":
            # remove a file from the directory
            os.remove(file_dir)
            subsystem_class = ""


    # display files in subsystem directory
    saved_files = display_directory("subsystems/")


    return render_template("model.html", variable = subsystem_class, drop_down = saved_files)


def open_browser():
  # open a window in default browser with connection to the local server
  webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()