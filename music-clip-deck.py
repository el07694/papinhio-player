from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from multiprocessing import Process, Queue, Pipe
import sys
from datetime import datetime, timedelta
import time
import traceback
import pyaudio
from pydub import AudioSegment, effects, utils, generators
import math
from pydub.utils import which
import numpy as np
AudioSegment.converter = which("ffmpeg")
import copy
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")

import importlib

icons = importlib.import_module('compiled-ui.icons')
database_functions = importlib.import_module("python+.lib.sqlite3-functions")
convert_time_function = importlib.import_module("python+.lib.convert-time-function")


class Music_Clip_Deck:
    def __init__(self,main_self):
        try:
            ### THIS DECK WILL ONLY PLAY SOUND CLIP FILES NO RETRANSMITIONS NO SOUND FILES NO TIME COLLECTIONS, ... ###
            self.main_self = main_self

            self.deck_status = "stopped"
            self.clip = None
            self.put_to_q = False

            self.main_self.ui.music_clip_deck_title.setText("")

            # create process
            self.process_number = 96
            self.music_clip_deck_mother_pipe, self.music_clip_deck_child_pipe = Pipe()
            self.music_clip_deck_queue = Queue()
            self.music_clip_deck_emitter = Music_Clip_Deck_Emitter(self.music_clip_deck_mother_pipe)
            self.music_clip_deck_emitter.error_signal.connect(lambda error_message: self.main_self.open_music_clip_deck_error_window(error_message))
            self.music_clip_deck_emitter.music_clip_deck_ready.connect(lambda slice: self.music_clip_deck_slice_ready(slice))
            self.music_clip_deck_emitter.top_music_clips.connect(lambda clips: self.top_music_clips(clips))
            self.music_clip_deck_emitter.volume_amplitude.connect(lambda normalized_value: self.display_volume_amplitude(normalized_value))
            self.music_clip_deck_emitter.current_duration_milliseconds.connect(lambda duration: self.display_current_duration(duration))
            self.music_clip_deck_emitter.deck_finished.connect(lambda: self.deck_finished())
            self.music_clip_deck_emitter.chunk_number_answer.connect(lambda chunk_number: self.main_self.player_list_instance.chunk_number_answer("music_clip_deck", chunk_number))
            self.music_clip_deck_emitter.fade_out_start.connect(lambda: self.fade_out_start())


            self.music_clip_deck_emitter.start()
            self.music_clip_deck_child_process = Music_Clip_Deck_Child_Proc(self.music_clip_deck_child_pipe, self.music_clip_deck_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.music_clip_deck_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.music_clip_deck_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
            self.put_to_q = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def fade_out_start(self):
        try:
            if self.main_self.player_list_instance.player_list_settings["auto_dj"]:
                self.main_self.player_list_instance.dj_fade_out_start()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def deck_finished(self):
        try:
            self.deck_status = "stopped"
            self.display_current_duration(0)
            self.display_volume_amplitude(0)
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(":/rest-icons/assets/icons/rest-icons/play-song.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
            self.main_self.ui.music_clip_deck_play_or_pause.setIcon(icon1)

            if self.main_self.player_list_instance.auto_dj_mode:
                if not (self.main_self.player_list_instance.player_list_settings["player_fade_out"] and self.main_self.player_list_instance.player_list_settings["player_fade_in"]):
                    self.main_self.player_list_instance.dj_play_finished()
                else:
                    self.main_self.player_list_instance.dj_fade_out_end()
            else:
                if "playlist_play_in_progress" in dir(self.main_self.player_list_instance):
                    if self.main_self.player_list_instance.playlist_play_in_progress:
                        self.main_self.player_list_instance.current_playlist_skip += 1

                        total_items, item = self.main_self.player_list_instance.find_playlist_next_item(self.main_self.player_list_instance.playlist, skip=self.main_self.player_list_instance.current_playlist_skip)
                        if item is not None:
                            # 1. stop music clip deck
                            self.stop_button_clicked(disable_extra_plays=False)

                            # 2. load item to music clip deck
                            self.load_clip(item)

                            # 3. start music clip deck
                            self.play_or_pause_clicked()
                        else:
                            self.main_self.player_list_instance.playlist_play_in_progress = False


                if "time_collection_play_in_progress" in dir(self.main_self.player_list_instance):
                    if self.main_self.player_list_instance.time_collection_play_in_progress:
                        time_items = self.main_self.player_list_instance.time_collection[1]
                        if len(time_items)>self.main_self.player_list_instance.current_time_collection_skip:
                            if len(time_items) == self.main_self.player_list_instance.current_time_collection_skip + 1:
                                return None
                            self.main_self.player_list_instance.current_time_collection_skip += 1
                            item = time_items[self.main_self.player_list_instance.current_time_collection_skip]
                            item["time_collection"] = self.main_self.player_list_instance.time_collection[0]

                            # 1. stop music clip deck
                            self.stop_button_clicked(disable_extra_plays=False)

                            # 2. load item to music_clip_deck
                            self.load_clip(item)

                            # 3. start music clip deck
                            self.play_or_pause_clicked()
                        else:
                            self.main_self.player_list_instance.time_collection_play_in_progress = False
                    else:
                        if "restore_deck" in dir(self.main_self.player_list_instance):
                            if self.main_self.player_list_instance.restore_deck:
                                if "time_item" in self.clip["type"]:
                                    self.main_self.player_list_instance.restore_decks_after_time_play()
                        else:
                            if "time_item" in self.clip["type"]:
                                self.main_self.player_list_instance.restore_decks_after_time_play()
                else:
                    if "restore_deck" in dir(self.main_self.player_list_instance):
                        if self.main_self.player_list_instance.restore_deck:
                            if "time_item" in self.clip["type"]:
                                self.main_self.player_list_instance.restore_decks_after_time_play()
                    else:
                        if "time_item" in self.clip["type"]:
                            self.main_self.player_list_instance.restore_decks_after_time_play()

            if self.deck_status == "stopped":
                if self.main_self.player_list_instance.player_list_play_music_clip_deck_queue.qsize()>0:
                    play_or_prepare,item = self.main_self.player_list_instance.player_list_play_music_clip_deck_queue.get()
                    # 1. stop music clip deck
                    self.main_self.music_clip_deck_instance.stop_button_clicked(disable_extra_plays=False)

                    # 2. load clip to music clip deck
                    self.main_self.music_clip_deck_instance.load_clip(item)

                    # 3. start music clip deck
                    if play_or_prepare == "play":
                        self.main_self.music_clip_deck_instance.play_or_pause_clicked()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def display_current_duration(self,duration):
        try:
            if self.deck_status == "stopped":
                duration = 0
            duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration)
            if self.clip is not None:
                self.main_self.ui.music_clip_deck_duration.setText(duration_human+"/"+str(self.clip["duration_human"]))

                self.main_self.ui.music_clip_deck_timeslider.blockSignals(True)
                self.main_self.ui.music_clip_deck_timeslider.setValue(int(duration))
                self.main_self.ui.music_clip_deck_timeslider.blockSignals(False)


            else:
                self.main_self.ui.music_clip_deck_duration.setText("00:00:00/-")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)


    def display_volume_amplitude(self,normalized_value):
        try:
            if self.deck_status == "stopped":
                normalized_value = 0

            frame_width = self.main_self.ui.music_clip_deck_timeline_container_frame.geometry().width()
            stop_red = 255
            stop_green = int(255 * (1 - normalized_value))
            if (stop_green > 255):
                stop_green = 255
            normalized_value = int(frame_width * normalized_value)
            self.main_self.ui.music_clip_deck_timeline_pick_frame.setGeometry(QtCore.QRect(0, 0, normalized_value, 16))
            self.main_self.ui.music_clip_deck_timeline_pick_frame.setStyleSheet("QFrame{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 255, 0), stop:1 rgb(" + str(stop_red) + ", " + str(stop_green) + ", 0))}")
            self.main_self.ui.music_clip_deck_timeline_pick_frame.update()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)


    def stop_button_clicked(self,disable_extra_plays=True):
        try:
            if disable_extra_plays:
                self.main_self.player_list_instance.time_collection_play_in_progress = False
                self.main_self.player_list_instance.playlist_play_in_progress = False
            self.deck_status = "stopped"
            self.music_clip_deck_queue.put({"type":"new-status","status":self.deck_status})
            self.display_current_duration(0)
            self.display_volume_amplitude(0)
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(":/rest-icons/assets/icons/rest-icons/play-song.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
            self.main_self.ui.music_clip_deck_play_or_pause.setIcon(icon1)

            self.main_self.ui.music_clip_deck_timeslider.blockSignals(True)
            self.main_self.ui.music_clip_deck_timeslider.setValue(0)
            self.main_self.ui.music_clip_deck_timeslider.blockSignals(False)

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def play_or_pause_clicked(self):
        try:
            if self.clip == None:
                return None
            if self.deck_status == "playing":
                self.deck_status = "paused"

                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/rest-icons/assets/icons/rest-icons/play-song.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
                self.main_self.ui.music_clip_deck_play_or_pause.setIcon(icon1)

            else:
                self.deck_status = "playing"

                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/rest-icons/assets/icons/rest-icons/pause-song.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
                self.main_self.ui.music_clip_deck_play_or_pause.setIcon(icon1)
            self.music_clip_deck_queue.put({"type":"new-status","status":self.deck_status})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def top_music_clips(self,clips):
        try:
            # deck stop button
            self.main_self.ui.music_clip_deck_stop.clicked.connect(lambda state:self.stop_button_clicked())

            # deck play or pause button
            self.main_self.ui.music_clip_deck_play_or_pause.clicked.connect(lambda state:self.play_or_pause_clicked())

            # deck timeline
            self.main_self.ui.music_clip_deck_timeslider.sliderReleased.connect(lambda :self.deck_timeline_slider_moved())

            # deck volume menu
            self.create_menu_for_volume()

            # deck pan menu
            self.create_menu_for_pan()

            # deck normalize menu
            self.create_menu_for_normalize()

            # deck filter menu
            self.create_menu_for_filter()

            self.top_20_clips = clips
            counter = 0
            for clip in self.top_20_clips:
                counter += 1
                btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter))
                btn.clicked.connect(lambda state, one_clip=clip: self.top_clip_clicked(one_clip))
                btn.setText(str(clip["title"]))
                btn.setStyleSheet('QPushButton{font-size:10px;}')
                btn.setStatusTip("Πατήστε για αναπαραγωγή του ηχητικού clip με τίτλο: "+str(clip["title"]))
            #example for music_clip_1
            #self.main_self.ui.music_clip_1.clicked.connect(lambda state,clip_id=self.top_20_clips[0]["id"]:self.top_clip_clicked(clip_id))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def deck_timeline_slider_moved(self):
        try:
            value = self.main_self.ui.music_clip_deck_timeslider.value()
            if (self.deck_status != "stopped"):
                # calculate new chunk_number
                chunk_number = round(value / 125)
                self.music_clip_deck_queue.put({"type": "duration_changed", "chunk_number": chunk_number})
            else:
                self.main_self.ui.music_clip_deck_timeslider.setProperty("value", 0)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def create_menu_for_volume(self):
        try:
            self.menu_for_volume = QtWidgets.QMenu(self.main_self.ui.music_clip_deck_volume)
            self.main_self.ui.music_clip_deck_volume.setMenu(self.menu_for_volume)

            self.volume_frame = Custom_QFrame(self.menu_for_volume)
            self.volume_frame.installEventFilter(self.volume_frame)
            self.volume_frame.setFixedWidth(600)
            self.volume_frame.setStyleSheet("QFrame{border:1px solid #ABABAB;background-color:rgb(253,253,253);}")
            self.volume_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.volume_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.volume_frame.setObjectName("volume_frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.volume_frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.label = QtWidgets.QLabel(self.volume_frame)
            self.label.setStyleSheet("QLabel{border:none;}")
            self.label.setObjectName("label")
            self.horizontalLayout.addWidget(self.label)
            self.volume_slider = QtWidgets.QSlider(self.volume_frame)
            self.volume_slider.setMaximum(200)
            self.volume_slider.setProperty("value", 100)
            self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
            self.volume_slider.setObjectName("volume_slider")
            self.horizontalLayout.addWidget(self.volume_slider)
            self.volume_label = QtWidgets.QLabel(self.volume_frame)
            self.volume_label.setObjectName("volume_label")
            self.volume_label.setStyleSheet("QLabel{border:none;}")
            self.horizontalLayout.addWidget(self.volume_label)
            self.volume_reset = QtWidgets.QPushButton(self.volume_frame)
            self.volume_reset.setMinimumSize(QtCore.QSize(0, 29))
            self.volume_reset.setObjectName("volume_reset")
            self.horizontalLayout.addWidget(self.volume_reset)

            self.label.setText("Ρύθμιση έντασης ήχου:")
            self.volume_label.setText(str(100)+"/200")
            self.volume_reset.setText("Επαναφορά (100/200)")

            # on sound volume changed
            self.volume_slider.valueChanged.connect(lambda slider_value: self.volume_changed(slider_value))

            # on sound volume apply new value
            self.volume_slider.sliderReleased.connect(lambda: self.volume_released())

            # on sound volume pressed
            self.volume_slider.actionTriggered.connect(lambda action: self.volume_action_triggered(action))

            # on sound volume reset
            self.volume_reset.clicked.connect(lambda state: self.volume_resetted())

            volume_widget = QtWidgets.QWidgetAction(self.menu_for_volume)
            volume_widget.setDefaultWidget(self.volume_frame)
            self.menu_for_volume.addAction(volume_widget)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def volume_resetted(self):
        try:
            self.volume_slider.setValue(100)
            self.volume_label.setText("100/200")
            self.music_clip_deck_queue.put({"type": "volume", "value_base_100": 100})

            if self.clip is not None:
                self.clip["volume"] = 100
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1


            #page 4
            #reload player list items
            self.main_self.ui.main_player_list_treeWidget.clear()
            self.main_self.player_list_instance.player_list_queue.put({"type": "get-player-list"})

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def volume_changed(self, slider_value):
        try:
            self.volume_label.setText(str(slider_value) + "/200")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def volume_released(self):
        try:
            slider_value = self.volume_slider.value()
            self.music_clip_deck_queue.put({"type": "volume", "value_base_100": slider_value})

            if self.clip is not None:
                self.clip["volume"] = slider_value
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1

            # page 4
            # reload player list items
            self.main_self.ui.main_player_list_treeWidget.clear()
            self.main_self.player_list_instance.player_list_queue.put({"type": "get-player-list"})

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def volume_action_triggered(self, action):
        try:
            if action == QtWidgets.QAbstractSlider.SliderSingleStepAdd or action == QtWidgets.QAbstractSlider.SliderSingleStepSub or action == QtWidgets.QAbstractSlider.SliderPageStepAdd or action == QtWidgets.QAbstractSlider.SliderPageStepSub:
                self.timer_2 = QtCore.QTimer()
                self.timer_2.timeout.connect(lambda: self.volume_released())
                self.timer_2.setSingleShot(True)
                self.timer_2.start(500)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def create_menu_for_pan(self):
        try:
            self.menu_for_pan = QtWidgets.QMenu(self.main_self.ui.music_clip_deck_pan)
            self.main_self.ui.music_clip_deck_pan.setMenu(self.menu_for_pan)

            self.pan_frame = Custom_QFrame(self.menu_for_pan)
            self.pan_frame.installEventFilter(self.pan_frame)
            self.pan_frame.setFixedWidth(600)
            self.pan_frame.setStyleSheet("QFrame{background-color:rgb(253,253,253);border:1px solid #ABABAB;}")
            self.pan_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.pan_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.pan_frame.setObjectName("pan_frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.pan_frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.label = QtWidgets.QLabel(self.pan_frame)
            self.label.setObjectName("label")
            self.label.setStyleSheet("QLabel{border:none;}")
            self.horizontalLayout.addWidget(self.label)
            self.pan_slider = QtWidgets.QSlider(self.pan_frame)
            self.pan_slider.setMinimum(-100)
            self.pan_slider.setMaximum(100)
            self.pan_slider.setProperty("value", 0)
            self.pan_slider.setOrientation(QtCore.Qt.Horizontal)
            self.pan_slider.setObjectName("pan_slider")
            self.horizontalLayout.addWidget(self.pan_slider)
            self.pan_label = QtWidgets.QLabel(self.pan_frame)
            self.pan_label.setObjectName("pan_label")
            self.pan_label.setStyleSheet("QLabel{border:none;}")
            self.horizontalLayout.addWidget(self.pan_label)
            self.pan_reset = QtWidgets.QPushButton(self.pan_frame)
            self.pan_reset.setObjectName("pan_reset")
            self.horizontalLayout.addWidget(self.pan_reset)

            self.label.setText("Ρύθμιση στερεοφωνικής ισοστάθμισης:")
            self.pan_label.setText(str(0))
            self.pan_reset.setText("Επαναφορά 0")

            # on sound pan changed
            self.pan_slider.valueChanged.connect(lambda slider_value: self.pan_changed(slider_value))

            # on sound pan apply new value
            self.pan_slider.sliderReleased.connect(lambda: self.pan_released())

            # on sound pan pressed
            self.pan_slider.actionTriggered.connect(lambda action: self.pan_action_triggered(action))

            # on sound volume reset
            self.pan_reset.clicked.connect(lambda state: self.pan_resetted())

            pan_widget = QtWidgets.QWidgetAction(self.menu_for_pan)
            pan_widget.setDefaultWidget(self.pan_frame)
            self.menu_for_pan.addAction(pan_widget)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def pan_resetted(self):
        try:
            self.pan_slider.setValue(0)
            self.pan_label.setText("0")
            self.music_clip_deck_queue.put({"type": "pan", "pan_value": 0})

            if self.clip is not None:
                self.clip["pan"] = 0
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def pan_changed(self, slider_value):
        try:
            self.pan_label.setText(str(slider_value))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def pan_released(self):
        try:
            slider_value = self.pan_slider.value()
            self.music_clip_deck_queue.put({"type": "pan", "pan_value": slider_value})

            if self.clip is not None:
                self.clip["pan"] = slider_value
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def pan_action_triggered(self, action):
        try:
            if action == QtWidgets.QAbstractSlider.SliderSingleStepAdd or action == QtWidgets.QAbstractSlider.SliderSingleStepSub or action == QtWidgets.QAbstractSlider.SliderPageStepAdd or action == QtWidgets.QAbstractSlider.SliderPageStepSub:
                self.timer_2 = QtCore.QTimer()
                self.timer_2.timeout.connect(lambda: self.pan_released())
                self.timer_2.setSingleShot(True)
                self.timer_2.start(500)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def create_menu_for_normalize(self):
        try:
            self.menu_for_normalize = QtWidgets.QMenu(self.main_self.ui.music_clip_deck_normalize)
            self.main_self.ui.music_clip_deck_normalize.setMenu(self.menu_for_normalize)

            self.normalize_frame = Custom_QFrame(self.menu_for_normalize)
            self.normalize_frame.installEventFilter(self.normalize_frame)
            self.normalize_frame.setFixedWidth(300)
            self.normalize_frame.setStyleSheet("QFrame{background-color:rgb(253,253,253);border:1px solid #ABABAB;}")
            self.normalize_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.normalize_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.normalize_frame.setObjectName("normalize_frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.normalize_frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.normalize_checkBox = QtWidgets.QCheckBox(self.normalize_frame)
            self.normalize_checkBox.setObjectName("normalize_checkBox")
            self.normalize_checkBox.setStyleSheet("border:none;")
            self.normalize_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.horizontalLayout.addWidget(self.normalize_checkBox)

            self.normalize_checkBox.setText("Κανονικοποίηση")

            # on normalize changed
            self.normalize_checkBox.stateChanged.connect(lambda new_state: self.normalize_changed(new_state))

            normalize_widget = QtWidgets.QWidgetAction(self.menu_for_normalize)
            normalize_widget.setDefaultWidget(self.normalize_frame)
            self.menu_for_normalize.addAction(normalize_widget)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def normalize_changed(self, new_state):
        try:
            if new_state == QtCore.Qt.Unchecked:
                boolean_value = 0
                self.music_clip_deck_queue.put({"type": "is_normalized", "boolean_value": 0})
            else:
                boolean_value = 1
                self.music_clip_deck_queue.put({"type": "is_normalized", "boolean_value": 1})

            if self.clip is not None:
                self.clip["normalize"] = boolean_value
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1


        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def create_menu_for_filter(self):
        try:
            self.menu_for_filter = QtWidgets.QMenu(self.main_self.ui.music_clip_deck_filter)
            self.main_self.ui.music_clip_deck_filter.setMenu(self.menu_for_filter)

            # self.filter_frame = QtWidgets.QFrame(self.menu_for_filter)
            self.filter_frame = Custom_QFrame(self.menu_for_filter)
            self.filter_frame.installEventFilter(self.filter_frame)
            self.filter_frame.setStyleSheet("QFrame{border:1px solid #ABABAB;background-color:rgb(253,253,253);}")
            self.filter_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.filter_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.filter_frame.setObjectName("filter_frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.filter_frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.label_7 = QtWidgets.QLabel(self.filter_frame)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
            self.label_7.setSizePolicy(sizePolicy)
            self.label_7.setMinimumSize(QtCore.QSize(0, 0))
            self.label_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.label_7.setStyleSheet("QLabel{border:none;}")
            self.label_7.setWordWrap(True)
            self.label_7.setObjectName("label_7")
            self.horizontalLayout.addWidget(self.label_7)
            self.frame_13 = QtWidgets.QFrame(self.filter_frame)
            self.frame_13.setStyleSheet("QFrame{border:none;}")
            self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_13.setObjectName("frame_13")
            self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_13)
            self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.high_frequency = QtWidgets.QSpinBox(self.frame_13)
            self.high_frequency.setMinimumSize(QtCore.QSize(0, 29))
            self.high_frequency.setMinimum(20)
            self.high_frequency.setMaximum(20000)
            self.high_frequency.setSingleStep(100)
            #self.high_frequency.setProperty("value", 20000)
            self.high_frequency.setValue(20000)
            self.high_frequency.setObjectName("high_frequency")
            self.gridLayout_4.addWidget(self.high_frequency, 1, 1, 1, 1)
            self.label_11 = QtWidgets.QLabel(self.frame_13)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
            self.label_11.setSizePolicy(sizePolicy)
            self.label_11.setObjectName("label_11")
            self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)
            self.label_13 = QtWidgets.QLabel(self.frame_13)
            self.label_13.setMinimumSize(QtCore.QSize(60, 0))
            self.label_13.setMaximumSize(QtCore.QSize(50, 16777215))
            self.label_13.setAlignment(QtCore.Qt.AlignCenter)
            self.label_13.setObjectName("label_13")
            self.gridLayout_4.addWidget(self.label_13, 1, 2, 1, 1)
            self.reset_filter = QtWidgets.QPushButton(self.frame_13)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.reset_filter.sizePolicy().hasHeightForWidth())
            self.reset_filter.setSizePolicy(sizePolicy)
            self.reset_filter.setMinimumSize(QtCore.QSize(260, 29))
            self.reset_filter.setMaximumSize(QtCore.QSize(205, 16777215))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/menu-icons/assets/icons/menu-icons/menu-1/select-default.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.reset_filter.setIcon(icon)
            self.reset_filter.setObjectName("reset_filter")
            self.gridLayout_4.addWidget(self.reset_filter, 1, 3, 1, 1)
            self.label_12 = QtWidgets.QLabel(self.frame_13)
            self.label_12.setMinimumSize(QtCore.QSize(60, 0))
            self.label_12.setMaximumSize(QtCore.QSize(50, 16777215))
            self.label_12.setAlignment(QtCore.Qt.AlignCenter)
            self.label_12.setObjectName("label_12")
            self.gridLayout_4.addWidget(self.label_12, 0, 2, 1, 1)
            self.apply_filter = QtWidgets.QPushButton(self.frame_13)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.apply_filter.sizePolicy().hasHeightForWidth())
            self.apply_filter.setSizePolicy(sizePolicy)
            self.apply_filter.setMinimumSize(QtCore.QSize(260, 29))
            self.apply_filter.setMaximumSize(QtCore.QSize(205, 16777215))
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(":/rest-icons/assets/icons/rest-icons/apply-filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.apply_filter.setIcon(icon1)
            self.apply_filter.setObjectName("apply_filter")
            self.gridLayout_4.addWidget(self.apply_filter, 0, 3, 1, 1)
            self.label_10 = QtWidgets.QLabel(self.frame_13)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
            self.label_10.setSizePolicy(sizePolicy)
            self.label_10.setObjectName("label_10")
            self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)
            self.low_frequency = QtWidgets.QSpinBox(self.frame_13)
            self.low_frequency.setMinimumSize(QtCore.QSize(0, 29))
            self.low_frequency.setMinimum(20)
            self.low_frequency.setMaximum(20000)
            self.low_frequency.setSingleStep(100)
            self.low_frequency.setValue(20)
            self.low_frequency.setObjectName("low_frequency")
            self.gridLayout_4.addWidget(self.low_frequency, 0, 1, 1, 1)
            self.horizontalLayout.addWidget(self.frame_13)

            self.label_7.setText("Ζωνοπερατό φίλτρο:\n 20Hz-20000Hz")
            self.label_11.setText("Υψηλή συχνότητα αποκοπής:")
            self.label_13.setText("Hz")
            self.reset_filter.setText("Επαναφορά (20Hz - 20000Hz)")
            self.label_12.setText("Hz")
            self.apply_filter.setText("Εφαρμογή φίλτρου")
            self.label_10.setText("Χαμηλή συχνότητα αποκοπής:")


            # on low_frequency change
            self.low_frequency.valueChanged.connect(lambda low_frequency: self.low_frequency_changed(low_frequency))

            # on high_frequency change
            self.high_frequency.valueChanged.connect(lambda high_frequency: self.high_frequency_changed(high_frequency))

            # on apply filter
            self.apply_filter.clicked.connect(lambda state: self.apply_filter_method(state))

            # on reset filter
            self.reset_filter.clicked.connect(lambda state: self.reset_filter_method(state))

            filter_widget = QtWidgets.QWidgetAction(self.menu_for_filter)
            filter_widget.setDefaultWidget(self.filter_frame)
            self.menu_for_filter.addAction(filter_widget)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def low_frequency_changed(self, low_frequency):
        try:
            self.high_frequency.setMinimum(low_frequency)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def high_frequency_changed(self, high_frequency):
        try:
            self.low_frequency.setMaximum(high_frequency)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def apply_filter_method(self, state):
        try:
            low_frequency = self.low_frequency.value()
            high_frequency = self.high_frequency.value()
            self.music_clip_deck_queue.put({"type": "low_frequency", "low_frequency_value": low_frequency})
            self.music_clip_deck_queue.put({"type": "high_frequency", "high_frequency_value": high_frequency})

            if self.clip is not None:
                self.clip["low_frequency"] = low_frequency
                self.clip["high_frequency"] = high_frequency
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def reset_filter_method(self, state):
        try:
            self.low_frequency.setValue(20)
            self.low_frequency.setMaximum(20000)
            self.high_frequency.setValue(20000)
            self.high_frequency.setMinimum(20)
            self.music_clip_deck_queue.put({"type": "low_frequency", "low_frequency_value": 20})
            self.music_clip_deck_queue.put({"type": "high_frequency", "high_frequency_value": 20000})

            if self.clip is not None:
                self.clip["low_frequency"] = 20
                self.clip["high_frequency"] = 20000
                counter = 0
                for clip_i in self.top_20_clips:
                    if clip_i["id"] == self.clip["id"]:
                        self.top_20_clips[counter] = self.clip
                        btn = getattr(self.main_self.ui, 'music_clip_{}'.format(counter+1))
                        btn.disconnect()
                        btn.clicked.connect(lambda state, one_clip=self.clip: self.top_clip_clicked(one_clip))
                        break
                    counter += 1

        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def load_clip(self,clip):
        try:
            clip = copy.deepcopy(clip)
            # 1. stop music clip deck
            self.main_self.music_clip_deck_instance.stop_button_clicked(disable_extra_plays=False)

            # 2. change music clip deck title
            self.main_self.ui.music_clip_deck_title.setText(clip["title"])

            # 3. set current clip
            self.clip = clip

            # 4. change music clip deck duration
            self.display_current_duration(0)

            # 5. change music clip deck amplitude
            self.display_volume_amplitude(0)

            # 6. set slider max value
            self.main_self.ui.music_clip_deck_timeslider.setMaximum(int(self.clip["duration_milliseconds"]))
            self.main_self.ui.music_clip_deck_timeslider.setSingleStep(500)
            self.main_self.ui.music_clip_deck_timeslider.setPageStep(1000)
            self.main_self.ui.music_clip_deck_timeslider.setProperty("value", 0)

            #7. set deck volume
            self.volume_slider.blockSignals(True)
            self.volume_slider.setValue(self.clip["volume"])
            self.volume_label.setText(str(self.clip["volume"])+"/200")
            self.volume_slider.blockSignals(False)
            #self.music_clip_deck_queue.put({"type": "volume", "value_base_100": self.clip["volume"]})

            #8. set deck pan
            self.pan_slider.blockSignals(True)
            self.pan_slider.setValue(int(self.clip["pan"]))
            self.pan_label.setText(str(self.clip["pan"]))
            self.pan_slider.blockSignals(False)
            #self.music_clip_deck_queue.put({"type": "pan", "pan_value": int(self.clip["pan"])})

            #9. set deck normalize
            self.normalize_checkBox.blockSignals(True)
            if self.clip["normalize"]:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Checked)
                #self.music_clip_deck_queue.put({"type": "is_normalized", "boolean_value": 0})
            else:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Unchecked)
                #self.music_clip_deck_queue.put({"type": "is_normalized", "boolean_value": 1})
            self.normalize_checkBox.blockSignals(False)

            #10. set deck filter
            self.low_frequency.blockSignals(True)
            self.high_frequency.blockSignals(True)
            self.low_frequency.setValue(self.clip["low_frequency"])
            self.low_frequency.setMaximum(self.clip["high_frequency"])
            self.high_frequency.setValue(self.clip["high_frequency"])
            self.high_frequency.setMinimum(self.clip["low_frequency"])
            self.low_frequency.blockSignals(False)
            self.high_frequency.blockSignals(False)
            #self.music_clip_deck_queue.put({"type": "low_frequency", "low_frequency_value": self.clip["low_frequency"]})
            #self.music_clip_deck_queue.put({"type": "high_frequency", "high_frequency_value": self.clip["high_frequency"]})


            # 11. load clip to process
            self.music_clip_deck_queue.put({"type": "load", "clip": self.clip})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def top_clip_clicked(self,clip):
        try:
            #1. stop music clip deck
            self.main_self.ui.music_clip_deck_stop.click()

            #2. change music clip deck title
            self.main_self.ui.music_clip_deck_title.setText(clip["title"])

            #3. set current clip
            self.clip = clip

            #4. change music clip deck duration
            self.display_current_duration(0)

            #5. change music clip deck amplitude
            self.display_volume_amplitude(0)

            #6. set slider max value
            self.main_self.ui.music_clip_deck_timeslider.setMaximum(int(self.clip["duration_milliseconds"]))
            self.main_self.ui.music_clip_deck_timeslider.setSingleStep(500)
            self.main_self.ui.music_clip_deck_timeslider.setPageStep(1000)
            self.main_self.ui.music_clip_deck_timeslider.setProperty("value", 0)

            #7. set deck volume
            self.volume_slider.blockSignals(True)
            self.volume_slider.setValue(self.clip["volume"])
            self.volume_label.setText(str(self.clip["volume"])+"/200")
            self.volume_slider.blockSignals(False)
            #self.music_clip_deck_queue.put({"type": "volume", "value_base_100": self.clip["volume"]})

            #8. set deck pan
            self.pan_slider.blockSignals(True)
            self.pan_slider.setValue(int(self.clip["pan"]))
            self.pan_label.setText(str(self.clip["pan"]))
            self.pan_slider.blockSignals(False)
            #self.music_clip_deck_queue.put({"type": "pan", "pan_value": int(self.clip["pan"])})

            #9. set deck normalize
            self.normalize_checkBox.blockSignals(True)
            if self.clip["normalize"]:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Checked)
                #self.music_clip_deck_queue.put({"type": "is_normalized", "boolean_value": 0})
            else:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Unchecked)
                #self.music_clip_deck_queue.put({"type": "is_normalized", "boolean_value": 1})
            self.normalize_checkBox.blockSignals(False)

            #10. set deck filter
            self.low_frequency.blockSignals(True)
            self.high_frequency.blockSignals(True)
            self.low_frequency.setValue(self.clip["low_frequency"])
            self.low_frequency.setMaximum(self.clip["high_frequency"])
            self.high_frequency.setValue(self.clip["high_frequency"])
            self.high_frequency.setMinimum(self.clip["low_frequency"])
            self.low_frequency.blockSignals(False)
            self.high_frequency.blockSignals(False)
            #self.music_clip_deck_queue.put({"type": "low_frequency", "low_frequency_value": self.clip["low_frequency"]})
            #self.music_clip_deck_queue.put({"type": "high_frequency", "high_frequency_value": self.clip["high_frequency"]})

            #11. load clip to process
            self.music_clip_deck_queue.put({"type":"load","clip":self.clip})

            #12. play the loaded clip
            self.main_self.ui.music_clip_deck_play_or_pause.click()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)

    def close(self):
        try:
            if self.deck_status == "playing":
                self.deck_status = "stopped"
                self.music_clip_deck_queue.put({"type":"new-status","status":self.deck_status})
                time.sleep(0.125)
            self.music_clip_deck_queue.put({"type": "close"})
            try:
                if self.music_clip_deck_child_process is not None:
                    self.music_clip_deck_child_process.terminate()
                    self.music_clip_deck_child_process.close()
            except:
                pass
            try:
                if self.music_clip_deck_emitter is not None:
                    self.music_clip_deck_emitter.quit()
            except:
                pass

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = None
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = None
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "stopped"
                        self.main_self.manage_processes_instance.processes[counter]["cpu"] = 0
                        self.main_self.manage_processes_instance.processes[counter]["ram"] = 0
                counter += 1
            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.main_self.open_music_clip_deck_error_window(error_message)

    def music_clip_deck_slice_ready(self,slice):
        try:
            if self.put_to_q:
                self.main_self.final_slice_instance.music_clip_deck_queue.put({"type":"slice","slice":slice})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_music_clip_deck_error_window(error_message)


