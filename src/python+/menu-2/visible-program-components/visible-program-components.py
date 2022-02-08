from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from multiprocessing import Process, Queue, Pipe
from PyQt5.QtCore import pyqtSignal, QThread
from datetime import datetime
import importlib
import traceback

import sys

sys.path.append("../../")
sys.path.append("../../../")

database_functions = importlib.import_module("python+.lib.sqlite3_functions")

class Support_Ui_Dialog:

    def __init__(self,main_self):
        try:
            self.main_self = main_self
            
            #apply theme
            self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
            self.main_self.visible_programm_components_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
            self.main_self.visible_programm_components_window.showMaximized()
            self.main_self.visible_programm_components_window.update()

            self.main_self.visible_programm_components_window.show()
            self.main_self.visible_programm_components_window.hide()
            
            self.save_in_progress = False
            self.need_save = False
            
            
            #create proccess for fetch and save player list fields settings
            self.proccess_number = 22
            self.programm_components_mother_pipe, self.programm_components_child_pipe = Pipe()
            self.programm_components_queue = Queue()
            self.programm_components_emitter = Programm_Components_Emitter(self.programm_components_mother_pipe)
            self.programm_components_emitter.start()
            self.programm_components_child_process = Programm_Components_Child_Proc(self.programm_components_child_pipe, self.programm_components_queue)
            self.programm_components_child_process.start()
            self.programm_components_emitter.settings_ready.connect(self.settings_ready)
            self.programm_components_emitter.save_finished.connect(self.save_finished)
            self.programm_components_emitter.error_signal.connect(lambda error_message:self.main_self.open_select_programm_components_error_window(error_message))
            
            
            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.proccess_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = self.programm_components_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1
                
            self.make_custom_groupBox()
            
            self.main_self.ui_visible_programm_components_window.save.clicked.connect(lambda state:self.save(state))
            self.main_self.ui_visible_programm_components_window.cancel.clicked.connect(lambda state:self.main_self.visible_programm_components_window.close())

            
            self.main_self.visible_programm_components_window.closeEvent = lambda event:self.closeEvent(event)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def make_custom_groupBox(self):
        try:
            self.main_self.ui_visible_programm_components_window.gridLayout_2.removeWidget(self.main_self.ui_visible_programm_components_window.label_2)
            self.main_self.ui_visible_programm_components_window.gridLayout_2.addWidget(self.main_self.ui_visible_programm_components_window.label_2, 2, 0, 1, 1)
            
            self.main_self.ui_visible_programm_components_window.gridLayout_2.removeWidget(self.main_self.ui_visible_programm_components_window.frame_4)
            self.main_self.ui_visible_programm_components_window.gridLayout_2.addWidget(self.main_self.ui_visible_programm_components_window.frame_4, 3, 0, 1, 1)
            
            self.main_self.ui_visible_programm_components_window.groupBox = Custom_QGroupBox('Επιλογή όλων')
            self.main_self.ui_visible_programm_components_window.groupBox.toggled.connect(self.toggleCheckBoxes)
            self.main_self.ui_visible_programm_components_window.layout = QtWidgets.QGridLayout(self.main_self.ui_visible_programm_components_window.groupBox)

            self.main_self.ui_visible_programm_components_window.timeline_widget = QtWidgets.QCheckBox('Time lines')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.timeline_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.timeline_widget, 0, 0)
            self.main_self.ui_visible_programm_components_window.timeline_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.general_deck_widget = QtWidgets.QCheckBox('General deck')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.general_deck_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.general_deck_widget, 1, 0)
            self.main_self.ui_visible_programm_components_window.general_deck_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.deck_1_widget = QtWidgets.QCheckBox('Deck 1')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.deck_1_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.deck_1_widget, 2, 0)
            self.main_self.ui_visible_programm_components_window.deck_1_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.deck_2_widget = QtWidgets.QCheckBox('Deck 2')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.deck_2_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.deck_2_widget, 3, 0)
            self.main_self.ui_visible_programm_components_window.deck_2_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.music_clip_widget = QtWidgets.QCheckBox('Music clip deck')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.music_clip_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.music_clip_widget, 4, 0)
            self.main_self.ui_visible_programm_components_window.music_clip_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.speackers_deck_widget = QtWidgets.QCheckBox('Speackers deck')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.speackers_deck_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.speackers_deck_widget, 0, 1)
            self.main_self.ui_visible_programm_components_window.speackers_deck_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.ip_calls_widget = QtWidgets.QCheckBox('Τηλεφωνικές κλήσεις')
            #self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.ip_calls_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.ip_calls_widget, 1, 1)
            self.main_self.ui_visible_programm_components_window.ip_calls_widget.stateChanged.connect(lambda state:self.settings_changed(state))
            self.main_self.ui_visible_programm_components_window.ip_calls_widget.setEnabled(False)

            self.main_self.ui_visible_programm_components_window.player_list_widget = QtWidgets.QCheckBox('Player list')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.player_list_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.player_list_widget, 2, 1)
            self.main_self.ui_visible_programm_components_window.player_list_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.web_pages_widget = QtWidgets.QCheckBox('Σελίδες ακρόασης')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.web_pages_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.web_pages_widget, 3, 1)
            self.main_self.ui_visible_programm_components_window.web_pages_widget.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget = QtWidgets.QCheckBox('Προγραμματισμένες μεταδόσεις')
            self.main_self.ui_visible_programm_components_window.groupBox.addCheckBox(self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget)
            self.main_self.ui_visible_programm_components_window.layout.addWidget(self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget, 4, 1)
            self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget.stateChanged.connect(lambda state:self.settings_changed(state))
            
            self.main_self.ui_visible_programm_components_window.gridLayout_2.addWidget(self.main_self.ui_visible_programm_components_window.groupBox, 1, 0, 1, 1)

            self.need_save = False
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def settings_changed(self,state):
        try:
            self.need_save = True
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def toggleCheckBoxes(self,on):
        try:
            self.need_save = False
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)
        
    def settings_ready(self,settings):
        try:
            all_true = True
            if settings["program_component_time_lines"]==1:
                self.main_self.ui_visible_programm_components_window.timeline_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.timeline_widget.setCheckState(Qt.Unchecked)
                all_true = False
            
            if settings["program_component_general_deck"]==1:
                self.main_self.ui_visible_programm_components_window.general_deck_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.general_deck_widget.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["program_component_deck_1"]==1:
                self.main_self.ui_visible_programm_components_window.deck_1_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.deck_1_widget.setCheckState(Qt.Unchecked)
                all_true = False
            
            if settings["program_component_deck_2"]==1:
                self.main_self.ui_visible_programm_components_window.deck_2_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.deck_2_widget.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["program_component_music_clip_deck"]==1:
                self.main_self.ui_visible_programm_components_window.music_clip_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.music_clip_widget.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["program_component_speackers_deck"]==1:
                self.main_self.ui_visible_programm_components_window.speackers_deck_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.speackers_deck_widget.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["program_component_ip_calls"]==1:
                self.main_self.ui_visible_programm_components_window.ip_calls_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.ip_calls_widget.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["program_component_player_list"]==1:
                self.main_self.ui_visible_programm_components_window.player_list_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.player_list_widget.setCheckState(Qt.Unchecked)
                all_true = False
            
            if settings["program_component_web_sites"]==1:
                self.main_self.ui_visible_programm_components_window.web_pages_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.web_pages_widget.setCheckState(Qt.Unchecked)
                all_true = False

            if settings["program_component_scheduled_transmitions"]==1:
                self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget.setCheckState(Qt.Unchecked)
                all_true = False
            self.need_save = False
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)
       
    def save(self,state):
        try:
            self.main_self.ui_visible_programm_components_window.groupBox.setEnabled(False)
            
            self.save_in_progress = True

            program_component_time_lines = int(self.main_self.ui_visible_programm_components_window.timeline_widget.isChecked())
            program_component_general_deck = int(self.main_self.ui_visible_programm_components_window.general_deck_widget.isChecked())
            program_component_deck_1 = int(self.main_self.ui_visible_programm_components_window.deck_1_widget.isChecked())
            program_component_deck_2 = int(self.main_self.ui_visible_programm_components_window.deck_2_widget.isChecked())
            program_component_music_clip_deck = int(self.main_self.ui_visible_programm_components_window.music_clip_widget.isChecked())
            program_component_speackers_deck = int(self.main_self.ui_visible_programm_components_window.speackers_deck_widget.isChecked())
            program_component_ip_calls = int(self.main_self.ui_visible_programm_components_window.ip_calls_widget.isChecked())
            program_component_player_list = int(self.main_self.ui_visible_programm_components_window.player_list_widget.isChecked())
            program_component_web_sites = int(self.main_self.ui_visible_programm_components_window.web_pages_widget.isChecked())
            program_component_scheduled_transmitions =int(self.main_self.ui_visible_programm_components_window.scheduled_transmitions_widget.isChecked())
            
                    
            settings = {
                "program_component_time_lines":program_component_time_lines,
                "program_component_general_deck":program_component_general_deck,
                "program_component_deck_1":program_component_deck_1,
                "program_component_deck_2":program_component_deck_2,
                "program_component_music_clip_deck":program_component_music_clip_deck,
                "program_component_speackers_deck":program_component_speackers_deck,
                "program_component_ip_calls":program_component_ip_calls,
                "program_component_player_list":program_component_player_list,
                "program_component_web_sites":program_component_web_sites,
                "program_component_scheduled_transmitions":program_component_scheduled_transmitions,
            }
             
            self.programm_components_queue.put({"type":"save","settings":settings})
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def save_finished(self):
        try:
            self.main_self.programm_components.programm_components_queue.put({"type":"programm_components"})
        
            self.programm_components_child_process.terminate()
            self.programm_components_emitter.terminate()
            
            self.programm_components_child_process = None
            self.programm_components_emitter = None
            
            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.proccess_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = None
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = None
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "stopped"
                        self.main_self.manage_processes_instance.processes[counter]["cpu"] = 0
                        self.main_self.manage_processes_instance.processes[counter]["ram"] = 0
                counter += 1
            
            self.need_save = False
            self.save_in_progress = False
            self.main_self.visible_programm_components_window.close()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)
           
    def close_window(self,state):
        self.main_self.visible_programm_components_window.close()


    def closeEvent(self,event):
        try:
            if self.save_in_progress:
                event.ignore()
                return 1
             
            if self.need_save == True:
                self.main_self.open_visible_programm_components_save_question_window()
                
            if self.need_save == False:
                if self.programm_components_child_process is not None:
                    self.programm_components_child_process.terminate()
                    self.programm_components_emitter.terminate()
                    
                    counter = 0
                    for process in self.main_self.manage_processes_instance.processes:
                        if "process_number" in process:
                            if process["process_number"]==self.proccess_number:
                                self.main_self.manage_processes_instance.processes[counter]["pid"] = None
                                self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = None
                                self.main_self.manage_processes_instance.processes[counter]["status"] = "stopped"
                                self.main_self.manage_processes_instance.processes[counter]["cpu"] = 0
                                self.main_self.manage_processes_instance.processes[counter]["ram"] = 0
                        counter += 1


                
                self.need_save = False
                self.main_self.visible_program_components_window_is_open = False
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)
                        
