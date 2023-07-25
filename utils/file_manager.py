import os


class FileManager:

    def __init__(self):
        pass

    def display_directory(self, directory: str) -> str:
        """
        Function display_directory:
        ----------------------------

        """
        files = os.listdir(directory)

        drop_down = ""
        for file in [file for file in files if ".py" in file]:
            option = f"""<option value="{file}">{file}</option>\n\t"""
            drop_down += option

        return drop_down
    

if __name__ == "__main__":

    manager = FileManager()
    print(manager.display_directory("../subsystems/"))





