"""
This module creates a new subsystem template with the 
appropriate name provided by the user. Define an instance
with the name of a subsystem and use "build_template" to 
return a template for the subsystem in the same directory.
This class is intended to be used privately.
"""

class CreateSubsystem:

    def __init__(self, subsystem: str = None) -> None:

        self.subsystem = subsystem


    def build_template(self, file_path: str = "subsystem_templates/subsystem_template.txt") -> str:
        """
        Function build_template:
        ---------------------------
        file_path: directory in which to save to subsystem. Must end with '/' and 
        contain a valid path. File name is decided by the name of subsystem. Defaulted
        to blank subsystem path.
        """

        with open(file_path, "r") as input:
            full_text = []
            
            for input_line in input:

                if self.subsystem:
                    if "fill_in" in input_line:
                        input_line = input_line.replace("fill_in", f"{self.subsystem.lower()}")

                full_text.append(input_line)

        return "".join(full_text)


if __name__ == "__main__":
    temp = CreateSubsystem("ADCS").build_template()
    print(temp)
    