class Programm_Components_Emitter(QThread):
    try:
        settings_ready = pyqtSignal(dict)
        save_finished = pyqtSignal()
        error_signal = pyqtSignal(str)
    except Exception as e:
        pass

    def __init__(self, from_process: Pipe):
        try:
            super().__init__()
            self.data_from_process = from_process
        except Exception as e:
            pass

    def run(self):
        try:
            while True:
                data = self.data_from_process.recv()
                if data["type"]=="settings_ready":
                    self.settings_ready.emit(data["settings"])
                elif data["type"] == "save_finished":
                    self.save_finished.emit()
                elif data["type"] == "error":
                    self.error_signal.emit(data["error_message"])
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.error_signal.emit(error_message)
            except Exception as e:
                pass
                
class Programm_Components_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass
        
    def run(self):
        try:
            self.read_programm_components()
            while(True):
                data = self.data_from_mother.get()
                if data["type"] == "save":
                    self.save_data(data["settings"])
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass
                
    def read_programm_components(self):
        try:
            program_component_time_lines = int(database_functions.read_setting("program_component_time_lines")["current_value"])
            program_component_general_deck = int(database_functions.read_setting("program_component_general_deck")["current_value"])
            program_component_deck_1 = int(database_functions.read_setting("program_component_deck_1")["current_value"])
            program_component_deck_2 = int(database_functions.read_setting("program_component_deck_2")["current_value"])
            program_component_music_clip_deck = int(database_functions.read_setting("program_component_music_clip_deck")["current_value"])
            program_component_speackers_deck = int(database_functions.read_setting("program_component_speackers_deck")["current_value"])
            program_component_ip_calls = int(database_functions.read_setting("program_component_ip_calls")["current_value"])
            program_component_player_list = int(database_functions.read_setting("program_component_player_list")["current_value"])
            program_component_web_sites = int(database_functions.read_setting("program_component_web_sites")["current_value"])
            program_component_scheduled_transmitions = int(database_functions.read_setting("program_component_scheduled_transmitions")["current_value"])
            
            settings = {
                "program_component_time_lines":program_component_time_lines,
                "program_component_general_deck":program_component_general_deck,
                "program_component_deck_1":program_component_deck_1,
                "program_component_deck_2":program_component_deck_2,
                "program_component_music_clip_deck":program_component_music_clip_deck,
                "program_component_speackers_deck":program_component_speackers_deck,
                "program_component_ip_calls":program_component_ip_calls,
                "program_component_player_list":program_component_player_list,
                "program_component_web_sites":program_component_web_sites,
                "program_component_scheduled_transmitions":program_component_scheduled_transmitions
            }
            
            self.to_emitter.send({"type":"settings_ready","settings":settings})
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass

    def save_data(self,settings):
        try:
            for setting_key in settings:
                database_functions.update_setting({"current_value":settings[setting_key],"keyword":setting_key})
            
            self.to_emitter.send({"type":"save_finished"})
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass

