#external imports
from typing import Optional
import sys, re, os
import unittest

def parse_class_from_file(file_path: str) -> Optional[str]:
    """
    Function parse_class_name:
    ---------------------------
    file_path: Location of file to be searched for class name.
    """
    class_name = None

    with open(file_path, "r") as f:
        for line in f:
            if "class" in line:
                try:
                    class_name = parse_class_name(line)
                except:
                    pass # possibly log the name and/or failure to log file

    return class_name


def parse_class_name(string: str) -> Optional[str]:
    """
    Function parse_class_name:
    ----------------------------
    string: String to be searched for a class name.
    """

    pattern = re.compile(r'class (\w+)')

    try:
        result = pattern.search(string)
        class_name = result.group(1)
        return class_name
    except:
        pass # possibly log the name and/or failure to log file

    return None


def parse_module_from_path(module_path: str) -> Optional[str]:
    """
    Function parse_module_from_path:
    ----------------------------------
    string: module path to be searched.

    return: (module_name, module_directory) tuple containing the module name and module 
    directory
    """

    pattern = re.compile(r'(\w+).py')

    # keep track of directory if not in cwd
    module_directory = None

    try:
        if "/" in module_path:
            split_path = module_path.split("/")
            file = split_path.pop()
            module_directory = "/".join(split_path) + "/"
        else:
            file = module_path
        result = pattern.search(file)
        module_name = result.group(1)
        
        return module_name, module_directory
    
    except:
        pass

    return None



# ---------------------- tests -----------------------------------
class Test_Case(unittest.TestCase):

    def test_parse01(self):
        line = "class temp:"
        parsed_name = parse_class_name(line)
        self.assertEqual("temp", parsed_name)

    def test_parse02(self):
        line = "Nada"
        parsed_name = parse_class_name(line)
        self.assertIsNone(parsed_name)

    def test_parse03(self):
        file = "temp.txt"
        with open(file, "w") as output:
            output.write("class temp(HSFSubsystem):")
        
        parsed_name = parse_class_from_file(file)
        self.assertEqual("temp", parsed_name)

        os.remove(file)

    def test_parse04(self):
        module_path = "mod1/mod2/module.py"
        parsed_module = parse_module_from_path(module_path)
        self.assertEqual(parsed_module, ("module", "mod1/mod2/"))

    def test_parse05(self):
        module_path = "mod1/mod2.py"
        parsed_module = parse_module_from_path(module_path)
        self.assertEqual(parsed_module, ("mod2", "mod1/"))

    def test_parse06(self):
        module_path = "mod_2.py"
        parsed_module = parse_module_from_path(module_path)
        self.assertEqual(parsed_module, ("mod_2", None))


if __name__ == "__main__":
    unittest.main()