"""
This module is used to validate testing parameter inputs. 
"""

# external imports
from typing import Dict, Optional
import logging, unittest, os

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# fh = logging.fileHandler("")

class UserInputHandler:

    def __init__(self, request_form: Dict[str, str]) -> None:


        # unpack request form
        try:
            if ".py" not in request_form["moduleName"]:
                self._module_name = request_form["moduleName"] + ".py"
            else:
                self._module_name = request_form["moduleName"]
            self._class_name = request_form["className"]
            self._asset_name = request_form["assetName"]
            self._task_name = request_form["taskName"]
            self._event_start = request_form["eventStart"]
            self._event_end = request_form["eventEnd"]
            self._task_start = request_form["taskStart"]
            self._task_end = request_form["taskEnd"]

        except:
            raise Exception("Could not parse input, check input values")
        
        # check for correct xml files
        xml_string = self._get_xml_documents()
        if not xml_string:
            raise Exception("Provide xml files with correct naming struction")
        

        
    def _get_xml_documents(self, xml_directory: str = "files/xml_files/") -> Optional[str]:
        """
        Function get_xml_documents:

        Get the first part of the command line argument for test_runner.py. This includes
        a model.xml, sim.xml, and target.xml
        ------------------------------
        xml_directory: directory where xml files reside

        return: string with files seperated by spaces. Order is 'model.xml sim.xml target.xml'
        """
        model_file = None
        sim_file = None
        target_file = None

        for file in os.listdir(xml_directory):

            if "model" in file:
                model_file = xml_directory + file
            elif "sim" in file:
                sim_file = xml_directory + file
            elif "target" in file:
                target_file = xml_directory + file

        if model_file and sim_file and target_file:
            return f"{model_file} {sim_file} {target_file}"
        else:
            return None
        
    
    def get_test_input_string(self, log_file: str = "files/log_files/run_results.log", 
                              xml_directory: str = "files/xml_files/") -> str:
        """
        Function: get_test_input_string

        return a string containing xml document directories and event/task arguments
        """

        return f"{self._get_xml_documents(xml_directory)} {self._module_name} {self._class_name} \
        {self._asset_name} {self._task_name} {self._event_start} {self._event_end} {self._task_start} \
        {self._task_end} {log_file}"
    

# ---------------------- tests -----------------------------------
class Test_Case(unittest.TestCase):

    def test_xml_function01(self):
        directory = "../files/xml_files/"
        xmls = get_xml_documents(directory)
        actual = f"{directory}model.xml {directory}sim.xml {directory}target.xml"
        self.assertEqual(xmls, actual)
        
    def test_xml_function02(self):
        directory = "../files/subsystems/"
        xmls = get_xml_documents(directory)
        self.assertIsNone(xmls)

if __name__ == "__main__":
    unittest.main()
