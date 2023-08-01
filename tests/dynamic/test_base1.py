"""
This module tests the basic functionality of the subsystem class. It tests the abstract methods
of the base class HSFSubsystem.
"""

# external imports
import unittest

# internal imports
from .parent import ParametrizedTestCase

class Test_Base01(ParametrizedTestCase):

    def test_has_CanPerform(self):
        self.assertTrue(hasattr(self.param, "CanPerform"))

    def test_has_GetDependencyDictionary(self):
        self.assertTrue(hasattr(self.param, "GetDependencyDictionary"))

    def test_has_GetDependencyCollector(self):
        self.assertTrue(hasattr(self.param, "GetDependencyCollector"))

    def test_has_CanExtend(self):
        self.assertTrue(hasattr(self.param, "CanExtend"))

    def test_has_DependencyCollector(self):
        self.assertTrue(hasattr(self.param, "DependencyCollector"))

