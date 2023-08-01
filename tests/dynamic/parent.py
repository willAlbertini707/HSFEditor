"""
This module acts as a parent to the dynamic unit test objects. It allows for the 
parametrization of unittest test fixture. For this application, the passed in 
parameter will be the subsystem object being tested
"""

# external imports
import unittest 

class ParametrizedTestCase(unittest.TestCase):

    def __init__(self, methodName="runTest", param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_class, param=None):

        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name, param=param))
        return suite