# CAUTION: no try except block for opening error window!
class Custom_QFrame(QtWidgets.QFrame):
    def __init__(self, parent, *args, **kwargs):
        super(QtWidgets.QFrame, self).__init__(parent, *args, **kwargs)

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            return True
        return super(QtWidgets.QFrame, self).eventFilter(obj, event)


class Music_Clip_Deck_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        music_clip_deck_ready = pyqtSignal(AudioSegment)
        top_music_clips = pyqtSignal(list)
        volume_amplitude = pyqtSignal(float)
        current_duration_milliseconds = pyqtSignal(int)
        deck_finished = pyqtSignal()
        chunk_number_answer = pyqtSignal(int)
        fade_out_start = pyqtSignal()
    except:
        pass

    def __init__(self, from_process: Pipe):
        try:
            super().__init__()
            self.data_from_process = from_process
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)

    def run(self):
        try:
            while True:
                data = self.data_from_process.recv()
                if data["type"] == "error":
                    self.error_signal.emit(data["error_message"])
                elif data["type"] == "slice":
                    self.music_clip_deck_ready.emit(data["slice"])
                elif data["type"] == "top-music-clips":
                    self.top_music_clips.emit(data["clips"])
                elif data["type"] == "close":
                    break
                elif data["type"] == "volume_amplitude":
                    self.volume_amplitude.emit(data["normalized_value"])
                elif data["type"] == "current_duration_milliseconds":
                    self.current_duration_milliseconds.emit(data["duration"])
                elif data["type"] == "deck_finished":
                    self.deck_finished.emit()
                elif data["type"] == "chunk-number-answer":
                    self.chunk_number_answer.emit(data["chunk-number"])
                elif data["type"] == "fade-out-start":
                    self.fade_out_start.emit()
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)


