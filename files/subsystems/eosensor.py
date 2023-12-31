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
#clr.AddReferenceByName('SystemState')
import System.Xml
import HSFSystem
import MissionElements
import Utilities
import HSFUniverse
import UserModel
# from MissionElements import SystemState
from HSFSystem import *
from System.Xml import XmlNode
from Utilities import *
from HSFUniverse import *
from UserModel import *
from MissionElements import *
from System import Func, Delegate, Math
from System.Collections.Generic import Dictionary, KeyValuePair
from IronPython.Compiler import CallTarget0

class eosensor(HSFSystem.Subsystem):
    def __new__(cls, node, asset):
        instance = HSFSystem.Subsystem.__new__(cls)
        instance.Asset = asset
        instance.Name = instance.Asset.Name + '.' + node.Attributes['subsystemName'].Value.ToString().ToLower()

        instance.PIXELS_KEY = Utilities.StateVariableKey[System.Double](instance.Asset.Name + '.' + 'numpixels')
        instance.INCIDENCE_KEY = Utilities.StateVariableKey[System.Double](instance.Asset.Name + '.' + 'incidenceangle')
        instance.EOON_KEY = Utilities.StateVariableKey[System.Boolean](instance.Asset.Name + '.' + 'eosensoron')
        instance.addKey(instance.PIXELS_KEY)
        instance.addKey(instance.INCIDENCE_KEY)
        instance.addKey(instance.EOON_KEY)

        instance._lowQualityPixels = 5000
        instance._lowQualityTime = 3
        instance._midQualityPixels = 10000
        instance._midQualityTime = 5
        instance._highQualityPixels = 15000
        instance._highQualityTime = 7
        if (node.Attributes['lowQualityPixels'] != None):
            instance._lowQualityPixels = float(node.Attributes['lowQualityPixels'].Value.ToString())
        if (node.Attributes['lowQualityTime'] != None):
            instance._lowQualityTime = float(node.Attributes['lowQualityTime'].Value.ToString())
        if (node.Attributes['midQualityPixels'] != None):
            instance._midQualityPixels = float(node.Attributes['midQualityPixels'].Value.ToString())
        if (node.Attributes['midQualityTime'] != None):
            instance._midQualityTime = float(node.Attributes['midQualityTime'].Value.ToString())
        if (node.Attributes['highQualityPixels'] != None):
            instance._highQualityPixels = float(node.Attributes['highQualityPixels'].Value.ToString())
        if (node.Attributes['highQualityTime'] != None):
            instance._highQualityTime = float(node.Attributes['highQualityTime'].Value.ToString())

        return instance

    def GetDependencyDictionary(self):
        dep = Dictionary[str, Delegate]()
        depFunc1 = Func[Event,  Utilities.HSFProfile[System.Double]](self.POWERSUB_PowerProfile_EOSENSORSUB)
        dep.Add("PowerfromEOSensor" + "." + self.Asset.Name, depFunc1)
        depFunc1 = Func[Event,  Utilities.HSFProfile[System.Double]](self.SSDRSUB_NewDataProfile_EOSENSORSUB)
        dep.Add("SSDRfromEOSensor" + "." + self.Asset.Name, depFunc1)
        return dep

    def GetDependencyCollector(self):
        return Func[Event,  Utilities.HSFProfile[System.Double]](self.DependencyCollector)

    def CanPerform(self, event, universe):
         if (self._task.Type == TaskType.IMAGING):
             value = self._task.Target.Value
             pixels = self._lowQualityPixels
             timetocapture = self._lowQualityTime
             if (value <= self._highQualityTime and value >= self._midQualityTime):
                    pixels = self._midQualityPixels
                    timetocapture = self._midQualityTime
             if (value > self._highQualityTime):
                pixels = self._highQualityPixels
                timetocapture = self._highQualityTime

             es = event.GetEventStart(self.Asset)
             ts = event.GetTaskStart(self.Asset)
             te = event.GetTaskEnd(self.Asset)
             if (ts > te):
                # Logger.Report("EOSensor lost access")
                 return False
             te = ts + timetocapture
             event.SetTaskEnd(self.Asset, te)

             position = self.Asset.AssetDynamicState
             timage = ts + timetocapture / 2
             m_SC_pos_at_tf_ECI = position.PositionECI(timage)
             m_target_pos_at_tf_ECI = self._task.Target.DynamicState.PositionECI(timage)
             m_pv = m_target_pos_at_tf_ECI - m_SC_pos_at_tf_ECI
             pos_norm = -m_SC_pos_at_tf_ECI / Matrix[System.Double].Norm(-m_SC_pos_at_tf_ECI)
             pv_norm = m_pv / Matrix[System.Double].Norm(m_pv)

             incidenceang = 90 - 180 / Math.PI * Math.Acos(Matrix[System.Double].Dot(pos_norm, pv_norm))
             self._newState.AddValue(self.INCIDENCE_KEY, KeyValuePair[System.Double, System.Double](timage, incidenceang))
             self._newState.AddValue(self.INCIDENCE_KEY, KeyValuePair[System.Double, System.Double](timage + 1, 0.0))

             self._newState.AddValue(self.PIXELS_KEY, KeyValuePair[System.Double, System.Double](timage, pixels))
             self._newState.AddValue(self.PIXELS_KEY, KeyValuePair[System.Double, System.Double](timage + 1, 0.0))

             self._newState.AddValue(self.EOON_KEY, KeyValuePair[System.Double, System.Boolean](ts, True))
             self._newState.AddValue(self.EOON_KEY, KeyValuePair[System.Double, System.Boolean](te, False))
             return True

    def CanExtend(self, event, universe, extendTo):
        return super(eosensor, self).CanExtend(event, universe, extendTo)

    def POWERSUB_PowerProfile_EOSENSORSUB(self, event):
        prof1 = HSFProfile[System.Double]()
        prof1[event.GetEventStart(self.Asset)] = 10
        if (event.State.GetValueAtTime(self.EOON_KEY, event.GetTaskStart(self.Asset)).Value):
            prof1[event.GetTaskStart(self.Asset)] = 60
            prof1[event.GetTaskEnd(self.Asset)] = 10	
        return prof1

    def SSDRSUB_NewDataProfile_EOSENSORSUB(self, event):
        return event.State.GetProfile(self.PIXELS_KEY) / 500

    def DependencyCollector(self, currentEvent):
        return super(eosensor, self).DependencyCollector(currentEvent)
