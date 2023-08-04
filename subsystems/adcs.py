import sys
import clr
import System.Collections.Generic
import System
clr.AddReference('System.Core')
clr.AddReference('IronPython')
clr.AddReference('System.Xml')
clr.AddReference('Utilities')
clr.AddReference('HSFUniverse')
clr.AddReference('UserModel')
clr.AddReference('MissionElements')
clr.AddReference('HSFSystem')

import System.Xml
import HSFSystem
import HSFSubsystem
import MissionElements
import Utilities
import HSFUniverse
import UserModel
from HSFSubsystem import *
from HSFSystem import *
from System.Xml import XmlNode
from Utilities import *
from HSFUniverse import *
from UserModel import *
from MissionElements import *
from System import Func, Delegate
from System.Collections.Generic import Dictionary
from IronPython.Compiler import CallTarget0

class adcs(HSFSubsystem.Subsystem):

    __namespace__ = "PythonBaseModel"

    def __init__(self, node, asset):
        pass


    def GetDependencyDictionary(self):
        dep = Dictionary[str, Delegate]()
        return dep

        
    def GetDependencyCollector(self):
        return Func[Event,  Utilities.HSFProfile[System.Double]](self.DependencyCollector)


    def CanPerform(self, event, universe):
        return super(adcs, self).CanPerform(event, universe)


    def CanExtend(self, event, universe, extendTo):
        return super(adcs, self).CanExtend(self, event, universe, extendTo)


    def DependencyCollector(self, currentEvent):
        return super(adcs, self).DependencyCollector(currentEvent)
