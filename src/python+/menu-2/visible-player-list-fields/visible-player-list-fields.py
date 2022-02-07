from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from multiprocessing import Process, Queue, Pipe
from PyQt5.QtCore import pyqtSignal, QThread
from datetime import datetime
import importlib

import sys
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
            self.main_self.visible_player_list_fields_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
            self.main_self.visible_player_list_fields_window.showMaximized()
            self.main_self.visible_player_list_fields_window.update()

            self.main_self.visible_player_list_fields_window.hide()
            self.main_self.visible_player_list_fields_window.show()

            self.save_in_progress = False
            self.need_save = False
            
            self.make_custom_groupBox()
            
            #create proccess for fetch and save player list fields settings
            self.proccess_number = 20
            self.player_list_fields_mother_pipe, self.player_list_fields_child_pipe = Pipe()
            self.player_list_fields_queue = Queue()
            self.player_list_fields_emitter = Player_List_Fields_Emitter(self.player_list_fields_mother_pipe)
            self.player_list_fields_emitter.start()
            self.player_list_fields_child_process = Player_List_Fields_Child_Proc(self.player_list_fields_child_pipe, self.player_list_fields_queue)
            self.player_list_fields_child_process.start()
            self.player_list_fields_emitter.settings_ready.connect(self.settings_ready)
            self.player_list_fields_emitter.save_finished.connect(self.save_finished)
            self.player_list_fields_emitter.error_signal.connect(lambda error_message:self.main_self.open_select_player_list_fields_error_window(error_message))
            
            
            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.proccess_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = self.player_list_fields_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1
                        
            self.main_self.ui_visible_player_list_fields_window.save.clicked.connect(lambda state:self.save(state))
            self.main_self.ui_visible_player_list_fields_window.cancel.clicked.connect(lambda state:self.main_self.visible_player_list_fields_window.close())
            

            
            self.main_self.visible_player_list_fields_window.closeEvent = lambda event:self.closeEvent(event)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

    def make_custom_groupBox(self):
        try:
            self.main_self.ui_visible_player_list_fields_window.gridLayout_2.removeWidget(self.main_self.ui_visible_player_list_fields_window.label_2)
            self.main_self.ui_visible_player_list_fields_window.gridLayout_2.addWidget(self.main_self.ui_visible_player_list_fields_window.label_2, 2, 0, 1, 1)
            
            self.main_self.ui_visible_player_list_fields_window.gridLayout_2.removeWidget(self.main_self.ui_visible_player_list_fields_window.frame_4)
            self.main_self.ui_visible_player_list_fields_window.gridLayout_2.addWidget(self.main_self.ui_visible_player_list_fields_window.frame_4, 3, 0, 1, 1)
            
            self.main_self.ui_visible_player_list_fields_window.groupBox = Custom_QGroupBox('Επιλογή όλων',main_self=self.main_self)
            self.main_self.ui_visible_player_list_fields_window.groupBox.toggled.connect(self.toggleCheckBoxes)
            self.main_self.ui_visible_player_list_fields_window.layout = QtWidgets.QGridLayout(self.main_self.ui_visible_player_list_fields_window.groupBox)

            self.main_self.ui_visible_player_list_fields_window.change_position = QtWidgets.QCheckBox('Αλλαγή θέσης')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.change_position)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.change_position, 0, 0)
            self.main_self.ui_visible_player_list_fields_window.change_position.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.play_or_skip = QtWidgets.QCheckBox('Αναπαραγωγή')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.play_or_skip)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.play_or_skip, 1, 0)
            self.main_self.ui_visible_player_list_fields_window.play_or_skip.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.title = QtWidgets.QCheckBox('Τίτλος (πάντα ορατό)')
            #self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.title)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.title, 2, 0)
            self.main_self.ui_visible_player_list_fields_window.title.stateChanged.connect(lambda state:self.settings_changed(state))
            self.main_self.ui_visible_player_list_fields_window.title.setEnabled(False)

            self.main_self.ui_visible_player_list_fields_window.last_play = QtWidgets.QCheckBox('Τελευταία εκτέλεση')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.last_play)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.last_play, 3, 0)
            self.main_self.ui_visible_player_list_fields_window.last_play.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.next_play = QtWidgets.QCheckBox('Επόμενη εκτέλεση')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.next_play)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.next_play, 4, 0)
            self.main_self.ui_visible_player_list_fields_window.next_play.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.image = QtWidgets.QCheckBox('Εικόνα')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.image)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.image, 5, 0)
            self.main_self.ui_visible_player_list_fields_window.image.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.prepare_play = QtWidgets.QCheckBox('Προετοιμασία για αναπαραγωγή')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.prepare_play)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.prepare_play, 6, 0)
            self.main_self.ui_visible_player_list_fields_window.prepare_play.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.play_now = QtWidgets.QCheckBox('Αναπαραγωγή τώρα')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.play_now)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.play_now, 7, 0)
            self.main_self.ui_visible_player_list_fields_window.play_now.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.delete_from_playlist = QtWidgets.QCheckBox('Αφαίρεση')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.delete_from_playlist)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.delete_from_playlist, 8, 0)
            self.main_self.ui_visible_player_list_fields_window.delete_from_playlist.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.duration = QtWidgets.QCheckBox('Διάρκεια')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.duration)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.duration, 9, 0)
            self.main_self.ui_visible_player_list_fields_window.duration.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.artist = QtWidgets.QCheckBox('Καλλιτέχνης')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.artist)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.artist, 10, 0)
            self.main_self.ui_visible_player_list_fields_window.artist.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.album = QtWidgets.QCheckBox('Λεύκωμα')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.album)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.album, 11, 0)
            self.main_self.ui_visible_player_list_fields_window.album.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.composer = QtWidgets.QCheckBox('Συνθέτης')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.composer)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.composer, 0, 1)
            self.main_self.ui_visible_player_list_fields_window.composer.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.author = QtWidgets.QCheckBox('Στιχουργός')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.author)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.author, 1, 1)
            self.main_self.ui_visible_player_list_fields_window.author.stateChanged.connect(lambda state:self.settings_changed(state))
            

            self.main_self.ui_visible_player_list_fields_window.year = QtWidgets.QCheckBox('Έτος')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.year)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.year, 2, 1)
            self.main_self.ui_visible_player_list_fields_window.year.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.description = QtWidgets.QCheckBox('Περιγραφή')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.description)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.description, 3, 1)
            self.main_self.ui_visible_player_list_fields_window.description.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.source = QtWidgets.QCheckBox('Πηγή')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.source)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.source, 4, 1)
            self.main_self.ui_visible_player_list_fields_window.source.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.rating = QtWidgets.QCheckBox('Αξιολόγηση')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.rating)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.rating, 5, 1)
            self.main_self.ui_visible_player_list_fields_window.rating.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.volume = QtWidgets.QCheckBox('Ένταση ήχου')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.volume)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.volume, 6, 1)
            self.main_self.ui_visible_player_list_fields_window.volume.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.normalize = QtWidgets.QCheckBox('Κανονικοποίηση')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.normalize)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.normalize, 7, 1)
            self.main_self.ui_visible_player_list_fields_window.normalize.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.pan = QtWidgets.QCheckBox('Στερεοφωνική ισοστάθμιση')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.pan)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.pan, 8, 1)
            self.main_self.ui_visible_player_list_fields_window.pan.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.band_pass_filter = QtWidgets.QCheckBox('Ζωνοπερατό φίλτρο')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.band_pass_filter)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.band_pass_filter, 9, 1)
            self.main_self.ui_visible_player_list_fields_window.band_pass_filter.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.repeat = QtWidgets.QCheckBox('Επανάληψη')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.repeat)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.repeat, 10, 1)
            self.main_self.ui_visible_player_list_fields_window.repeat.stateChanged.connect(lambda state:self.settings_changed(state))

            self.main_self.ui_visible_player_list_fields_window.file_location = QtWidgets.QCheckBox('Θέση αρχείου')
            self.main_self.ui_visible_player_list_fields_window.groupBox.addCheckBox(self.main_self.ui_visible_player_list_fields_window.file_location)
            self.main_self.ui_visible_player_list_fields_window.layout.addWidget(self.main_self.ui_visible_player_list_fields_window.file_location, 11, 1)
            self.main_self.ui_visible_player_list_fields_window.file_location.stateChanged.connect(lambda state:self.settings_changed(state))


            
            self.main_self.ui_visible_player_list_fields_window.gridLayout_2.addWidget(self.main_self.ui_visible_player_list_fields_window.groupBox, 1, 0, 1, 1)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

    def settings_changed(self,state):
        try:
            self.need_save = True
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

    def toggleCheckBoxes(self,on):
        try:
            self.need_save = True
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
        
    def settings_ready(self,settings):
        try:
            all_true = True
            if settings["player_field_change_position"]==1:
                self.main_self.ui_visible_player_list_fields_window.change_position.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.change_position.setCheckState(Qt.Unchecked)
                all_true = False
            
            if settings["player_field_play"]==1:
                self.main_self.ui_visible_player_list_fields_window.play_or_skip.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.play_or_skip.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_title"]==1:
                self.main_self.ui_visible_player_list_fields_window.title.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.title.setCheckState(Qt.Unchecked)
                all_true = False
            
            if settings["player_field_last_play"]==1:
                self.main_self.ui_visible_player_list_fields_window.last_play.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.last_play.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_next_play"]==1:
                self.main_self.ui_visible_player_list_fields_window.next_play.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.next_play.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_image"]==1:
                self.main_self.ui_visible_player_list_fields_window.image.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.image.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_prepare"]==1:
                self.main_self.ui_visible_player_list_fields_window.prepare_play.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.prepare_play.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_play_now"]==1:
                self.main_self.ui_visible_player_list_fields_window.play_now.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.play_now.setCheckState(Qt.Unchecked)
                all_true = False
            
            if settings["player_field_remove"]==1:
                self.main_self.ui_visible_player_list_fields_window.delete_from_playlist.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.delete_from_playlist.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_duration"]==1:
                self.main_self.ui_visible_player_list_fields_window.duration.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.duration.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_artist"]==1:
                self.main_self.ui_visible_player_list_fields_window.artist.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.artist.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_album"]==1:
                self.main_self.ui_visible_player_list_fields_window.album.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.album.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_author"]==1:
                self.main_self.ui_visible_player_list_fields_window.author.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.author.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_composer"]==1:
                self.main_self.ui_visible_player_list_fields_window.composer.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.composer.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_year"]==1:
                self.main_self.ui_visible_player_list_fields_window.year.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.year.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_description"]==1:
                self.main_self.ui_visible_player_list_fields_window.description.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.description.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_from"]==1:
                self.main_self.ui_visible_player_list_fields_window.source.setCheckState(Qt.Checked)            
            else:
                self.main_self.ui_visible_player_list_fields_window.source.setCheckState(Qt.Unchecked)
                all_true = False

            if settings["player_field_rating"]==1:
                self.main_self.ui_visible_player_list_fields_window.rating.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.rating.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_volume"]==1:
                self.main_self.ui_visible_player_list_fields_window.volume.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.volume.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_normalize"]==1:
                self.main_self.ui_visible_player_list_fields_window.normalize.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.normalize.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_pan"]==1:
                self.main_self.ui_visible_player_list_fields_window.pan.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.pan.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_frequencies"]==1:
                self.main_self.ui_visible_player_list_fields_window.band_pass_filter.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.band_pass_filter.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_repeat"]==1:
                self.main_self.ui_visible_player_list_fields_window.repeat.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.repeat.setCheckState(Qt.Unchecked)
                all_true = False
                
            if settings["player_field_open_file"]==1:
                self.main_self.ui_visible_player_list_fields_window.file_location.setCheckState(Qt.Checked)
            else:
                self.main_self.ui_visible_player_list_fields_window.file_location.setCheckState(Qt.Unchecked)
                all_true = False

            self.need_save = False
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
        
       
    def save(self,state):
        try:
            self.main_self.ui_visible_player_list_fields_window.groupBox.setEnabled(False)
            
            self.save_in_progress = True

            player_field_change_position = int(self.main_self.ui_visible_player_list_fields_window.change_position.isChecked())
            player_field_play = int(self.main_self.ui_visible_player_list_fields_window.play_or_skip.isChecked())
            player_field_title = int(self.main_self.ui_visible_player_list_fields_window.title.isChecked())
            player_field_last_play = int(self.main_self.ui_visible_player_list_fields_window.last_play.isChecked())
            player_field_next_play = int(self.main_self.ui_visible_player_list_fields_window.next_play.isChecked())
            player_field_image = int(self.main_self.ui_visible_player_list_fields_window.image.isChecked())
            player_field_prepare = int(self.main_self.ui_visible_player_list_fields_window.prepare_play.isChecked())
            player_field_play_now = int(self.main_self.ui_visible_player_list_fields_window.play_now.isChecked())
            player_field_remove = int(self.main_self.ui_visible_player_list_fields_window.delete_from_playlist.isChecked())
            player_field_duration = int(self.main_self.ui_visible_player_list_fields_window.duration.isChecked())
            player_field_artist = int(self.main_self.ui_visible_player_list_fields_window.artist.isChecked())
            player_field_album = int(self.main_self.ui_visible_player_list_fields_window.album.isChecked())
            player_field_author = int(self.main_self.ui_visible_player_list_fields_window.author.isChecked())
            player_field_composer = int(self.main_self.ui_visible_player_list_fields_window.composer.isChecked())
            player_field_year = int(self.main_self.ui_visible_player_list_fields_window.year.isChecked())
            player_field_description = int(self.main_self.ui_visible_player_list_fields_window.description.isChecked())
            player_field_from = int(self.main_self.ui_visible_player_list_fields_window.source.isChecked())
            player_field_rating = int(self.main_self.ui_visible_player_list_fields_window.rating.isChecked())
            player_field_volume = int(self.main_self.ui_visible_player_list_fields_window.volume.isChecked())
            player_field_normalize = int(self.main_self.ui_visible_player_list_fields_window.normalize.isChecked())
            player_field_pan = int(self.main_self.ui_visible_player_list_fields_window.pan.isChecked())
            player_field_frequencies = int(self.main_self.ui_visible_player_list_fields_window.band_pass_filter.isChecked())
            player_field_repeat = int(self.main_self.ui_visible_player_list_fields_window.repeat.isChecked())
            player_field_open_file = int(self.main_self.ui_visible_player_list_fields_window.file_location.isChecked())
                    
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
             
            self.player_list_fields_queue.put({"type":"save","settings":settings})
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

    def save_finished(self):
        try:
            self.main_self.manage_player_list_table_instance.main_player_list_queue.put({"type":"player_list_fields"})
        
            self.player_list_fields_child_process.terminate()
            self.player_list_fields_emitter.terminate()
            
            self.player_list_fields_child_process = None
            self.player_list_fields_emitter = None
            
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
            self.main_self.visible_player_list_fields_window.close()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)


    def close_window(self,state):
        self.main_self.visible_player_list_fields_window.close()

    def closeEvent(self,event):
        try:
            if self.save_in_progress:
                event.ignore()
                return 1

            if self.need_save == True:
                self.main_self.open_select_player_list_fields_save_question_window()
                
            if self.need_save == False:
                if self.player_list_fields_child_process is not None:
                    self.player_list_fields_child_process.terminate()
                    self.player_list_fields_emitter.terminate()
                    
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
                self.main_self.visible_player_list_fields_window_is_open = False
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

               

class Player_List_Fields_Emitter(QThread):
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
                
class Player_List_Fields_Child_Proc(Process):

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
            self.read_player_list_fields()
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
                
    def read_player_list_fields(self):
        try:
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
            self.main_self.open_select_player_list_fields_error_window(error_message)


    def addCheckBox(self, cb):
        try:
            self.checkBoxes.append(cb)
            cb.toggled.connect(self.update)
            cb.destroyed.connect(lambda: self.removeCheckBox(cb))
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

    def removeCheckBox(self, cb):
        try:
            self.checkBoxes.remove(cb)
            cb.toggled.disconnect(self.update)
        except Exception as e:
            pass
            error_message = str(traceback.format_exc())
            #self.main_self.open_select_player_list_fields_error_window(error_message)

    def allStates(self):
        try:
            return [cb.isChecked() for cb in self.checkBoxes]
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

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
            self.main_self.open_select_player_list_fields_error_window(error_message)

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
            self.main_self.open_select_player_list_fields_error_window(error_message)