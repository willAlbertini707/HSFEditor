"""
This module is intended to be used to parse relevant information from
the xml files to be used in testing. The object will return HSF c# objects
to be used in evaluating models. Particular the ones used in scripted 
subsystems.
"""

# external imports
import clr 
import sys
from typing import Dict, List, Union, Optional
from bs4 import BeautifulSoup

sys.path.append("dlls/")

# internal imports
clr.AddReference("System")
clr.AddReference("UserModel")
clr.AddReference("MissionElements")
clr.AddReference("HSFSystem")
clr.AddReference("HSFUniverse")

from System.Xml import XmlNode
from System.Collections.Generic import Dictionary, Stack
from UserModel import XmlParser
from MissionElements import Asset, SystemState, Task, Event
from HSFUniverse import UniverseFactory, Domain, SpaceEnvironment
from HSFSystem import SubsystemFactory, Subsystem


class HSFObjectParser:


    def __init__(self, model_xml: str, sim_xml: str, target_xml: str) -> None:
        """
        Function __init__:
        --------------------
        model_xml: full or relative path to HSF model xml file
        sim_xml: full or relative path to HSF sim xml file
        target_xml: full or relative path to HSF target deck
        """

        # define sim setup file paths
        self.model_path = model_xml
        self.sim_path = sim_xml
        self.target_path = target_xml

        # load in sim parameters
        XmlParser.ParseSimulationInput(self.sim_path)
        self._modelInputNode = XmlParser.GetModelNode(self.model_path)

        # load in targets
        self._targets = self._load_tasks_into_list(self.target_path)

        # create dict to store data on each asset
        self._asset_dict = self._get_asset_dict(self._modelInputNode)

        # get universe/Domain
        self._universe = self._get_universe()

            
    def _get_asset_dict(self, model_xml_node: XmlNode) -> Dict[Asset, List[Subsystem]]:
        """
        Function _get_asset_dict:

        Used in the initialization of object
        --------------------------
        model_xml_node: C# XmlNode object

        return: Dictionary containing assets and list of subsystems
        """
        # create initial system state
        self._initial_state = SystemState()

        # create dictionary to hold assets and subsystems
        asset_dict = {}

        # loop through assets from model xml
        assets = model_xml_node.SelectNodes("ASSET")
        for asset_node in assets:

            new_asset = Asset(asset_node)

            # create a subsystem dict
            sub_list = []

            # loop through subsystems to store initial states
            # store subsystem nodes so they can be retrieved in get_subsystem_node()
            self._subsystem_nodes = asset_node.SelectNodes("SUBSYSTEM")
            for subsystem_node in self._subsystem_nodes:

                # create new subsystem from node
                new_sub = SubsystemFactory.GetSubsystem(subsystem_node, new_asset)

                # add subsystem to list
                sub_list.append(new_sub)

                # loop through subsystem state
                states = subsystem_node.SelectNodes("STATE")
                for state_node in states:

                    key_name = SubsystemFactory.SetStateKeys(state_node, new_sub)
                    self._initial_state.SetInitialSystemState(state_node, key_name)

            # add asset and subsystem to asset dictionary
            asset_dict[new_asset] = sub_list

        return asset_dict


    def _load_tasks_into_list(self, target_path: str) -> List[Task]:
        """
        Function _load_tasks_into_list:

        By default, tasks are stored in a stack. Because tasks will need to be
        iterated over and chosen, this will need to be turned into a list.
        --------------------------------
        target_path: path to target deck xml file
        """

        # load targets into a stack
        target_stack = Stack[Task]()
        targets_loaded = Task.loadTargetsIntoTaskList(XmlParser.GetTargetNode(target_path), target_stack)
        
        # check to see if targets were loaded
        if not targets_loaded:
            raise Exception("Targets not loaded in")
        
        stack_full = True

        target_list = []

        # pop entire stack and add targets to list
        while stack_full:

            # pop target is in stack, else exit loop
            try:
                target = target_stack.Pop()
                target_list.append(target)
            except:
                stack_full = False

        return target_list
    

    def _get_universe(self) -> Domain:
        """
        Function: _get_universe
        ------------------------

        return: HSF c# datatype Domain from xml or create space 
        """

        # self._modelInputNode defined in __init__()
        environments = self._modelInputNode.SelectNodes("ENVIRONMENT")

        if environments.Count == 0:
            universe = SpaceEnvironment()
            print("Using default space")

        else:
            print("found environment")
            for node in environments:
                universe = UniverseFactory.GetUniverseClass(node)

        return universe


    def _get_asset(self, asset_name: str) -> Asset:
        # loop through asset keys and return desired asset

        for asset in self._asset_dict.keys():
            if asset.Name == asset_name.lower():
                return asset
            
            raise Exception("Asset not found")


    def _get_task(self, task_name: str) -> Task:
        # loop through task list and return desired task

        # all tasks are lowercase in sim
        task_name = task_name.lower()

        for task in self._targets:
            # Task overrides c# ToString() to return name
            if task.ToString() == task_name:
                return task
            
        raise Exception("Task not found")
    
    def _get_event_start_end(self) -> (float, float):
        """
        Function _get_event_start_end:

        Takes the initial start time as the start time and
        adds a single step for end time. To be used in 
        self.parse_event()
        ---------------------------
        
        return: an event start and finish
        """
        with open(self.sim_path, "r") as sim_file:
            sim_data = sim_file.read()

        soup = BeautifulSoup(sim_data, "xml")

        # get simulation and scheduler nodes
        sim_params = soup.find_all("SIMULATION_PARAMETERS")[0]
        scheduler_params = soup.find_all("SCHEDULER_PARAMETERS")[0]

        # pull the start time, add simStepSeconds for end
        start = float(sim_params["SimStartSeconds"])
        end = start + float(scheduler_params["simStepSeconds"])

        return start, end


    def parse_asset(self, asset_name: str) -> Asset:
        """
        Function parse_asset:

        return HSF c# Asster object
        -----------------------
        asset_name: name of asset to be returned
        """

        return self._get_asset(asset_name)
    

    def parse_event(self, asset_name: str, task_name: str, 
                    event_bracket: Optional[List[float]] = None,
                    task_bracket: Optional[List[float]] = None) -> Event:
        """
        Function parse_event:

        build the HSF c# Event object. Assumes a starting time of 0.0 if no time
        bracket is given for Event. If not time bracket is given from Task,
        start and end times are chosen so task fits in event.
        ---------------------------------
        asset_name: Asset name which the subsystem belongs to
        task_name: Name of target
        event_bracket: [start, end] times of event
        task_bracket: [start, end] times of task
        """
        
        # get asset and task, SystemState is given by xml
        asset = self._get_asset(asset_name)
        task = self._get_task(task_name)

        # create a temporary c# dict to load asset and task into Event
        temp_dict = Dictionary[Asset, Task]()
        temp_dict.Add(asset, task)

        # create event
        event = Event(temp_dict, self._initial_state)

        # get start and end times for event and task
        if event_bracket == None and task_bracket == None:
            event_start, event_end = self._get_event_start_end()
            task_start = event_start + (event_end - event_start) * 0.01
            task_end = event_end - (event_end - event_start) * 0.01

        elif event_bracket == None and task_bracket != None:
            event_start, event_end = self._get_event_start_end()
            task_start, task_end = task_bracket

        else:
            event_start, event_end = event_bracket
            task_start, task_end = task_bracket

        # set event/task start and finish times
        event.SetEventStart(asset, event_start)
        event.SetEventEnd(asset, event_end)
        event.SetTaskStart(asset, task_start)
        event.SetTaskEnd(asset, task_end)

        return event
    

    def parse_subsystem_node(self, subsystem_name: str) -> XmlNode:
        """
        Function parse_subsystem_node:

        return xml node corresponding to desired subsystem. Returns
        c# System.XmlNode type.
        --------------------------------
        subsystem_name: name of subsystem to be returned
        """ 
        # loop through subsystem nodes
        for subsystem_node in self._subsystem_nodes:

            # check ea
            if subsystem_node.GetAttribute("subsystemName").lower() == subsystem_name.lower():
                return subsystem_node
            
        raise Exception(f"{subsystem_node} not found in {self.model_path}")
    
    
    def parse_universe(self) -> Union[Domain, SpaceEnvironment]:
        """
        Function parse_universe:
        ---------------------------

        return: returns domain/space environment loaded in during contruction of class
        """

        return self._universe


if __name__ == "__main__":
    sys.path.append("../files/subsystems/")
    from adcs import adcs

    ec = HSFObjectParser("../files/xml_files/model.xml", "../files/xml_files/sim.xml", "../files/xml_files/target.xml")
    asset = ec.parse_asset("asset1")
    event = ec.parse_event("asset1", "groundstation2", [0, 30], [10, 20])
    state = ec.parse_universe()
    node = ec.parse_subsystem_node("adcs")


    my_adcs = adcs(node, asset)

    test_bool = my_adcs.CanPerform(event, state)
    print(test_bool)


    