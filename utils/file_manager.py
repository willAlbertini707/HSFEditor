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