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
database_functions = importlib.import_module("Αρχεία κώδικα python (Python files).Συναρτήσεις sqlite3 (Sqlite3 functions)")
label_clickable = importlib.import_module("Βοηθητικές συναρτήσεις (Ηelpful functions).Label clickable")
when_to_play_function = importlib.import_module("Βοηθητικές συναρτήσεις (Ηelpful functions).Εύρεση επόμενης εκτέλεσης ώρα Ελλάδας (find next when to play Greece time)")
convert_time_function = importlib.import_module("Βοηθητικές συναρτήσεις (Ηelpful functions).Μετατροπή από milliseconds σε ανθρώπινη μορφή (Convert time function)")
convert_bytes_function = importlib.import_module("Βοηθητικές συναρτήσεις (Ηelpful functions).Μετατροπή από bytes σε αναγνώσιμη μορφή (convert bytes for read)")

class Manage_Player_List_Table:

    def __init__(self,main_self):
        self.main_self = main_self
        
        self.main_self.ui.player_list_frame.setEnabled(False)
        self.player_list_data = []
        self.saves_in_progress = 0
        self.quit_requested = False
        
        self.data_fetched = False
        self.settings_saved = False
        
        self.repeat_player_list = False
        
        self.main_self.ui.player_list_inner_frame.hide()
        self.main_self.ui.player_list_table.hide()
        
        #on player_list_repeat change
        self.main_self.ui.general_deck_repeat_player_list_checkbox.stateChanged.connect(lambda state:self.player_list_repeat_changed(state))
        self.main_self.ui.player_list_repeat_checkbox.stateChanged.connect(lambda state:self.player_list_repeat_changed(state))

        #create proccess for main player list
        self.proccess_number = 12
        self.main_player_list_mother_pipe, self.main_player_list_child_pipe = Pipe()
        self.main_player_list_queue = Queue()
        self.main_player_list_emitter = Main_Player_List_Emitter(self.main_player_list_mother_pipe)
        self.main_player_list_emitter.start()
        self.main_player_list_child_process = Main_Player_List_Child_Proc(self.main_player_list_child_pipe, self.main_player_list_queue)
        self.main_player_list_child_process.start()
        self.main_player_list_emitter.player_list_data_fetched.connect(self.player_list_data_fetched)
        self.main_player_list_emitter.repeat_and_auto_dj_settings.connect(self.repeat_and_auto_dj_settings)
        self.main_player_list_emitter.search_results.connect(self.search_results)
        self.main_player_list_emitter.proccess_save_finished.connect(self.proccess_save_finished)
        self.main_player_list_emitter.metrics.connect(self.display_player_list_frame_information)
        self.main_player_list_emitter.insert_finished.connect(self.insert_finished)
        self.main_player_list_emitter.update_time_row.connect(self.update_time_row)
        self.main_player_list_emitter.insert_and_play_finished.connect(self.insert_and_play_finished)
        self.main_player_list_emitter.player_list_fields.connect(self.display_player_list_fields)
        self.main_player_list_emitter.next_play.connect(self.display_next_play)
        #self.main_player_list_emitter.last_player_history.connect(self.main_self.manage_decks_instance.last_player_history)


        self.main_self.ui.player_list_mode.currentIndexChanged.connect(lambda index:self.display_mode_changed(index))
  
        ### QListWidget ###
        self.selected_row = -1
        
        #self.main_self.ui.listWidget.setModel(QtGui.QStandardItemModel())
        self.delegate = Delegate(self.main_self.ui.listWidget)
        #self.main_self.ui.listWidget.setModel(QtGui.QStandardItemModel())
        self.main_self.ui.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_self.ui.player_list_select_all.setTristate(False)
        self.delegate.checked.connect(self.list_widget_play_changed)
        
        self.main_self.ui.listWidget.setItemDelegate(self.delegate)
        self.main_self.ui.listWidget.model().rowsMoved.connect(self.list_widget_row_moved)
        
        self.main_self.ui.player_list_play_now_checkbox.stateChanged.connect(lambda state:self.list_widget_play_now_changed(state))
        self.main_self.ui.player_list_prepare_deck_1.clicked.connect(lambda state:self.list_widget_prepare_deck_1(state))
        self.main_self.ui.player_list_prepare_deck_2.clicked.connect(lambda state:self.list_widget_prepare_deck_2(state))
        self.main_self.ui.player_list_prepare_music_clip_deck.clicked.connect(lambda state:self.list_widget_prepare_music_clip_deck(state))
        self.main_self.ui.player_list_play_now_deck_1.clicked.connect(lambda state:self.list_widget_prepare_and_play_deck_1(state))
        self.main_self.ui.player_list_play_now_deck_2.clicked.connect(lambda state:self.list_widget_prepare_and_play_deck_2(state))
        self.main_self.ui.player_list_play_now_music_clip_deck.clicked.connect(lambda state:self.list_widget_prepare_and_play_music_clip_deck(state))
        self.main_self.ui.player_list_remove_button.clicked.connect(lambda state:self.list_widget_remove_clicked(state))
        self.main_self.ui.player_list_volume_slider.valueChanged.connect(lambda slider_value:self.list_widget_volume_moved(slider_value))
        self.main_self.ui.player_list_volume_slider.sliderReleased.connect(lambda:self.list_widget_volume_released())
        self.main_self.ui.player_list_reset_volume.clicked.connect(lambda state:self.list_widget_reset_volume(state))
        self.main_self.ui.player_list_normalize_checkbox.stateChanged.connect(lambda new_state:self.list_widget_normalize_changed(new_state))
        self.main_self.ui.player_list_pan_slider.valueChanged.connect(lambda slider_value:self.list_widget_pan_changed(slider_value))
        self.main_self.ui.player_list_pan_slider.sliderReleased.connect(lambda:self.list_widget_pan_released())
        self.main_self.ui.player_list_reset_pan.clicked.connect(lambda state:self.list_widget_reset_pan(state))
        self.main_self.ui.player_list_low_frequency_spinbox.valueChanged.connect(lambda low_frequency:self.list_widget_low_frequency_changed(low_frequency))
        self.main_self.ui.player_list_high_frequency_spinbox.valueChanged.connect(lambda high_frequency:self.list_widget_high_frequency_changed(high_frequency))
        self.main_self.ui.player_list_apply_filter.clicked.connect(lambda state:self.list_widget_apply_filter(state))
        self.main_self.ui.player_list_reset_filter.clicked.connect(lambda state:self.list_widget_reset_filter(state))
        self.main_self.ui.player_list_repeats_button.clicked.connect(lambda state:self.list_widget_repeats_changed(state))
        self.main_self.ui.player_list_open_file_button.clicked.connect(lambda state:self.list_widget_open_file_folder(state))
        self.make_list_widget_rating_stars()

        #QTableWidget
        self.main_self.ui.player_list_table.currentCellChanged.connect(lambda row,column:self.player_list_table_selected_item_change(row,column))
        
        #on search
        self.main_self.ui.player_list_search_button.clicked.connect(lambda state:self.search_player_list_table(state))

        #on show all
        self.main_self.ui.player_list_clear_search.clicked.connect(lambda state:self.clear_player_list_search(state))
        
        #auto_dj
        self.auto_dj = 0
        #watch(self.auto_dj)
        self.main_self.ui.general_deck_manage_auto_dj_button.clicked.connect(lambda state:self.auto_dj_state_changed("button"))
        self.main_self.ui.player_list_auto_dj_checkbox.clicked.connect(lambda state:self.auto_dj_state_changed("checkbox"))
        
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

    def insert_and_play_finished(self,relative_type,relative_number,player_list_item,deck):
        self.player_list_data.insert(0,player_list_item)
        if deck=="deck_1":
            self.prepare_and_play_deck_1(None,player_list_item["player_number"])
        elif deck=="deck_2":
            self.prepare_and_play_deck_2(None,player_list_item["player_number"])
        elif deck=="music_clip_deck":
            self.load_track_to_music_clip_deck(None,player_list_item["player_number"])
            
        self.main_self.manage_decks_instance.general_deck_next_player_list_items()

    def update_time_row(self,row,player_list_row):
        self.proccess_save_finished()
        self.player_list_data[row] = player_list_row
        self.main_self.ui.listWidget.item(row).setText(player_list_row["current_time_item"]["title"])
        if self.selected_row == row:
            self.list_widget_changed(self.main_self.ui.listWidget.item(row),None)
            
        #2. QTableWidget
        self.main_self.ui.player_list_table.removeRow(row)
        del self.player_list_position[row]
        del self.player_list_image[row]
        del self.player_list_play[row]
        del self.player_list_play_now[row]
        del self.player_list_remove[row]
        del self.player_list_volume[row]
        del self.player_list_rating[row]
        del self.player_list_speed[row]
        del self.player_list_normalize[row]
        del self.player_list_pan[row]
        del self.player_list_frequencies[row]
        del self.player_list_repeat[row]
        del self.player_list_open_file[row]
        self.display_player_list_row(row,player_list_row,insert_new_row=True)
        self.player_list_position = []
        for row in range(0,self.player_list_data_length):
            #Change position cell
            self.player_list_position.append({})
            column_counter = 0
            change_position_frame = QtWidgets.QFrame()
            change_position_frame.setMinimumHeight(150)
            verticalLayout = QtWidgets.QVBoxLayout(change_position_frame)
            
            if(row!=0):
                self.player_list_position[row]["move up"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move up"].setMinimumHeight(50)
                self.player_list_position[row]["move up"].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move up"].setIcon(icon)
                verticalLayout.addWidget(self.player_list_position[row]["move up"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move up"].clicked.connect(lambda state,start_row=row,end_row=row-1: self.move_table_row(state,start_row,end_row))

            if(row!=self.player_list_data_length-1):
                self.player_list_position[row]["move down"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move down"].setMinimumHeight(50)
                self.player_list_position[row]["move down"].setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move down"].setIcon(icon1)
                verticalLayout.addWidget(self.player_list_position[row]["move down"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move down"].clicked.connect(lambda state,start_row=row,end_row=row+1: self.move_table_row(state,start_row,end_row))

            change_position_frame.setStyleSheet("QFrame{border:0;padding:10px 10px 10px 10px;background:transparent;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,change_position_frame)

        self.main_self.ui.player_list_table.resizeRowsToContents()
        self.main_self.ui.player_list_table.resizeColumnsToContents()

    def insert_finished(self,relative_type,relative_number,play,player_list_row):
        self.player_list_data.insert(0,player_list_row)
        if play==1:
            if relative_type=="sound_clips":
                self.main_self.manage_decks_instance.prepare_and_play_music_clip_deck(self.player_list_data[0])

        self.main_self.manage_decks_instance.general_deck_next_player_list_items()

    def repeat_and_auto_dj_settings(self,repeat_player_list,auto_dj):
        self.repeat_player_list = repeat_player_list
        if self.auto_dj==1:
            self.repeat_player_list_old = repeat_player_list
        if self.repeat_player_list==1 or self.repeat_player_list==True:
            self.main_self.ui.general_deck_repeat_player_list_checkbox.setCheckState(Qt.Checked)
        else:
            self.main_self.ui.general_deck_repeat_player_list_checkbox.setCheckState(Qt.Unchecked)
            
        self.repeat_player_list_old = self.repeat_player_list
        if auto_dj == 1 or auto_dj == True or auto_dj:
            self.auto_dj = 1
            if self.data_fetched == True:
                self.auto_dj_state_changed(auto_dj)
        else:
        
            self.auto_dj = 0
            
            
        self.settings_saved = True
 
    def player_list_data_fetched(self,rows,display_mode,items_count,duration_count,size_count,all_false,all_true):       
        self.main_self.ui.player_list_select_all.blockSignals(True)
        if all_false == True:
            self.main_self.ui.player_list_select_all.setCheckState(Qt.Unchecked)
        elif all_true == True:
            self.main_self.ui.player_list_select_all.setCheckState(Qt.Checked)
        else:
            self.main_self.ui.player_list_select_all.setCheckState(Qt.PartiallyChecked)
        self.main_self.ui.player_list_select_all.blockSignals(False)
        self.all_false = all_false
        self.all_true = all_true
        
        self.display_player_list_frame_information(items_count,duration_count,size_count)
        self.player_list_data = rows
        self.player_list_data_length = len(rows)
        
        self.make_player_list_table()
        self.make_player_list_list()

       
        
        index = self.main_self.ui.player_list_mode.findText(display_mode)
        self.main_self.ui.player_list_mode.setCurrentIndex(index)
        self.display_mode = display_mode
        
        self.main_self.ui.listWidget.currentItemChanged.connect(lambda current,previous:self.list_widget_changed(current,previous))
        
        self.main_self.ui.player_list_frame.setEnabled(True)
        
        if display_mode == "Προβολή λίστας":
            self.main_self.ui.player_list_table.hide()
            self.main_self.ui.player_list_inner_frame.show()
        else:
            self.main_self.ui.player_list_table.show()
            self.main_self.ui.player_list_inner_frame.hide()
        
        self.data_fetched = True
        if self.settings_saved:
            
            if self.auto_dj == 1 or self.auto_dj==True:
                
                self.auto_dj_state_changed(self.auto_dj)
                
        self.main_self.manage_decks_instance.manage_decks_saves_queue.put({"type":"decks_state"})
        
        self.main_self.manage_decks_instance.set_greek_timer_function()
        
        self.main_self.manage_decks_instance.general_deck_next_player_list_items()
    
    ### QListWidget ###

    def make_player_list_list(self):
        self.hidden_rows = []

        while(self.main_self.ui.listWidget.count()>0):
            self.main_self.ui.listWidget.takeItem(0)
              
        counter = 0
        for player_list_row in self.player_list_data:
            if "current_time_item" in player_list_row:
                item = player_list_row["current_time_item"]
            else:
                item = player_list_row["details"]
            if player_list_row["relative_type"]=="retransmitions":
                item["duration_milliseconds"] = player_list_row["duration_milliseconds"]
                item["duration_human"] = player_list_row["duration_human"]
            self.main_self.ui.listWidget.addItem(item["title"]+" ("+item["duration_human"]+")")
            self.main_self.ui.listWidget.item(counter).setFlags(self.main_self.ui.listWidget.item(counter).flags() | Qt.ItemIsUserCheckable)
            if player_list_row["play"] == 0:
                self.main_self.ui.listWidget.item(counter).setBackground(QtGui.QBrush(QtGui.QColor(255,228,228), Qt.SolidPattern))
                self.main_self.ui.listWidget.item(counter).setCheckState(Qt.Unchecked)
            else:
                self.main_self.ui.listWidget.item(counter).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255), Qt.SolidPattern))
                self.main_self.ui.listWidget.item(counter).setCheckState(Qt.Checked)
                
            #self.main_self.ui.listWidget.item(counter).dataChanged.connect(self.list_widget_play_changed)
            
            counter += 1
        
        if self.player_list_data_length>0:
            self.main_self.ui.listWidget.setCurrentRow(0)            
        
        self.main_self.ui.player_list_select_all.stateChanged.connect(lambda state:self.list_widget_select_all_checkbox_clicked(state))
        
        self.list_widget_changed(self.main_self.ui.listWidget.item(0),None)

    def list_widget_changed(self,current,previous):
        if self.main_self.ui.listWidget.row(current)==-1:
            return 1
        if(self.player_list_data_length!=len(self.player_list_data)):
            return 1
        row = self.main_self.ui.listWidget.row(current)
        self.selected_row = row
        
        self.main_self.ui.player_list_table.selectRow(self.selected_row)
        player_list_row = self.player_list_data[row]
        
        if "current_time_item" in player_list_row:
            item = player_list_row["current_time_item"]
        else:
            item = player_list_row["details"]
        
        #Image
        image_path_found = False
        
        if "image_path" in item:
            if item["image_path"]!="":
                if os.path.exists(item["image_path"]):
                    pixmap = QtGui.QPixmap(item["image_path"]).scaledToHeight(260)
                    self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                    image_path_found = True
                else:
                    image_path_found = False
            else:
                image_path_found = False
        else:
            image_path_found = False
            
        if image_path_found == False:
            if player_list_row["relative_type"]=="sound_clips":
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/deck_image.png").scaledToHeight(150)
                self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                image_path_found = True
            elif player_list_row["relative_type"]=="weather_news":
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/weather.png").scaledToHeight(150)
                self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                image_path_found = True  
            elif player_list_row["relative_type"]=="church_news":
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/church.png").scaledToHeight(150)
                self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                image_path_found = True
            elif player_list_row["relative_type"]=="time_collections":
                now = datetime.now()
                now_hour = now.hour
                now_minute = now.minute
                Greece_time_case = int(player_list_row["details"][0]["case"])
                if Greece_time_case == 1 or Greece_time_case==2:
                    next_Greece_time_announcement_hour = now_hour+1
                    next_Greece_time_announcement_minute = 0
                else:
                    if now_minute<30:
                        next_Greece_time_announcement_hour = now_hour
                        next_Greece_time_announcement_minute = 30
                    else:
                        next_Greece_time_announcement_hour = now_hour+1
                        next_Greece_time_announcement_minute = 0
                if next_Greece_time_announcement_minute ==0:
                    if next_Greece_time_announcement_hour==1 or next_Greece_time_announcement_hour==13:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-01.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==2 or next_Greece_time_announcement_hour==14:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-02.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==3 or next_Greece_time_announcement_hour==15:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-03.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==4 or next_Greece_time_announcement_hour==16:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-04.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==5 or next_Greece_time_announcement_hour==17:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-05.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==6 or next_Greece_time_announcement_hour==18:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-06.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==7 or next_Greece_time_announcement_hour==19:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-07.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==8 or next_Greece_time_announcement_hour==20:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-08.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==9 or next_Greece_time_announcement_hour==21:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-09.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==10 or next_Greece_time_announcement_hour==22:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-10.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==11 or next_Greece_time_announcement_hour==23:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-11.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==12 or next_Greece_time_announcement_hour==24:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-12.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                else:
                    if next_Greece_time_announcement_hour==1 or next_Greece_time_announcement_hour==13:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-01-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==2 or next_Greece_time_announcement_hour==14:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-02-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==3 or next_Greece_time_announcement_hour==15:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-03-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==4 or next_Greece_time_announcement_hour==16:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-04-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==5 or next_Greece_time_announcement_hour==17:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-05-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==6 or next_Greece_time_announcement_hour==18:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-06-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==7 or next_Greece_time_announcement_hour==19:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-07-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==8 or next_Greece_time_announcement_hour==20:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-08-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==9 or next_Greece_time_announcement_hour==21:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-09-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==10 or next_Greece_time_announcement_hour==22:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-10-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==11 or next_Greece_time_announcement_hour==23:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-11-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==12 or next_Greece_time_announcement_hour==24:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-12-30.png").scaledToHeight(150)
                        self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                        image_path_found = True
            elif player_list_row["relative_type"]=="station_logos":
                #may be changed
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/deck_image.png").scaledToHeight(150)
                self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                image_path_found = True
            else:
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/deck_image.png").scaledToHeight(150)
                self.main_self.ui.player_list_image_label.setPixmap(pixmap)
                image_path_found = True
                
        if "image_title" in item:
            self.main_self.ui.player_list_image_title.setText(str(item["image_title"]))
        else:
            self.main_self.ui.player_list_image_title.setText(str(item["title"]))

        #title
        self.main_self.ui.player_list_title_text.setText(str(item["title"]))
        
        #artist
        if "artist" in item:
            self.main_self.ui.player_list_artist_text.setText(str(item["artist"]))
        else:
            self.main_self.ui.player_list_artist_text.setText("")
            
        #composer
        if "composer" in item:
            self.main_self.ui.player_list_composer_text.setText(str(item["composer"]))
        else:
            self.main_self.ui.player_list_composer_text.setText("")

        #author
        if "author" in item:
            self.main_self.ui.player_list_author_text.setText(str(item["author"]))
        else:
            self.main_self.ui.player_list_author_text.setText("")
            
        #album
        if "album" in item:
            self.main_self.ui.player_list_album_text.setText(str(item["album"]))
        else:
            self.main_self.ui.player_list_album_text.setText("")
            
        #duration
        self.main_self.ui.player_list_duration_text.setText(str(item["duration_human"]))
        
        #year
        if "year" in item:
            self.main_self.ui.player_list_year_text.setText(str(item["year"]))
        else:
            self.main_self.ui.player_list_year_text.setText("")

        #description
        if "description" in item:
            self.main_self.ui.player_list_description_text.setText(str(item["description"]))
        else:
            self.main_self.ui.player_list_description_text.setText("")
            
        #source
        if "from" in item:
            self.main_self.ui.player_list_source_text.setText(str(item["from"]))
        else:
            self.main_self.ui.player_list_source_text.setText("")

        #last play
        self.main_self.ui.player_list_last_play_text.setText(str(player_list_row["last_play"]))
        
        #next_play
        if self.auto_dj == 1:
            if "next_play" in player_list_row:
                self.main_self.ui.next_play_time_text.setText(str(player_list_row["next_play"]))
            else:
                self.main_self.ui.next_play_time_text.setText("")
        else:
            self.main_self.ui.next_play_time_text.setText("")
                
        #play
        play = int(player_list_row["play"])
        if play == 1 or play == True:
            self.main_self.ui.player_list_play_now_checkbox.setCheckState(Qt.Checked)
        else:
            self.main_self.ui.player_list_play_now_checkbox.setCheckState(Qt.Unchecked)


        #load to deck
        if player_list_row["relative_type"]=="sound_clips" or player_list_row["relative_type"]=="time_collections":
            self.main_self.ui.player_list_prepare_deck_1.hide()
            self.main_self.ui.player_list_prepare_deck_2.hide()
            self.main_self.ui.player_list_prepare_music_clip_deck.show()
        else:
            self.main_self.ui.player_list_prepare_deck_1.show()
            self.main_self.ui.player_list_prepare_deck_2.show()
            self.main_self.ui.player_list_prepare_music_clip_deck.hide()
            
        #play now
        if player_list_row["relative_type"] == "sound_clips" or player_list_row["relative_type"]=="time_collections":
            self.main_self.ui.player_list_play_now_deck_1.hide()
            self.main_self.ui.player_list_play_now_deck_2.hide()
            self.main_self.ui.player_list_play_now_music_clip_deck.show()
        else:
            self.main_self.ui.player_list_play_now_deck_1.show()
            self.main_self.ui.player_list_play_now_deck_2.show()
            self.main_self.ui.player_list_play_now_music_clip_deck.hide()
        
        #rating
        self.list_widget_rating_changed(None,int(item["rating"]))
        
        #sound volume
        volume = int(item["volume"])
        self.main_self.ui.player_list_volume_slider.setValue(volume)
        self.main_self.ui.player_list_volume_text.setText(str(volume)+"/200")
        
        #normalize
        normalize = int(item["normalize"])
        if normalize == 1 or normalize == True:
            self.main_self.ui.player_list_normalize_checkbox.setCheckState(Qt.Checked)
        else:
            self.main_self.ui.player_list_normalize_checkbox.setCheckState(Qt.Unchecked)

        #pan
        pan = int(item["pan"])
        self.main_self.ui.player_list_pan_slider.setValue(pan)
        self.main_self.ui.player_list_pan_text.setText(str(pan))
        
        #filter
        low_frequency = int(item["low_frequency"])
        high_frequency = int(item["high_frequency"])
        self.main_self.ui.player_list_low_frequency_spinbox.setMaximum(20000)
        self.main_self.ui.player_list_high_frequency_spinbox.setMinimum(20)
        self.main_self.ui.player_list_low_frequency_spinbox.setValue(low_frequency)
        self.main_self.ui.player_list_high_frequency_spinbox.setValue(high_frequency)
        self.main_self.ui.player_list_low_frequency_spinbox.setMaximum(high_frequency)
        self.main_self.ui.player_list_high_frequency_spinbox.setMinimum(low_frequency)
        
        #repeats
        if player_list_row["relative_type"] == "time_collections":
            self.main_self.ui.player_list_repeats_frame.hide()
        else:
            self.main_self.ui.player_list_repeats_frame.show()

        repeats = int(player_list_row["repeats"])
        self.main_self.ui.player_list_repeats_spinbox.setValue(repeats)
        
        #file location
        if player_list_row["relative_type"] == "retransmitions":
            self.main_self.ui.player_list_open_file_button.hide()
        else:
            self.main_self.ui.player_list_open_file_button.show()

    def list_widget_select_all_checkbox_clicked(self,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if state==Qt.Checked:
            play = 1
        else:
            play = 0
            
        #1. Player list table
        counter = 0
        for player_list_row in self.player_list_data:
            self.player_list_data[counter]["play"] = play
            counter += 1
            
        #2. QListWidget
        self.main_self.ui.player_list_play_now_checkbox.setCheckState(state)
        for row in range(0,len(self.player_list_data)):
            self.delegate.checked.disconnect()
            self.main_self.ui.listWidget.item(row).setCheckState(state)
            self.delegate.checked.connect(self.list_widget_play_changed)
            if play == 0:
                self.main_self.ui.listWidget.item(row).setBackground(QtGui.QBrush(QtGui.QColor(255,228,228), Qt.SolidPattern))
            else:
                self.main_self.ui.listWidget.item(row).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255), Qt.SolidPattern))
                
           
        
        #3. QTableWidget
        for row in range(0,len(self.player_list_data)):
            self.player_list_play[row]["play checkbox"].blockSignals(True)
            self.player_list_play[row]["play checkbox"].setCheckState(state)
            self.player_list_play[row]["play checkbox"].blockSignals(False)
            
        #4. Process table + database save
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"select_all","play":play})
        
        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            
                       
    def list_widget_play_now_changed(self,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if state==Qt.Checked:
            play = 1
        else:
            play = 0
            
        #1. Player list table
        self.player_list_data[self.selected_row]["play"] = play
            
        #2. QListWidget
        self.delegate.checked.disconnect()
        self.main_self.ui.listWidget.item(self.selected_row).setCheckState(state)
        self.delegate.checked.connect(self.list_widget_play_changed)
        if play == 0:
            self.main_self.ui.listWidget.item(self.selected_row).setBackground(QtGui.QBrush(QtGui.QColor(255,228,228), Qt.SolidPattern))
        else:
            self.main_self.ui.listWidget.item(self.selected_row).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255), Qt.SolidPattern))
    
        #3. QTableWidget
        self.player_list_play[self.selected_row]["play checkbox"].blockSignals(True)
        self.player_list_play[self.selected_row]["play checkbox"].setCheckState(state)
        self.player_list_play[self.selected_row]["play checkbox"].blockSignals(False)
            
        #4. Process table + database save
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"play","play":play,"player_number":self.player_list_data[self.selected_row]["player_number"]})

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
                
    def list_widget_play_changed(self,index,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        index = index.row()
        if state==Qt.Checked:
            play = 1
        else:
            play = 0
            
        #1. Player list table
        self.player_list_data[index]["play"] = play
            
        #2. QListWidget
        if index == self.selected_row:
            self.delegate.checked.disconnect()
            self.main_self.ui.listWidget.item(self.selected_row).setCheckState(state)
            self.delegate.checked.connect(self.list_widget_play_changed)
            if play == 0:
                self.main_self.ui.listWidget.item(self.selected_row).setBackground(QtGui.QBrush(QtGui.QColor(255,228,228), Qt.SolidPattern))
            else:
                self.main_self.ui.listWidget.item(self.selected_row).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255), Qt.SolidPattern))
        
        #3. QTableWidget
        self.player_list_play[index]["play checkbox"].blockSignals(True)
        self.player_list_play[index]["play checkbox"].setCheckState(state)
        self.player_list_play[index]["play checkbox"].blockSignals(False)
            
        #4. Process table + database save
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"play","play":play,"player_number":self.player_list_data[index]["player_number"]})

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
       
    def list_widget_row_moved(self,parent,start,end,destination,row):       
        self.main_self.ui.player_list_frame.setEnabled(False)
        start_row = end
        end_row = row
        if start_row<end_row:
            end_row = end_row - 1
        
        self.selected_row = end_row
        #1. Player list table
        item_full = self.player_list_data[start_row]
        if item_full["relative_type"]=="time_collections":
            item = item_full["current_time_item"]
        else:
            item = item_full["details"]
        del self.player_list_data[start_row]
        self.player_list_data.insert(end_row,item_full)
        
        #2. QTableWidget
        self.main_self.ui.player_list_table.removeRow(start_row)
        del self.player_list_position[start_row]
        del self.player_list_image[start_row]
        del self.player_list_play[start_row]
        del self.player_list_play_now[start_row]
        del self.player_list_remove[start_row]
        del self.player_list_volume[start_row]
        del self.player_list_rating[start_row]
        del self.player_list_speed[start_row]
        del self.player_list_normalize[start_row]
        del self.player_list_pan[start_row]
        del self.player_list_frequencies[start_row]
        del self.player_list_repeat[start_row]
        del self.player_list_open_file[start_row]
        self.display_player_list_row(end_row,item_full,insert_new_row=True)
        self.player_list_position = []
        for row in range(0,self.player_list_data_length):
            #Change position cell
            self.player_list_position.append({})
            column_counter = 0
            change_position_frame = QtWidgets.QFrame()
            change_position_frame.setMinimumHeight(150)
            verticalLayout = QtWidgets.QVBoxLayout(change_position_frame)
            
            if(row!=0):
                self.player_list_position[row]["move up"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move up"].setMinimumHeight(50)
                self.player_list_position[row]["move up"].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move up"].setIcon(icon)
                verticalLayout.addWidget(self.player_list_position[row]["move up"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move up"].clicked.connect(lambda state,start_row=row,end_row=row-1: self.move_table_row(state,start_row,end_row))

            if(row!=self.player_list_data_length-1):
                self.player_list_position[row]["move down"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move down"].setMinimumHeight(50)
                self.player_list_position[row]["move down"].setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move down"].setIcon(icon1)
                verticalLayout.addWidget(self.player_list_position[row]["move down"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move down"].clicked.connect(lambda state,start_row=row,end_row=row+1: self.move_table_row(state,start_row,end_row))

            change_position_frame.setStyleSheet("QFrame{border:0;padding:10px 10px 10px 10px;background:transparent;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,change_position_frame)

        self.main_self.ui.player_list_table.resizeRowsToContents()
        self.main_self.ui.player_list_table.resizeColumnsToContents()
        
        #3. QListWidget
        self.main_self.ui.listWidget.setCurrentRow(end_row)
        
            
        #4. save row move in database
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"move","start":start_row,"end":end_row})
        
        self.main_self.manage_decks_instance.general_deck_next_player_list_items()

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})

    def list_widget_prepare_deck_1(self,state):
        self.main_self.manage_decks_instance.deck_1_play_requested = False
        self.main_self.manage_decks_instance.prepare_deck_1(self.player_list_data[self.selected_row])

        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,self.player_list_data[self.selected_row]["player_number"])
        else:
            self.move_table_row(None,self.selected_row,self.player_list_data_length-1)
        
    def list_widget_prepare_deck_2(self,state):
        self.main_self.manage_decks_instance.deck_2_play_requested = False
        self.main_self.manage_decks_instance.prepare_deck_2(self.player_list_data[self.selected_row])

        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,self.player_list_data[self.selected_row]["player_number"])
        else:
            self.move_table_row(None,self.selected_row,self.player_list_data_length-1)
            
    def list_widget_prepare_music_clip_deck(self,state):
        self.main_self.manage_decks_instance.music_clip_deck_play_requested = False
        self.main_self.manage_decks_instance.prepare_music_clip_deck(self.player_list_data[self.selected_row])

        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,self.player_list_data[self.selected_row]["player_number"])
        else:
            self.move_table_row(None,self.selected_row,self.player_list_data_length-1)
            
    def list_widget_prepare_and_play_deck_1(self,state):
        self.main_self.manage_decks_instance.prepare_and_play_deck_1(self.player_list_data[self.selected_row])

        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,self.player_list_data[self.selected_row]["player_number"])
        else:
            self.move_table_row(None,self.selected_row,self.player_list_data_length-1)

    def list_widget_prepare_and_play_deck_2(self,state):
        self.main_self.manage_decks_instance.prepare_and_play_deck_2(self.player_list_data[self.selected_row])

        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,self.player_list_data[self.selected_row]["player_number"])
        else:
            self.move_table_row(None,self.selected_row,self.player_list_data_length-1)

    def list_widget_prepare_and_play_music_clip_deck(self,state):
        self.main_self.manage_decks_instance.prepare_and_play_music_clip_deck(self.player_list_data[self.selected_row])

        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,self.player_list_data[self.selected_row]["player_number"])
        else:
            self.move_table_row(None,self.selected_row,self.player_list_data_length-1)

    def list_widget_remove_clicked(self,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        current_row = self.selected_row
        player_number = self.player_list_data[current_row]["player_number"]
        
        #1. Player list table
        del self.player_list_data[current_row]
        self.player_list_data_length -= 1

        #2. QTableWidget
        self.main_self.ui.player_list_table.removeRow(current_row)
        del self.player_list_position[current_row]
        del self.player_list_image[current_row]
        del self.player_list_play[current_row]
        del self.player_list_play_now[current_row]
        del self.player_list_remove[current_row]
        del self.player_list_volume[current_row]
        del self.player_list_rating[current_row]
        del self.player_list_speed[current_row]
        del self.player_list_normalize[current_row]
        del self.player_list_pan[current_row]
        del self.player_list_frequencies[current_row]
        del self.player_list_repeat[current_row]
        del self.player_list_open_file[current_row]
        self.player_list_position = []
        for row in range(0,self.player_list_data_length):
            #Change position cell
            self.player_list_position.append({})
            column_counter = 0
            change_position_frame = QtWidgets.QFrame()
            change_position_frame.setMinimumHeight(150)
            verticalLayout = QtWidgets.QVBoxLayout(change_position_frame)
            
            if(row!=0):
                self.player_list_position[row]["move up"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move up"].setMinimumHeight(50)
                self.player_list_position[row]["move up"].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move up"].setIcon(icon)
                verticalLayout.addWidget(self.player_list_position[row]["move up"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move up"].clicked.connect(lambda state,start_row=row,end_row=row-1: self.move_table_row(state,start_row,end_row))

            if(row!=self.player_list_data_length-1):
                self.player_list_position[row]["move down"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move down"].setMinimumHeight(50)
                self.player_list_position[row]["move down"].setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move down"].setIcon(icon1)
                verticalLayout.addWidget(self.player_list_position[row]["move down"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move down"].clicked.connect(lambda state,start_row=row,end_row=row+1: self.move_table_row(state,start_row,end_row))

            change_position_frame.setStyleSheet("QFrame{border:0;padding:10px 10px 10px 10px;background:transparent;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,change_position_frame)

        self.main_self.ui.player_list_table.resizeRowsToContents()
        self.main_self.ui.player_list_table.resizeColumnsToContents()
        if current_row!=self.player_list_data_length:
            self.main_self.ui.player_list_table.selectRow(current_row)
        else:
            self.main_self.ui.player_list_table.selectRow(self.player_list_data_length)
        
        #3. QListWidget
        if current_row!=self.player_list_data_length:#not the last
            self.main_self.ui.listWidget.blockSignals(True)
            self.selected_row = current_row
            self.main_self.ui.listWidget.takeItem(current_row)
            self.main_self.ui.listWidget.blockSignals(False)
            self.main_self.ui.listWidget.setCurrentRow(current_row)
            self.list_widget_changed(self.main_self.ui.listWidget.item(current_row),None)          
        else:
            self.main_self.ui.listWidget.blockSignals(True)
            self.selected_row = self.player_list_data_length-1
            self.main_self.ui.listWidget.takeItem(current_row)
            self.main_self.ui.listWidget.blockSignals(False)
            self.main_self.ui.listWidget.setCurrentRow(self.player_list_data_length-1)
            self.list_widget_changed(self.main_self.ui.listWidget.item(self.player_list_data_length),None)
            
        
        #4. Process table and database
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"delete","player_number":player_number})
        
        self.main_self.manage_decks_instance.general_deck_next_player_list_items()

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
        
    def list_widget_volume_moved(self,volume):
        self.main_self.ui.player_list_volume_text.setText(str(volume)+"/200")
        
    def list_widget_volume_changed(self,volume,save=True):
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["volume"] = volume
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["volume"] = volume
        
        self.main_self.ui.player_list_volume_slider.blockSignals(True)
        self.main_self.ui.player_list_volume_slider.setValue(volume)
        self.main_self.ui.player_list_volume_slider.blockSignals(False)
        self.main_self.ui.player_list_volume_text.setText(str(volume)+"/200")
         
        if save==True:
            self.main_self.ui.player_list_frame.setEnabled(False)        
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                
                    self.main_self.ui.deck_1_volume_slider.blockSignals(True)
                    self.main_self.ui.deck_1_volume_slider.setValue(volume)
                    self.main_self.ui.deck_1_volume_label.setText(str(volume)+"/200")
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["volume"] = volume
                    self.main_self.ui.deck_1_volume_slider.blockSignals(False)                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_volume_slider.blockSignals(True)
                    self.main_self.ui.deck_2_volume_slider.setValue(volume)
                    self.main_self.ui.deck_2_volume_label.setText(str(volume)+"/200")
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["volume"] = volume
                    self.main_self.ui.deck_2_volume_slider.blockSignals(False) 
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["volume"] = volume
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["volume"] = volume
                        
                    self.main_self.ui.music_clip_deck_volume_slider.blockSignals(True)
                    self.main_self.ui.music_clip_deck_volume_slider.setValue(volume)
                    self.main_self.ui.music_clip_deck_volume_label.setText(str(volume)+"/200")
                    self.main_self.ui.music_clip_deck_volume_slider.blockSignals(False) 
                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"volume","relative_number":relative_number,"relative_type":relative_type,"volume":volume,"save":False})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    self.player_list_volume_changed(player_list_row["player_number"],volume,save=False)
                            
    def list_widget_volume_released(self):
        volume = self.main_self.ui.player_list_volume_slider.value()
        return self.list_widget_volume_changed(volume,save=True)
        
    def list_widget_reset_volume(self,state):
        volume = 100
        return self.list_widget_volume_changed(volume,save=True)
        
    def list_widget_normalize_changed(self,new_state,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if new_state == Qt.Checked:
            normalize = 1
        else:
            normalize = 0
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["normalize"] = normalize
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["normalize"] = normalize
        
        self.main_self.ui.player_list_normalize_checkbox.blockSignals(True)
        self.main_self.ui.player_list_normalize_checkbox.setCheckState(new_state)
        self.main_self.ui.player_list_normalize_checkbox.blockSignals(False)
         
        if save==True:
        
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                
                    self.main_self.ui.deck_1_normalize_checkbox.blockSignals(True)
                    self.main_self.ui.deck_1_normalize_checkbox.setCheckState(new_state)
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["normalize"] = normalize
                    self.main_self.ui.deck_1_normalize_checkbox.blockSignals(False)                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_normalize_checkbox.blockSignals(True)
                    self.main_self.ui.deck_2_normalize_checkbox.setCheckState(new_state)
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["normalize"] = normalize
                    self.main_self.ui.deck_2_normalize_checkbox.blockSignals(False) 
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["normalize"] = normalize
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["normalize"] = normalize
                        
                    self.main_self.ui.music_clip_deck_normalize_checkbox.blockSignals(True)
                    self.main_self.ui.music_clip_deck_normalize_checkbox.setCheckState(new_state)
                    self.main_self.ui.music_clip_deck_normalize_checkbox.blockSignals(False) 
                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"normalize","relative_number":relative_number,"relative_type":relative_type,"normalize":normalize,"save":save})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    self.player_list_normalize_changed(player_list_row["player_number"],new_state,save=False)
                                
    def list_widget_pan_changed(self,pan,save=True):
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["pan"] = pan
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["pan"] = pan
        
        self.main_self.ui.player_list_pan_slider.blockSignals(True)
        self.main_self.ui.player_list_pan_slider.setValue(pan)
        self.main_self.ui.player_list_pan_slider.blockSignals(False)
        self.main_self.ui.player_list_pan_text.setText(str(pan))
         
        if save==True:
            self.main_self.ui.player_list_frame.setEnabled(False)
        
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                
                    self.main_self.ui.deck_1_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_1_pan_slider.setValue(pan)
                    self.main_self.ui.deck_1_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_1_pan_slider.blockSignals(False)                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_2_pan_slider.setValue(pan)
                    self.main_self.ui.deck_2_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_2_pan_slider.blockSignals(False) 
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["pan"] = pan
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["pan"] = pan
                        
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(True)
                    self.main_self.ui.music_clip_deck_pan_slider.setValue(pan)
                    self.main_self.ui.music_clip_deck_pan_label.setText(str(pan))
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(False) 
                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"pan","relative_number":relative_number,"relative_type":relative_type,"pan":pan,"save":True})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                    self.player_list_pan_changed(pan,player_list_row["player_number"],save=False)
        
    def list_widget_pan_released(self):
        pass
        
    def list_widget_reset_pan(self,state,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        pan = 0
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["pan"] = pan
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["pan"] = pan
        
        self.main_self.ui.player_list_pan_slider.blockSignals(True)
        self.main_self.ui.player_list_pan_slider.setValue(pan)
        self.main_self.ui.player_list_pan_slider.blockSignals(False)
        self.main_self.ui.player_list_pan_text.setText(str(pan))
         
        if save==True:
        
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                
                    self.main_self.ui.deck_1_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_1_pan_slider.setValue(pan)
                    self.main_self.ui.deck_1_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_1_pan_slider.blockSignals(False)                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_2_pan_slider.setValue(pan)
                    self.main_self.ui.deck_2_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_2_pan_slider.blockSignals(False) 
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["pan"] = pan
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["pan"] = pan
                        
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(True)
                    self.main_self.ui.music_clip_deck_pan_slider.setValue(pan)
                    self.main_self.ui.music_clip_deck_pan_label.setText(str(pan))
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(False) 
                    
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"pan","relative_number":relative_number,"relative_type":relative_type,"pan":pan,"save":True})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                    self.player_list_pan_changed(pan,player_list_row["player_number"],save=False)
        
    def list_widget_low_frequency_changed(self,low_frequency):
        self.main_self.ui.player_list_high_frequency_spinbox.setMinimum(low_frequency)
        
    def list_widget_high_frequency_changed(self,high_frequency):
        self.main_self.ui.player_list_low_frequency_spinbox.setMaximum(high_frequency)
        
    def list_widget_apply_filter(self,state,low_frequency=None,high_frequency=None,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if low_frequency == None:
            low_frequency = self.main_self.ui.player_list_low_frequency_spinbox.value()
        if high_frequency == None:
            high_frequency = self.main_self.ui.player_list_high_frequency_spinbox.value()
            
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["low_frequency"] = low_frequency
            self.player_list_data[self.selected_row]["details"]["high_frequency"] = high_frequency
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["low_frequency"] = low_frequency
            self.player_list_data[self.selected_row]["current_time_item"]["high_frequency"] = high_frequency
        
        self.main_self.ui.player_list_low_frequency_spinbox.blockSignals(True)
        self.main_self.ui.player_list_low_frequency_spinbox.setMaximum(high_frequency)
        self.main_self.ui.player_list_low_frequency_spinbox.setValue(low_frequency)
        self.main_self.ui.player_list_low_frequency_spinbox.blockSignals(False)
        self.main_self.ui.player_list_high_frequency_spinbox.blockSignals(True)
        self.main_self.ui.player_list_high_frequency_spinbox.setMinimum(low_frequency)
        self.main_self.ui.player_list_high_frequency_spinbox.setValue(high_frequency)
        self.main_self.ui.player_list_high_frequency_spinbox.blockSignals(False)
         
        if save==True:
        
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                
                    self.main_self.ui.deck_1_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.deck_1_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_1_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.deck_1_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                    
                    self.main_self.ui.deck_2_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.deck_2_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_2_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.deck_2_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["high_frequency"] = high_frequency
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["high_frequency"] = high_frequency
                        
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.setValue(low_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(False)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.setValue(high_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})            
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"filter","relative_number":relative_number,"relative_type":relative_type,"low_frequency":low_frequency,"high_frequency":high_frequency,"save":True})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                    self.apply_filter(None,player_list_row["player_number"],low_frequency,high_frequency,save=False)
          
    def list_widget_reset_filter(self,state,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        low_frequency = 20
        high_frequency = 20000
            
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["low_frequency"] = low_frequency
            self.player_list_data[self.selected_row]["details"]["high_frequency"] = high_frequency
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["low_frequency"] = low_frequency
            self.player_list_data[self.selected_row]["current_time_item"]["high_frequency"] = high_frequency
        
        self.main_self.ui.player_list_low_frequency_spinbox.blockSignals(True)
        self.main_self.ui.player_list_low_frequency_spinbox.setMaximum(20000)
        self.main_self.ui.player_list_low_frequency_spinbox.setValue(low_frequency)
        self.main_self.ui.player_list_low_frequency_spinbox.blockSignals(False)
        self.main_self.ui.player_list_high_frequency_spinbox.blockSignals(True)
        self.main_self.ui.player_list_high_frequency_spinbox.setMinimum(20)
        self.main_self.ui.player_list_high_frequency_spinbox.setValue(high_frequency)
        self.main_self.ui.player_list_high_frequency_spinbox.blockSignals(False)
         
        if save==True:
        
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                
                    self.main_self.ui.deck_1_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_low_frequency.setMaximum(20000)
                    self.main_self.ui.deck_1_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_1_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_high_frequency.setMinimum(20)
                    self.main_self.ui.deck_1_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                    
                    self.main_self.ui.deck_2_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_low_frequency.setMaximum(20000)
                    self.main_self.ui.deck_2_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_2_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_high_frequency.setMinimum(20)
                    self.main_self.ui.deck_2_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["high_frequency"] = high_frequency
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["high_frequency"] = high_frequency
                        
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_low_frequency.setMaximum(20000)
                    self.main_self.ui.music_clip_deck_low_frequency.setValue(low_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(False)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_high_frequency.setMinimum(20)
                    self.main_self.ui.music_clip_deck_high_frequency.setValue(high_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})            
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"filter","relative_number":relative_number,"relative_type":relative_type,"low_frequency":low_frequency,"high_frequency":high_frequency,"save":True})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                    self.apply_filter(None,player_list_row["player_number"],low_frequency,high_frequency,save=False)

    def list_widget_repeats_changed(self,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        repeats = self.main_self.ui.player_list_repeats_spinbox.value()
        player_list_row = self.player_list_data[self.selected_row]
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"repeats","player_number":player_list_row["player_number"],"repeats":repeats})
        
        self.player_list_data[self.selected_row]["repeats"] = repeats
        self.player_list_repeat[self.selected_row]["repeats input"].setValue(repeats)

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
        
    def list_widget_open_file_folder(self,state):
        if self.player_list_data[self.selected_row]["relative_type"] == "time_collections":
            saved_path = self.player_list_data[self.selected_row]["current_time_item"]["saved_path"]
        else:    
            saved_path = self.player_list_data[self.selected_row]["details"]["saved_path"]
        saved_path = saved_path.replace("/","\\")
        subprocess.Popen('explorer /select,"'+saved_path+'"', shell=False)

    def make_list_widget_rating_stars(self):
        self.list_rating_labels = []

        self.list_rating = int(10)
        self.list_rest_rating = 10 - self.list_rating
        
		
        for i in range(0,self.list_rating):
            star_label = label_clickable.QLabelClickable(self.main_self.ui.player_list_rating_frame)
            star_label.setMinimumSize(QtCore.QSize(20, 20))
            star_label.setMaximumSize(QtCore.QSize(20, 20))
            star_label.setText("")
            star_label.setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star_yellow.png"))
            star_label.setScaledContents(True)

            star_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            star_label.clicked.connect(lambda state,new_rating=i+1:print(str(new_rating)))
            self.main_self.ui.horizontalLayout_60.insertWidget(i,star_label)
            self.list_rating_labels.append(star_label)

        for i in range(0,self.list_rest_rating):
            star_label = label_clickable.QLabelClickable(self.main_self.ui.player_list_rating_frame)
            star_label.setMinimumSize(QtCore.QSize(20, 20))
            star_label.setMaximumSize(QtCore.QSize(20, 20))
            star_label.setText("")
            star_label.setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star.png"))
            star_label.setScaledContents(True)

            star_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            star_label.clicked.connect(lambda state,new_rating=self.list_rating+i+1:print(str(new_rating)))
            self.main_self.ui.horizontalLayout_60.insertWidget(self.list_rating+i,star_label)
            self.list_rating_labels.append(star_label)
            
        #spacer_item = QtWidgets.QSpacerItem(1,1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        #self.main_self.ui.horizontalLayout.addSpacerItem(spacer_item)
        
        self.main_self.ui.horizontalLayout_60.addStretch()
        self.main_self.ui.horizontalLayout_60.update()        
        self.main_self.ui.player_list_rating_frame.update()

    def list_widget_rating_changed(self,state,new_rating,save=True):
        self.list_rating = int(new_rating)
        self.list_rest_rating = 10 - int(new_rating)
        
        if self.player_list_data[self.selected_row]["relative_type"]!="time_collections":
            self.player_list_data[self.selected_row]["details"]["rating"] = new_rating
        else:
            self.player_list_data[self.selected_row]["current_time_item"]["rating"] = new_rating
        
        for i in range(0,self.list_rating):
            self.list_rating_labels[i].setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star_yellow.png"))
            self.list_rating_labels[i].clicked.disconnect()
            self.list_rating_labels[i].clicked.connect(lambda state,new_rating=i+1:self.list_widget_rating_changed(state,new_rating))

        for i in range(0,self.list_rest_rating):
            self.list_rating_labels[self.list_rating+i].setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star.png"))
            self.list_rating_labels[self.list_rating+i].clicked.disconnect()
            self.list_rating_labels[self.list_rating+i].clicked.connect(lambda state,new_rating=self.list_rating+i+1:self.list_widget_rating_changed(state,new_rating))
         
        if save==True:
            relative_type = self.player_list_data[self.selected_row]["relative_type"]
            relative_number = self.player_list_data[self.selected_row]["relative_number"]
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.manage_decks_instance.deck_1_rating_changed(None,new_rating,save=False)
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                    self.main_self.manage_decks_instance.deck_2_rating_changed(None,new_rating,save=False)
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["rating"] = new_rating
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["rating"] = new_rating
                    
            #4. Player list proccess table
            self.main_player_list_queue.put({"type":"rating","relative_number":relative_number,"relative_type":relative_type,"rating":new_rating,"save":False})
            
            #5. QTableWidget
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    self.rating_changed(None,new_rating,player_list_row["player_number"],save=False)
            
    ### QTableWidget ###

    def make_player_list_table(self):

        self.hidden_rows = []

        #player list row widgets list
        self.player_list_position = []
        self.player_list_image = []
        self.player_list_play = []
        self.player_list_play_now = []
        self.player_list_remove = []
        self.player_list_volume = []
        self.player_list_rating = []
        self.player_list_speed = []
        self.player_list_normalize = []
        self.player_list_pan = []
        self.player_list_frequencies = []
        self.player_list_repeat = []
        self.player_list_open_file = []


        self.main_self.ui.player_list_table.setRowCount(0)
            
        row = 0
        for player_list_row in self.player_list_data:
            self.display_player_list_row(row,player_list_row,insert_new_row=True)
            row = row + 1
        self.main_self.ui.player_list_table.setStyleSheet("QTableWidget::item {padding: 10px 10px 10px 10px; }QTableWidget > *{border:none;background:white;}")

        
        self.main_self.ui.player_list_table.resizeRowsToContents()
        self.main_self.ui.player_list_table.resizeColumnsToContents()
        

        self.main_self.ui.player_list_table.setColumnWidth(19, 800)
        
        self.main_self.ui.player_list_table.verticalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        self.main_self.ui.player_list_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        for column_number in range(0,22):
            item = self.main_self.ui.player_list_table.horizontalHeaderItem(column_number)
            item_text = item.text()
            item.setText( "\n"+str(item_text)+"\n")
                
        self.main_self.ui.player_list_frame.setEnabled(True)
        self.main_self.ui.player_list_table.currentCellChanged.connect(lambda row,column:self.player_list_table_selected_item_change(row,column))
        self.main_self.ui.player_list_table.verticalHeader().setFixedWidth(70)
        
        if self.player_list_data_length!=0:
            self.main_self.ui.player_list_table.selectRow(0)

    def display_player_list_row(self,row,player_list_row,insert_new_row=False):
        if insert_new_row==True:
            self.main_self.ui.player_list_table.insertRow(row)
            self.player_list_position.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_image.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_play.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_play_now.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_remove.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_rating.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_volume.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_speed.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_normalize.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_pan.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_frequencies.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_repeat.insert(row,{"player_number":player_list_row["player_number"]})
            self.player_list_open_file.insert(row,{"player_number":player_list_row["player_number"]})
        else:
            counter = 0
            for player_list_row_1 in self.player_list_data:
                if player_list_row_1["player_number"]==player_list_row["player_number"]:
                    self.player_list_position[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_image[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_play[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_play_now[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_remove[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_rating[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_volume[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_speed[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_normalize[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_pan[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_frequencies[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_repeat[counter] = {"player_number":player_list_row["player_number"]}
                    self.player_list_open_file[counter] = {"player_number":player_list_row["player_number"]}
                counter +=1
		

        #Change position cell
        column_counter = 0
        change_position_frame = QtWidgets.QFrame()
        change_position_frame.setMinimumHeight(150)
        verticalLayout = QtWidgets.QVBoxLayout(change_position_frame)
		
        if(row!=0):
            self.player_list_position[row]["move up"] = QtWidgets.QPushButton(change_position_frame)
            self.player_list_position[row]["move up"].setMinimumHeight(50)
            self.player_list_position[row]["move up"].setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.player_list_position[row]["move up"].setIcon(icon)
            verticalLayout.addWidget(self.player_list_position[row]["move up"])

            spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            verticalLayout.addItem(spacerItem)


            self.player_list_position[row]["move up"].clicked.connect(lambda state,start_row=row,end_row=row-1: self.move_table_row(state,start_row,end_row))

        if(row!=self.player_list_data_length-1):
            self.player_list_position[row]["move down"] = QtWidgets.QPushButton(change_position_frame)
            self.player_list_position[row]["move down"].setMinimumHeight(50)
            self.player_list_position[row]["move down"].setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.player_list_position[row]["move down"].setIcon(icon1)
            verticalLayout.addWidget(self.player_list_position[row]["move down"])

            spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            verticalLayout.addItem(spacerItem)


            self.player_list_position[row]["move down"].clicked.connect(lambda state,start_row=row,end_row=row+1: self.move_table_row(state,start_row,end_row))

        change_position_frame.setStyleSheet("QFrame{border:0;padding:10px 10px 10px 10px;background:transparent;}")
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,change_position_frame)

        #Play checkbox
        column_counter += 1
        player_list_play_frame = QtWidgets.QFrame()
        gridLayout = QtWidgets.QGridLayout(player_list_play_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        self.player_list_play[row]["play checkbox"] = QtWidgets.QCheckBox(player_list_play_frame)
        self.player_list_play[row]["play checkbox"].setStyleSheet("QCheckBox{padding-left:5px;}")
        self.player_list_play[row]["play checkbox"].setText("")
        gridLayout.addWidget(self.player_list_play[row]["play checkbox"], 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem3, 1, 2, 1, 1)
        if(player_list_row["play"]==1 or player_list_row["play"]==True):
            self.player_list_play[row]["play checkbox"].setCheckState(Qt.Checked)
        else:
            self.player_list_play[row]["play checkbox"].setCheckState(Qt.Unchecked)
            
        self.player_list_play[row]["play checkbox"].stateChanged.connect(lambda state,player_number=player_list_row["player_number"]:self.table_play_state_changed(state,player_number))
        player_list_play_frame.setStyleSheet("QFrame{border:0;background:transparent;}")
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_play_frame)
		
        if player_list_row["relative_type"]!="time_collections":
            item = player_list_row["details"]
        else:
            item = player_list_row["current_time_item"]
        
        #Title
        column_counter += 1
        title_item = QtWidgets.QTableWidgetItem(str(item["title"]))
        title_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,title_item)

        #Τελευταία εκτέλεσης
        column_counter += 1
        last_play_item = QtWidgets.QTableWidgetItem(str(player_list_row["last_play"]))
        last_play_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,last_play_item)
        
        #Επόμενη εκτέλεσης
        column_counter += 1

        #Image
        column_counter += 1
        image_frame = QtWidgets.QFrame()
        image_frame.setStyleSheet("QFrame{\nborder:none;background:transparent;\n}QFrame:selected{color:white;}")
        gridLayout = QtWidgets.QGridLayout(image_frame)
        image_title = QtWidgets.QLabel(image_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(image_title.sizePolicy().hasHeightForWidth())
        image_title.setSizePolicy(sizePolicy)
        image_title.setAlignment(QtCore.Qt.AlignCenter)
        image_title.setWordWrap(True)
        image_title.setStyleSheet("QLabel{\nborder:none;background:transparent;\n}")
        gridLayout.addWidget(image_title, 1, 0, 1, 3)
        image = QtWidgets.QLabel(image_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(image.sizePolicy().hasHeightForWidth())
        image.setSizePolicy(sizePolicy)
        image.setMinimumSize(QtCore.QSize(150, 150))
        image.setMaximumSize(QtCore.QSize(150, 150))
        image.setText("")
        image.setScaledContents(True)
        gridLayout.addWidget(image, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem1, 0, 0, 1, 1)

        image_path_found = False
        if "image_path" in item:
            if item["image_path"]!="":
                if os.path.exists(item["image_path"]):
                    pixmap = QtGui.QPixmap(item["image_path"]).scaledToHeight(150)
                    image.setPixmap(pixmap)
                    image_path_found = True
                else:
                    image_path_found = False
            else:
                image_path_found = False
        else:
            image_path_found = False
            
        if image_path_found == False:
            if player_list_row["relative_type"]=="sound_clips":
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/deck_image.png").scaledToHeight(150)
                image.setPixmap(pixmap)
                image_path_found = True
            elif player_list_row["relative_type"]=="weather_news":
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/weather.png").scaledToHeight(150)
                image.setPixmap(pixmap)
                image_path_found = True  
            elif player_list_row["relative_type"]=="church_news":
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/church.png").scaledToHeight(150)
                image.setPixmap(pixmap)
                image_path_found = True
            elif player_list_row["relative_type"]=="time_collections":
                now = datetime.now()
                now_hour = now.hour
                now_minute = now.minute
                Greece_time_case = int(player_list_row["details"][0]["case"])
                if Greece_time_case == 1 or Greece_time_case==2:
                    next_Greece_time_announcement_hour = now_hour+1
                    next_Greece_time_announcement_minute = 0
                else:
                    if now_minute<30:
                        next_Greece_time_announcement_hour = now_hour
                        next_Greece_time_announcement_minute = 30
                    else:
                        next_Greece_time_announcement_hour = now_hour+1
                        next_Greece_time_announcement_minute = 0
                if next_Greece_time_announcement_minute ==0:
                    if next_Greece_time_announcement_hour==1 or next_Greece_time_announcement_hour==13:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-01.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==2 or next_Greece_time_announcement_hour==14:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-02.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==3 or next_Greece_time_announcement_hour==15:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-03.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==4 or next_Greece_time_announcement_hour==16:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-04.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==5 or next_Greece_time_announcement_hour==17:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-05.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==6 or next_Greece_time_announcement_hour==18:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-06.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==7 or next_Greece_time_announcement_hour==19:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-07.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==8 or next_Greece_time_announcement_hour==20:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-08.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==9 or next_Greece_time_announcement_hour==21:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-09.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==10 or next_Greece_time_announcement_hour==22:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-10.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==11 or next_Greece_time_announcement_hour==23:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-11.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==12 or next_Greece_time_announcement_hour==24:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-12.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                else:
                    if next_Greece_time_announcement_hour==1 or next_Greece_time_announcement_hour==13:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-01-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==2 or next_Greece_time_announcement_hour==14:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-02-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==3 or next_Greece_time_announcement_hour==15:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-03-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==4 or next_Greece_time_announcement_hour==16:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-04-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==5 or next_Greece_time_announcement_hour==17:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-05-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==6 or next_Greece_time_announcement_hour==18:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-06-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==7 or next_Greece_time_announcement_hour==19:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-07-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==8 or next_Greece_time_announcement_hour==20:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-08-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==9 or next_Greece_time_announcement_hour==21:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-09-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==10 or next_Greece_time_announcement_hour==22:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-10-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==11 or next_Greece_time_announcement_hour==23:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-11-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
                    elif next_Greece_time_announcement_hour==12 or next_Greece_time_announcement_hour==24:
                        pixmap = QtGui.QPixmap(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/clock-12-30.png").scaledToHeight(150)
                        image.setPixmap(pixmap)
                        image_path_found = True
            elif player_list_row["relative_type"]=="station_logos":
                #may be changed
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/deck_image.png").scaledToHeight(150)
                image.setPixmap(pixmap)
                image_path_found = True
            else:
                pixmap = QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/deck_image.png").scaledToHeight(150)
                image.setPixmap(pixmap)
                image_path_found = True
                
        if "image_title" in item:
            image_title.setText("\n\n"+str(item["image_title"]))
        else:
            image_title.setText("\n\n"+str(item["title"]))
        self.player_list_image[row]["image_title"] = image_title
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,image_frame)
        
        #Load to decks
        column_counter += 1
        if player_list_row["relative_type"]!="time_collections" and player_list_row["relative_type"]!="sound_clips":
            load_to_decks = QtWidgets.QFrame()
            gridLayout_play_decks = QtWidgets.QGridLayout(load_to_decks)
            play_from_deck_1 = QtWidgets.QPushButton(load_to_decks)
            gridLayout_play_decks.addWidget(play_from_deck_1, 0, 0, 1, 1)
            play_from_deck_2 = QtWidgets.QPushButton(load_to_decks)
            gridLayout_play_decks.addWidget(play_from_deck_2, 1, 0, 1, 1)
            play_from_deck_1.setText("Φόρτωση στο deck 1")
            play_from_deck_2.setText("Φόρτωση στο deck 2")
            load_to_decks.setStyleSheet("QFrame{border:0;padding:0;background:transparent;} QPushButton{width:300px;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,load_to_decks)

            self.player_list_play_now[row]["deck 1"] = play_from_deck_1
            self.player_list_play_now[row]["deck 2"] = play_from_deck_2
            self.player_list_play_now[row]["deck 1"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.prepare_deck_1(state,player_list_number))
            self.player_list_play_now[row]["deck 2"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.prepare_deck_2(state,player_list_number))
        elif player_list_row["relative_type"]=="sound_clips":
            load_to_decks = QtWidgets.QFrame()
            gridLayout_play_decks = QtWidgets.QGridLayout(load_to_decks)

            play_from_music_clip_deck = QtWidgets.QPushButton(load_to_decks)
            gridLayout_play_decks.addWidget(play_from_music_clip_deck, 1, 0, 1, 1)
            play_from_music_clip_deck.setText("Φόρτωση\n στο music clip deck")
            load_to_decks.setStyleSheet("QFrame{border:0;padding:0;background:transparent;} QPushButton{width:300px;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,load_to_decks)
            self.player_list_play_now[row]["music clip deck"] = play_from_music_clip_deck
            #to be done load to music clip deck
            self.player_list_play_now[row]["music clip deck"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.prepare_music_clip_deck(state,player_list_number))

        #Play now
        column_counter += 1
        if player_list_row["relative_type"]!="time_collections" and player_list_row["relative_type"]!="sound_clips":
            load_to_decks = QtWidgets.QFrame()
            gridLayout_play_decks = QtWidgets.QGridLayout(load_to_decks)
            play_from_deck_1 = QtWidgets.QPushButton(load_to_decks)
            gridLayout_play_decks.addWidget(play_from_deck_1, 0, 0, 1, 1)
            play_from_deck_2 = QtWidgets.QPushButton(load_to_decks)
            gridLayout_play_decks.addWidget(play_from_deck_2, 1, 0, 1, 1)
            play_from_deck_1.setText("Αναπαραγωγή\n στο deck 1")
            play_from_deck_2.setText("Αναπαραγωγή\n στο deck 2")
            load_to_decks.setStyleSheet("QFrame{border:0;padding:0;background:transparent;} QPushButton{width:300px;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,load_to_decks)

            self.player_list_play_now[row]["deck 1"] = play_from_deck_1
            self.player_list_play_now[row]["deck 2"] = play_from_deck_2
            self.player_list_play_now[row]["deck 1"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.prepare_and_play_deck_1(state,player_list_number))
            self.player_list_play_now[row]["deck 2"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.prepare_and_play_deck_2(state,player_list_number))
        elif player_list_row["relative_type"]=="sound_clips":
            load_to_decks = QtWidgets.QFrame()
            gridLayout_play_decks = QtWidgets.QGridLayout(load_to_decks)

            play_from_music_clip_deck = QtWidgets.QPushButton(load_to_decks)
            gridLayout_play_decks.addWidget(play_from_music_clip_deck, 1, 0, 1, 1)
            play_from_music_clip_deck.setText("Αναπαραγωγή\n στο music clip deck")
            load_to_decks.setStyleSheet("QFrame{border:0;padding:0;background:transparent;} QPushButton{width:300px;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,load_to_decks)
            self.player_list_play_now[row]["music clip deck"] = play_from_music_clip_deck
            #to be done load to music clip deck
            self.player_list_play_now[row]["music clip deck"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.load_track_to_music_clip_deck(state,player_list_number))

			
        #remove (delete)
        column_counter += 1
        player_list_remove_frame = QtWidgets.QFrame()
        verticalLayout = QtWidgets.QVBoxLayout(player_list_remove_frame)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        verticalLayout.addItem(spacerItem)
        self.player_list_remove[row]["remove button"] = QtWidgets.QPushButton(player_list_remove_frame)
        self.player_list_remove[row]["remove button"].setText("Αφαίρεση")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_list_remove[row]["remove button"].sizePolicy().hasHeightForWidth())
        self.player_list_remove[row]["remove button"].setSizePolicy(sizePolicy)
        verticalLayout.addWidget(self.player_list_remove[row]["remove button"])
        self.player_list_remove[row]["remove button"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.delete_player_list_item(state,player_list_number))
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        verticalLayout.addItem(spacerItem1)
        player_list_remove_frame.setStyleSheet("QFrame{border:0;padding:5px;background:transparent;} QPushButton{width:120px;}")
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_remove_frame)


        #duration
        column_counter += 1
        
        duration_for_humans = player_list_row["duration_human"]
        duration_item = QtWidgets.QTableWidgetItem(str(duration_for_humans))
        duration_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,duration_item)

        #artist
        column_counter += 1
        if("artist" in item):
            artist = str(item["artist"])
        else:
            artist = ""

        artist_item = QtWidgets.QTableWidgetItem(str(artist))
        artist_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,artist_item)
    
        #album
        column_counter += 1
        if("album" in item):
            album = str(item["album"])
        else:
            album = ""
            
        album_item = QtWidgets.QTableWidgetItem(str(album))
        album_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,album_item)

        #composer
        column_counter += 1
        if("composer" in item):
            composer = str(item["composer"])
        else:
            composer = ""

        composer_item = QtWidgets.QTableWidgetItem(str(composer))
        composer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,composer_item)

        #author
        column_counter += 1
        if("author" in player_list_row):
            author = str(player_list_row["author"])
        else:
            author = ""

        author_item = QtWidgets.QTableWidgetItem(str(author))
        author_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,author_item)
		
        #year
        column_counter +=1
        if("year" in item):
            year = str(item["year"])
        else:
            year = ""

        year_item = QtWidgets.QTableWidgetItem(str(year))
        year_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,year_item)

        #description
        column_counter +=1
        if("description" in item):
            description = str(item["description"])
        else:
            description = ""

        description_item = QtWidgets.QTableWidgetItem(str(description))
        description_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,description_item)
        
        #from
        column_counter +=1
        if("from" in item):
            from_text = str(item["from"])
        else:
            from_text = ""

        from_text_item = QtWidgets.QTableWidgetItem(str(from_text))
        from_text_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.main_self.ui.player_list_table.setItem(row,column_counter,from_text_item)
        
        #rating
        column_counter += 1
        if "rating" in item:
            rating_frame = QtWidgets.QFrame()
            horizontalLayout = QtWidgets.QHBoxLayout(rating_frame)
            rating_labels = []
            

            rating = int(item["rating"])
            rest_rating = 10 - rating

            
            for i in range(0,rating):
                star_label = label_clickable.QLabelClickable(rating_frame)
                star_label.setMinimumSize(QtCore.QSize(20, 20))
                star_label.setMaximumSize(QtCore.QSize(20, 20))
                star_label.setText("")
                star_label.setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star_yellow.png"))
                star_label.setScaledContents(True)

                star_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                star_label.clicked.connect(lambda state,new_rating=i+1,player_list_number=player_list_row["player_number"]:self.rating_changed(state,new_rating,player_list_number))
                horizontalLayout.insertWidget(i,star_label)
                rating_labels.append(star_label)

            for i in range(0,rest_rating):
                star_label = label_clickable.QLabelClickable(rating_frame)
                star_label.setMinimumSize(QtCore.QSize(20, 20))
                star_label.setMaximumSize(QtCore.QSize(20, 20))
                star_label.setText("")
                star_label.setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star.png"))
                star_label.setScaledContents(True)

                star_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                star_label.clicked.connect(lambda state,new_rating=rating+i+1,player_list_number=player_list_row["player_number"]:self.rating_changed(state,new_rating,player_list_number))
                horizontalLayout.insertWidget(rating+i,star_label)
                rating_labels.append(star_label)

            spacer_item = QtWidgets.QSpacerItem(1,1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            horizontalLayout.addSpacerItem(spacer_item)
            
            horizontalLayout.addStretch()
            horizontalLayout.update()
            self.player_list_rating[row]["labels"] = rating_labels
            rating_frame.setStyleSheet("QFrame{border:none;background:transparent;}QLabel{border:none;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,rating_frame)
            
				
		
        #volume
        column_counter +=1
        volume = int(item["volume"])
        
        player_list_volume_frame = QtWidgets.QFrame()
        
        gridLayout = QtWidgets.QGridLayout(player_list_volume_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        #spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem1, 0, 0, 4, 1)
        
        #horizontalLayout = QtWidgets.QHBoxLayout(player_list_volume_frame)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #horizontalLayout.addItem(spacerItem1)
        gridLayout.addItem(spacerItem1, 0, 1, 1, 2)
        self.player_list_volume[row]["volume"] = QtWidgets.QSlider(player_list_volume_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_list_volume[row]["volume"].sizePolicy().hasHeightForWidth())
        self.player_list_volume[row]["volume"].setSizePolicy(sizePolicy)
        self.player_list_volume[row]["volume"].setMaximum(200)
        self.player_list_volume[row]["volume"].setSingleStep(5)
        self.player_list_volume[row]["volume"].setPageStep(5)
        self.player_list_volume[row]["volume"].setProperty("value", volume)
        self.player_list_volume[row]["volume"].setSliderPosition(volume)
        self.player_list_volume[row]["volume"].setOrientation(QtCore.Qt.Horizontal)
        self.player_list_volume[row]["volume"].valueChanged.connect(lambda volume,player_list_number=player_list_row["player_number"]:self.player_list_volume_moved(volume,player_list_number))
        self.player_list_volume[row]["volume"].sliderReleased.connect(lambda player_list_number=player_list_row["player_number"]:self.player_list_volume_released(player_list_number))
        self.player_list_volume[row]["volume"].wheelEvent = lambda event: event.ignore()
        #horizontalLayout.addWidget(self.player_list_volume[row]["volume"])
        gridLayout.addWidget(self.player_list_volume[row]["volume"], 1, 1, 1, 1)
        self.player_list_volume[row]["volume label"] = QtWidgets.QLabel(player_list_volume_frame)

        self.player_list_volume[row]["volume label"].setText(str(volume)+"/200")
        #horizontalLayout.addWidget(self.player_list_volume[row]["volume label"])
        gridLayout.addWidget(self.player_list_volume[row]["volume label"], 1, 2, 1, 1)
        self.player_list_volume[row]["reset"] = QtWidgets.QPushButton(player_list_volume_frame)
        self.player_list_volume[row]["reset"].setText("Επαναφορά (100/200)")
        self.player_list_volume[row]["reset"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.reset_volume(state,player_list_number))
        #horizontalLayout.addItem(spacerItem2)
        gridLayout.addWidget(self.player_list_volume[row]["reset"],2,1,1,2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem2, 3, 2, 1, 2)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem1, 0, 3, 4, 1)
        
        player_list_volume_frame.setStyleSheet("QFrame{border:0px;background:transparent;}")				
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_volume_frame)

        #Normalize checkbox
        column_counter +=1
        player_list_normalize_frame = QtWidgets.QFrame()
        gridLayout = QtWidgets.QGridLayout(player_list_normalize_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        self.player_list_normalize[row]["normalize checkbox"] = QtWidgets.QCheckBox(player_list_normalize_frame)
        self.player_list_normalize[row]["normalize checkbox"].setStyleSheet("QCheckBox{padding-left:5px;}")
        self.player_list_normalize[row]["normalize checkbox"].setText("")
        gridLayout.addWidget(self.player_list_normalize[row]["normalize checkbox"], 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem3, 1, 2, 1, 1)
        if(int(item["normalize"])==1):
            self.player_list_normalize[row]["normalize checkbox"].setCheckState(Qt.Checked)
        else:
            self.player_list_normalize[row]["normalize checkbox"].setCheckState(Qt.Unchecked)
			
        self.player_list_normalize[row]["normalize checkbox"].stateChanged.connect(lambda state,player_list_number=player_list_row["player_number"]:self.player_list_normalize_changed(player_list_number,state,True))

        player_list_normalize_frame.setStyleSheet("QFrame{border:0;background:transparent;}")
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_normalize_frame)
		
        
        #pan
        column_counter +=1
        pan = int(item["pan"])
        player_list_pan_frame = QtWidgets.QFrame()
        
        gridLayout = QtWidgets.QGridLayout(player_list_pan_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem1, 0, 0, 4, 1)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem1, 0, 1, 1, 2)
        self.player_list_pan[row]["pan"] = QtWidgets.QSlider(player_list_pan_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_list_pan[row]["pan"].sizePolicy().hasHeightForWidth())
        self.player_list_pan[row]["pan"].setSizePolicy(sizePolicy)
        self.player_list_pan[row]["pan"].setMaximum(100)
        self.player_list_pan[row]["pan"].setMinimum(-100)
        self.player_list_pan[row]["pan"].setSingleStep(5)
        self.player_list_pan[row]["pan"].setPageStep(5)
        self.player_list_pan[row]["pan"].setProperty("value", pan)
        self.player_list_pan[row]["pan"].setSliderPosition(pan)
        self.player_list_pan[row]["pan"].setOrientation(QtCore.Qt.Horizontal)
        self.player_list_pan[row]["pan"].valueChanged.connect(lambda pan_value,player_list_number=player_list_row["player_number"]:self.player_list_pan_changed(pan_value,player_list_number))
        self.player_list_pan[row]["pan"].sliderReleased.connect(lambda player_list_number=player_list_row["player_number"]:self.player_list_pan_released(player_list_number))
        self.player_list_pan[row]["pan"].wheelEvent = lambda event: event.ignore()
        gridLayout.addWidget(self.player_list_pan[row]["pan"], 1, 1, 1, 1)
        self.player_list_pan[row]["pan label"] = QtWidgets.QLabel(player_list_pan_frame)

        self.player_list_pan[row]["pan label"].setText(str(pan))
        gridLayout.addWidget(self.player_list_pan[row]["pan label"], 1, 2, 1, 1)
        self.player_list_pan[row]["reset"] = QtWidgets.QPushButton(player_list_pan_frame)
        self.player_list_pan[row]["reset"].setText("Επαναφορά (0)")
        self.player_list_pan[row]["reset"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.reset_pan(state,player_list_number))
        gridLayout.addWidget(self.player_list_pan[row]["reset"],2,1,1,2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem2, 3, 2, 1, 2)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        gridLayout.addItem(spacerItem1, 0, 3, 4, 1)
        
        player_list_pan_frame.setStyleSheet("QFrame{border:0px;background:transparent;}")				
        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_pan_frame)

        #Ζωνοπερατό φίλτρο
        low_frequency_value = int(item["low_frequency"])
        high_frequency_value = int(item["high_frequency"])
        column_counter+=1
        filter_frame = QtWidgets.QFrame()
        filter_frame.setStyleSheet("QFrame{border:0px;background:transparent;padding:0px;width:110%;}")
        filter_frame.setMinimumSize(QtCore.QSize(500, 0))
        horizontalLayout_14 = QtWidgets.QHBoxLayout(filter_frame)
        horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        filter_select_frequencies_frame = QtWidgets.QFrame(filter_frame)
        filter_select_frequencies_frame.setStyleSheet("QFrame{padding:0;border:0px}")
        gridLayout_6 = QtWidgets.QGridLayout(filter_select_frequencies_frame)
        gridLayout_6.setContentsMargins(0, 0, 0, 0)
        filter_reset_filter_button = QtWidgets.QPushButton(filter_select_frequencies_frame)
        filter_reset_filter_button.setMinimumSize(QtCore.QSize(210, 0))
        filter_reset_filter_button.setMaximumSize(QtCore.QSize(144, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/default_filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        filter_reset_filter_button.setIcon(icon)
        filter_reset_filter_button.setStatusTip("Επαναφορά των τιμών του deck 1 ζωνοπερατού φίλτρου (χαμηλή συχνότητα: 20 Hz, υψηλή συχνότητα: 20000 Hz).")
        filter_reset_filter_button.setText("Επαναφορά (20Hz - 20000Hz)")
        gridLayout_6.addWidget(filter_reset_filter_button, 1, 3, 1, 1)
        label_12 = QtWidgets.QLabel(filter_select_frequencies_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_12.sizePolicy().hasHeightForWidth())
        label_12.setSizePolicy(sizePolicy)
        label_12.setText("Υψηλή συχνότητα αποκοπής:")
        gridLayout_6.addWidget(label_12, 1, 0, 1, 1)
        label_13 = QtWidgets.QLabel(filter_select_frequencies_frame)
        label_13.setText("Χαμηλή συχνότητα αποκοπής:")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_13.sizePolicy().hasHeightForWidth())
        label_13.setSizePolicy(sizePolicy)
        gridLayout_6.addWidget(label_13, 0, 0, 1, 1)
        filter_apply_filter_button = QtWidgets.QPushButton(filter_select_frequencies_frame)
        filter_apply_filter_button.setMinimumSize(QtCore.QSize(210, 0))
        filter_apply_filter_button.setMaximumSize(QtCore.QSize(144, 16777215))
        filter_apply_filter_button.setStatusTip("Εφαρμογή των επιλογών του deck 1 ζωνοπερατού φίλτρου.")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/apply_filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        filter_apply_filter_button.setIcon(icon1)
        filter_apply_filter_button.setText("Εφαρμογή φίλτρου")
        gridLayout_6.addWidget(filter_apply_filter_button, 0, 3, 1, 1)
        low_frequency = QtWidgets.QSpinBox(filter_select_frequencies_frame)
        low_frequency.setMinimum(20)
        low_frequency.setMaximum(high_frequency_value)
        low_frequency.setSingleStep(100)
        low_frequency.setProperty("value", low_frequency_value)
        low_frequency.setStatusTip("Επιλογή της χαμηλής συχνότητας αποκοπής του deck 1 ζωνοπερατού φίλτρου.")
        low_frequency.valueChanged.connect(lambda low_frequency,player_list_number=player_list_row["player_number"]:self.low_frequency_changed(low_frequency,player_list_number))
        gridLayout_6.addWidget(low_frequency, 0, 1, 1, 1)
        high_frequency = QtWidgets.QSpinBox(filter_select_frequencies_frame)
        high_frequency.setMinimum(low_frequency_value)
        high_frequency.setMaximum(20000)
        high_frequency.setSingleStep(100)
        high_frequency.setProperty("value", high_frequency_value)
        high_frequency.setStatusTip("Επιλογή της υψηλής συχνότητας αποκοπής του deck 1 ζωνοπερατού φίλτρου.")
        high_frequency.valueChanged.connect(lambda high_frequency,player_list_number=player_list_row["player_number"]:self.high_frequency_changed(high_frequency,player_list_number))
        gridLayout_6.addWidget(high_frequency, 1, 1, 1, 1)
        horizontalLayout_14.addWidget(filter_select_frequencies_frame)
        low_frequency.setSuffix(" Hz")
        high_frequency.setSuffix(" Hz")
        self.player_list_frequencies[row]["low_frequency spinbox"] = low_frequency
        self.player_list_frequencies[row]["high_frequency spinbox"] = high_frequency
        self.player_list_frequencies[row]["apply filter"] = filter_apply_filter_button
        filter_apply_filter_button.clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.apply_filter(state,player_list_number))
        self.player_list_frequencies[row]["reset filter"] = filter_reset_filter_button
        filter_reset_filter_button.clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.reset_filter(state,player_list_number))
        self.player_list_frequencies[row]["low label"] = label_13
        self.player_list_frequencies[row]["high label"] = label_12

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(filter_frame.sizePolicy().hasHeightForWidth())
        filter_frame.setSizePolicy(sizePolicy)

        self.main_self.ui.player_list_table.setCellWidget(row,column_counter,filter_frame)

        #Επαναλήψεις
        column_counter+=1
        if(player_list_row["relative_type"]!="time_collections"):
            player_list_repeats_frame = QtWidgets.QFrame()
            self.player_list_repeat[row]["repeats input"] = QtWidgets.QSpinBox(player_list_repeats_frame)
            self.player_list_repeat[row]["repeats input"].setMinimum(0)
            self.player_list_repeat[row]["repeats input"].setMaximum(10000)
            self.player_list_repeat[row]["repeats input"].setSingleStep(1)
            self.player_list_repeat[row]["repeats input"].setProperty("value", int(player_list_row["repeats"]))
            self.player_list_repeat[row]["repeats input"].setStatusTip("Επιλογή φορών επαναλήψεων (μηδενική τιμή για μία μοναδική επανάληψη).")
            verticalLayout = QtWidgets.QHBoxLayout(player_list_repeats_frame)
            self.player_list_repeat[row]["repeats input"].setAlignment(QtCore.Qt.AlignCenter)
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            verticalLayout.addItem(spacerItem)
            verticalLayout.addWidget(self.player_list_repeat[row]["repeats input"])
            self.player_list_repeat[row]["repeats button"] = QtWidgets.QPushButton(player_list_repeats_frame)
            verticalLayout.addWidget(self.player_list_repeat[row]["repeats button"])
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            verticalLayout.addItem(spacerItem)
            self.player_list_repeat[row]["repeats button"].setText("Εντάξει")
            self.player_list_repeat[row]["repeats button"].clicked.connect(lambda state,player_list_number=player_list_row["player_number"]:self.player_list_change_repeats(state,player_list_number))
            player_list_repeats_frame.setStyleSheet("QFrame{border:0px;background:transparent;padding:10px}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_repeats_frame)

        #Open file
        column_counter +=1
        if(player_list_row["relative_type"]!="retransmitions"):
            player_list_path_frame = QtWidgets.QFrame()
            verticalLayout = QtWidgets.QVBoxLayout(player_list_path_frame)
            verticalLayout.setContentsMargins(0, 0, 0, 0)
            spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            verticalLayout.addItem(spacerItem)
            self.player_list_open_file[row]["button"] = QtWidgets.QPushButton(player_list_path_frame)
            self.player_list_open_file[row]["button"].setText("Άνοιγμα")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.player_list_open_file[row]["button"].sizePolicy().hasHeightForWidth())
            self.player_list_open_file[row]["button"].setSizePolicy(sizePolicy)
            
            self.player_list_open_file[row]["button"].clicked.connect(lambda row=row:self.open_file(row))

            verticalLayout.addWidget(self.player_list_open_file[row]["button"])
            spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            verticalLayout.addItem(spacerItem1)
            player_list_path_frame.setStyleSheet("QFrame{border:0;padding:10px;background:transparent;} QPushButton{width:120px;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,player_list_path_frame)

    def player_list_table_selected_item_change(self,row,column):
        self.selected_row = row
        self.main_self.ui.listWidget.setCurrentRow(self.selected_row)
    
    def move_table_row(self,state,start_row,end_row):
        self.main_self.ui.player_list_frame.setEnabled(False)
        self.selected_row = end_row
        #1. Player list table
        item_full = self.player_list_data[start_row]
        if item_full["relative_type"]=="time_collections":
            item = item_full["current_time_item"]
        else:
            item = item_full["details"]
        del self.player_list_data[start_row]
        self.player_list_data.insert(end_row,item_full)
        
        #2. QTableWidget
        self.main_self.ui.player_list_table.removeRow(start_row)
        del self.player_list_position[start_row]
        del self.player_list_image[start_row]
        del self.player_list_play[start_row]
        del self.player_list_play_now[start_row]
        del self.player_list_remove[start_row]
        del self.player_list_volume[start_row]
        del self.player_list_rating[start_row]
        del self.player_list_speed[start_row]
        del self.player_list_normalize[start_row]
        del self.player_list_pan[start_row]
        del self.player_list_frequencies[start_row]
        del self.player_list_repeat[start_row]
        del self.player_list_open_file[start_row]
        self.display_player_list_row(end_row,item_full,insert_new_row=True)
        self.player_list_position = []
        for row in range(0,self.player_list_data_length):
            #Change position cell
            self.player_list_position.append({})
            column_counter = 0
            change_position_frame = QtWidgets.QFrame()
            change_position_frame.setMinimumHeight(150)
            verticalLayout = QtWidgets.QVBoxLayout(change_position_frame)
            
            if(row!=0):
                self.player_list_position[row]["move up"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move up"].setMinimumHeight(50)
                self.player_list_position[row]["move up"].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move up"].setIcon(icon)
                verticalLayout.addWidget(self.player_list_position[row]["move up"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move up"].clicked.connect(lambda state,start_row=row,end_row=row-1: self.move_table_row(state,start_row,end_row))

            if(row!=self.player_list_data_length-1):
                self.player_list_position[row]["move down"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move down"].setMinimumHeight(50)
                self.player_list_position[row]["move down"].setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move down"].setIcon(icon1)
                verticalLayout.addWidget(self.player_list_position[row]["move down"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move down"].clicked.connect(lambda state,start_row=row,end_row=row+1: self.move_table_row(state,start_row,end_row))

            change_position_frame.setStyleSheet("QFrame{border:0;padding:10px 10px 10px 10px;background:transparent;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,change_position_frame)

        self.main_self.ui.player_list_table.resizeRowsToContents()
        self.main_self.ui.player_list_table.resizeColumnsToContents()
        
        #3. QListWidget
        self.main_self.ui.listWidget.takeItem(start_row)
        self.main_self.ui.listWidget.insertItem(end_row,item["title"]+" ("+item["duration_human"]+")")
        self.main_self.ui.listWidget.setCurrentRow(end_row)
        
        #4. save row move in database
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"move","start":start_row,"end":end_row})
        
        self.main_self.manage_decks_instance.general_deck_next_player_list_items()

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})

    def table_play_state_changed(self,state,player_number):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if state==Qt.Checked:
            play = 1
        else:
            play = 0
            
        #1. Player list table
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"]==player_number:
                self.player_list_data[counter]["play"] = play
                row = counter
                break
            counter += 1
            
        #2. QListWidget
        if row == self.selected_row:
            self.delegate.checked.disconnect()
            self.main_self.ui.listWidget.item(self.selected_row).setCheckState(state)
            self.delegate.checked.connect(self.list_widget_play_changed)
            if play == 0:
                self.main_self.ui.listWidget.item(self.selected_row).setBackground(QtGui.QBrush(QtGui.QColor(255,228,228), Qt.SolidPattern))
            else:
                self.main_self.ui.listWidget.item(self.selected_row).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255), Qt.SolidPattern))
        
        #3. QTableWidget
        self.player_list_play[row]["play checkbox"].blockSignals(True)
        self.player_list_play[row]["play checkbox"].setCheckState(state)
        self.player_list_play[row]["play checkbox"].blockSignals(False)
            
        #4. Process table + database save
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"play","play":play,"player_number":player_number})

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
        
    def prepare_deck_1(self,state,player_list_number,stop=True):
        self.main_self.manage_decks_instance.deck_1_play_requested = False
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.main_self.manage_decks_instance.prepare_deck_1(player_list_row,stop)
                row = counter
                pl_row = player_list_row
            counter += 1
                
        player_list_row = pl_row
        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,player_list_row["player_number"])
        else:
            self.move_table_row(None,row,self.player_list_data_length-1)
        
    def prepare_deck_2(self,state,player_list_number,stop=True):
        self.main_self.manage_decks_instance.deck_2_play_requested = False
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.main_self.manage_decks_instance.prepare_deck_2(player_list_row,stop)
                pl_row = player_list_row
                row = counter
            counter += 1
                
        player_list_row = pl_row
        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,player_list_row["player_number"])
        else:
            self.move_table_row(None,row,self.player_list_data_length-1)
            
    def prepare_music_clip_deck(self,state,player_list_number):
        self.main_self.manage_decks_instance.music_clip_deck_play_requested = False
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.main_self.manage_decks_instance.prepare_music_clip_deck(player_list_row)
                pl_row = player_list_row
                row = counter
            counter += 1
                
        player_list_row = pl_row
        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,player_list_row["player_number"])
        else:
            self.move_table_row(None,row,self.player_list_data_length-1)
            
    def prepare_and_play_deck_1(self,state,player_list_number):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.main_self.manage_decks_instance.prepare_and_play_deck_1(player_list_row)
                pl_row = player_list_row
                row = counter
            counter += 1
                
        player_list_row = pl_row
        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,player_list_row["player_number"])
        else:
            self.move_table_row(None,row,self.player_list_data_length-1)
            
    def prepare_and_play_deck_2(self,state,player_list_number):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.main_self.manage_decks_instance.prepare_and_play_deck_2(player_list_row)
                pl_row = player_list_row
                row = counter
            counter += 1
                
        player_list_row = pl_row
        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,player_list_row["player_number"])
        else:
            self.move_table_row(None,row,self.player_list_data_length-1)
            
    def load_track_to_music_clip_deck(self,state,player_list_number):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.main_self.manage_decks_instance.prepare_and_play_music_clip_deck(player_list_row)
                pl_row = player_list_row
                row = counter
            counter += 1
            
        player_list_row = pl_row
        if self.repeat_player_list==0 or self.repeat_player_list==False:
            self.delete_player_list_item(None,player_list_row["player_number"])
        else:
            self.move_table_row(None,row,self.player_list_data_length-1)
            
    def delete_player_list_item(self,state,player_list_number):
        self.main_self.ui.player_list_frame.setEnabled(False)
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"]==player_list_number:
                current_row = counter
                break
            counter += 1
        
        #1. Player list table
        del self.player_list_data[current_row]
        self.player_list_data_length -= 1

        #2. QTableWidget
        self.main_self.ui.player_list_table.removeRow(current_row)
        del self.player_list_position[current_row]
        del self.player_list_image[current_row]
        del self.player_list_play[current_row]
        del self.player_list_play_now[current_row]
        del self.player_list_remove[current_row]
        del self.player_list_volume[current_row]
        del self.player_list_rating[current_row]
        del self.player_list_speed[current_row]
        del self.player_list_normalize[current_row]
        del self.player_list_pan[current_row]
        del self.player_list_frequencies[current_row]
        del self.player_list_repeat[current_row]
        del self.player_list_open_file[current_row]
        self.player_list_position = []
        for row in range(0,self.player_list_data_length):
            #Change position cell
            self.player_list_position.append({})
            column_counter = 0
            change_position_frame = QtWidgets.QFrame()
            change_position_frame.setMinimumHeight(150)
            verticalLayout = QtWidgets.QVBoxLayout(change_position_frame)
            
            if(row!=0):
                self.player_list_position[row]["move up"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move up"].setMinimumHeight(50)
                self.player_list_position[row]["move up"].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move up"].setIcon(icon)
                verticalLayout.addWidget(self.player_list_position[row]["move up"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move up"].clicked.connect(lambda state,start_row=row,end_row=row-1: self.move_table_row(state,start_row,end_row))

            if(row!=self.player_list_data_length-1):
                self.player_list_position[row]["move down"] = QtWidgets.QPushButton(change_position_frame)
                self.player_list_position[row]["move down"].setMinimumHeight(50)
                self.player_list_position[row]["move down"].setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (Media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.player_list_position[row]["move down"].setIcon(icon1)
                verticalLayout.addWidget(self.player_list_position[row]["move down"])

                spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                verticalLayout.addItem(spacerItem)


                self.player_list_position[row]["move down"].clicked.connect(lambda state,start_row=row,end_row=row+1: self.move_table_row(state,start_row,end_row))

            change_position_frame.setStyleSheet("QFrame{border:0;padding:10px 10px 10px 10px;background:transparent;}")
            self.main_self.ui.player_list_table.setCellWidget(row,column_counter,change_position_frame)

        self.main_self.ui.player_list_table.resizeRowsToContents()
        self.main_self.ui.player_list_table.resizeColumnsToContents()
        if current_row!=self.player_list_data_length+1:
            self.main_self.ui.player_list_table.selectRow(current_row)
        else:
            self.main_self.ui.player_list_table.selectRow(self.player_list_data_length)
        
        #3. QListWidget
        if current_row!=self.player_list_data_length:#not the last
            self.main_self.ui.listWidget.blockSignals(True)
            self.selected_row = current_row
            self.main_self.ui.listWidget.takeItem(current_row)
            self.main_self.ui.listWidget.blockSignals(False)
            self.main_self.ui.listWidget.setCurrentRow(current_row)
            self.list_widget_changed(self.main_self.ui.listWidget.item(current_row),None)          
        else:
            self.main_self.ui.listWidget.blockSignals(True)
            self.selected_row = self.player_list_data_length-1
            self.main_self.ui.listWidget.takeItem(current_row)
            self.main_self.ui.listWidget.blockSignals(False)
            self.main_self.ui.listWidget.setCurrentRow(self.player_list_data_length-1)
            self.list_widget_changed(self.main_self.ui.listWidget.item(self.player_list_data_length),None)            
            
        #4. Process table and database
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"delete","player_number":player_list_number})
        
        self.main_self.manage_decks_instance.general_deck_next_player_list_items()

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
       
    def rating_changed(self,state,new_rating,player_list_number,save=False):
        rating = int(new_rating)
        rest_rating = 10 - int(new_rating)
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                self.player_list_data[counter]["rating"] = new_rating
                break
            counter += 1
            
            
        for i in range(0,rating):
            self.player_list_rating[row]["labels"][i].setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star_yellow.png"))
            self.player_list_rating[row]["labels"][i].clicked.disconnect()
            self.player_list_rating[row]["labels"][i].clicked.connect(lambda state,new_rating=i+1,player_number=player_list_number:self.rating_changed(state,new_rating,player_number,save=True))

        for i in range(0,rest_rating):  
            self.player_list_rating[row]["labels"][rating+i].setPixmap(QtGui.QPixmap(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/star.png"))
            self.player_list_rating[row]["labels"][rating+i].clicked.disconnect()
            self.player_list_rating[row]["labels"][rating+i].clicked.connect(lambda state,new_rating=rating+i+1,player_number=player_list_number:self.rating_changed(state,new_rating,player_number,save=True))
        
        if save==True:
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.manage_decks_instance.deck_1_rating_changed(None,new_rating,save=False)
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                    self.main_self.manage_decks_instance.deck_2_rating_changed(None,new_rating,save=False)
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["rating"] = new_rating
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["rating"] = new_rating
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_rating_changed(None,rating,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"rating","relative_number":relative_number,"relative_type":relative_type,"rating":rating,"save":False})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.rating_changed(None,new_rating,player_list_row["player_number"],save=False)
                counter += 1
        
    def player_list_volume_released(self,player_list_number):
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                if player_list_row["relative_type"]!="time_collections":
                    volume = player_list_row["details"]["volume"]
                else:
                    volume = player_list_row["current_time_item"]["volume"]
                return self.player_list_volume_changed(player_list_number,volume,save=True)

    def player_list_volume_moved(self,volume,player_list_number):
        self.main_self.ui.player_list_frame.setEnabled(False)
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                if player_list_row["relative_type"]!="time_collections":
                    player_list_row["details"]["volume"] = volume
                else:
                    player_list_row["current_time_item"]["volume"] = volume
            counter += 1
            
        self.player_list_volume[row]["volume label"].setText(str(volume)+"/200")
        
    def player_list_volume_changed(self,player_list_number,volume,save=True):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                self.player_list_data[counter]["volume"] = volume
                break
            counter += 1
            
        self.player_list_volume[row]["volume"].blockSignals(True)
        self.player_list_volume[row]["volume"].setValue(volume)
        self.player_list_volume[row]["volume"].blockSignals(False)
        self.player_list_volume[row]["volume label"].setText(str(volume)+"/200")
        
        if save==True:
        
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.ui.deck_1_volume_slider.blockSignals(True)
                    self.main_self.ui.deck_1_volume_slider.setValue(volume)
                    self.main_self.ui.deck_1_volume_label.setText(str(volume)+"/200")
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["volume"] = volume
                    self.main_self.ui.deck_1_volume_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_volume_slider.blockSignals(True)
                    self.main_self.ui.deck_2_volume_slider.setValue(volume)
                    self.main_self.ui.deck_2_volume_label.setText(str(volume)+"/200")
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["volume"] = volume
                    self.main_self.ui.deck_2_volume_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["volume"] = volume
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["volume"] = volume
                        
                    self.main_self.ui.music_clip_deck_volume_slider.blockSignals(True)
                    self.main_self.ui.music_clip_deck_volume_slider.setValue(volume)
                    self.main_self.ui.music_clip_deck_volume_label.setText(str(volume)+"/200")
                    self.main_self.ui.music_clip_deck_volume_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_volume_changed(volume,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"volume","relative_number":relative_number,"relative_type":relative_type,"volume":volume,"save":False})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.player_list_volume_changed(player_list_row["player_number"],volume,save=False)
                counter += 1
        
    def reset_volume(self,state,player_list_number):
        volume = 100
        return self.player_list_volume_changed(player_list_number,volume,save=True)
        
    def player_list_normalize_changed(self,player_number,new_state,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if new_state == Qt.Checked:
            normalize = 1
        else:
            normalize = 0
        
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                self.player_list_data[counter]["normalize"] = normalize
                break
            counter += 1
            
        self.player_list_normalize[row]["normalize checkbox"].blockSignals(True)
        self.player_list_normalize[row]["normalize checkbox"].setCheckState(new_state)
        self.player_list_normalize[row]["normalize checkbox"].blockSignals(False)
        
        if save==True:
        
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.ui.deck_1_normalize_checkbox.blockSignals(True)
                    self.main_self.ui.deck_1_normalize_checkbox.setCheckState(new_state)
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["normalize"] = normalize
                    self.main_self.ui.deck_1_normalize_checkbox.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_normalize_checkbox.blockSignals(True)
                    self.main_self.ui.deck_2_normalize_checkbox.setCheckState(new_state)
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["normalize"] = normalize
                    self.main_self.ui.deck_2_normalize_checkbox.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["normalize"] = normalize
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["normalize"] = normalize
                        
                    self.main_self.ui.music_clip_deck_normalize_checkbox.blockSignals(True)
                    self.main_self.ui.music_clip_deck_normalize_checkbox.setCheckState(new_state)
                    self.main_self.ui.music_clip_deck_normalize_checkbox.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_normalize_changed(normalize,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"normalize","relative_number":relative_number,"relative_type":relative_type,"normalize":normalize,"save":save})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.player_list_normalize_changed(player_list_row["player_number"],new_state,save=False)
                counter += 1
       
    def player_list_pan_changed(self,pan,player_list_number,save=True):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                self.player_list_data[counter]["pan"] = pan
                break
            counter += 1
            
        self.player_list_pan[row]["pan"].blockSignals(True)
        self.player_list_pan[row]["pan"].setValue(pan)
        self.player_list_pan[row]["pan"].blockSignals(False)
        self.player_list_pan[row]["pan label"].setText(str(pan))
        
        if save==True:
        
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.ui.deck_1_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_1_pan_slider.setValue(pan)
                    self.main_self.ui.deck_1_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_1_pan_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_2_pan_slider.setValue(pan)
                    self.main_self.ui.deck_2_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_2_pan_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["pan"] = pan
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["pan"] = pan
                        
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(True)
                    self.main_self.ui.music_clip_deck_pan_slider.setValue(pan)
                    self.main_self.ui.music_clip_deck_pan_label.setText(str(pan))
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_pan_changed(pan,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"pan","relative_number":relative_number,"relative_type":relative_type,"pan":pan,"save":True})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.player_list_pan_changed(pan,player_list_row["player_number"],save=False)
                counter += 1
        
    def player_list_pan_released(self,player_list_number):
        pass
        
    def reset_pan(self,state,player_list_number,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        counter = 0
        pan = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                self.player_list_data[counter]["pan"] = pan
                break
            counter += 1
            
        self.player_list_pan[row]["pan"].blockSignals(True)
        self.player_list_pan[row]["pan"].setValue(pan)
        self.player_list_pan[row]["pan"].blockSignals(False)
        self.player_list_pan[row]["pan label"].setText(str(pan))
        
        if save==True:
        
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.ui.deck_1_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_1_pan_slider.setValue(pan)
                    self.main_self.ui.deck_1_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_1_pan_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_pan_slider.blockSignals(True)
                    self.main_self.ui.deck_2_pan_slider.setValue(pan)
                    self.main_self.ui.deck_2_pan_label.setText(str(pan))
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["pan"] = pan
                    self.main_self.ui.deck_2_pan_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["pan"] = pan
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["pan"] = pan
                        
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(True)
                    self.main_self.ui.music_clip_deck_pan_slider.setValue(pan)
                    self.main_self.ui.music_clip_deck_pan_label.setText(str(pan))
                    self.main_self.ui.music_clip_deck_pan_slider.blockSignals(False)  
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_pan_changed(pan,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"pan","relative_number":relative_number,"relative_type":relative_type,"pan":pan,"save":True})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.player_list_pan_changed(pan,player_list_row["player_number"],save=False)
                counter += 1
        
    def low_frequency_changed(self,low_frequency,player_list_number):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.player_list_frequencies[counter]["high_frequency spinbox"].setMinimum(low_frequency)
            counter += 1
        
    def high_frequency_changed(self,high_frequency,player_list_number):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                self.player_list_frequencies[counter]["low_frequency spinbox"].setMaximum(high_frequency)
            counter += 1
        
    def apply_filter(self,state,player_list_number,low_frequency=None,high_frequency=None,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                if low_frequency == None:
                    low_frequency = self.player_list_frequencies[row]["low_frequency spinbox"].value()
                if high_frequency == None:
                    high_frequency = self.player_list_frequencies[row]["high_frequency spinbox"].value()
                self.player_list_frequencies[row]["low_frequency spinbox"].blockSignals(True)
                self.player_list_frequencies[row]["low_frequency spinbox"].setMaximum(high_frequency)
                self.player_list_frequencies[row]["low_frequency spinbox"].setValue(low_frequency)
                self.player_list_frequencies[row]["low_frequency spinbox"].blockSignals(False)
                
                self.player_list_frequencies[row]["high_frequency spinbox"].blockSignals(True)
                self.player_list_frequencies[row]["high_frequency spinbox"].setMinimum(low_frequency)
                self.player_list_frequencies[row]["high_frequency spinbox"].setValue(high_frequency)
                self.player_list_frequencies[row]["high_frequency spinbox"].blockSignals(False)
                break
            counter += 1
        
        if save==True:
        
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.ui.deck_1_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.deck_1_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_1_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.deck_1_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})

            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.deck_2_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_2_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.deck_2_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})

            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["high_frequency"] = high_frequency
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["high_frequency"] = high_frequency
                        
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.setValue(low_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(False)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.setValue(high_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_apply_filter(None,low_frequency,high_frequency,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"filter","relative_number":relative_number,"relative_type":relative_type,"low_frequency":low_frequency,"high_frequency":high_frequency,"save":True})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.apply_filter(None,player_list_row["player_number"],low_frequency,high_frequency,save=False)
                counter += 1
        
    def reset_filter(self,state,player_list_number,save=True):
        self.main_self.ui.player_list_frame.setEnabled(False)
        low_frequency = 20
        high_frequency = 20000
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_list_number:
                row = counter
                relative_type = player_list_row["relative_type"]
                relative_number = player_list_row["relative_number"]
                self.player_list_frequencies[row]["low_frequency spinbox"].blockSignals(True)
                self.player_list_frequencies[row]["low_frequency spinbox"].setMaximum(high_frequency)
                self.player_list_frequencies[row]["low_frequency spinbox"].setValue(low_frequency)
                self.player_list_frequencies[row]["low_frequency spinbox"].blockSignals(False)
                
                self.player_list_frequencies[row]["high_frequency spinbox"].blockSignals(True)
                self.player_list_frequencies[row]["high_frequency spinbox"].setMinimum(low_frequency)
                self.player_list_frequencies[row]["high_frequency spinbox"].setValue(high_frequency)
                self.player_list_frequencies[row]["high_frequency spinbox"].blockSignals(False)
                break
            counter += 1
        
        if save==True:
        
            #1. Deck 1
            if self.main_self.manage_decks_instance.deck_1["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_1["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_1["item"]["relative_number"]:
                    self.main_self.ui.deck_1_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.deck_1_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_1_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_1_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.deck_1_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_1_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_1["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})

            
            #2. Deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.deck_2["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.deck_2["item"]["relative_number"]:
                
                    self.main_self.ui.deck_2_low_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.deck_2_low_frequency.setValue(low_frequency)
                    self.main_self.ui.deck_2_low_frequency.blockSignals(False)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(True)
                    self.main_self.ui.deck_2_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.deck_2_high_frequency.setValue(high_frequency)
                    self.main_self.ui.deck_2_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["low_frequency"] = low_frequency
                    self.main_self.manage_decks_instance.deck_2["item"]["details"]["high_frequency"] = high_frequency
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})

            
            #3. Music clip Deck
            if self.main_self.manage_decks_instance.music_clip_deck["item"] is not None:
            
                if relative_type==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_type"] and relative_number==self.main_self.manage_decks_instance.music_clip_deck["item"]["relative_number"]:
                
                    if relative_type!="time_collections":
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["details"]["high_frequency"] = high_frequency
                    else:
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["low_frequency"] = low_frequency
                        self.main_self.manage_decks_instance.music_clip_deck["item"]["current_time_item"]["high_frequency"] = high_frequency
                        
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_low_frequency.setMaximum(high_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.setValue(low_frequency)
                    self.main_self.ui.music_clip_deck_low_frequency.blockSignals(False)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(True)
                    self.main_self.ui.music_clip_deck_high_frequency.setMinimum(low_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.setValue(high_frequency)
                    self.main_self.ui.music_clip_deck_high_frequency.blockSignals(False)
                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
            
            #4. QListWidget
            current_player_list_row = self.player_list_data[self.selected_row]
            if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
                self.list_widget_apply_filter(None,low_frequency,high_frequency,save=False)
            
            #4. Process table
            self.main_player_list_queue.put({"type":"filter","relative_number":relative_number,"relative_type":relative_type,"low_frequency":low_frequency,"high_frequency":high_frequency,"save":True})
            
            #6. QTableWidget
            counter = 0
            for player_list_row in self.player_list_data:
                if player_list_row["relative_number"]==relative_number and player_list_row["relative_type"]==relative_type:
                    if counter != row:
                        self.apply_filter(None,player_list_row["player_number"],low_frequency,high_frequency,save=False)
                counter += 1
        
    def player_list_change_repeats(self,state,player_list_number):
        self.main_self.ui.player_list_frame.setEnabled(False)
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"]==player_list_number:
                row = counter
                break
            counter += 1
            
        repeats = self.player_list_repeat[row]["repeats input"].value()
        self.player_list_data[row]["repeats"] = repeats
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"repeats","player_number":player_list_number,"repeats":repeats})
        
        if self.selected_row == row:
            self.main_self.ui.player_list_repeats_spinbox.setValue(repeats)

        if self.auto_dj==1:
            if self.main_self.manage_decks_instance.deck_1["item"] is not None and self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            elif self.main_self.manage_decks_instance.deck_1["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":self.main_self.manage_decks_instance.deck_1["play-status"],"deck_1_relative_type":self.main_self.manage_decks_instance.deck_1["item"]["relative_type"],"deck_1_relative_number":self.main_self.manage_decks_instance.deck_1["item"]["relative_number"],"deck_1_current_duration":self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"],"deck_1_total_duration":self.main_self.manage_decks_instance.deck_1["item"]["duration_milliseconds"],"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
            elif self.main_self.manage_decks_instance.deck_2["item"] is not None:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":self.main_self.manage_decks_instance.deck_2["play-status"],"deck_2_relative_type":self.main_self.manage_decks_instance.deck_2["item"]["relative_type"],"deck_2_relative_number":self.main_self.manage_decks_instance.deck_2["item"]["relative_number"],"deck_2_current_duration":self.main_self.manage_decks_instance.deck_2["current-duration-milliseconds"],"deck_2_total_duration":self.main_self.manage_decks_instance.deck_2["item"]["duration_milliseconds"]})
            else:
                self.main_player_list_queue.put({"type":"next_play","deck_1_status":"stopped","deck_1_relative_type":"","deck_1_relative_number":"","deck_1_current_duration":0,"deck_1_total_duration":0,"deck_2_status":"stopped","deck_2_relative_type":"","deck_2_relative_number":0,"deck_2_current_duration":0,"deck_2_total_duration":0})
        
    def open_file(self,row):
        if self.player_list_data[row]["relative_type"] == "time_collections":
            saved_path = self.player_list_data[row]["current_time_item"]["saved_path"]
        else:    
            saved_path = self.player_list_data[row]["details"]["saved_path"]
        saved_path = saved_path.replace("/","\\")
        subprocess.Popen('explorer /select,"'+saved_path+'"', shell=False)
        
    ### QListWidget + QTableWidget ###

    def display_mode_changed(self,index):
        self.main_self.ui.player_list_frame.setEnabled(False)
        self.main_self.ui.player_list_play_now_checkbox.blockSignals(True)
        if index==1:#Προβολή λίστας
            self.main_self.ui.player_list_inner_frame.show()
            self.main_self.ui.listWidget.setCurrentRow(self.selected_row)
            self.main_self.ui.player_list_table.hide()
        else:
            self.main_self.ui.player_list_inner_frame.hide()
            self.main_self.ui.player_list_table.show()
            self.main_self.ui.player_list_table.selectRow(self.selected_row)
        
        self.saves_in_progress += 1
        #self.main_self.ui.player_list_frame.setEnabled(False)
        self.main_player_list_queue.put({"type":"save_mode","mode":self.main_self.ui.player_list_mode.currentText()})
        self.main_self.ui.player_list_play_now_checkbox.blockSignals(False)
  
    def search_player_list_table(self,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        search_phrase = self.main_self.ui.player_list_search_phrase.text()
        if search_phrase=="":
            return self.clear_player_list_search(None)
        else:
            self.main_player_list_queue.put({"type":"search","search phrase":search_phrase})
 
    def search_results(self,hidden_rows):
        
        self.hidden_rows = hidden_rows
        for i in range(0,self.player_list_data_length):
            if i in self.hidden_rows:
                self.main_self.ui.listWidget.item(i).setHidden(True)
                self.main_self.ui.player_list_table.hideRow(i)
            else:
                self.main_self.ui.listWidget.setCurrentRow(i)            
                self.main_self.ui.listWidget.item(i).setHidden(False)
                self.main_self.ui.player_list_table.showRow(i)
                
        if len(self.hidden_rows)==self.player_list_data_length:
            for i in range(0,self.main_self.ui.gridLayout_24.count()):
                self.main_self.ui.gridLayout_24.itemAt(i).widget().hide()
        self.main_self.ui.player_list_frame.setEnabled(True)

    def clear_player_list_search(self,state):
        
        for i in range(0,self.main_self.ui.gridLayout_24.count()):
            self.main_self.ui.gridLayout_24.itemAt(i).widget().show()
        self.main_self.ui.player_list_search_phrase.setText("")
        self.main_self.ui.listWidget.setCurrentRow(0)
        for i in range(0,self.player_list_data_length):
            if i in self.hidden_rows:
                self.main_self.ui.player_list_table.showRow(i)
                self.main_self.ui.listWidget.item(i).setHidden(False)
        self.main_self.ui.player_list_frame.setEnabled(True)

    def proccess_save_finished(self):
        self.main_self.ui.player_list_frame.setEnabled(True)
        self.saves_in_progress -= 1
        if self.saves_in_progress<0:
            self.saves_in_progress = 0
        if self.saves_in_progress == 0:
            if self.quit_requested:
                self.main_self.MainWindow.close()

    def display_player_list_frame_information(self,total_files,total_duration,total_size):
        self.main_self.ui.player_list_frame.setEnabled(True)
        self.main_self.ui.player_list_sum_total_items_label.setText(str(total_files))
        self.main_self.ui.player_list_sum_total_duration_label.setText(str(total_duration))
        self.main_self.ui.player_list_sum_total_size_label.setText(str(total_size))

    def deck_rating_changed(self,relative_type,relative_number,rating):
        #1. Table
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["rating"] = rating
                else:
                    self.player_list_data[counter]["current_time_item"]["rating"] = rating
            counter += 1
            
        #2. Process table
        self.main_player_list_queue.put({"type":"rating","relative_number":relative_number,"relative_type":relative_type,"rating":rating,"save":False})
                
        #3. List widget
        current_player_list_row = self.player_list_data[self.selected_row]
        if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
            self.list_widget_rating_changed(None,rating,save=False)
        
        #4. Table widget
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                self.rating_changed(None,rating,player_list_row["player_number"],save=False)
               
    def deck_volume_changed(self,relative_type,relative_number,volume):
        #1. Table
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["volume"] = volume
                else:
                    self.player_list_data[counter]["current_time_item"]["volume"] = volume
            counter += 1
            
        #2. Process table
        self.main_player_list_queue.put({"type":"volume","relative_number":relative_number,"relative_type":relative_type,"volume":volume,"save":False})
                
        #3. List widget
        current_player_list_row = self.player_list_data[self.selected_row]
        if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
            self.list_widget_volume_changed(volume,save=False)
        
        #4. Table widget
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                self.player_list_volume_changed(player_list_row["player_number"],volume,save=False)
                             
    def deck_normalize_changed(self,relative_type,relative_number,new_state):
        if new_state == Qt.Checked:
            normalize = 1
        else:
            normalize = 0
        
        #1. Table
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["normalize"] = normalize
                else:
                    self.player_list_data[counter]["current_time_item"]["normalize"] = normalize
            counter += 1
            
        #2. Process table
        self.main_player_list_queue.put({"type":"normalize","relative_number":relative_number,"relative_type":relative_type,"normalize":normalize,"save":False})
                
        #3. List widget
        current_player_list_row = self.player_list_data[self.selected_row]
        if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
            self.list_widget_normalize_changed(new_state,save=False)
        
        #4. Table widget
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                self.player_list_normalize_changed(player_list_row["player_number"],new_state,save=False)
                                    
    def deck_pan_changed(self,relative_type,relative_number,pan):
        #1. Table
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["pan"] = pan
                else:
                    self.player_list_data[counter]["current_time_item"]["pan"] = pan
            counter += 1
            
        #2. Process table
        self.main_player_list_queue.put({"type":"pan","relative_number":relative_number,"relative_type":relative_type,"pan":pan,"save":False})
                
        #3. List widget
        current_player_list_row = self.player_list_data[self.selected_row]
        if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
            self.list_widget_pan_changed(pan,save=False)
        
        #4. Table widget
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                self.player_list_pan_changed(pan,player_list_row["player_number"],save=False)
                                     
    def deck_filter_changed(self,relative_type,relative_number,low_frequency,high_frequency):
        #1. Table
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["low_frequency"] = low_frequency
                    self.player_list_data[counter]["details"]["high_frequency"] = high_frequency
                else:
                    self.player_list_data[counter]["current_time_item"]["low_frequency"] = low_frequency
                    self.player_list_data[counter]["current_time_item"]["high_frequency"] = high_frequency
            counter += 1
            
        #2. Process table
        self.main_player_list_queue.put({"type":"filter","relative_number":relative_number,"relative_type":relative_type,"low_frequency":low_frequency,"high_frequency":high_frequency,"save":False})
                
        #3. List widget
        current_player_list_row = self.player_list_data[self.selected_row]
        if current_player_list_row["relative_type"] == relative_type and current_player_list_row["relative_number"] == relative_number:
            self.list_widget_apply_filter(None,low_frequency,high_frequency,save=False)
        
        #4. Table widget
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                self.apply_filter(None,player_list_row["player_number"],low_frequency,high_frequency,save=False)

    def player_list_repeat_changed(self,state):
        self.main_self.ui.player_list_frame.setEnabled(False)
        if state==Qt.Checked:
            self.repeat_player_list = 1
        else:
            self.repeat_player_list = 0
            
        self.main_self.ui.player_list_repeat_checkbox.blockSignals(True)
        self.main_self.ui.general_deck_repeat_player_list_checkbox.blockSignals(True)
        
        self.main_self.ui.player_list_repeat_checkbox.setCheckState(state)
        self.main_self.ui.general_deck_repeat_player_list_checkbox.setCheckState(state)
        
        self.main_self.ui.player_list_repeat_checkbox.blockSignals(False)
        self.main_self.ui.general_deck_repeat_player_list_checkbox.blockSignals(False)
        
        #save setting to database
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"repeat_player_list","repeat_player_list":self.repeat_player_list})

    def display_next_play(self,player_list_next_play):
        self.clear_next_play()
        
        #QListWidget
        for player_list_next_play_row in player_list_next_play:
            if player_list_next_play_row["player_number"]==self.player_list_data[self.selected_row]["player_number"]:
                self.main_self.ui.next_play_time_text.setText(str(player_list_next_play_row["next_play"]))
                break
                
        #QTableWidget
        for player_list_next_play_row in player_list_next_play:
            counter = 0
            
            for player_list_row in self.player_list_data:
                if int(player_list_next_play_row["player_number"]) == int(player_list_row["player_number"]):
                    column_counter = 4
                    next_play_item = QtWidgets.QTableWidgetItem(str(player_list_next_play_row["next_play"]))
                    next_play_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
                    self.main_self.ui.player_list_table.setItem(counter,column_counter,next_play_item)
                    self.player_list_data[counter]["next_play"] = str(player_list_next_play_row["next_play"])
                    break
                counter += 1
                
    def clear_next_play(self):
        #QListWidget
        self.main_self.ui.next_play_time_text.setText("")
                
        #QTableWidget
        counter = 0
        column_counter = 4
        for player_list_row in self.player_list_data:
            next_play_item = QtWidgets.QTableWidgetItem("")
            next_play_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
            self.main_self.ui.player_list_table.setItem(counter,column_counter,next_play_item)
            self.player_list_data[counter]["next_play"] = ""
            counter += 1

    ### Auto DJ ###
    def auto_dj_state_changed(self,auto_dj):
        if auto_dj == 1:
            self.auto_dj = 1
        elif auto_dj == 0:
            self.auto_dj = 0
        elif auto_dj == "button":
            if self.main_self.ui.general_deck_manage_auto_dj_button.text()=="Ενεργοποίηση αυτόματου DJ":
                self.auto_dj = 1
            else:
                self.auto_dj = 0
        else:
            if self.main_self.ui.player_list_auto_dj_checkbox.checkState()==Qt.Checked:
                self.auto_dj = 1
            else:
                self.auto_dj = 0
        if self.auto_dj == 0:
            self.main_self.ui.general_deck_manage_auto_dj_button.blockSignals(True)
            self.main_self.ui.general_deck_manage_auto_dj_button.setText("Ενεργοποίηση αυτόματου DJ")
            self.main_self.ui.general_deck_manage_auto_dj_button.blockSignals(False)

            self.main_self.ui.player_list_auto_dj_checkbox.blockSignals(True)
            self.main_self.ui.player_list_auto_dj_checkbox.setCheckState(Qt.Unchecked)
            self.main_self.ui.player_list_auto_dj_checkbox.blockSignals(False)

            self.deactivate_auto_dj()
        else:
            self.main_self.ui.general_deck_manage_auto_dj_button.blockSignals(True)
            self.main_self.ui.general_deck_manage_auto_dj_button.setText("Απενεργοποίηση αυτόματου DJ")
            self.main_self.ui.general_deck_manage_auto_dj_button.blockSignals(False)

            self.main_self.ui.player_list_auto_dj_checkbox.blockSignals(True)
            self.main_self.ui.player_list_auto_dj_checkbox.setCheckState(Qt.Checked)
            self.main_self.ui.player_list_auto_dj_checkbox.blockSignals(False)

            self.activate_auto_dj()			
		
        #save setting
        self.saves_in_progress += 1
        self.main_self.ui.player_list_frame.setEnabled(False)
        self.main_player_list_queue.put({"type":"auto_dj","auto_dj":self.auto_dj})
        
    def deactivate_auto_dj(self):
        #enable repeat playlist
        self.auto_dj = 0
        self.clear_next_play()
        if self.repeat_player_list_old == 1 or self.repeat_player_list_old==True or self.repeat_player_list_old:
            self.player_list_repeat_changed(Qt.Checked)
        else:
            self.player_list_repeat_changed(Qt.Unchecked)
		
		#enable buttons
        self.main_self.ui.general_deck_frame.setEnabled(True)
        self.main_self.ui.deck_1_frame.setEnabled(True)
        self.main_self.ui.deck_2_frame.setEnabled(True)
        self.main_self.ui.music_clip_deck_frame.setEnabled(True)
		
        self.main_self.manage_decks_instance.deck_1["play-status"] = self.main_self.manage_decks_instance.deck_1_status_changed("stopped")
        self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
        self.main_self.manage_decks_instance.deck_2["play-status"] = self.main_self.manage_decks_instance.deck_2_status_changed("stopped")
        self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_2","deck_2":self.main_self.manage_decks_instance.deck_2})
        self.main_self.manage_decks_instance.music_clip_deck["play-status"] = self.main_self.manage_decks_instance.music_clip_deck_status_changed("stopped")
        self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"music_clip_deck","music_clip_deck":self.main_self.manage_decks_instance.music_clip_deck})
        
        #save setting
        self.saves_in_progress += 1
        self.main_player_list_queue.put({"type":"auto_dj","auto_dj":self.auto_dj})
        
    def activate_auto_dj(self,repeat=1):
        #enable repeat playlist
        self.auto_dj = 1
        self.repeat_player_list_old = self.repeat_player_list
        if repeat == 1:
            self.player_list_repeat_changed(Qt.Checked)
        else:
            self.player_list_repeat_changed(Qt.Unchecked)
		
        #disable decks
        self.main_self.ui.general_deck_frame.setEnabled(False)
        self.main_self.ui.deck_1_frame.setEnabled(False)
        self.main_self.ui.deck_2_frame.setEnabled(False)
        self.main_self.ui.music_clip_deck_frame.setEnabled(False)

        if self.main_self.manage_decks_instance.deck_1["play-status"]!="playing" and self.main_self.manage_decks_instance.deck_2["play-status"]!="playing":
            if self.main_self.manage_decks_instance.deck_1["item"] is None:
                #play first track in deck 1
                
                
                for player_list_row in self.player_list_data:
                    if player_list_row["relative_type"]!="time_collections":
                        player_list_number = player_list_row["player_number"]
                        self.prepare_and_play_deck_1(None,player_list_number)
                        break
            else:
                self.main_self.manage_decks_instance.deck_1["chunk-number"] = 0
                self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"] = 0
                self.main_self.manage_decks_instance.deck_1["play-status"] = self.main_self.manage_decks_instance.deck_1_status_changed("playing")
                self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1","deck_1":self.main_self.manage_decks_instance.deck_1})
                if self.main_self.manage_decks_instance.deck_1_current_duration!=0:
                    #calculate new chunk_number
                    chunk_number = round(self.main_self.manage_decks_instance.deck_1_current_duration/744)
                    current_duration_milliseconds = chunk_number*744
                    self.main_self.manage_decks_instance.deck_1["chunk-number"] = chunk_number
                    self.main_self.manage_decks_instance.deck_1["current-duration-milliseconds"] = current_duration_milliseconds

                    current_duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(current_duration_milliseconds)
                    self.main_self.ui.deck_1_time_label.setText(str(current_duration_human)+"/"+str(self.deck_1["item"]["duration_human"]))

                    self.main_self.manage_decks_instance.manage_final_sound_queue.put({"type":"deck_1_chunk","chunk-number":chunk_number,"current-duration-milliseconds":current_duration_milliseconds})

                    self.main_self.manage_decks_instance.deck_1_current_duration = 0
                 
			
            #prepare next song in deck 2
            if self.main_self.manage_decks_instance.deck_2["item"] is None:
                for player_list_row in self.player_list_data:
                    if player_list_row["relative_type"]!="time_collections":
                        player_list_number = player_list_row["player_number"]
                        self.prepare_deck_2(None,player_list_number)
                        break
        else:
            if self.main_self.manage_decks_instance.deck_1["play-status"]=="playing" and self.main_self.manage_decks_instance.deck_1["play-status"]!="playing":
                if self.main_self.manage_decks_instance.deck_2["item"] is None:
                    #prepare deck 2
                    for player_list_row in self.player_list_data:
                        if player_list_row["relative_type"]!="time_collections":
                            player_list_number = player_list_row["player_number"]
                            self.prepare_deck_2(None,player_list_number)
                            break
            else:
                #prepare deck 1
                if self.main_self.manage_decks_instance.deck_1["item"] is None:
                    for player_list_row in self.player_list_data:
                        if player_list_row["relative_type"]!="time_collections":
                            player_list_number = player_list_row["player_number"]
                            self.prepare_deck_1(None,player_list_number)
                            break
        
