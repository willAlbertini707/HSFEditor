# HSFEditor
Proof of concept for a developement/testing interface for Horizon Simulation Framework ([HSF](https://github.com/emehiel/Horizon)) subsystems. 
The project explores how to aid a user in creating HSF subsystems and test them in a Python runtime before consumption by the HSF software. 
It utilizes a web application feel and is locally hosted. The program relies on dynamically linked libraries and documents from the HSF repository 
(linked above), as well as the project PythonNet, to allow access to native HSF C# objects in a python runtime. 

## Dependencies
>Python 3.10.11  

The program uses the following non-native libraries/projects:  
>Flask 2.2.2  
>PythonNet 3.0.1  
>bs4 4.12.2  

## Disclaimer
This software relies on XML documents and Python scripts for subsystems, targets, and sim parameters. The documents currently used are
taken from the HSF repository as a means of testing functionality.
