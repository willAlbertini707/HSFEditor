import unittest
import sys, inspect

def setUpModule(obj):
    print("Setting up class")
    global subsystem
    subsystem = obj

def tearDownModule():
    del subsystem

class TestCase01(unittest.TestCase):

    def test_case01(self):
        self.assertTrue(hasattr(subsystem, "multiply"))