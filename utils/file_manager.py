"""
This module contains functions for managing the files in the app. Functionality
includes but is not limited to displaying files and dynamically loading in modules.
"""
# external imports
import os, re
from typing import Optional
import unittest

def display_directory(directory: str) -> str:
    """
    Function display_directory:
    ----------------------------
    directory: A string containing the path to the direcotry to be displayed.
    Files are displayed as <option> types.

    """
    files = os.listdir(directory)

    drop_down = ""
    for file in [file for file in files if ".py" in file]:
        option = f"""<option value="{file}">{file}</option>\n\t"""
        drop_down += option

    return drop_down


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

    pattern = re.compile(r'class (\w+)')

    try:
        result = pattern.search(string)
        class_name = result.group(1)
        return class_name
    except:
        pass # possibly log the name and/or failure to log file

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


if __name__ == "__main__":
    unittest.main()