class Custom_QGroupBox(QtWidgets.QGroupBox):
    checkAllIfAny = True
    def __init__(self,title,main_self=None):
        try:
            self.main_self = main_self
            super(Custom_QGroupBox, self).__init__(title=title,parent=None)
            self.setCheckable(True)
            self.checkBoxes = []
            self.toggled.connect(self.toggleCheckBoxes)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)


    def addCheckBox(self, cb):
        try:
            self.checkBoxes.append(cb)
            cb.toggled.connect(self.update)
            cb.destroyed.connect(lambda: self.removeCheckBox(cb))
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def removeCheckBox(self, cb):
        try:
            self.checkBoxes.remove(cb)
            cb.toggled.disconnect(self.update)
        except Exception as e:
            pass
            error_message = str(traceback.format_exc())
            #self.main_self.open_select_programm_components_error_window(error_message)

    def allStates(self):
        try:
            return [cb.isChecked() for cb in self.checkBoxes]
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def toggleCheckBoxes(self):
        try:
            if self.checkAllIfAny:
                state = not all(self.allStates())
            else:
                state = not any(self.allStates())

            for widget in self.children():
                if not widget.isWidgetType():
                    continue
                if not widget.testAttribute(QtCore.Qt.WA_ForceDisabled):
                    # restore the enabled state in order to override the default
                    # behavior of setChecked(False); previous explicit calls for
                    # setEnabled(False) on the target widget will be ignored
                    widget.setEnabled(True)
                    if widget in self.checkBoxes:
                        widget.setChecked(state)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)

    def paintEvent(self, event):
        try:
            opt = QtWidgets.QStyleOptionGroupBox()
            self.initStyleOption(opt)
            states = self.allStates()
            if all(states):
                # force the "checked" state
                opt.state |= QtWidgets.QStyle.State_On
                opt.state &= ~QtWidgets.QStyle.State_Off
            else:
                # force the "not checked" state
                opt.state &= ~QtWidgets.QStyle.State_On
                if any(states):
                    # force the "not unchecked" state and set the tristate mode
                    opt.state &= ~QtWidgets.QStyle.State_Off
                    opt.state |= QtWidgets.QStyle.State_NoChange
                else:
                    # force the "unchecked" state
                    opt.state |= QtWidgets.QStyle.State_Off
            painter = QtWidgets.QStylePainter(self)
            painter.drawComplexControl(QtWidgets.QStyle.CC_GroupBox, opt)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_programm_components_error_window(error_message)