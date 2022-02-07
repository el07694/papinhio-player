from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt
from multiprocessing import Process, Queue, Pipe
import subprocess
from PyQt5.QtCore import pyqtSignal, QThread
import sys
import os
import importlib
from datetime import datetime, timedelta
import time
#from watchpoints import watch

sys.path.append("../../")
sys.path.append("../../../")

database_functions = importlib.import_module("python+.lib.sqlite3_functions")
label_clickable = importlib.import_module("python+.lib.label-clickable")
when_to_play_function = importlib.import_module("python+.lib.Greece-time-when-to-play")
convert_time_function = importlib.import_module("python+.lib.convert-time-function")
convert_bytes_function = importlib.import_module("python+.lib.convert-bytes-for-read")


class Manage_Player_List_Table:
    def __init__(self,main_self):
        self.main_self = main_self

        
        #create proccess for main player list
        self.proccess_number = 12
        self.main_player_list_mother_pipe, self.main_player_list_child_pipe = Pipe()
        self.main_player_list_queue = Queue()
        self.main_player_list_emitter = Main_Player_List_Emitter(self.main_player_list_mother_pipe)
        self.main_player_list_emitter.start()
        self.main_player_list_child_process = Main_Player_List_Child_Proc(self.main_player_list_child_pipe, self.main_player_list_queue)
        self.main_player_list_child_process.start()
        self.main_player_list_emitter.player_list_fields.connect(self.display_player_list_fields)
        

        
        
        counter = 0
        for process in self.main_self.manage_processes_instance.processes:
            if "process_number" in process:
                if process["process_number"]==self.proccess_number:
                    self.main_self.manage_processes_instance.processes[counter]["pid"] = self.main_player_list_child_process.pid
                    self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                    self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
            counter += 1

    def display_player_list_fields(self,settings):
        if settings["player_field_change_position"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(0, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(0, True)
        if settings["player_field_play"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(1, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(1, True)
        if settings["player_field_title"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(2, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(2, True)
        if settings["player_field_last_play"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(3, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(3, True)
        if settings["player_field_next_play"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(4, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(4, True)
        if settings["player_field_image"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(5, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(5, True)
        if settings["player_field_prepare"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(6, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(6, True)
        if settings["player_field_play_now"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(7, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(7, True)
        if settings["player_field_remove"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(8, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(8, True)
        if settings["player_field_duration"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(9, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(9, True)
        if settings["player_field_artist"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(10, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(10, True)
        if settings["player_field_album"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(11, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(11, True)
        if settings["player_field_composer"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(12, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(12, True)
        if settings["player_field_author"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(13, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(13, True)
        if settings["player_field_year"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(14, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(14, True)
        if settings["player_field_description"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(15, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(15, True)
        if settings["player_field_from"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(16, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(16, True)
        if settings["player_field_rating"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(17, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(17, True)
        if settings["player_field_volume"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(18, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(18, True)
        if settings["player_field_normalize"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(19, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(19, True)
        if settings["player_field_pan"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(20, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(20, True)
        if settings["player_field_frequencies"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(21, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(21, True)
        if settings["player_field_repeat"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(22, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(22, True)
        if settings["player_field_open_file"]==1:
            self.main_self.ui.player_list_table.setColumnHidden(23, False)
        else:
            self.main_self.ui.player_list_table.setColumnHidden(23, True)


        
class Main_Player_List_Emitter(QThread):
    player_list_fields = pyqtSignal(dict)

    def __init__(self, from_process: Pipe):
        super().__init__()
        self.data_from_process = from_process

    def run(self):
        while True:
            data = self.data_from_process.recv()
            if data["type"] == "player_list_fields":
            	self.player_list_fields.emit(data["settings"])
            

class Main_Player_List_Child_Proc(Process):
    
    def __init__(self, to_emitter, from_mother):
        super().__init__()
        self.daemon = False
        self.to_emitter = to_emitter
        self.data_from_mother = from_mother
        
    def run(self):
        while(True):
            data = self.data_from_mother.get()
            if data["type"] == "player_list_fields":
                self.player_list_fields()
           
    
    
    def player_list_fields(self):
        player_field_change_position = int(database_functions.read_setting("player_field_change_position")["current_value"])
        player_field_play = int(database_functions.read_setting("player_field_play")["current_value"])
        player_field_title = int(database_functions.read_setting("player_field_title")["current_value"])
        player_field_last_play = int(database_functions.read_setting("player_field_last_play")["current_value"])
        player_field_next_play = int(database_functions.read_setting("player_field_next_play")["current_value"])
        player_field_image = int(database_functions.read_setting("player_field_image")["current_value"])
        player_field_prepare = int(database_functions.read_setting("player_field_prepare")["current_value"])
        player_field_play_now = int(database_functions.read_setting("player_field_play_now")["current_value"])
        player_field_remove = int(database_functions.read_setting("player_field_remove")["current_value"])
        player_field_duration = int(database_functions.read_setting("player_field_duration")["current_value"])
        player_field_artist = int(database_functions.read_setting("player_field_artist")["current_value"])
        player_field_album = int(database_functions.read_setting("player_field_album")["current_value"])
        player_field_author = int(database_functions.read_setting("player_field_author")["current_value"])
        player_field_composer = int(database_functions.read_setting("player_field_composer")["current_value"])
        player_field_year = int(database_functions.read_setting("player_field_year")["current_value"])
        player_field_description = int(database_functions.read_setting("player_field_description")["current_value"])
        player_field_from = int(database_functions.read_setting("player_field_from")["current_value"])
        player_field_rating = int(database_functions.read_setting("player_field_rating")["current_value"])
        player_field_volume = int(database_functions.read_setting("player_field_volume")["current_value"])
        player_field_normalize = int(database_functions.read_setting("player_field_normalize")["current_value"])
        player_field_pan = int(database_functions.read_setting("player_field_pan")["current_value"])
        player_field_frequencies = int(database_functions.read_setting("player_field_frequencies")["current_value"])
        player_field_repeat = int(database_functions.read_setting("player_field_repeat")["current_value"])
        player_field_open_file = int(database_functions.read_setting("player_field_open_file")["current_value"])
        
        settings = {
            "player_field_change_position":player_field_change_position,
            "player_field_play":player_field_play,
            "player_field_title":player_field_title,
            "player_field_last_play":player_field_last_play,
            "player_field_next_play":player_field_next_play,
            "player_field_image":player_field_image,
            "player_field_prepare":player_field_prepare,
            "player_field_play_now":player_field_play_now,
            "player_field_remove":player_field_remove,
            "player_field_duration":player_field_duration,
            "player_field_artist":player_field_artist,
            "player_field_album":player_field_album,
            "player_field_author":player_field_author,
            "player_field_composer":player_field_composer,
            "player_field_year":player_field_year,
            "player_field_description":player_field_description,
            "player_field_from":player_field_from,
            "player_field_rating":player_field_rating,
            "player_field_volume":player_field_volume, 
            "player_field_normalize":player_field_normalize,
            "player_field_pan":player_field_pan,
            "player_field_frequencies":player_field_frequencies,
            "player_field_repeat":player_field_repeat,
            "player_field_open_file":player_field_open_file
        }
        
        self.to_emitter.send({"type":"player_list_fields","settings":settings})
