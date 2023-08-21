# external imports
import unittest

# internal imports
from .parent import ParametrizedTestCase
from .test_base1 import Test_Base01

def run_suite(obj: object, log_file: str) -> None:
    """
    Function run_suite:

    runs the unittest tests and stores result in file
    ---------------------
    obj: subsystem object being tested
    log_file: file to write test results to
    """
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(Test_Base01, param = obj))

    with open(log_file, "w") as file:
        unittest.TextTestRunner(file, verbosity=2).run(suite)