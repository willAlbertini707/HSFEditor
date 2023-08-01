# external imports
import unittest

# internal imports
from .parent import ParametrizedTestCase
from .test_base1 import Test_Base01

def run_suite(obj):
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(Test_Base01, param = obj))
    unittest.TextTestRunner(verbosity=2).run(suite)
    print("done")