class Music_Clip_Deck_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.deck_status = "stopped"
            self.volume = 100
            self.pan = 0
            self.normalize = 0
            self.low_frequency = 20
            self.high_frequency = 20000
            self.clip = None
            self.current_duration_milliseconds = 0
            self.chunk_number = 0
            self.packet_time = 125
            self.fade_out_emitted = False
        except:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.send({"type": "error", "error_message": error_message})
            except:
                pass

    def run(self):
        try:
            self.database_functions = database_functions
            self.fetch_player_list_settings()
            self.fetch_top_music_clip_decks()
            current_frame = 0
            while (True):
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return None
                self.one_chunk()
                current_frame += 1
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def one_chunk(self):
        try:
            q_size = self.data_from_mother.qsize()
            if q_size > 0:
                data = self.data_from_mother.get()
            else:
                data = None
            if data is not None:
                if data["type"] == "volume":
                    self.volume = data["value_base_100"]
                    self.update_clip()
                elif data["type"] == "pan":
                    self.pan = data["pan_value"]
                    self.update_clip()
                elif data["type"] == "is_normalized":
                    self.normalize = data["boolean_value"]
                    self.update_clip()
                elif data["type"] == "low_frequency":
                    self.low_frequency = data["low_frequency_value"]
                    self.update_clip()
                elif data["type"] == "high_frequency":
                    self.high_frequency = data["high_frequency_value"]
                    self.update_clip()
                elif data["type"] == "player-list-settings":
                    self.player_list_settings_previous = self.player_list_settings
                    self.player_list_settings = data["settings"]
                elif data["type"] == "close":
                    self.to_emitter.send({"type": "close"})
                    # self.quit_event.set()
                elif data["type"] == "duration_changed":
                    self.chunk_number = data["chunk_number"]
                    self.current_duration_milliseconds = self.chunk_number * self.packet_time
                elif data["type"] == "ask-for-chunk-number":
                    self.to_emitter.send({"type":"chunk-number-answer","chunk-number":self.chunk_number})
                elif data["type"] == "new-status":
                    self.deck_status = data["status"]
                    self.update_player_history(self.deck_status)
                    if self.deck_status == "playing":
                        pass
                    elif self.deck_status == "paused":
                        pass
                    else:
                        self.fade_out_emitted = False
                        self.chunk_number = 0
                        self.current_duration_milliseconds = 0
                elif data["type"] == "load":
                    self.fade_out_emitted = False
                    self.deck_status = "stopped"
                    self.update_player_history(self.deck_status)
                    self.clip = data["clip"]
                    self.volume = self.clip["volume"]
                    self.pan = self.clip["pan"]
                    self.normalize = self.clip["normalize"]
                    self.low_frequency = self.clip["low_frequency"]
                    self.high_frequency = self.clip["high_frequency"]

                    saved_path = self.clip["saved_path"]
                    self.audio_segment = AudioSegment.from_file(saved_path, format="mp3")
                    self.total_duration_milliseconds = len(self.audio_segment)
                    self.chunk_number = 0
                    self.current_duration_milliseconds = 0

            if self.clip is not None:
                if self.current_duration_milliseconds >= self.total_duration_milliseconds:
                    self.fade_out_emitted = False
                    self.to_emitter.send({"type": "deck_finished"})
                    self.deck_status = "stopped"
                    self.update_player_history(self.deck_status)
                    self.chunk_number = 0
                    self.current_duration_milliseconds = 0
                if self.deck_status == "playing":
                    if ((self.chunk_number + 1) * (self.packet_time) <= self.total_duration_milliseconds):
                        slice = self.audio_segment[self.chunk_number * (self.packet_time):(self.chunk_number + 1) * (self.packet_time)]
                    else:
                        if ((self.chunk_number) * (self.packet_time) < self.current_duration_milliseconds):
                            slice = self.audio_segment[self.chunk_number * (self.packet_time):]
                        else:
                            self.fade_out_emitted = False
                            slice = AudioSegment.empty()
                            self.deck_status = "stopped"
                            self.update_player_history(self.deck_status)
                            self.to_emitter.send({"type": "deck_finished"})
                            self.chunk_number = 0
                            self.current_duration_milliseconds = 0

                    if self.pan != 0:
                        slice = slice.pan(self.pan / 100)
                    if slice != AudioSegment.empty():
                        try:
                            if self.low_frequency > 20:
                                slice = effects.high_pass_filter(slice, self.low_frequency)
                            if self.high_frequency > 20000:
                                slice = effects.low_pass_filter(slice, self.high_frequency)
                        except:
                            pass
                    volume = self.volume
                    if self.total_duration_milliseconds > 5000:
                        if self.chunk_number * self.packet_time < 5000 and self.player_list_settings["player_fade_in"]:
                            volume = volume * self.fade_in(self.chunk_number * self.packet_time)
                        if self.chunk_number * self.packet_time > self.total_duration_milliseconds - 5000 and self.player_list_settings["player_fade_out"]:
                            volume = volume * self.fade_out(self.chunk_number * self.packet_time,self.total_duration_milliseconds)
                    if (volume == 0):
                        db_volume = -200
                    else:
                        db_volume = 20 * math.log10(volume / 100)
                    slice = slice + db_volume
                    if self.normalize:
                        slice = self.normalize_method(slice, 0.1)

                    chunk_time = len(slice)

                    average_data_value = slice.max
                    normalized_value = abs(average_data_value) / slice.max_possible_amplitude
                    if normalized_value > 1:
                        normalized_value = 1
                    if self.deck_status == "stopped":
                        normalized_value = 0

                    self.to_emitter.send({"type": "volume_amplitude", "normalized_value": normalized_value})

                    self.now = datetime.now()

                    self.chunk_number += 1
                    if (self.chunk_number * self.packet_time >= self.total_duration_milliseconds - 5000) and (self.player_list_settings["player_fade_out"] or self.player_list_settings[
                        "player_fade_in"]):
                        if self.fade_out_emitted == False:
                            self.fade_out_emitted = True
                            self.to_emitter.send({"type": "fade-out-start"})
                    else:
                        if "player_list_settings_previous" in dir(self):
                            if (self.chunk_number * self.packet_time >= self.total_duration_milliseconds - 5000) and (
                                    self.player_list_settings_previous["player_fade_out"] or self.player_list_settings_previous[
                                "player_fade_in"]):
                                if self.fade_out_emitted == False:
                                    self.fade_out_emitted = True
                                    self.to_emitter.send({"type": "fade-out-start"})
                                    del self.player_list_settings_previous

                    self.current_duration_milliseconds += chunk_time

                    self.to_emitter.send({"type": "current_duration_milliseconds", "duration": self.current_duration_milliseconds})
                    self.to_emitter.send({"type": "slice", "slice": slice})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def fetch_player_list_settings(self):
        try:
            self.database_functions = database_functions

            player_fade_out = int(database_functions.read_setting("player_fade_out")["value"])
            player_fade_in = int(database_functions.read_setting("player_fade_in")["value"])
            auto_dj = int(database_functions.read_setting("auto_dj")["value"])
            repeat_player_list = int(database_functions.read_setting("repeat_player_list")["value"])
            is_live = int(database_functions.read_setting("is_live")["value"])

            self.player_list_settings = {
                "player_fade_out":player_fade_out,
                "player_fade_in":player_fade_in,
                "auto_dj":auto_dj,
                "repeat_player_list":repeat_player_list,
                "is_live":is_live
            }
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})


    def fade_in(self,time_milliseconds):
        try:
            if time_milliseconds>5000:
                return 1
            elif time_milliseconds == 0:
                return 0
            else:
                fade_in = 3*time_milliseconds
                fade_in = fade_in ** (1./3)
                fade_in = fade_in / ((15000) ** (1./3))
                return fade_in
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def fade_out(self,time_milliseconds,total_duration_milliseconds):
        try:
            if time_milliseconds>=total_duration_milliseconds:
                return 0
            elif time_milliseconds<total_duration_milliseconds-5000:
                return 1
            else:
                fade_out = total_duration_milliseconds - time_milliseconds
                fade_out = fade_out*3
                fade_out = fade_out ** (1./3)
                fade_out = fade_out / ((15000) ** (1. / 3))
                return fade_out
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})


    def update_player_history(self,deck_status):
        try:
            if self.clip is not None:
                now = datetime.now()
                if deck_status == "playing":
                    self.player_history = {
                        "datetime_started_played":now.strftime("%d-%m-%Y, %H:%M:%S"),
                        "datetime_stoped_played":"",
                        "relative_type":"sound_clips",
                        "relative_number":self.clip["id"],
                        "deck":"music_clip_deck",
                        "updated":0
                    }
                    self.player_history = self.database_functions.import_player_history(self.player_history)
                else:
                    if "player_history" in dir(self):
                        self.player_history["updated"] = 1
                        self.player_history["datetime_stoped_played"] = now.strftime("%d-%m-%Y, %H:%M:%S")
                        self.player_history = self.database_functions.update_player_history(self.player_history)
                        if self.deck_status == "stopped":
                            del self.player_history
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})


    def update_clip(self):
        try:
            if self.clip == None:
                return
            else:
                self.clip["volume"] = self.volume
                self.clip["normalize"] = self.normalize
                self.clip["pan"] = self.pan
                self.clip["low_frequency"] = self.low_frequency
                self.clip["high_frequency"] = self.high_frequency
                self.database_functions.update_sound_clip(self.clip,update_vote=False)
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def fetch_top_music_clip_decks(self):
        try:
            self.sound_clips = self.database_functions.read_sound_clips()
            top_20 = self.sound_clips[0:20]
            self.to_emitter.send({"type":"top-music-clips","clips":top_20})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    # Use pydub effect to normalize the volume of a sound file
    def normalize_method(self, seg, headroom):
        try:
            peak_sample_val = seg.max

            # if the max is 0, this audio segment is silent, and can't be normalized
            if peak_sample_val == 0:
                return seg

            target_peak = seg.max_possible_amplitude * utils.db_to_float(-headroom)
            # target_peak = seg.max_possible_amplitude * (percent_headroom)

            needed_boost = utils.ratio_to_db(target_peak / peak_sample_val)
            return seg.apply_gain(needed_boost)
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.to_emitter.send({"type": "error", "error_message": error_message})
            return seg