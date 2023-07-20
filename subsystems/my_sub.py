import sys
import clr
import System.Collections.Generic
import System
clr.AddReference('System.Core')
clr.AddReference('IronPython')
clr.AddReference('System.Xml')
clr.AddReferenceByName('Utilities')
clr.AddReferenceByName('HSFUniverse')
clr.AddReferenceByName('UserModel')
clr.AddReferenceByName('MissionElements')
clr.AddReferenceByName('HSFSystem')

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

class my_sub(HSFSubsystem.Subsystem):

    def __init__(self, node, asset):
        pass


    def GetDependencyDictionary(self):
        dep = Dictionary[str, Delegate]()
        return dep

        
    def GetDependencyCollector(self):
        return Func[Event,  Utilities.HSFProfile[System.Double]](self.DependencyCollector)


    def CanPerform(self, event, universe):
        return super(my_sub, self).CanPerform(event, universe)


    def CanExtend(self, event, universe, extendTo):
        return super(my_sub, self).CanExtend(self, event, universe, extendTo)


    def DependencyCollector(self, currentEvent):
        return super(my_sub, self).DependencyCollector(currentEvent)