class Main_Player_List_Emitter(QThread):

    player_list_data_fetched = pyqtSignal(list,str,str,str,str,bool,bool)
    repeat_and_auto_dj_settings = pyqtSignal(bool,bool)
    search_results = pyqtSignal(list)
    proccess_save_finished = pyqtSignal()
    insert_finished = pyqtSignal(str,int,bool,dict)
    insert_and_play_finished = pyqtSignal(str,int,dict,str)
    metrics = pyqtSignal(str,str,str)
    update_time_row = pyqtSignal(int,dict)
    last_player_history = pyqtSignal(list)
    player_list_fields = pyqtSignal(dict)
    next_play = pyqtSignal(list)

    def __init__(self, from_process: Pipe):
        super().__init__()
        self.data_from_process = from_process

    def run(self):
        while True:
            data = self.data_from_process.recv()
            if data["type"]=="player_list_data_fetched":
                self.player_list_data_fetched.emit(data["rows"],data["display mode"],data["items count"],data["duration count"],data["size count"],data["all_false"],data["all_true"])
            elif data["type"]=="search_results":
                self.search_results.emit(data["hidden rows"])
            elif data["type"]=="metrics":
                self.metrics.emit(data["items count"],data["duration count"],data["size count"])
            elif data["type"]=="proccess_save_finished":
                self.proccess_save_finished.emit()
            elif data["type"]=="insert_finished":
                self.insert_finished.emit(data["relative_type"],data["relative_number"],data["play"],data["player_list_item"])
            elif data["type"]=="insert_and_play_finished":
                self.insert_and_play_finished.emit(data["relative_type"],data["relative_number"],data["player_list_item"],data["deck"])
            elif data["type"] == "repeat_and_auto_dj_settings":
                self.repeat_and_auto_dj_settings.emit(data["repeat_player_list"],data["auto_dj"])
            elif data["type"] == "update_time_row":
                self.update_time_row.emit(data["row"],data["player_list_row"])
            elif data["type"] == "last_player_history":
                self.last_player_history.emit(data["last_player_history"])
            elif data["type"] == "player_list_fields":
                self.player_list_fields.emit(data["settings"])
            elif data["type"] == "next_play":
                self.next_play.emit(data["next_play"])
                
