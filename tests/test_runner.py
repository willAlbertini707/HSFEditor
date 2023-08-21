# external imports 
import sys, os, logging
from importlib import import_module

# add path to dlls for testing
dlls_path = os.path.join(os.path.dirname(__file__), "dlls/")
sys.path.append(dlls_path)

# internal imports
from utils import parse_module_from_path
from dynamic.runner import run_suite
from hsf_parser import HSFObjectParser

# set up logger
log_file = sys.argv[-1]

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# unpack the input arguments
xml_files = sys.argv[1:4]
module_path = sys.argv[4]
class_name = sys.argv[5]
asset_name = sys.argv[6]
target_name = sys.argv[7]
try:
    event_time = [float(x) for x in sys.argv[8:10]]
except Exception as e:
    logger.exception(e.__str__())
    logger.exception("event time values must be numerical")

try:
    task_time = [float(x) for x in sys.argv[10:12]]
except Exception as e:
    logger.exception(e.__str__())
    logger.exception("event time values must be numerical")

# delete system variables
del sys.argv[1:]

# try to read the module from the path
try:
    print(module_path)
    with open(module_path, "r") as _:
        pass
except Exception as e:
    logger.exception(e.__str__())
    print("Module could not be opened, check path")
    sys.exit()


# try to import the class from the module
try:
    # use function from utils.py
    module, directory = parse_module_from_path(module_path)
    
    # append the module directory for ease of import
    if directory:
        sys.path.append(directory)

    # import the class
    mod = import_module(module)
    obj = getattr(mod, class_name)

except Exception as e:
    logger.exception(e.__str__())
    print("class name could not be found or loaded")
    sys.exit()

# parse c# objects into python
sim_parser = HSFObjectParser(*xml_files)
asset = sim_parser.parse_asset(asset_name)
event = sim_parser.parse_event(asset_name, target_name, event_time, task_time)
state = sim_parser.parse_universe()
node = sim_parser.parse_subsystem_node(class_name)

# create the temporary subsystem object
temp = obj(node, asset)

# run the test suite on the object
run_suite(temp, log_file)

# run CanPerform() method
result = temp.CanPerform(event, state)
logger.info("\n\nResults of CanPerform():")
logger.info(result)