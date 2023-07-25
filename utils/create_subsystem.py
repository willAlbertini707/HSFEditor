"""
This module creates a new subsystem template with the 
appropriate name provided by the user. Define an instance
with the name of a subsystem and use "build_template" to 
return a template for the subsystem in the same directory.
This class is intended to be used privately.
"""

class SubsystemBuilder:


    def __init__(self, subsystem: str = None) -> None:
        self.subsystem = subsystem
        self._file_name = None


    def build_template(self, file_path: str = "subsystem_templates/subsystem_template.txt", from_template: bool = True) -> str:
        """
        Function build_template:
        ---------------------------
        file_path: directory in which to save to subsystem. Must end with '/' and 
        contain a valid path. File name is decided by the name of subsystem. Defaulted
        to blank subsystem path.

        from_template: Boolean flag that decides if text is parsed from the subsystem template. Default to True, use False if
        reading a saved file.
        """

        with open(file_path, "r") as input:
            full_text = []
            
            for input_line in input:

                if from_template:
                    if "fill_in" in input_line:
                        input_line = input_line.replace("fill_in", f"{self.subsystem}")

                full_text.append(input_line)

        return "".join(full_text)

    
    def save_subsystem(self, class_text: str, file_path: str = "subsystems/", file_name: str = None) -> None:
        """
        Function save_subsystem:
        --------------------------
        class_text: entire edited/generated text from subsystem

        file_path: directory in which to store the model. The file name will be self.subsystem and the extension will be .py
        """
        

        if file_name:
            self._file_name = self.check_extension(file_name)
            full_path = file_path + f"{self._file_name}"
        elif self._file_name:
            full_path = file_path + f"{self._file_name}"
        elif self.subsystem:
            full_path = file_path + f"{self.subsystem}" + ".py"
        else:
            full_path = file_path + "Unnamed.py" 

            
        with open(full_path, "w") as output:
            output.write(class_text)


    def parse_upload(self, file_path: str, file_name: str) -> str:
        """
        Function parse_upload:
        -----------------------
        file_path: file path to saved upload file. The text of the file will be returned

        file_name: the name of the file being parsed
        """

        self._file_name = file_name
        return self.build_template(file_path)

    
    def check_extension(self, file_name: str) -> str:
        """
        Function check_extension:
        --------------------------
        file_name: checks string to see if it contains a .py, otherwise one is added
        """
        if ".py" not in file_name:
            return file_name + ".py"
        else:
            return file_name