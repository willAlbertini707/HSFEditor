# external imports 
import sys, os
from importlib import import_module

# internal imports
from utils import parse_class_from_file, parse_module_from_path
from dynamic.runner import run_suite

sys.path.append("dlls/")

try:
    module_path = sys.argv.pop()
    with open(module_path, "r") as _:
        pass
except:
    print("Module could not be opened")
    sys.exit()


try:

    module, directory = parse_module_from_path(module_path)
    
    if directory:
        sys.path.append(directory)

    mod = import_module(module)
    class_name = parse_class_from_file(module_path)
    obj = getattr(mod, class_name)

except:
    print("class name could not be found")
    sys.exit()


temp = obj(None, None)
run_suite(temp)