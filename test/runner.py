"""
This module is used to run the test suite given a module.
The module should be called using a command line argument structured in
the following way:

python runner.py module class 
----------------------------
module: module to import
class: class to import/test
"""

# external imports
import inspect, sys, unittest
from importlib import import_module


def load_class_from_module() -> None:
    # check for valid input variables
    try:
        class_name = sys.argv.pop()
        module = sys.argv.pop()
    except:
        raise Exception("Provide valid input arguments")
    
    # attempt to load in module and class
    try:
        global subsystem
        subsystem = getattr(import_module(module), class_name)
    except:
        raise Exception("Cannot import class, make sure class name and file path is correct")

# dynamically import class from CLI argument
load_class_from_module()
calculator = subsystem()



# ------------------- Testing ------------------------
class TestCase01(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global test_class
        test_class = subsystem()

    @classmethod
    def tearDownClass(cls):
        global test_class
        del test_class

    def test_add_attr(self):
        self.assertTrue(hasattr(test_class, "add"))


# running tests with runner and printing results
suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
runner = unittest.TextTestRunner(verbosity=0)
result = runner.run(suite)

if result.wasSuccessful():
    print("Tests Passed")
else:
    print("Tests Failed")
