"""
This module contains functions for managing the files in the app. Functionality
includes but is not limited to displaying files and dynamically loading in modules.
"""
# external imports
import os, re, sys
from typing import Optional
import unittest
from importlib import import_module, reload

def display_directory(directory: str) -> str:
    """
    Function display_directory:
    ----------------------------
    directory: A string containing the path to the direcotry to be displayed.
    Files are displayed as <option> types.

    """
    files = os.listdir(directory)

    drop_down = ""
    for file in [file for file in files if ".py" in file or ".xml" in file]:
        option = f"""<option value="{file}">{file}</option>\n\t"""
        drop_down += option

    return drop_down


def wipe_log_file(log_file: str = "files/log_files/run_results.log") -> None:
    """
    Function clean_log_file:

    erases the results of the previous test so new output can shown
    """

    # remove the file if it exists
    try:
        os.remove(log_file)
    # else creat empty file only
    except:
        pass

    with open(log_file, "w") as _:
        pass


def display_log_file(log_file: str = "files/log_files/run_results.log") -> str:
    """
    Function display_log_file:

    display the contents of the log file
    """
    try:
        with open(log_file, "r") as file:
            result = "<br>".join([line for line in file])
            return result
    except:
        with open(log_file, "w") as _:
            pass

        with open(log_file, "r") as file:
            return file.read()