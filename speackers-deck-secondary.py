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


class Speackers_Deck_Secondary:
    def __init__(self, main_self):
        try:
            self.main_self = main_self

            self.deck_status = "stopped"
            self.put_to_q = False

            self.display_current_duration(0)
            self.display_volume_amplitude(0)

            # create process
            self.process_number = 103
            self.manage_speackers_deck_secondary_mother_pipe, self.manage_speackers_deck_secondary_child_pipe = Pipe()
            self.manage_speackers_deck_secondary_queue = Queue()
            self.manage_speackers_deck_secondary_emitter = Manage_Speackers_Deck_Secondary_Emitter(self.manage_speackers_deck_secondary_mother_pipe)
            self.manage_speackers_deck_secondary_emitter.error_signal.connect(lambda error_message: self.main_self.open_speackers_deck_secondary_error_window(error_message))
            self.manage_speackers_deck_secondary_emitter.microphone_settings.connect(lambda settings: self.microphone_settings(settings))
            self.manage_speackers_deck_secondary_emitter.update_microphone_settings.connect(lambda settings: self.update_microphone_settings(settings))
            self.manage_speackers_deck_secondary_emitter.volume_amplitude.connect(lambda normalized_value: self.display_volume_amplitude(normalized_value))
            self.manage_speackers_deck_secondary_emitter.current_duration_milliseconds.connect(lambda duration: self.display_current_duration(duration))
            self.manage_speackers_deck_secondary_emitter.microphone_slice.connect(lambda slice: self.microphone_slice_ready(slice))

            self.manage_speackers_deck_secondary_emitter.start()
            self.manage_speackers_deck_secondary_child_process = Manage_Speackers_Deck_Secondary_Child_Proc(self.manage_speackers_deck_secondary_child_pipe, self.manage_speackers_deck_secondary_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.manage_speackers_deck_secondary_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.manage_speackers_deck_secondary_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
            self.put_to_q = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def microphone_slice_ready(self,slice):
        try:
            if self.put_to_q:
                self.main_self.secondary_slice_instance.speackers_deck_secondary_queue.put({"type":"slice","slice":slice})
                self.main_self.ip_calls_instance.speackers_deck_queue.put({"type":"slice","slice":slice})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def display_volume_amplitude(self,normalized_value):
        try:
            if self.deck_status == "stopped":
                normalized_value = 0

            frame_width = self.main_self.ui.local_video_call_timeline_container_frame.geometry().width()
            stop_red = 255
            stop_green = int(255 * (1 - normalized_value))
            if (stop_green > 255):
                stop_green = 255
            normalized_value = int(frame_width * normalized_value)
            self.main_self.ui.local_video_call_timeline_pick_frame.setGeometry(QtCore.QRect(0, 0, normalized_value, 16))
            self.main_self.ui.local_video_call_timeline_pick_frame.setStyleSheet("QFrame{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 255, 0), stop:1 rgb(" + str(stop_red) + ", " + str(stop_green) + ", 0))}")
            self.main_self.ui.local_video_call_timeline_pick_frame.update()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def display_current_duration(self,duration):
        try:
            if self.deck_status == "stopped":
                duration = 0
            duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration)
            self.main_self.ui.local_video_time_label.setText(duration_human)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def update_microphone_settings(self,settings):
        try:
            self.settings = settings

            self.volume_slider.setProperty("value", self.settings["volume"])
            self.pan_slider.setProperty("value", self.settings["pan"])
            if self.settings["is_normalized"]:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Checked)
            else:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Unchecked)

            self.low_frequency.setMinimum(20)
            self.low_frequency.setMaximum(self.settings["high_frequency"])
            self.low_frequency.setValue(self.settings["low_frequency"])

            self.high_frequency.setMinimum(self.settings["low_frequency"])
            self.high_frequency.setMaximum(20000)
            self.high_frequency.setValue(self.settings["high_frequency"])
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)


    def microphone_settings(self,settings):
        try:
            self.settings = settings
            # speackers deck volume menu
            self.create_menu_for_volume()

            # speackers deck pan menu
            self.create_menu_for_pan()

            # speackers deck normalize menu
            self.create_menu_for_normalize()

            # speackers deck filter menu
            self.create_menu_for_filter()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def play_or_pause(self):
        try:
            if self.deck_status == "stopped":
                self.deck_status = "playing"
                self.manage_speackers_deck_secondary_queue.put({"type":"new-status","status":self.deck_status})
            else:
                self.deck_status = "stopped"
                self.display_current_duration(0)
                self.display_volume_amplitude(0)
                self.manage_speackers_deck_secondary_queue.put({"type": "new-status", "status": self.deck_status})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def create_menu_for_volume(self):
        try:
            self.menu_for_volume = QtWidgets.QMenu(self.main_self.ui.local_video_volume)
            self.main_self.ui.local_video_volume.setMenu(self.menu_for_volume)

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
            self.volume_slider.setProperty("value", self.settings["volume"])
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
            self.volume_label.setText(str(self.settings["volume"])+"/200")
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
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def volume_resetted(self):
        try:
            self.volume_slider.setValue(100)
            self.volume_label.setText("100/200")
            self.manage_speackers_deck_secondary_queue.put({"type": "volume", "value_base_100": 100})
            self.main_self.speackers_deck_instance.volume_slider.blockSignals(True)
            self.main_self.speackers_deck_instance.volume_slider.setValue(100)
            self.main_self.speackers_deck_instance.volume_slider.blockSignals(False)
            self.main_self.speackers_deck_instance.volume_label.setText("100/200")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def volume_changed(self, slider_value):
        try:
            self.volume_label.setText(str(slider_value) + "/200")
            self.main_self.speackers_deck_instance.volume_label.setText(str(slider_value) + "/200")
            self.main_self.speackers_deck_instance.volume_slider.blockSignals(True)
            self.main_self.speackers_deck_instance.volume_slider.setValue(slider_value)
            self.main_self.speackers_deck_instance.volume_slider.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def volume_released(self):
        try:
            slider_value = self.volume_slider.value()
            self.manage_speackers_deck_secondary_queue.put({"type": "volume", "value_base_100": slider_value})
            self.main_self.speackers_deck_instance.volume_label.setText(str(slider_value) + "/200")
            self.main_self.speackers_deck_instance.volume_slider.blockSignals(True)
            self.main_self.speackers_deck_instance.volume_slider.setValue(slider_value)
            self.main_self.speackers_deck_instance.volume_slider.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def volume_action_triggered(self, action):
        try:
            if action == QtWidgets.QAbstractSlider.SliderSingleStepAdd or action == QtWidgets.QAbstractSlider.SliderSingleStepSub or action == QtWidgets.QAbstractSlider.SliderPageStepAdd or action == QtWidgets.QAbstractSlider.SliderPageStepSub:
                self.timer_2 = QtCore.QTimer()
                self.timer_2.timeout.connect(lambda: self.volume_released())
                self.timer_2.setSingleShot(True)
                self.timer_2.start(500)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def create_menu_for_pan(self):
        try:
            self.menu_for_pan = QtWidgets.QMenu(self.main_self.ui.local_video_pan)
            self.main_self.ui.local_video_pan.setMenu(self.menu_for_pan)

            self.pan_frame = Custom_QFrame(self.menu_for_pan)
            self.pan_frame.installEventFilter(self.pan_frame)
            self.pan_frame.setFixedWidth(600)
            self.pan_frame.setStyleSheet("QFrame{background-color:rgb(253,253,253);border:1px solid #ABABAB;}")
            self.pan_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.pan_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.pan_frame.setObjectName("pan_frame")
            self.horizontalLayout_pan = QtWidgets.QHBoxLayout(self.pan_frame)
            #self.horizontalLayout.setObjectName("horizontalLayout")
            self.label = QtWidgets.QLabel(self.pan_frame)
            self.label.setObjectName("label")
            self.label.setStyleSheet("QLabel{border:none;}")
            self.horizontalLayout_pan.addWidget(self.label)
            self.pan_slider = QtWidgets.QSlider(self.pan_frame)
            self.pan_slider.setMinimum(-100)
            self.pan_slider.setMaximum(100)
            self.pan_slider.setProperty("value", self.settings["pan"])
            self.pan_slider.setOrientation(QtCore.Qt.Horizontal)
            self.pan_slider.setObjectName("pan_slider")
            self.horizontalLayout_pan.addWidget(self.pan_slider)
            self.pan_label = QtWidgets.QLabel(self.pan_frame)
            self.pan_label.setObjectName("pan_label")
            self.pan_label.setStyleSheet("QLabel{border:none;}")
            self.horizontalLayout_pan.addWidget(self.pan_label)
            self.pan_reset = QtWidgets.QPushButton(self.pan_frame)
            self.pan_reset.setObjectName("pan_reset")
            self.horizontalLayout_pan.addWidget(self.pan_reset)

            self.label.setText("Ρύθμιση στερεοφωνικής ισοστάθμισης:")
            self.pan_label.setText(str(self.settings["pan"]))
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
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def pan_resetted(self):
        try:
            self.pan_slider.setValue(0)
            self.pan_label.setText("0")
            self.manage_speackers_deck_secondary_queue.put({"type": "pan", "pan_value": 0})
            self.main_self.speackers_deck_instance.pan_slider.blockSignals(True)
            self.main_self.speackers_deck_instance.pan_slider.setValue(0)
            self.main_self.speackers_deck_instance.pan_slider.blockSignals(False)
            self.main_self.speackers_deck_instance.pan_label.setText("0")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def pan_changed(self, slider_value):
        try:
            self.pan_label.setText(str(slider_value))
            self.main_self.speackers_deck_instance.pan_slider.blockSignals(True)
            self.main_self.speackers_deck_instance.pan_slider.setValue(slider_value)
            self.main_self.speackers_deck_instance.pan_slider.blockSignals(False)
            self.main_self.speackers_deck_instance.pan_label.setText(str(slider_value))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def pan_released(self):
        try:
            slider_value = self.pan_slider.value()
            self.manage_speackers_deck_secondary_queue.put({"type": "pan", "pan_value": slider_value})
            self.main_self.speackers_deck_instance.pan_slider.blockSignals(True)
            self.main_self.speackers_deck_instance.pan_slider.setValue(slider_value)
            self.main_self.speackers_deck_instance.pan_slider.blockSignals(False)
            self.main_self.speackers_deck_instance.pan_label.setText(str(slider_value))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def pan_action_triggered(self, action):
        try:
            if action == QtWidgets.QAbstractSlider.SliderSingleStepAdd or action == QtWidgets.QAbstractSlider.SliderSingleStepSub or action == QtWidgets.QAbstractSlider.SliderPageStepAdd or action == QtWidgets.QAbstractSlider.SliderPageStepSub:
                self.timer_2 = QtCore.QTimer()
                self.timer_2.timeout.connect(lambda: self.pan_released())
                self.timer_2.setSingleShot(True)
                self.timer_2.start(500)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def create_menu_for_normalize(self):
        try:
            self.menu_for_normalize = QtWidgets.QMenu(self.main_self.ui.local_video_normalize)
            self.main_self.ui.local_video_normalize.setMenu(self.menu_for_normalize)

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
            if self.settings["is_normalized"]:
                self.normalize_checkBox.setCheckState(QtCore.Qt.Checked)
            else:
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
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def normalize_changed(self, new_state):
        try:
            if new_state == QtCore.Qt.Unchecked:
                self.manage_speackers_deck_secondary_queue.put({"type": "is_normalized", "boolean_value": 0})
            else:
                self.manage_speackers_deck_secondary_queue.put({"type": "is_normalized", "boolean_value": 1})

            self.main_self.speackers_deck_instance.normalize_checkBox.blockSignals(True)
            self.main_self.speackers_deck_instance.normalize_checkBox.setCheckState(new_state)
            self.main_self.speackers_deck_instance.normalize_checkBox.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def create_menu_for_filter(self):
        try:
            self.menu_for_filter = QtWidgets.QMenu(self.main_self.ui.local_video_filter)
            self.main_self.ui.local_video_filter.setMenu(self.menu_for_filter)

            # self.filter_frame = QtWidgets.QFrame(self.menu_for_filter)
            self.filter_frame = Custom_QFrame(self.menu_for_filter)
            self.filter_frame.installEventFilter(self.filter_frame)
            self.filter_frame.setStyleSheet("QFrame{border:1px solid #ABABAB;background-color:rgb(253,253,253);}")
            self.filter_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.filter_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.filter_frame.setObjectName("filter_frame")
            self.horizontalLayout_filter = QtWidgets.QHBoxLayout(self.filter_frame)
            #self.horizontalLayout.setObjectName("horizontalLayout")
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
            self.horizontalLayout_filter.addWidget(self.label_7)
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
            self.high_frequency.setMinimum(self.settings["low_frequency"])
            self.high_frequency.setMaximum(20000)
            self.high_frequency.setSingleStep(100)
            #self.high_frequency.setProperty("value", 20000)
            self.high_frequency.setValue(self.settings["high_frequency"])
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
            self.low_frequency.setMaximum(self.settings["high_frequency"])
            self.low_frequency.setSingleStep(100)
            self.low_frequency.setValue(self.settings["low_frequency"])
            self.low_frequency.setObjectName("low_frequency")
            self.gridLayout_4.addWidget(self.low_frequency, 0, 1, 1, 1)
            self.horizontalLayout_filter.addWidget(self.frame_13)

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
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def low_frequency_changed(self, low_frequency):
        try:
            self.high_frequency.setMinimum(low_frequency)
            self.main_self.speackers_deck_instance.high_frequency.setMinimum(low_frequency)
            self.main_self.speackers_deck_instance.low_frequency.blockSignals(True)
            self.main_self.speackers_deck_instance.low_frequency.setValue(low_frequency)
            self.main_self.speackers_deck_instance.low_frequency.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def high_frequency_changed(self, high_frequency):
        try:
            self.low_frequency.setMaximum(high_frequency)
            self.main_self.speackers_deck_instance.low_frequency.setMaximum(high_frequency)
            self.main_self.speackers_deck_instance.high_frequency.blockSignals(True)
            self.main_self.speackers_deck_instance.high_frequency.setValue(high_frequency)
            self.main_self.speackers_deck_instance.high_frequency.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def apply_filter_method(self, state):
        try:
            low_frequency = self.low_frequency.value()
            high_frequency = self.high_frequency.value()
            self.manage_speackers_deck_secondary_queue.put({"type": "low_frequency", "low_frequency_value": low_frequency})
            self.manage_speackers_deck_secondary_queue.put({"type": "high_frequency", "high_frequency_value": high_frequency})

            self.main_self.speackers_deck_instance.high_frequency.setMinimum(low_frequency)
            self.main_self.speackers_deck_instance.low_frequency.blockSignals(True)
            self.main_self.speackers_deck_instance.low_frequency.setValue(low_frequency)
            self.main_self.speackers_deck_instance.low_frequency.blockSignals(False)

            self.main_self.speackers_deck_instance.low_frequency.setMaximum(high_frequency)
            self.main_self.speackers_deck_instance.high_frequency.blockSignals(True)
            self.main_self.speackers_deck_instance.high_frequency.setValue(high_frequency)
            self.main_self.speackers_deck_instance.high_frequency.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def reset_filter_method(self, state):
        try:
            self.low_frequency.setValue(20)
            self.low_frequency.setMaximum(20000)
            self.high_frequency.setValue(20000)
            self.high_frequency.setMinimum(20)
            self.manage_speackers_deck_secondary_queue.put({"type": "low_frequency", "low_frequency_value": 20})
            self.manage_speackers_deck_secondary_queue.put({"type": "high_frequency", "high_frequency_value": 20000})

            low_frequency = 20
            high_frequency = 20000

            self.main_self.speackers_deck_instance.high_frequency.setMinimum(low_frequency)
            self.main_self.speackers_deck_instance.low_frequency.blockSignals(True)
            self.main_self.speackers_deck_instance.low_frequency.setValue(low_frequency)
            self.main_self.speackers_deck_instance.low_frequency.blockSignals(False)

            self.main_self.speackers_deck_instance.low_frequency.setMaximum(high_frequency)
            self.main_self.speackers_deck_instance.high_frequency.blockSignals(True)
            self.main_self.speackers_deck_instance.high_frequency.setValue(high_frequency)
            self.main_self.speackers_deck_instance.high_frequency.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

    def close(self):
        try:
            if self.deck_status != "stopped":
                self.manage_speackers_deck_secondary_queue.put({"type":"new-status","status":"stopped"})
                self.deck_status = "stopped"
                time.sleep(0.125)
            self.manage_speackers_deck_secondary_queue.put({"type": "close"})
            time.sleep(0.8)
            try:
                if self.manage_speackers_deck_secondary_child_process is not None:
                    self.manage_speackers_deck_secondary_child_process.terminate()
                    self.manage_speackers_deck_secondary_child_process.close()
            except:
                pass
            try:
                if self.manage_speackers_deck_secondary_emitter is not None:
                    self.manage_speackers_deck_secondary_emitter.quit()
                    del self.manage_speackers_deck_secondary_emitter
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
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put({"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_speackers_deck_secondary_error_window(error_message)

# CAUTION: no try except block for opening error window!
class Custom_QFrame(QtWidgets.QFrame):
    def __init__(self, parent, *args, **kwargs):
        super(QtWidgets.QFrame, self).__init__(parent, *args, **kwargs)

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            return True
        return super(QtWidgets.QFrame, self).eventFilter(obj, event)


class Manage_Speackers_Deck_Secondary_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        microphone_settings = pyqtSignal(dict)
        update_microphone_settings = pyqtSignal(dict)
        volume_amplitude = pyqtSignal(float)
        current_duration_milliseconds = pyqtSignal(int)
        microphone_slice = pyqtSignal(AudioSegment)
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
                elif data["type"] == "microphone_settings":
                    self.microphone_settings.emit(data["settings"])
                elif data["type"] == "update_microphone_settings":
                    self.update_microphone_settings.emit(data["settings"])
                elif data["type"] == "volume_amplitude":
                    self.volume_amplitude.emit(data["normalized_value"])
                elif data["type"] == "current_duration_milliseconds":
                    self.current_duration_milliseconds.emit(data["duration"])
                elif data["type"] == "microphone_slice":
                    self.microphone_slice.emit(data["slice"])
                elif data["type"] == "close":
                    break

        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)


class Manage_Speackers_Deck_Secondary_Child_Proc(Process):

    def __init__(self, to_emitter,from_mother,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.condition = condition
            self.data_from_mother = from_mother
            self.deck_status = "stopped"
            self.frame_number = frame_number
            self.quit_event = quit_event
        except:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.send({"type": "error", "error_message": error_message})
            except:
                pass

    def run(self):
        try:
            self.bit_rate = 128 * 1024  # 128 kb/sec
            self.packet_time = 125  # 125 msec
            # self.packet_time = 125*44100/32768
            self.packet_size = int(1)
            # self.new_sample_rate = 32768
            self.new_sample_rate = 44100
            self.TIME_WINDOW = 3000

            self.format = pyaudio.paInt16
            self.channels = 2

            self.input_stream = None

            self.database_functions = database_functions
            self.fetch_microphone_settings()
            current_frame = 0
            while(True):
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
                if data["type"] == "update-microphone-settings":
                    self.update_microphone_settings()
                elif data["type"] == "volume":
                    self.microphone_settings["volume"] = data["value_base_100"]
                    self.save_microphone_settings()
                elif data["type"] == "pan":
                    self.microphone_settings["pan"] = data["pan_value"]
                    self.save_microphone_settings()
                elif data["type"] == "is_normalized":
                    self.microphone_settings["is_normalized"] = data["boolean_value"]
                    self.save_microphone_settings()
                elif data["type"] == "low_frequency":
                    self.microphone_settings["low_frequency"] = data["low_frequency_value"]
                    self.save_microphone_settings()
                elif data["type"] == "high_frequency":
                    self.microphone_settings["high_frequency"] = data["high_frequency_value"]
                    self.save_microphone_settings()
                elif data["type"] == "close":
                    self.to_emitter.send({"type": "close"})
                    #self.quit_event.set()
                elif data["type"] == "new-status":
                    self.deck_status = data["status"]
                    if self.deck_status == "playing":
                        if self.input_device_name != "Καμία συσκευή μικροφώνου":
                            for input_device in self.input_devices:
                                if (self.input_device_name == input_device[2]):
                                    self.input_device_index = input_device[1]
                                    self.input_stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                                                    rate=self.new_sample_rate, input=True,
                                                                    input_device_index=self.input_device_index)
                                    self.input_stream.start_stream()
                                    self.input_channels = 1
                                    self.chunk_number = 0
                                    self.current_duration_milliseconds = 0
                                    break
                        else:
                            self.input_stream = None
                    else:
                        self.chunk_number = 0
                        self.current_duration_milliseconds = 0
                        try:
                            self.input_stream.stop_stream()
                            self.input_stream.close()
                        except:
                            pass

            if self.deck_status == "playing":
                if self.input_stream is not None:
                    in_data = self.input_stream.read(int(1024 * (44100 // 1024 * 0.125)))
                else:
                    return None
                if self.input_channels == 2:
                    slice = AudioSegment(in_data, sample_width=2, frame_rate=self.new_sample_rate, channels=2)
                else:
                    slice = AudioSegment(in_data, sample_width=2, frame_rate=self.new_sample_rate, channels=1)
                    slice = AudioSegment.from_mono_audiosegments(slice, slice)
                if self.microphone_settings["pan"] != 0:
                    slice = slice.pan(self.microphone_settings["pan"] / 100)
                if self.microphone_settings["low_frequency"] > 20:
                    slice = effects.high_pass_filter(slice, self.microphone_settings["low_frequency"])
                if self.microphone_settings["high_frequency"] > 20000:
                    slice = effects.low_pass_filter(slice, self.microphone_settings["high_frequency"])
                if (self.microphone_settings["volume"] == 0):
                    db_volume = -200
                else:
                    db_volume = 20 * math.log10(self.microphone_settings["volume"] / 100)
                slice = slice + db_volume
                if self.microphone_settings["is_normalized"]:
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
                self.current_duration_milliseconds += chunk_time

                self.to_emitter.send(
                    {"type": "current_duration_milliseconds", "duration": self.current_duration_milliseconds})
                self.to_emitter.send({"type": "microphone_slice", "slice": slice})
        except:
            error_message = str(traceback.format_exc())
            print(error_message)
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

    def update_microphone_settings(self):
        try:
            self.input_device_name = database_functions.read_setting("input_device_name")["value"]
            self.input_device_number = int(self.database_functions.read_setting("input_device_number")["value"])

            self.p = pyaudio.PyAudio()
            self.info = self.p.get_host_api_info_by_index(0)
            self.numdevices = self.info.get('deviceCount')

            self.input_devices = [[0, -1, "Καμία συσκευή μικροφώνου"]]
            api_info, api_index = self.get_api_info(self.p)
            api_name = api_info['name']
            PREFERRED_HOST_API_NAME = 'Windows WASAPI'
            if api_name != PREFERRED_HOST_API_NAME:
                print(f'[WARNING] "{PREFERRED_HOST_API_NAME}" not available on this system, '
                      f'going with "{api_name}" instead')

            numdevices = api_info.get('deviceCount')

            counter = 1
            for i in range(0, self.numdevices):
                dev_info = self.p.get_device_info_by_host_api_device_index(0, i)
                if dev_info.get('maxInputChannels') > 0:
                    device_name_cropped = str(dev_info.get('name'))
                    for j in range(0, numdevices):
                        one_dev_info = self.p.get_device_info_by_host_api_device_index(api_index, j)
                        if one_dev_info.get('maxInputChannels') > 0:
                            one_device_name = str(one_dev_info.get('name'))
                            if device_name_cropped in one_device_name:
                                device_name_cropped = one_device_name
                                break

                    self.input_devices.append([counter, i, device_name_cropped])
                    counter += 1

            self.volume = int(self.database_functions.read_setting("input_device_sound_volume")["value"])
            self.is_normalized = int(self.database_functions.read_setting("input_device_normalize")["value"])
            self.pan = float(self.database_functions.read_setting("input_device_pan")["value"])
            self.low_frequency = int(self.database_functions.read_setting("input_device_low_frequency")["value"])
            self.high_frequency = int(self.database_functions.read_setting("input_device_high_frequency")["value"])

            self.microphone_settings = {
                "volume": self.volume,
                "is_normalized": self.is_normalized,
                "pan": self.pan,
                "low_frequency": self.low_frequency,
                "high_frequency": self.high_frequency,
                "input_devices": self.input_devices
            }
            self.to_emitter.send({"type": "update_microphone_settings", "settings": self.microphone_settings})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def fetch_microphone_settings(self):
        try:
            self.input_device_name = database_functions.read_setting("input_device_name")["value"]
            self.input_device_number = int(self.database_functions.read_setting("input_device_number")["value"])

            self.p = pyaudio.PyAudio()
            self.info = self.p.get_host_api_info_by_index(0)
            self.numdevices = self.info.get('deviceCount')

            self.input_devices = [[0, -1, "Καμία συσκευή μικροφώνου"]]
            api_info, api_index = self.get_api_info(self.p)
            api_name = api_info['name']
            PREFERRED_HOST_API_NAME = 'Windows WASAPI'
            if api_name != PREFERRED_HOST_API_NAME:
                print(f'[WARNING] "{PREFERRED_HOST_API_NAME}" not available on this system, '
                      f'going with "{api_name}" instead')

            numdevices = api_info.get('deviceCount')

            counter = 1
            for i in range(0, self.numdevices):
                dev_info = self.p.get_device_info_by_host_api_device_index(0, i)
                if dev_info.get('maxInputChannels') > 0:
                    device_name_cropped = str(dev_info.get('name'))
                    for j in range(0, numdevices):
                        one_dev_info = self.p.get_device_info_by_host_api_device_index(api_index, j)
                        if one_dev_info.get('maxInputChannels') > 0:
                            one_device_name = str(one_dev_info.get('name'))
                            if device_name_cropped in one_device_name:
                                device_name_cropped = one_device_name
                                break

                    self.input_devices.append([counter, i, device_name_cropped])
                    counter += 1

            self.volume = int(self.database_functions.read_setting("input_device_sound_volume")["value"])
            self.is_normalized = int(self.database_functions.read_setting("input_device_normalize")["value"])
            self.pan = float(self.database_functions.read_setting("input_device_pan")["value"])
            self.low_frequency = int(self.database_functions.read_setting("input_device_low_frequency")["value"])
            self.high_frequency = int(self.database_functions.read_setting("input_device_high_frequency")["value"])

            self.microphone_settings = {
                "volume":self.volume,
                "is_normalized":self.is_normalized,
                "pan":self.pan,
                "low_frequency":self.low_frequency,
                "high_frequency":self.high_frequency,
                "input_devices":self.input_devices
            }

            self.to_emitter.send({"type": "microphone_settings", "settings": self.microphone_settings})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})


    def get_api_info(self, p):
        try:
            PREFERRED_HOST_API_NAME = 'Windows WASAPI'
            api_info, api_index = None, 0
            for i in range(p.get_host_api_count()):
                current_api_info = p.get_host_api_info_by_index(i)
                if i == 0:
                    api_info = current_api_info
                else:
                    if current_api_info['name'] == PREFERRED_HOST_API_NAME:
                        api_info, api_index = current_api_info, i
                        break
            return api_info, api_index
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def save_microphone_settings(self):
        try:
            database_functions.update_setting({"value":self.microphone_settings["volume"],"setting":"input_device_sound_volume"})
            database_functions.update_setting({"value":self.microphone_settings["is_normalized"],"setting":"input_device_normalize"})
            database_functions.update_setting({"value":self.microphone_settings["pan"],"setting":"input_device_pan"})
            database_functions.update_setting({"value":self.microphone_settings["low_frequency"],"setting":"input_device_low_frequency"})
            database_functions.update_setting({"value":self.microphone_settings["high_frequency"],"setting":"input_device_high_frequency"})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})