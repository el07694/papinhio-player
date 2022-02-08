from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
from qt_material import list_themes
from multiprocessing import Process, Queue, Pipe
from PyQt5.QtCore import pyqtSignal, QThread
import sys
import os
from datetime import datetime
import time
import importlib
import traceback


sys.path.append("../../")
sys.path.append("../../../")

database_functions = importlib.import_module("python+.lib.sqlite3_functions")

class Support_Ui_Dialog:

    def __init__(self,main_self):
        try:
            self.main_self = main_self
            
            #apply theme
            self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
            self.main_self.choose_theme_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
            self.main_self.choose_theme_window.showMaximized()
            self.main_self.choose_theme_window.update()

            self.need_save = False
            self.save_in_progress = False

            self.main_self.choose_theme_window.resize(676, 456)
            self.main_self.choose_theme_window.hide()
            self.main_self.choose_theme_window.show()
            
            self.default_font = self.main_self.default_font
            self.default_font_size = self.main_self.default_font_size
            self.default_font_color = self.main_self.default_font_color
            self.default_background_color = self.main_self.default_background_color
            self.default_buttons_background = self.main_self.default_buttons_background
            self.default_buttons_font_color = self.main_self.default_buttons_font_color
            self.default_style = self.main_self.default_style
            self.default_custome_theme = self.main_self.default_custome_theme

            self.main_self.ui_choose_theme_window.font.setCurrentFont(self.font)
            self.main_self.ui_choose_theme_window.font_size.setValue(int(self.default_font_size))
            self.main_self.ui_choose_theme_window.font_size.setMinimum(6)
            self.main_self.ui_choose_theme_window.font_size.setMaximum(40)
            self.main_self.ui_choose_theme_window.font_size.valueChanged.connect(lambda new_font_size:self.font_size_changed(new_font_size))

            self.factor_styles = QtWidgets.QStyleFactory.keys()
            counter = 0
            for factor_style in self.factor_styles:
                self.main_self.ui_choose_theme_window.style.addItem(factor_style)
                if(factor_style==self.default_style):
                    self.main_self.ui_choose_theme_window.style.setCurrentIndex(counter)
                counter += 1
                
            self.main_self.ui_choose_theme_window.style.currentIndexChanged.connect(lambda index:self.current_style_changed(index))
            self.custom_themes = list_themes()
            counter = 1
            for custom_theme in self.custom_themes:
                self.main_self.ui_choose_theme_window.qt_material_themes.addItem(custom_theme)
                if custom_theme == self.default_custome_theme:
                    self.main_self.ui_choose_theme_window.qt_material_themes.setCurrentIndex(counter)
                counter += 1


            self.main_self.ui_choose_theme_window.font_colour.clicked.connect(lambda state:self.text_color_changed(state))
            self.main_self.ui_choose_theme_window.background_colour.clicked.connect(lambda state:self.background_color_changed(state))

            self.main_self.ui_choose_theme_window.button_background_colour.clicked.connect(lambda state:self.button_background_changed(state))
            self.main_self.ui_choose_theme_window.button_font_colour.clicked.connect(lambda state:self.button_text_color_changed(state))

            self.main_self.ui_choose_theme_window.font.currentFontChanged.connect(lambda new_font:self.current_font_changed(new_font))

            self.main_self.ui_choose_theme_window.qt_material_themes.currentIndexChanged.connect(lambda index:self.custom_theme_changed(index))

            self.main_self.ui_choose_theme_window.save.clicked.connect(lambda state:self.save(state))

            self.main_self.ui_choose_theme_window.cancel.clicked.connect(lambda state:self.close_window(state))
            
            #create process
            self.process_number = 13
            self.choose_theme_mother_pipe, self.choose_theme_child_pipe = Pipe()
            self.choose_theme_queue = Queue()
            self.choose_theme_emitter = Choose_Theme_Emitter(self.choose_theme_mother_pipe)
            self.choose_theme_emitter.start()
            self.choose_theme_child_process = Choose_Theme_Child_Proc(self.choose_theme_child_pipe, self.choose_theme_queue)
            self.choose_theme_child_process.start()
            self.choose_theme_emitter.save_finished.connect(self.save_finished)
            self.choose_theme_emitter.error_signal.connect(lambda error_message:self.main_self.open_choose_theme_error_window(error_message))
            
            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.process_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = self.choose_theme_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            
            
            self.main_self.choose_theme_window.closeEvent = lambda event:self.closeEvent(event)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
        
    def font_size_changed(self,new_font_size):
        try:
            index = self.main_self.ui_choose_theme_window.qt_material_themes.currentIndex()
            self.default_font_size = self.main_self.ui_choose_theme_window.font_size.value()
            if index==0:
                self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
            else:
                self.custom_theme_changed(index)
            self.need_save = True
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
        
    def current_style_changed(self,index):
        try:
            self.default_style = self.factor_styles[index]
            self.main_self.app.setStyle(self.default_style)
            self.need_save = True
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
    
    def text_color_changed(self,state):
        try:
            color = QtWidgets.QColorDialog.getColor()

            if color.isValid():
                self.default_font_color = color.name()
                self.need_save = True
                index = self.main_self.ui_choose_theme_window.qt_material_themes.currentIndex()
                if index==0:
                    self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
                else:
                    self.custom_theme_changed(index)
            else:
                pass
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
   
    def background_color_changed(self,state):
        try:
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                self.default_background_color = color.name()
                self.need_save = True
                index = self.main_self.ui_choose_theme_window.qt_material_themes.currentIndex()
                if index==0:
                    self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
                else:
                    self.custom_theme_changed(index)
            else:
                pass
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
        
    def button_background_changed(self,state):
        try:
            color = QtWidgets.QColorDialog.getColor()

            if color.isValid():
                self.default_buttons_background = color.name()
                self.need_save = True
                index = self.main_self.ui_choose_theme_window.qt_material_themes.currentIndex()
                if index==0:
                    self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
                else:
                    self.custom_theme_changed(index)
            else:
                pass
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
        
    def button_text_color_changed(self,state):
        try:
            color = QtWidgets.QColorDialog.getColor()

            if color.isValid():
                self.default_buttons_font_color = color.name()
                self.need_save = True
                index = self.main_self.ui_choose_theme_window.qt_material_themes.currentIndex()
                if index==0:
                    self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
                else:
                    self.custom_theme_changed(index)
            else:
                pass
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
            
    def current_font_changed(self,new_font):
        try:
            self.default_font = self.main_self.ui_choose_theme_window.font.currentFont().family()
            self.need_save = True
            index = self.main_self.ui_choose_theme_window.qt_material_themes.currentIndex()
            if index==0:
                self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
            else:
                self.custom_theme_changed(index)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
        
    def custom_theme_changed(self,index):
        try:
           self.need_save = True
           if index == 0:
                self.default_custome_theme = ""
           else:        
                self.default_custome_theme = self.main_self.ui_choose_theme_window.qt_material_themes.currentText()
           if index != 0:
                self.main_self.app.setStyle("")
                self.main_self.app.setStyleSheet("")
                self.main_self.choose_theme_window.setStyleSheet("")
                apply_stylesheet(self.main_self.app, theme=self.default_custome_theme)
           else:
                self.main_self.app.setStyle("")
                self.main_self.app.setStyleSheet("")
                self.main_self.choose_theme_window.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+str(self.default_font_size)+"px;color:\""+self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)

    def save(self,state):
        try:
            self.save_in_progress = True
            self.choose_theme_queue.put({"type":"save","default_font":self.default_font,"default_font_size":self.default_font_size,"default_font_color":self.default_font_color,"default_background_color":self.default_background_color,"default_buttons_background":self.default_buttons_background,"default_buttons_font_color":self.default_buttons_font_color,"default_style":self.default_style,"default_custome_theme":self.default_custome_theme})
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)

    def save_finished(self):
        try:
            self.need_save = False
            self.save_in_progress = False
            self.main_self.apply_theme_settings()

            if self.main_self.visible_player_list_fields_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.visible_player_list_fields_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.visible_player_list_fields_window.showMaximized()
                self.main_self.visible_player_list_fields_window.update()

            if self.main_self.select_player_list_fields_save_question_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.select_player_list_fields_save_question_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.select_player_list_fields_save_question_window.showMaximized()
                self.main_self.select_player_list_fields_save_question_window.update()

            if self.main_self.visible_player_list_fields_error_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.visible_player_list_fields_error_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.visible_player_list_fields_error_window.showMaximized()
                self.main_self.visible_player_list_fields_error_window.update()

            if self.main_self.visible_program_components_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.visible_programm_components_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.visible_programm_components_window.showMaximized()
                self.main_self.visible_programm_components_window.update()


            if self.main_self.select_visible_programm_components_save_question_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.select_visible_programm_components_save_question_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.select_visible_programm_components_save_question_window.showMaximized()
                self.main_self.select_visible_programm_components_save_question_window.update()

            if self.main_self.visible_programm_components_error_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.visible_programm_components_error_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.visible_programm_components_error_window.showMaximized()
                self.main_self.visible_programm_components_error_window.update()

            if self.main_self.programm_abstract_information_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.programm_abstract_information_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.programm_abstract_information_window.showMaximized()
                self.main_self.programm_abstract_information_window.update()

            if self.main_self.programm_abstract_information_error_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.programm_abstract_information_error_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.programm_abstract_information_error_window.showMaximized()
                self.main_self.programm_abstract_information_error_window.update()

            if self.main_self.contact_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.contact_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.contact_window.showMaximized()
                self.main_self.contact_window.update()

            if self.main_self.contact_error_window_is_open:
                #apply theme
                self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
                self.main_self.contact_error_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
                self.main_self.contact_error_window.showMaximized()
                self.main_self.contact_error_window.update()

            self.close_window(None)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_choose_theme_error_window(error_message)
        
    def close_window(self,state):
        self.main_self.choose_theme_window.close()

    def closeEvent(self,event):
        if self.save_in_progress:
            event.ignore()
            return 1

        if self.need_save == True:
            self.main_self.open_change_theme_save_question_window()
            event.ignore()
            
        if self.need_save == False:
            if self.choose_theme_child_process is not None:
                self.choose_theme_child_process.terminate()
                self.choose_theme_emitter.terminate()
                
                counter = 0
                for process in self.main_self.manage_processes_instance.processes:
                    if "process_number" in process:
                        if process["process_number"]==self.process_number:
                            self.main_self.manage_processes_instance.processes[counter]["pid"] = None
                            self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = None
                            self.main_self.manage_processes_instance.processes[counter]["status"] = "stopped"
                            self.main_self.manage_processes_instance.processes[counter]["cpu"] = 0
                            self.main_self.manage_processes_instance.processes[counter]["ram"] = 0
                    counter += 1
            
            self.need_save = False
            self.main_self.choose_theme_window_is_open = False
            event.accept()
        else:
            event.ignore()


class Choose_Theme_Emitter(QThread):
    try:
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
                if data["type"]=="save_finished":
                    self.save_finished.emit()
                else:
                    self.error_signal.emit(data["error_message"])
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.error_signal.emit(error_message)
            except Exception as e:
                pass
        
class Choose_Theme_Child_Proc(Process):

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
            data = self.data_from_mother.get()
            self.save_theme_settings(data)
            while True:
                time.sleep(1)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type":"error","error_message":error_message})
            
    def save_theme_settings(self,data):
        try:
            for key in data:
                if key!="save":
                    database_functions.update_setting({"keyword":key,"current_value":data[key]})
            self.to_emitter.send({"type":"error","type":"save_finished"})
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type":"error","error_message":error_message})