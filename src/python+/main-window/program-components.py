from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import sys
import os
import importlib
import ctypes
import traceback
from multiprocessing import freeze_support, Queue
import time

from multiprocessing import Process, Queue, Pipe
from PyQt5.QtCore import pyqtSignal, QThread
from datetime import datetime

sys.path.append("../")
sys.path.append("../../")

### import database functions ###
database_functions = importlib.import_module("python+.lib.sqlite3_functions")


class Programm_Components:
    def __init__(self,main_self):  
        self.main_self = main_self

        #create proccess for program components
        self.programm_components_proccess_number = 21
        self.programm_components_mother_pipe, self.programm_components_child_pipe = Pipe()
        self.programm_components_queue = Queue()
        self.programm_components_emitter = Programm_Components_Emitter(self.programm_components_mother_pipe)
        self.programm_components_emitter.start()
        self.programm_components_child_process = Programm_Components_Child_Proc(self.programm_components_child_pipe, self.programm_components_queue)
        self.programm_components_child_process.start()
        self.programm_components_emitter.programm_components_ready.connect(self.programm_components_ready)

            
        counter = 0
        for process in self.main_self.manage_processes_instance.processes:
            if "process_number" in process:
                if process["process_number"]==self.programm_components_proccess_number:
                    self.main_self.manage_processes_instance.processes[counter]["pid"] = self.programm_components_child_process.pid
                    self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                    self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
            counter += 1

    def programm_components_ready(self,settings):
        if settings["program_component_time_lines"]==1:
            self.main_self.ui.graphs_tab.show()
        else:
            self.main_self.ui.graphs_tab.hide()
        if settings["program_component_general_deck"]==1:
            self.main_self.ui.general_deck_frame.show()
        else:
            self.main_self.uigeneral_deck_frame.hide()
        if settings["program_component_deck_1"]==1:
            self.main_self.ui.deck_1_frame.show()
        else:
            self.main_self.uideck_1_frame.hide()
        if settings["program_component_deck_2"]==1:
            self.main_self.ui.deck_2_frame.show()
        else:
            self.main_self.ui.deck_2_frame.hide()
        if settings["program_component_music_clip_deck"]==1:
            self.main_self.ui.music_clip_deck_frame.show()
        else:
            self.main_self.ui.music_clip_deck_frame.hide()
        if settings["program_component_speackers_deck"]==1:
            self.main_self.ui.speackers_deck_frame.show()
        else:
            self.main_self.ui.speackers_deck_frame.hide()
        if settings["program_component_ip_calls"]==1:
            self.main_self.ui.ip_calls_tabs.show()
        else:
            self.main_self.ui.ip_calls_tabs.hide()
        if settings["program_component_player_list"]==1:
            self.main_self.ui.player_list_frame.show()
        else:
            self.main_self.ui.player_list_frame.hide()
        if settings["program_component_web_sites"]==1:
            self.main_self.ui.web_pages.show()
        else:
            self.main_self.ui.web_pages.hide()
        

class Programm_Components_Emitter(QThread):

    programm_components_ready = pyqtSignal(dict)

    def __init__(self, from_process: Pipe):
        super().__init__()
        self.data_from_process = from_process

    def run(self):
        while True:
            data = self.data_from_process.recv()
            if data["type"]=="programm_components_ready":
                self.programm_components_ready.emit(data["settings"])
                
class Programm_Components_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother):
        super().__init__()
        self.daemon = False
        self.to_emitter = to_emitter
        self.data_from_mother = from_mother
        
    def run(self):
        self.programm_components()
        while(True):
            data = self.data_from_mother.get()
            if data["type"] == "programm_components":
                self.programm_components()
                
    def programm_components(self):
        program_component_time_lines = int(database_functions.read_setting("program_component_time_lines")["current_value"])
        program_component_general_deck = int(database_functions.read_setting("program_component_general_deck")["current_value"])
        program_component_deck_1 = int(database_functions.read_setting("program_component_deck_1")["current_value"])
        program_component_deck_2 = int(database_functions.read_setting("program_component_deck_2")["current_value"])
        program_component_music_clip_deck = int(database_functions.read_setting("program_component_music_clip_deck")["current_value"])
        program_component_speackers_deck = int(database_functions.read_setting("program_component_speackers_deck")["current_value"])
        program_component_ip_calls = int(database_functions.read_setting("program_component_ip_calls")["current_value"])
        program_component_player_list = int(database_functions.read_setting("program_component_player_list")["current_value"])
        program_component_web_sites = int(database_functions.read_setting("program_component_web_sites")["current_value"])

        
        settings = {
            "program_component_time_lines":program_component_time_lines,
            "program_component_general_deck":program_component_general_deck,
            "program_component_deck_1":program_component_deck_1,
            "program_component_deck_2":program_component_deck_2,
            "program_component_music_clip_deck":program_component_music_clip_deck,
            "program_component_speackers_deck":program_component_speackers_deck,
            "program_component_ip_calls":program_component_ip_calls,
            "program_component_player_list":program_component_player_list,
            "program_component_web_sites":program_component_web_sites
        }
        
        self.to_emitter.send({"type":"programm_components_ready","settings":settings})