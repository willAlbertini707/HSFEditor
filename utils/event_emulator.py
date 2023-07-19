"""
This class exists to mock the c# Event class in order to debug an
existing subsystem. All inputs are provided by the user through the 
user interface. This object will be used as an input to python 
subsystems.
"""
from typing import Any

class Event:

    def __init__(self, _event_start: float, _task_start: float, _task_end: float) -> None:
        self._event_start = _event_start
        self._task_start = _task_start
        self._task_end = _task_end

    def GetEventStart(self, _: Any = None) -> float:
        """
        Function GetEventStart:
        -------------------------
        _: has to take in input for function to work, but input will
        be taken from constructor/provided by user interface. 
        """
        return self._event_start
    
    def GetTaskStart(self, _: Any = None) -> float:
        """
        Function GetTaskStart:
        -----------------------
        _: has to take in input for function to work, but input will
        be taken from constructor/provided by user interface. 
        """
        return self._task_start
    
    def GetTaskEnd(self, _: Any = None) -> float:
        """
        Function GetTaskEnd:
        ---------------------
        _: has to take in input for function to work, but input will
        be taken from constructor/provided by user interface. 
        """
        return self._task_end