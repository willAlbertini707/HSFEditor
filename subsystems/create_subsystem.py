"""
This module creates a new subsystem template with the 
appropriate name provided by the user. Define an instance
with the name of a subsystem and use "build_template" to 
return a template for the subsystem in the same directory.
This class is intended to be used privately.
"""

class CreateSubsystem:

    def __init__(self, subsystem: str) -> None:

        self.subsystem = subsystem


    def build_template(self, file_path: str = "") -> None:
        """
        Function build_template:
        ---------------------------
        file_path: directory in which to save to subsystem. Must end with '/' and 
        contain a valid path. File name is decided by the name of subsystem.
        """

        with open("template.txt", "r") as input:
            with open(f"{file_path + self.subsystem.lower()}.py", "w") as output:
                
                for input_line in input:

                    if "fill_in" in input_line:
                        input_line = input_line.replace("fill_in", f"{self.subsystem.lower()}")

                    output.write(input_line)



if __name__ == "__main__":
    CreateSubsystem("ADCS").build_template("../")