class Main_Player_List_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother):
        super().__init__()
        self.daemon = False
        self.to_emitter = to_emitter
        self.data_from_mother = from_mother
        
    def run(self):
        self.read_data()
        self.repeat_and_auto_dj_settings()
        self.player_list_fields()
        while(True):
            data = self.data_from_mother.get()
            if data["type"] == "read":
                self.read_data()
            elif data["type"] == "insert":
                self.insert_player_list_item(data["relative_type"],data["relative_number"],data["repeats"],data["play"])
            elif data["type"] == "insert_and_play":
                self.insert_and_play(data["relative_type"],data["relative_number"],data["deck"])
            elif data["type"] == "insert_bottom":    
                self.insert_player_list_item_bottom(data["relative_type"],data["relative_number"],data["repeats"],data["play"])
            elif data["type"]=="rating":
                self.rating_changed(data["relative_type"],data["relative_number"],data["rating"],data["save"])
            elif data["type"]=="volume":
                self.volume_changed(data["relative_type"],data["relative_number"],data["volume"],data["save"])
            elif data["type"]=="pan":
                self.pan_changed(data["relative_type"],data["relative_number"],data["pan"],data["save"])
            elif data["type"] == "save_mode":
                self.save_mode(data["mode"])
            elif data["type"] == "repeats":
                self.repeats_changed(data["player_number"],data["repeats"])
            elif data["type"] == "normalize":
                self.normalize_changed(data["relative_number"],data["relative_type"],data["normalize"],data["save"])
            elif data["type"] == "filter":
                self.filter_changed(data["relative_number"],data["relative_type"],data["low_frequency"],data["high_frequency"],data["save"])
            elif data["type"] == "select_all":
                self.select_all(data["play"])
            elif data["type"] == "play":
                self.play_changed(data["play"],data["player_number"])
            elif data["type"] == "move":
                self.move(data["start"],data["end"])
            elif data["type"] == "delete":
                self.delete_row(data["player_number"])
            elif data["type"] == "search":
                self.search_data(data["search phrase"])
            elif data["type"] == "repeat_player_list":
                self.save_repeat_player_list(data["repeat_player_list"])
            elif data["type"] == "update_last_play":
                self.last_play_changed(data["relative_type"],data["relative_number"],data["last_play"])
            elif data["type"] == "auto_dj":
                self.auto_dj_changed(data["auto_dj"])
            elif data["type"] == "update_time_row":
                self.update_time_row()
            elif data["type"] == "last_player_history":
                self.last_player_history()
            elif data["type"] == "player_list_fields":
                self.player_list_fields()
            elif data["type"] == "next_play":
                self.find_next_play(data["deck_1_status"],data["deck_1_relative_type"],data["deck_1_relative_number"],data["deck_1_current_duration"],data["deck_1_total_duration"],data["deck_2_status"],data["deck_2_relative_type"],data["deck_2_relative_number"],data["deck_2_current_duration"],data["deck_2_total_duration"])
    
    def find_next_play(self,deck_1_status,deck_1_relative_type,deck_1_relative_number,deck_1_current_duration,deck_1_total_duration,deck_2_status,deck_2_relative_type,deck_2_relative_number,deck_2_current_duration,deck_2_total_duration):
        #this method will only be called when auto_dj == True
        now = datetime.now()
        self.player_list_next_play = []
        
        t1 = now
        if deck_1_status=="playing":
            time_remaining = deck_1_total_duration - deck_1_current_duration
            t1 = now + timedelta(milliseconds=time_remaining)+timedelta(milliseconds=deck_2_total_duration)
        elif deck_2_status=="playing":
            time_remaining = deck_2_total_duration - deck_2_current_duration
            t1 = now + timedelta(milliseconds=time_remaining)+timedelta(milliseconds=deck_1_total_duration)
            
        for player_list_row in self.player_list_data:
            if int(player_list_row["play"])==1:
                self.player_list_next_play.append({"player_number":player_list_row["player_number"],"next_play":t1.strftime("%Y-%m-%d %H:%M:%S")})
                if player_list_row["relative_type"]!="time_collections" and player_list_row["relative_type"]!="retransmitions":
                    item_total_time = (int(player_list_row["repeats"])+1)*int(player_list_row["details"]["duration_milliseconds"])
                elif player_list_row["relative_type"]=="retransmitions":
                    item_total_time = (int(player_list_row["repeats"])+1)*int(player_list_row["duration_milliseconds"])
                else:
                    item_total_time = int(player_list_row["current_time_item"]["duration_milliseconds"])
                    append = int(player_list_row["details"][0]["append"])
                    if append == 1:
                        append_relative_type = player_list_row["details"][0]["append_relative_type"]
                        append_relative_number = player_list_row["details"][0]["append_relative_number"]
                        item = database_functions.read_item_by_type_and_number(append_relative_type,append_relative_number)
                        item_total_time += item["duration_milliseconds"]
                            
                t1 = t1 + timedelta(milliseconds=item_total_time)
            
        self.to_emitter.send({"type":"next_play","next_play":self.player_list_next_play})
                                      
    def read_data(self):
        self.display_mode = database_functions.read_setting("player_list_display")["current_value"]
        self.player_list_data = database_functions.read_player_list()
        counter = 0
        for player_list_item in self.player_list_data:
            if player_list_item["relative_type"]=="time_collections":
                time_collection = player_list_item["details"][0]
                time_collection_items = player_list_item["details"][1]
                time_collection_case = time_collection["case"]
                when_to_play = when_to_play_function.find_when_to_play(time_collection_case)
                for collection_item in time_collection_items:
                    if when_to_play == collection_item["when_to_play"]:
                        self.player_list_data[counter]["current_time_item"] = collection_item

                        append = int(time_collection["append"])
                        if append == 1:
                            append_relative_type = time_collection["append_relative_type"]
                            append_relative_number = time_collection["append_relative_number"]
                            append_item = database_functions.read_item_by_type_and_number(append_relative_type,append_relative_number)
                            self.player_list_data[counter]["duration_milliseconds"] = int(collection_item["duration_milliseconds"])+int(append_item["duration_milliseconds"])
                            self.player_list_data[counter]["current_time_item"]["duration_milliseconds"] = self.player_list_data[counter]["duration_milliseconds"]
                            self.player_list_data[counter]["duration_human"] = convert_time_function.convert_duration_from_milliseconds_to_human(self.player_list_data[counter]["duration_milliseconds"])
                            self.player_list_data[counter]["current_time_item"]["duration_human"] = self.player_list_data[counter]["duration_human"]
                        break
                        
            counter += 1
        
        plays = [str(item["play"]) for item in self.player_list_data]
        if "1" in plays:
            all_false = False
        else:
            all_false = True
        if "0" in plays:
            all_true = False
        else:
            all_true = True
        
        total_items,total_duration,total_size = self.player_list_metrics()

        #self.repeat_player_list = bool(database_functions.read_setting("repeat_player_list")["current_value"])
        #self.auto_dj = bool(int(database_functions.read_setting("auto_dj")["current_value"]))

        self.to_emitter.send({"type":"player_list_data_fetched","rows":self.player_list_data,"display mode":self.display_mode,"items count":total_items,"duration count":total_duration,"size count":total_size,"all_false":all_false,"all_true":all_true})

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

    def repeat_and_auto_dj_settings(self):
        self.repeat_player_list = bool(database_functions.read_setting("repeat_player_list")["current_value"])
        self.auto_dj = bool(int(database_functions.read_setting("auto_dj")["current_value"]))
        self.to_emitter.send({"type":"repeat_and_auto_dj_settings","repeat_player_list":self.repeat_player_list,"auto_dj":self.auto_dj})

    def player_list_metrics(self):
        total_items = 0
        total_duration = 0
        total_size = 0
        for player_list_row in self.player_list_data:
            if int(player_list_row["play"])==1:
                repeats = player_list_row["repeats"]
                total_items+= 1+repeats
                if player_list_row["relative_type"]!="time_collections":
                    item = player_list_row["details"]
                else:
                    item = player_list_row["current_time_item"]
                    append = int(player_list_row["details"][0]["append"])
                    if append == 1:
                        append_relative_type = player_list_row["details"][0]["append_relative_type"]
                        append_relative_number = player_list_row["details"][0]["append_relative_number"]
                        append_item = database_functions.read_item_by_type_and_number(append_relative_type,append_relative_number)
                        item["duration_milliseconds"] = int(item["duration_milliseconds"])+int(append_item["duration_milliseconds"])
                    
                if player_list_row["relative_type"]=="retransmitions":
                    item["duration_milliseconds"] = player_list_row["duration_milliseconds"]
                    item["duration_human"] = player_list_row["duration_human"]
                total_duration += (item["duration_milliseconds"])*(repeats+1)
                if(item["type"]=="retransmitions"):
                    #to be correct 100% change 128 with stream bit rate
                    total_size += (1+repeats)*(128*1024*int(item["duration_milliseconds"])/1000)
                else:
                    try:
                        path = item["saved_path"]
                        if(os.path.exists(path)):
                            total_size += (1+repeats)*os.path.getsize(os.path.realpath(os.path.abspath(path)))
                    except:
                        print("Error")
            
        total_duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(total_duration)
        total_size = convert_bytes_function.convert_size(total_size)
        return str(total_items),total_duration_human,total_size
          
    def search_data(self,search_phrase):
        hidden_rows = []
        counter = 0
        for player_list_row in self.player_list_data:
            hide_row = True
            for key in player_list_row:
                if str(search_phrase) in str(player_list_row[key]):
                    hide_row = False
                    break
            if hide_row == True:
                hidden_rows.append(counter)
            counter += 1
        self.to_emitter.send({"type":"search_results","hidden rows":hidden_rows})

    def insert_player_list_item(self,relative_type,relative_number,repeats,play):
        item = database_functions.read_item_by_type_and_number(relative_type,relative_number)
        player_list_item = {
            "play":1,
            "relative_type":relative_type,
            "relative_number":relative_number,
            "repeats":repeats,
            "duration_milliseconds":item["duration_milliseconds"],
            "duration_human":item["duration_human"],
            "position":1
        }
        player_list_item = database_functions.import_player_list_item(player_list_item)
        
        self.to_emitter.send({"type":"insert_finished","relative_type":relative_type,"relative_number":relative_number,"play":play,"player_list_item":player_list_item})
        
        self.player_list_data.insert(0,player_list_item)
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})
        
    def insert_and_play(self,relative_type,relative_number,deck):
        item = database_functions.read_item_by_type_and_number(relative_type,relative_number)
        player_list_item = {
            "play":1,
            "relative_type":relative_type,
            "relative_number":relative_number,
            "repeats":0,
            "duration_milliseconds":item["duration_milliseconds"],
            "duration_human":item["duration_human"],
            "position":1
        }
        player_list_item = database_functions.import_player_list_item(player_list_item)
        
        self.to_emitter.send({"type":"insert_and_play_finished","relative_type":relative_type,"relative_number":relative_number,"player_list_item":player_list_item,"deck":deck})
        
        self.player_list_data.insert(0,player_list_item)
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})
        
    def insert_player_list_item_bottom(self,relative_type,relative_number,repeats,play):
        item = database_functions.read_item_by_type_and_number(relative_type,relative_number)
        player_list_item = {
            "play":1,
            "relative_type":relative_type,
            "relative_number":relative_number,
            "repeats":repeats,
            "duration_milliseconds":item["duration_milliseconds"],
            "duration_human":item["duration_human"],
            "position":len(self.player_list_data)
        }
        player_list_item = database_functions.import_player_list_item(player_list_item)
        
        self.to_emitter.send({"type":"insert_finished","relative_type":relative_type,"relative_number":relative_number,"play":play,"player_list_item":player_list_item})
        
        self.player_list_data.insert(0,player_list_item)
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})
       
    def rating_changed(self,relative_type,relative_number,rating,save):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["rating"] = rating
                else:
                    self.player_list_data[counter]["current_time_item"]["rating"] = rating
            counter += 1
            
        if save==True:
            if relative_type!="time_collections":
                database_functions.db_item_rating_changed(relative_type,relative_number,rating)
            else:
                database_functions.db_item_rating_changed("time_items",relative_number,rating)

        self.to_emitter.send({"type":"proccess_save_finished"})

    def volume_changed(self,relative_type,relative_number,volume,save):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["volume"] = volume
                else:
                    self.player_list_data[counter]["current_time_item"]["volume"] = volume
            counter += 1
            
        if save==True:
            if relative_type!="time_collections":
                database_functions.update_item_volume(relative_type,relative_number,volume)
            else:
                database_functions.update_item_volume("time_items",relative_number,volume)

            
        self.to_emitter.send({"type":"proccess_save_finished"})
 
    def pan_changed(self,relative_type,relative_number,pan,save):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["pan"] = pan
                else:
                    self.player_list_data[counter]["current_time_item"]["pan"] = pan
            counter += 1
            
        if save==True:
            if relative_type!="time_collections":
                database_functions.update_item_pan(relative_type,relative_number,pan)
            else:
                database_functions.update_item_pan("time_items",relative_number,pan)

            
        self.to_emitter.send({"type":"proccess_save_finished"})
 
    def save_mode(self,mode):
        setting = {"current_value":mode,"keyword":"player_list_display"}
        success = database_functions.update_setting(setting)
        self.to_emitter.send({"type":"proccess_save_finished"})

    def repeats_changed(self,player_number,repeats):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"]==player_number:
                self.player_list_data[counter]["repeats"] = repeats
            counter += 1
            
        database_functions.player_list_repeats_changed(player_number,repeats)
        self.to_emitter.send({"type":"proccess_save_finished"})
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})
        
    def normalize_changed(self,relative_number,relative_type,normalize,save):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["normalize"] = normalize
                else:
                    self.player_list_data[counter]["current_time_item"]["normalize"] = normalize
            counter += 1
        
        if save==True:
            if relative_type!="time_collections":
                database_functions.update_item_normalize(relative_type,relative_number,normalize)
            else:
                database_functions.update_item_normalize("time_items",relative_number,normalize)

            
        self.to_emitter.send({"type":"proccess_save_finished"})

    def filter_changed(self,relative_number,relative_type,low_frequency,high_frequency,save):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"]==relative_type and player_list_row["relative_number"]==relative_number:
                if relative_type!="time_collections":
                    self.player_list_data[counter]["details"]["low_frequency"] = low_frequency
                    self.player_list_data[counter]["details"]["high_frequency"] = high_frequency
                else:
                    self.player_list_data[counter]["current_time_item"]["low_frequency"] = low_frequency
                    self.player_list_data[counter]["current_time_item"]["high_frequency"] = high_frequency
            counter += 1
            
        if save==True:
            if relative_type!="time_collections":
                database_functions.update_item_filter(relative_type,relative_number,low_frequency,high_frequency)
            else:
                database_functions.update_item_filter("time_items",relative_number,low_frequency,high_frequency)

            
        self.to_emitter.send({"type":"proccess_save_finished"})
        
    def select_all(self,play):
        for row in range(0,len(self.player_list_data)):
            self.player_list_data[row]["play"] = play
        
        database_functions.player_list_play_all(play)
        self.to_emitter.send({"type":"proccess_save_finished"})
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})
                     
    def play_changed(self,play,player_number):
        
        for row in range(0,len(self.player_list_data)):
            if self.player_list_data[row]["player_number"] == player_number:
                self.player_list_data[row]["play"] = play
                break
        
        database_functions.player_list_play_changed(player_number,play)
        self.to_emitter.send({"type":"proccess_save_finished"})
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})

    def move(self,start,end):
    
        start_position = self.player_list_data[start]["position"]
        success = database_functions.move_player_list_item(start_position,end+1,self.player_list_data[start])
        
        #self.read_data()
        
        item_full = self.player_list_data[start]
        del self.player_list_data[start]
        self.player_list_data.insert(end,item_full)
        
        self.to_emitter.send({"type":"proccess_save_finished"})
    
    def delete_row(self,player_number):
        counter = 0
        row = None
        for player_list_row in self.player_list_data:
            if player_list_row["player_number"] == player_number:
                row = counter
                break
            counter += 1
        success = database_functions.delete_player_list_item(self.player_list_data[row])
        del self.player_list_data[row]
        self.to_emitter.send({"type":"proccess_save_finished"})
        
        total_items,total_duration_human,total_size = self.player_list_metrics()
        self.to_emitter.send({"type":"metrics","items count":total_items,"duration count":total_duration_human,"size count": total_size})

    def search_data(self,search_phrase):
        hidden_rows = []
        counter = 0
        for player_list_row in self.player_list_data:
            hide_row = True
            for key in player_list_row:
                if str(search_phrase) in str(player_list_row[key]):
                    hide_row = False
                    break
            if hide_row == True:
                hidden_rows.append(counter)
            counter += 1
        self.to_emitter.send({"type":"search_results","hidden rows":hidden_rows})

    def save_repeat_player_list(self,repeat_player_list):
        database_functions.update_setting({"current_value":repeat_player_list,"keyword":"repeat_player_list"})
        self.to_emitter.send({"type":"proccess_save_finished"})    

    def last_play_changed(self,relative_type,relative_number,last_play):
        counter = 0
        for player_list_row in self.player_list_data:
            if player_list_row["relative_type"] == relative_type and player_list_row["relative_number"] == relative_number:
                self.player_list_data[counter]["last_play"] = last_play
                
        #database_functions.update_last_play(relative_type,relative_number,last_play)
        self.to_emitter.send({"type":"proccess_save_finished"})
        
    def auto_dj_changed(self,auto_dj):
        database_functions.update_setting({"keyword":"auto_dj","current_value":auto_dj})
        self.to_emitter.send({"type":"proccess_save_finished"})

    def update_time_row(self):
        self.player_list_data = database_functions.read_player_list()
        counter = 0
        for player_list_item in self.player_list_data:
            if player_list_item["relative_type"]=="time_collections":
                time_collection = player_list_item["details"][0]
                time_collection_items = player_list_item["details"][1]
                time_collection_case = time_collection["case"]
                when_to_play = when_to_play_function.find_when_to_play(time_collection_case)
                for collection_item in time_collection_items:
                    if when_to_play == collection_item["when_to_play"]:
                        self.player_list_data[counter]["current_time_item"] = collection_item
                        row = counter
                        break
            counter += 1
            
        self.to_emitter.send({"type":"update_time_row","row":row,"player_list_row":self.player_list_data[row]})

    def last_player_history(self):
        last_player_history_items = database_functions.read_last_player_histories()
        self.to_emitter.send({"type":"last_player_history","last_player_history":last_player_history_items})
        
class Delegate(QStyledItemDelegate):
    checked = pyqtSignal(QtCore.QModelIndex,int)
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.text = f"{index.row() + 1}. {option.text}"
        
    def editorEvent(self, event, model, option, index):
        if model.flags(index) & QtCore.Qt.ItemIsUserCheckable:
            # before the change
            last_value = index.data(QtCore.Qt.CheckStateRole)
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if model.flags(index) & QtCore.Qt.ItemIsUserCheckable:
            # after the change
            new_value = index.data(QtCore.Qt.CheckStateRole)
            if last_value != new_value:
                self.checked.emit(index, new_value)
        return value