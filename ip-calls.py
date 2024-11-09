import aiohttp_cors
import av.logging
restore_default_callback = lambda *args: args
av.logging.restore_default_callback = restore_default_callback
av.logging.set_level(av.logging.ERROR)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread
from aiohttp import web
from aiohttp.web_runner import GracefulExit
from aiortc.mediastreams import MediaStreamTrack,MediaStreamError
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRelay
import av
import pyaudio
from pydub import AudioSegment,generators
import asyncio
import json
import os
from multiprocessing import Process, Queue, Pipe, freeze_support
from queue import Queue as Simple_Queue
import sys
import threading
import fractions
import requests
from PIL import Image
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from pyngrok import ngrok, conf
from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import cv2
import subprocess

from pygrabber.dshow_graph import FilterGraph
import traceback

import socket

ngrok.set_auth_token("1kxaH4jyih9qTuyTBE0V6bzYbnq_nVaCNY5wwUriYY5oiLDr")


import uuid


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


class Ip_Calls:
    def __init__(self, main_self):
        try:
            self.main_self = main_self

            self.put_to_q = False

            self.call_1_is_local = True
            self.call_2_is_local = True
            self.call_3_is_local = True

            self.main_self.ui.local_video_frame.hide()
            self.main_self.ui.ip_call_1_frame.hide()
            self.main_self.ui.ip_call_2_frame.hide()
            self.main_self.ui.ip_call_3_frame.hide()

            # create process
            self.process_number = 101
            self.ip_calls_mother_pipe, self.ip_calls_child_pipe = Pipe()
            self.ip_calls_queue = Queue()
            self.speackers_deck_queue = Queue()
            self.ip_calls_emitter = Ip_Calls_Emitter(self.ip_calls_mother_pipe)
            self.ip_calls_emitter.error_signal.connect(lambda error_message: self.main_self.open_ip_calls_error_window(error_message))
            self.ip_calls_emitter.call_1_offering.connect(lambda name, surname: self.new_call(1, name, surname))
            self.ip_calls_emitter.call_1_status.connect(lambda status: self.call_status(1, status))
            self.ip_calls_emitter.transport_error.connect(lambda call_number:self.transport_error(call_number))
            self.ip_calls_emitter.stop_peer_connection.connect(lambda call_number:self.stop_peer_connection(call_number))
            self.ip_calls_emitter.is_available.connect(lambda is_available_for_ip_calls:self.producer_is_available(is_available_for_ip_calls))

            self.ip_calls_emitter.call_2_offering.connect(lambda name, surname: self.new_call(2, name, surname))
            self.ip_calls_emitter.call_2_status.connect(lambda status: self.call_status(2, status))

            self.ip_calls_emitter.call_3_offering.connect(lambda name, surname: self.new_call(3, name, surname))
            self.ip_calls_emitter.call_3_status.connect(lambda status: self.call_status(3, status))

            self.ip_calls_emitter.server_web_camera_packet.connect(lambda pil_image: self.display_video_frame(0, pil_image[0]))
            self.ip_calls_emitter.hide_server_web_camera.connect(lambda: self.hide_server_web_camera())

            self.ip_calls_emitter.ip_call_packet.connect(lambda call_number,frame: self.ip_call_packet_received(call_number,frame))


            self.ip_calls_emitter.client_1_web_camera_packet.connect(lambda pil_image: self.display_video_frame(1, pil_image[0]))
            self.ip_calls_emitter.client_2_web_camera_packet.connect(lambda pil_image: self.display_video_frame(2, pil_image[0]))
            self.ip_calls_emitter.client_3_web_camera_packet.connect(lambda pil_image: self.display_video_frame(3, pil_image[0]))



            self.ip_calls_emitter.start()
            self.ip_calls_child_process = Ip_Calls_Child_Proc(
                self.ip_calls_child_pipe, self.ip_calls_queue,self.speackers_deck_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.ip_calls_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.ip_calls_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})

            self.init_buttons_and_sub_menus()
            self.put_to_q = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def producer_is_available(self,is_available_for_ip_calls):
        try:
            if is_available_for_ip_calls:
                self.main_self.ui.action_available_for_ip_calls.blockSignals(True)
                self.main_self.ui.action_available_for_ip_calls.setChecked(True)
                self.ip_calls_queue.put({"type": "start-aiortc-server"})
                self.is_available_for_ip_calls = is_available_for_ip_calls
                self.main_self.ui.action_available_for_ip_calls.triggered.connect(lambda action:self.is_available_button_clicked())
                self.main_self.ui.action_available_for_ip_calls.blockSignals(False)
            else:
                self.main_self.ui.action_available_for_ip_calls.blockSignals(True)
                self.main_self.ui.action_available_for_ip_calls.setChecked(False)
                self.is_available_for_ip_calls = is_available_for_ip_calls
                self.main_self.ui.action_available_for_ip_calls.triggered.connect(lambda action:self.is_available_button_clicked())
                self.main_self.ui.action_available_for_ip_calls.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.main_self.open_ip_calls_error_window(error_message)

    def is_available_button_clicked(self):
        try:
            if self.main_self.ui.action_available_for_ip_calls.isChecked():
                self.main_self.ui.action_available_for_ip_calls.blockSignals(True)
                self.ip_calls_queue.put({"type": "start-aiortc-server"})
                self.is_available_for_ip_calls = 1
                self.main_self.ui.action_available_for_ip_calls.blockSignals(False)
            else:
                self.main_self.ui.action_available_for_ip_calls.blockSignals(True)
                self.is_available_for_ip_calls = 0
                self.ip_calls_queue.put({"type": "stop-aiortc-server"})
                self.main_self.ui.action_available_for_ip_calls.blockSignals(False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)



    def stop_peer_connection(self,call_number):
        try:
            self.main_self.ip_calls_record_deck_instance.stop_record(call_number)
            if self.main_self.ip_call_offering_window_is_open:
                self.main_self.ip_call_offering_window.close()
            frame = getattr(self.main_self.ui, 'ip_call_{}_frame'.format(call_number))
            frame.hide()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def transport_error(self,call_number):
        try:
            self.main_self.ip_calls_record_deck_instance.stop_record(call_number)
            if self.main_self.ip_call_offering_window_is_open:
                self.main_self.ip_call_offering_window_support_code.call_answered = True
                self.main_self.ip_call_offering_window.close()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def init_buttons_and_sub_menus(self):
        try:
            # ip_call volume menu
            self.create_menu_for_volume()

            # ip_call pan menu
            self.create_menu_for_pan()

            # ip_call normalize menu
            self.create_menu_for_normalize()

            # ip_call filter menu
            self.create_menu_for_filter()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

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
            self.main_self.open_ip_calls_error_window(error_message)

    def volume_resetted(self):
        try:
            self.volume_slider.setValue(100)
            self.volume_label.setText("100/200")
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "volume", "value_base_100": 100})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def volume_changed(self, slider_value):
        try:
            self.volume_label.setText(str(slider_value) + "/200")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def volume_released(self):
        try:
            slider_value = self.volume_slider.value()
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "volume", "value_base_100": slider_value})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def volume_action_triggered(self, action):
        try:
            if action == QtWidgets.QAbstractSlider.SliderSingleStepAdd or action == QtWidgets.QAbstractSlider.SliderSingleStepSub or action == QtWidgets.QAbstractSlider.SliderPageStepAdd or action == QtWidgets.QAbstractSlider.SliderPageStepSub:
                self.timer_2 = QtCore.QTimer()
                self.timer_2.timeout.connect(lambda: self.volume_released())
                self.timer_2.setSingleShot(True)
                self.timer_2.start(500)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

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
            self.pan_slider.setProperty("value", 0)
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
            self.main_self.open_ip_calls_error_window(error_message)

    def pan_resetted(self):
        try:
            self.pan_slider.setValue(0)
            self.pan_label.setText("0")
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "pan", "pan_value": 0})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def pan_changed(self, slider_value):
        try:
            self.pan_label.setText(str(slider_value))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def pan_released(self):
        try:
            slider_value = self.pan_slider.value()
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "pan", "pan_value": slider_value})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def pan_action_triggered(self, action):
        try:
            if action == QtWidgets.QAbstractSlider.SliderSingleStepAdd or action == QtWidgets.QAbstractSlider.SliderSingleStepSub or action == QtWidgets.QAbstractSlider.SliderPageStepAdd or action == QtWidgets.QAbstractSlider.SliderPageStepSub:
                self.timer_2 = QtCore.QTimer()
                self.timer_2.timeout.connect(lambda: self.pan_released())
                self.timer_2.setSingleShot(True)
                self.timer_2.start(500)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

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
            self.horizontalLayout_normalize = QtWidgets.QHBoxLayout(self.normalize_frame)
            #self.horizontalLayout.setObjectName("horizontalLayout")
            self.normalize_checkBox = QtWidgets.QCheckBox(self.normalize_frame)
            self.normalize_checkBox.setObjectName("normalize_checkBox")
            self.normalize_checkBox.setStyleSheet("border:none;")
            self.normalize_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.horizontalLayout_normalize.addWidget(self.normalize_checkBox)

            self.normalize_checkBox.setText("Κανονικοποίηση")

            # on normalize changed
            self.normalize_checkBox.stateChanged.connect(lambda new_state: self.normalize_changed(new_state))

            normalize_widget = QtWidgets.QWidgetAction(self.menu_for_normalize)
            normalize_widget.setDefaultWidget(self.normalize_frame)
            self.menu_for_normalize.addAction(normalize_widget)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def normalize_changed(self, new_state):
        try:
            if new_state == QtCore.Qt.Unchecked:
                self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "is_normalized", "boolean_value": 0})
            else:
                self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "is_normalized", "boolean_value": 1})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

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
            self.main_self.open_ip_calls_error_window(error_message)

    def low_frequency_changed(self, low_frequency):
        try:
            self.high_frequency.setMinimum(low_frequency)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def high_frequency_changed(self, high_frequency):
        try:
            self.low_frequency.setMaximum(high_frequency)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def apply_filter_method(self, state):
        try:
            low_frequency = self.low_frequency.value()
            high_frequency = self.high_frequency.value()
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "low_frequency", "low_frequency_value": low_frequency})
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "high_frequency", "high_frequency_value": high_frequency})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def reset_filter_method(self, state):
        try:
            self.low_frequency.setValue(20)
            self.low_frequency.setMaximum(20000)
            self.high_frequency.setValue(20000)
            self.high_frequency.setMinimum(20)
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "low_frequency", "low_frequency_value": 20})
            self.main_self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "high_frequency", "high_frequency_value": 20000})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def ip_call_packet_received(self, call_number, frame):
        try:
            if self.put_to_q:
                packet_data = {"type": "packet", "packet": frame[0]}
                call_queue_map = {
                    1: self.main_self.ip_call_1_instance.ip_call_1_packet_queue,
                    2: self.main_self.ip_call_2_instance.ip_call_2_packet_queue,
                    3: self.main_self.ip_call_3_instance.ip_call_3_packet_queue,
                }

                if call_number in call_queue_map:
                    call_queue_map[call_number].put(packet_data)
        except Exception as e:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def hide_server_web_camera(self):
        try:
            self.main_self.ui.local_video_label.clear()
            self.main_self.ui.local_video_frame.hide()
            if self.main_self.speackers_deck_secondary_instance.deck_status != "stopped":
                self.main_self.speackers_deck_secondary_instance.play_or_pause()
            self.main_self.ip_calls_record_deck_instance.stop_record(1)
            self.main_self.ip_calls_record_deck_instance.stop_record(2)
            self.main_self.ip_calls_record_deck_instance.stop_record(3)
            self.main_self.stacked_widget_instance.go_to_page(0)
            self.main_self.stacked_widget_instance.hide_page_3()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def display_video_frame(self, call_id, pil_image):
        try:
            if call_id == 0:  # 0 for self video
                self.main_self.ui.local_video_frame.show()
                pixmap = self.pil2pixmap(pil_image)
                self.main_self.ui.local_video_label.setPixmap(pixmap)
                self.main_self.ui.local_video_label.show()
            elif call_id == 1:
                if pil_image is None:
                    return self.end_call(1, None)
                pixmap = self.pil2pixmap(pil_image)
                client_1_video = getattr(self.main_self.ui, 'ip_call_{}_video_label'.format(call_id))
                client_1_video.setPixmap(pixmap)
                client_1_video.show()
                self.call_1_timer.stop()
                self.call_1_timer = QtCore.QTimer()
                self.call_1_timer.timeout.connect(lambda: self.end_call(1, None))
                self.call_1_timer.setSingleShot(True)
                self.call_1_timer.start(15000)
            if call_id == 2:
                if pil_image is None:
                    return self.end_call(1, None)
                pixmap = self.pil2pixmap(pil_image)
                client_2_video = getattr(self.main_self.ui, 'ip_call_{}_video_label'.format(call_id))
                client_2_video.setPixmap(pixmap)
                client_2_video.show()
                self.call_2_timer.stop()
                self.call_2_timer = QtCore.QTimer()
                self.call_2_timer.timeout.connect(lambda: self.end_call(2, None))
                self.call_2_timer.setSingleShot(True)
                self.call_2_timer.start(15000)
            if call_id == 3:
                if pil_image is None:
                    return self.end_call(1, None)
                pixmap = self.pil2pixmap(pil_image)
                client_3_video = getattr(self.main_self.ui, 'ip_call_{}_video_label'.format(call_id))
                client_3_video.setPixmap(pixmap)
                client_3_video.show()
                self.call_3_timer.stop()
                self.call_3_timer = QtCore.QTimer()
                self.call_3_timer.timeout.connect(lambda: self.end_call(3, None))
                self.call_3_timer.setSingleShot(True)
                self.call_3_timer.start(15000)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def pil2pixmap(self, im):
        try:
            if im.mode == "RGB":
                r, g, b = im.split()
                im = Image.merge("RGB", (b, g, r))
            elif im.mode == "RGBA":
                r, g, b, a = im.split()
                im = Image.merge("RGBA", (b, g, r, a))
            elif im.mode == "L":
                im = im.convert("RGBA")
            # Bild in RGBA konvertieren, falls nicht bereits passiert
            im2 = im.convert("RGBA")
            data = im2.tobytes("raw", "RGBA")
            qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap.fromImage(qim)
            return pixmap
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def new_call(self, call_number, name, surname):
        try:
            self.main_self.open_ip_call_offering_window(call_number,name,surname)
            self.main_self.stacked_widget_instance.show_page_3()
            self.main_self.stacked_widget_instance.go_to_page(2)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def reject_call(self, call_number, state):
        try:
            frame = getattr(self.main_self.ui, 'ip_call_{}_frame'.format(call_number))
            frame.hide()
            label = getattr(self.main_self.ui, 'ip_call_{}_video_label'.format(call_number))
            label.clear()
            btn = getattr(self.main_self.ui, 'ip_call_{}_forward_call'.format(call_number))
            btn.show()
            btn = getattr(self.main_self.ui, 'ip_call_{}_dismiss'.format(call_number))
            btn.show()
            #btn = getattr(self.main_self.ui, 'ip_call_{}_answer'.format(call_number))
            #btn.show()
            self.ip_calls_queue.put({"type": "call-"+str(call_number), "call": "reject"})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def call_status(self,call_number, status):
        try:
            if status == "closed-by-client" or status == "closed-by-server":
                self.main_self.ip_calls_record_deck_instance.stop_record(call_number)
                frame = getattr(self.main_self.ui, 'ip_call_{}_frame'.format(call_number))
                frame.hide()
                label = getattr(self.main_self.ui, 'ip_call_{}_video_label'.format(call_number))
                label.clear()
                btn = getattr(self.main_self.ui, 'ip_call_{}_forward_call'.format(call_number))
                btn.show()
                btn = getattr(self.main_self.ui, 'ip_call_{}_dismiss'.format(call_number))
                btn.show()
                #btn = getattr(self.main_self.ui, 'ip_call_{}_answer'.format(call_number))
                #btn.show()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def local_answer(self,call_number,name,surname):
        try:
            self.main_self.ui.local_video_frame.show()
            frame = getattr(self.main_self.ui, 'ip_call_{}_frame'.format(call_number))
            frame.show()
            btn_ignore = getattr(self.main_self.ui, 'ip_call_{}_dismiss'.format(call_number))
            try:
                btn_ignore.clicked.disconnect()
            except:
                pass
            btn_ignore.clicked.connect(lambda state,call_nmbr=call_number: self.end_call(call_nmbr,state))
            btn = getattr(self.main_self.ui, 'ip_call_{}_title_label'.format(call_number))
            btn.setText(name+" "+surname)

            btn = getattr(self.main_self.ui, 'ip_call_{}_forward_call'.format(call_number))
            try:
                btn.clicked.disconnect()
            except:
                pass
            btn.clicked.connect(lambda state,call_nmbr = call_number:self.forward_call(call_nmbr))
            btn.show()

            self.ip_calls_queue.put({"type": "call-"+str(call_number), "call": "answer"})

            if call_number == 1:
                self.call_1_is_local = True
                self.call_1_timer = QtCore.QTimer()
                self.call_1_timer.timeout.connect(lambda: self.end_call(1, None))
                self.call_1_timer.setSingleShot(True)
                self.call_1_timer.start(30000)
            elif call_number == 2:
                self.call_2_is_local = True
                self.call_2_timer = QtCore.QTimer()
                self.call_2_timer.timeout.connect(lambda: self.end_call(2, None))
                self.call_2_timer.setSingleShot(True)
                self.call_2_timer.start(30000)
            else:
                self.call_3_is_local = True
                self.call_3_timer = QtCore.QTimer()
                self.call_3_timer.timeout.connect(lambda: self.end_call(3, None))
                self.call_3_timer.setSingleShot(True)
                self.call_3_timer.start(30000)

            if self.main_self.speackers_deck_secondary_instance.deck_status != "playing":
                self.main_self.speackers_deck_secondary_instance.play_or_pause()

            #start recording
            self.main_self.ip_calls_record_deck_instance.start_record(call_number,name,surname,is_local=True)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def public_answer(self,call_number,name,surname):
        try:
            self.main_self.ui.local_video_frame.show()
            frame = getattr(self.main_self.ui, 'ip_call_{}_frame'.format(call_number))
            frame.show()
            btn_ignore = getattr(self.main_self.ui, 'ip_call_{}_dismiss'.format(call_number))
            try:
                btn_ignore.clicked.disconnect()
            except:
                pass
            btn_ignore.clicked.connect(lambda state,call_nmbr=call_number: self.end_call(call_nmbr,state))
            btn = getattr(self.main_self.ui, 'ip_call_{}_title_label'.format(call_number))
            btn.setText(name + " " + surname)

            btn = getattr(self.main_self.ui, 'ip_call_{}_forward_call'.format(call_number))
            try:
                btn.clicked.disconnect()
            except:
                pass
            btn.hide()

            self.ip_calls_queue.put({"type": "call-"+str(call_number), "call": "answer"})

            if call_number == 1:
                self.call_1_is_local = True
                self.call_1_timer = QtCore.QTimer()
                self.call_1_timer.timeout.connect(lambda: self.end_call(1, None))
                self.call_1_timer.setSingleShot(True)
                self.call_1_timer.start(30000)
            elif call_number == 2:
                self.call_2_is_local = True
                self.call_2_timer = QtCore.QTimer()
                self.call_2_timer.timeout.connect(lambda: self.end_call(2, None))
                self.call_2_timer.setSingleShot(True)
                self.call_2_timer.start(30000)
            else:
                self.call_2_is_local = True
                self.call_3_timer = QtCore.QTimer()
                self.call_3_timer.timeout.connect(lambda: self.end_call(3, None))
                self.call_3_timer.setSingleShot(True)
                self.call_3_timer.start(30000)

            if self.main_self.speackers_deck_secondary_instance.deck_status == "playing":
                self.main_self.speackers_deck_secondary_instance.play_or_pause()

            #open speackers deck microphone
            if self.main_self.speackers_deck_instance.deck_status !="playing":
                self.main_self.speackers_deck_instance.click_to_talk_button_clicked()

            # start recording
            self.main_self.ip_calls_record_deck_instance.start_record(call_number, name, surname, is_local=False)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def forward_call(self,call_number):
        try:
            btn = getattr(self.main_self.ui, 'ip_call_{}_forward_call'.format(call_number))
            try:
                btn.clicked.disconnect()
            except:
                pass
            btn.hide()


            if call_number == 1:
                self.call_1_is_local = True
            elif call_number == 2:
                self.call_2_is_local = True
            else:
                self.call_2_is_local = True

            if self.main_self.speackers_deck_secondary_instance.deck_status == "playing":
                self.main_self.speackers_deck_secondary_instance.play_or_pause()

            #open speackers deck microphone
            if self.main_self.speackers_deck_instance.deck_status !="playing":
                self.main_self.speackers_deck_instance.click_to_talk_button_clicked()

            # change record source
            self.main_self.ip_calls_record_deck_instance.set_is_local(call_number,is_local=False)
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.main_self.open_ip_calls_error_window(error_message)

    def end_call(self, call_number, state):
        try:
            self.main_self.ip_calls_record_deck_instance.stop_record(call_number)
            frame = getattr(self.main_self.ui, 'ip_call_{}_frame'.format(call_number))
            if frame.isVisible() == False:
                return None
            frame.hide()

            frame_1 = self.main_self.ui.ip_call_1_frame.isVisible()
            frame_2 = self.main_self.ui.ip_call_2_frame.isVisible()
            frame_3 = self.main_self.ui.ip_call_3_frame.isVisible()
            if frame_1 == False and frame_2 == False and frame_3 == False:
                self.main_self.ui.local_video_frame.hide()
                self.main_self.stacked_widget_instance.go_to_page(0)
                self.main_self.stacked_widget_instance.hide_page_3()
            else:
                self.main_self.ui.local_video_frame.show()

            label = getattr(self.main_self.ui, 'ip_call_{}_video_label'.format(call_number))
            label.clear()
            btn = getattr(self.main_self.ui, 'ip_call_{}_forward_call'.format(call_number))
            btn.show()
            btn = getattr(self.main_self.ui, 'ip_call_{}_dismiss'.format(call_number))
            btn.show()
            #btn = getattr(self.main_self.ui, 'ip_call_{}_answer'.format(call_number))
            #btn.show()
            self.ip_calls_queue.put({"type": "call-"+str(call_number), "call": "end"})

            if call_number == 1:
                try:
                    self.call_1_timer.stop()
                except:
                    pass
            elif call_number == 2:
                try:
                    self.call_2_timer.stop()
                except:
                    pass
            elif call_number == 3:
                try:
                    self.call_3_timer.stop()
                except:
                    pass
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_error_window(error_message)

    def close(self):
        try:
            self.ip_calls_queue.put({"type": "close"})
            try:
                if self.ip_calls_child_process is not None:
                    self.ip_calls_child_process.terminate()
                    self.ip_calls_child_process.close()
            except:
                pass
            try:
                if self.ip_calls_emitter is not None:
                    self.ip_calls_emitter.quit()
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
            self.main_self.open_ip_calls_error_window(error_message)

# CAUTION: no try except block for opening error window!
class Custom_QFrame(QtWidgets.QFrame):
    def __init__(self, parent, *args, **kwargs):
        super(QtWidgets.QFrame, self).__init__(parent, *args, **kwargs)

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            return True
        return super(QtWidgets.QFrame, self).eventFilter(obj, event)


class Ip_Calls_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        call_1_offering = pyqtSignal(str, str)
        call_1_status = pyqtSignal(str)

        call_2_offering = pyqtSignal(str, str)
        call_2_status = pyqtSignal(str)

        call_3_offering = pyqtSignal(str, str)
        call_3_status = pyqtSignal(str)

        hide_server_web_camera = pyqtSignal()

        server_web_camera_packet = pyqtSignal(list)
        client_1_web_camera_packet = pyqtSignal(list)
        client_2_web_camera_packet = pyqtSignal(list)
        client_3_web_camera_packet = pyqtSignal(list)

        ip_call_packet = pyqtSignal(int,list)

        transport_error = pyqtSignal(int)
        stop_peer_connection = pyqtSignal(int)

        is_available = pyqtSignal(int)
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
                elif data["type"] == "close":
                    break
                elif data["type"] == "call_1_offering":
                    self.call_1_offering.emit(data["name"], data["surname"])
                elif data["type"] == "call-1-status":
                    self.call_1_status.emit(data["status"])
                elif data["type"] == "call_2_offering":
                    self.call_2_offering.emit(data["name"], data["surname"])
                elif data["type"] == "call-2-status":
                    self.call_2_status.emit(data["status"])
                elif data["type"] == "call_3_offering":
                    self.call_3_offering.emit(data["name"], data["surname"])
                elif data["type"] == "call-3-status":
                    self.call_3_status.emit(data["status"])
                elif data["type"] == "server-web-camera-frame":
                    self.server_web_camera_packet.emit(data["pil_image"])
                elif data["type"] == "client-1-web-camera-frame":
                    self.client_1_web_camera_packet.emit(data["pil_image"])
                elif data["type"] == "client-2-web-camera-frame":
                    self.client_2_web_camera_packet.emit(data["pil_image"])
                elif data["type"] == "client-3-web-camera-frame":
                    self.client_3_web_camera_packet.emit(data["pil_image"])
                elif data["type"] == "hide_server_web_camera":
                    self.hide_server_web_camera.emit()
                elif data["type"] == "ip-call-packet":
                    self.ip_call_packet.emit(data["call-number"],data["frame"])
                elif data["type"] == "transport-error":
                    self.transport_error.emit(data["call-number"])
                elif data["type"] == "stop-peer-connection":
                    self.stop_peer_connection.emit(data["call_number"])
                elif data["type"] == "is_available":
                    self.is_available.emit(data["is_available"])
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)


class Ip_Calls_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,speackers_deck_queue,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
            self.speackers_deck_queue = speackers_deck_queue
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.aiortc_process = None
            self.call_queues = [Queue(), Queue(), Queue()]
        except:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.send({"type": "error", "error_message": error_message})
            except:
                pass

    def run(self):
        try:
            #print("Ip_Calls_Child_Proc pid: " + str(self.pid))
            self.radio_producer_available_for_ip_calls = int(database_functions.read_setting("radio_producer_available_for_ip_calls")["value"])
            self.to_emitter.send({"type":"is_available","is_available":self.radio_producer_available_for_ip_calls})
            current_frame = 0
            while (True):
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return
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
                if data["type"] == "close":
                    try:
                        if self.aiortc_process is not None:
                            try:
                                ngrok.disconnect(self.tunnel.public_url)
                                self.call_queues[0].put({"type":"call-1","call":"end"})
                                self.call_queues[1].put({"type":"call-2","call":"end"})
                                self.call_queues[2].put({"type":"call-3","call":"end"})
                            except:
                                pass
                            self.aiortc_process.terminate()
                            self.aiortc_process.close()
                            self.aiortc_process = None
                            self.ip_calls_queue = None
                    except:
                        pass
                    self.to_emitter.send({"type": "close"})
                elif data["type"] == "start-aiortc-server":
                    si = subprocess.STARTUPINFO()
                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    subprocess.call('taskkill /f /im ngrok.exe', startupinfo=si)
                    hostname = socket.gethostname()
                    ip_address = socket.gethostbyname(hostname)
                    self.tunnel = ngrok.connect(str(ip_address) + ":8080", "http", "host_header:rewrite")
                    print(self.tunnel.public_url)
                    self.call_queues = [Queue(), Queue(), Queue()]
                    self.ip_calls_queue = Queue()
                    self.aiortc_process = WebRtcServer(self.to_emitter,self.ip_calls_queue,self.call_queues,self.speackers_deck_queue)
                    self.aiortc_process.start()
                    self.radio_producer_available_for_ip_calls = 1
                    database_functions.update_setting({"setting": "radio_producer_available_for_ip_calls", "value": 1})
                elif data["type"] == "stop-aiortc-server":
                    try:
                        if self.aiortc_process is not None:
                            try:
                                ngrok.disconnect(self.tunnel.public_url)
                                self.call_queues[0].put({"type": "call-1", "call": "end"})
                                self.call_queues[1].put({"type": "call-2", "call": "end"})
                                self.call_queues[2].put({"type": "call-3", "call": "end"})
                            except:
                                pass
                            self.aiortc_process.terminate()
                            self.aiortc_process.close()
                            self.aiortc_process = None
                            self.ip_calls_queue = None
                    except:
                        pass
                    self.radio_producer_available_for_ip_calls = 0
                    database_functions.update_setting({"setting": "radio_producer_available_for_ip_calls", "value": 0})

                elif data["type"] == "slice":
                    self.speackers_deck_queue.put(data)
                elif data["type"] == "call-1":
                    if data["call"] == "end":
                        self.call_queues[0].put(data)
                    else:
                        self.ip_calls_queue.put(data)
                elif data["type"] == "call-2":
                    if data["call"] == "end":
                        self.call_queues[1].put(data)
                    else:
                        self.ip_calls_queue.put(data)
                elif data["type"] == "call-3":
                    if data["call"] == "end":
                        self.call_queues[2].put(data)
                    else:
                        self.ip_calls_queue.put(data)
                else:
                    if self.ip_calls_queue is not None:
                        self.ip_calls_queue.put(data)
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})


class WebRtcServer(Process):
    def __init__(self, to_emitter,ip_calls_queue,call_queues,speackers_deck_queue):
        try:
            super().__init__()

            self.to_emitter = to_emitter
            self.ip_calls_queue = ip_calls_queue
            self.call_queues = call_queues
            self.speackers_deck_queue = speackers_deck_queue

            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                self.www_root_folder = os.path.abspath("extra-files/ip_calls")
            else:
                self.www_root_folder = os.path.abspath("../../../extra-files/ip_calls")

            self.pcs = {}
            self.webcam = None
            self.server_audio_stream_offer = None
            self.server_audio_blackholde = None
            self.server_video_stream_offer = None
            self.server_video_track = None
            self.server_video_blackholde = None
        except:
            error = traceback.format_exc()
            to_emitter.send({"type": "error", "error_message": error})

    def run(self):
        try:
            print("WebRtcServer pid: " + str(self.pid))
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)



            self.app = web.Application()
            self.app.on_shutdown.append(self.on_shutdown)
            self.app.router.add_get("/", self.index)
            self.app.router.add_get("/telephone-call.ico", self.icon)
            self.app.router.add_get("/telephone-call.png", self.png)
            self.app.router.add_get("/signal.mp3", self.mp3)
            self.app.router.add_get("/video_calls.js", self.javascript)
            self.app.router.add_post("/offer", self.offer)
            self.app.router.add_post("/shutdown", self.shutdown_aiohttp)
            cors = aiohttp_cors.setup(self.app, defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True,expose_headers="*",allow_headers="*")})
            for route in list(self.app.router.routes()):
                cors.add(route)
            web.run_app(self.app, access_log=None, host=str(ip_address), port=8080, ssl_context=None,keepalive_timeout=60.0, backlog=300)
        except:
            error = traceback.format_exc()
            print(error)
            self.to_emitter.send({"type": "error", "error_message": error})

    async def index(self,request):
        content = open(os.path.abspath("exe/extra-files/ip_calls/index.html"), "r", encoding='utf-8').read()
        return web.Response(content_type="text/html", text=content)

    async def mp3(self,request):
        file_path = os.path.abspath("exe/extra-files/ip_calls/signal.mp3")

        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            content = f.read()

        # Return the response with correct content type and binary data
        return web.Response(body=content, content_type='audio/mpeg')

    async def icon(self,request):
        file_path = os.path.abspath("exe/extra-files/ip_calls/telephone-call.ico")

        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            content = f.read()

        # Return the response with correct content type and binary data
        return web.Response(body=content, content_type='image/x-icon')

    async def png(self,request):
        file_path = os.path.abspath("exe/extra-files/ip_calls/telephone-call.png")

        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            content = f.read()

        # Return the response with correct content type and binary data
        return web.Response(body=content, content_type='image/png')

    async def javascript(self,request):
        content = open(os.path.abspath("exe/extra-files/ip_calls/video_calls.js"), "r", encoding='utf-8').read()
        return web.Response(content_type="application/javascript", text=content)

    def get_available_cameras(self):
        try:
            devices = FilterGraph().get_input_devices()
            available_cameras = {}
            for device_index, device_name in enumerate(devices):
                available_cameras[device_index] = device_name
            return available_cameras
        except:
            error = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error})

    def create_local_tracks(self):
        try:
            options = {"framerate": "30", "video_size": "640x480"}  # Reduced frame rate and resolution
            camera_name = "video=" + self.get_available_cameras()[0]
            self.webcam = MediaPlayer(camera_name, format='dshow', options=options)
            relay = MediaRelay()
            video_track = relay.subscribe(self.webcam.video)  # Relay the video stream
            return video_track
        except Exception as e:
            error = f"Error in create_local_tracks: {str(e)}"
            self.to_emitter.send({"type": "error", "error_message": error})
            print(error)  # Print the error for debugging

    async def offer(self, request):
        try:
            params = await request.json()

            peer_connection = {
                "name": params["name"],
                "surname": params["surname"],
                "pc": None,
                "is_closed": False,
                "dc": None,
                "uid": uuid.uuid4(),
                "audio_track": None,
                "audio_track_for_local_use": None,
                "audio_blackhole": None,
                "video_track": None,
                "video_track_for_local_use": None,
                "video_blackhole": None,
                "offer_in_progress": True,
                "call_answered": False,
                "manage_call_end_thread": None,
                "stop_in_progress": False,
                "call_number": None
            }

            if len(list(self.pcs.keys())) == 3:
                return web.Response(content_type="application/json", text=json.dumps({"sdp": "", "type": ""}))

            reserved_call_numbers = list(self.pcs.keys())

            if 1 not in reserved_call_numbers:
                call_number = 1
            elif 2 not in reserved_call_numbers:
                call_number = 2
            else:
                call_number = 3

            peer_connection["call_number"] = call_number
            self.pcs[call_number] = peer_connection

            if call_number == 1:
                self.to_emitter.send({"type": "call_1_offering", "name": peer_connection["name"], "surname": peer_connection["surname"]})
                #data_from_mother = self.call_queues[0]
            elif call_number == 2:
                self.to_emitter.send({"type": "call_2_offering", "name": peer_connection["name"], "surname": peer_connection["surname"]})
                #data_from_mother = self.call_queues[1]
            else:
                self.to_emitter.send({"type": "call_3_offering", "name": peer_connection["name"], "surname": peer_connection["surname"]})
                #data_from_mother = self.call_queues[2]

            timer = 0
            while (timer < 30 and self.ip_calls_queue.qsize() == 0 and self.pcs[call_number]["call_answered"] == False):
                if request.transport is None or request.transport.is_closing():
                    self.to_emitter.send({"type":"transport-error","call-number":call_number})
                    try:
                        request.transport.close()
                    except:
                        pass
                    del self.pcs[call_number]
                    return None
                timer += 0.1
                await asyncio.sleep(0.1)
            self.pcs[call_number]["call_answered"] = True
            if self.ip_calls_queue.qsize() == 0:
                # reject offer
                while not self.ip_calls_queue.empty():
                    self.ip_calls_queue.get()
                if call_number == 1:
                    self.to_emitter.send({"type": "call-1-status", "status": "closed-by-server"})
                elif call_number == 2:
                    self.to_emitter.send({"type": "call-2-status", "status": "closed-by-server"})
                else:
                    self.to_emitter.send({"type": "call-3-status", "status": "closed-by-server"})
                await self.stop_peer_connection(peer_connection["uid"])
                return web.Response(content_type="application/json", text=json.dumps({"sdp": "", "type": ""}))
            else:
                data = self.ip_calls_queue.get()
                if (data["type"] == "call-1" and data["call"] == "reject") or (
                        data["type"] == "call-2" and data["call"] == "reject") or (
                        data["type"] == "call-3" and data["call"] == "reject"):
                    # reject call
                    while not self.ip_calls_queue.empty():
                        self.ip_calls_queue.get()
                    await self.stop_peer_connection(peer_connection["uid"])
                    return web.Response(content_type="application/json", text=json.dumps({"sdp": "", "type": ""}))
                elif (data["type"] == "call-1" and data["call"] == "answer") or (
                        data["type"] == "call-2" and data["call"] == "answer") or (
                        data["type"] == "call-3" and data["call"] == "answer"):
                    while not self.ip_calls_queue.empty():
                        self.ip_calls_queue.get()


                    #self.pcs[call_number]["pc"] = RTCPeerConnection()

                    self.pcs[call_number]["pc"] = RTCPeerConnection(configuration=RTCConfiguration([RTCIceServer("stun:stun.l.google:19302"),]))

                    '''
                    configuration = RTCConfiguration(
                        iceServers=[
                            RTCIceServer(urls=["stun:stun.l.google.com:19302"]),
                        ]
                    )
                    self.pcs[call_number]["pc"] = RTCPeerConnection(configuration=configuration)
                    '''

                    @self.pcs[call_number]["pc"].on("iceconnectionstatechange")
                    async def on_ice_connection_state_change():
                        print("ICE connection state is "+self.pcs[call_number]["pc"].iceConnectionState)
                        if self.pcs[call_number]["pc"].iceConnectionState == "failed":
                            print("ICE connection failed. Attempting to restart ICE.")
                            await self.pcs[call_number]["pc"].restartIce()

                    @self.pcs[call_number]["pc"].on("connectionstatechange")
                    async def on_connectionstatechange():
                        try:
                            if self.pcs[call_number]["pc"].connectionState == "failed":
                                await self.stop_peer_connection(peer_connection["uid"])
                        except:
                            pass

                    @self.pcs[call_number]["pc"].on("datachannel")
                    async def on_datachannel(channel):
                        self.pcs[call_number]["dc"] = channel
                        try:
                            channel.send('{"type":"uid","uid":"' + str(peer_connection["uid"]) + '"}')
                        except:
                            pass

                        counter = 1
                        for pc_i_call_number in self.pcs:
                            try:
                                if pc_i_call_number != call_number:
                                    pc_i = self.pcs[pc_i_call_number]
                                    channel.send('{"type":"new-client","uid":"' + str(pc_i["uid"]) + '","name":"' + str(
                                        pc_i["name"]) + '","surname":"' + str(pc_i["surname"]) + '"}')
                                    counter += 1
                            except:
                                pass

                        @channel.on("message")
                        async def on_message(message):
                            message = json.loads(message)
                            if message["type"] == "disconnected":
                                await self.stop_peer_connection(peer_connection["uid"])

                    # audio from server to client
                    if self.server_audio_stream_offer == None:
                        self.server_audio_stream_offer = Server_Audio_Stream_Offer(self.speackers_deck_queue)
                    self.pcs[call_number]["pc"].addTrack(self.server_audio_stream_offer)

                    # video from server to client
                    if self.server_video_stream_offer is None:
                        self.server_video_stream_offer = self.create_local_tracks()
                    self.pcs[call_number]["pc"].addTrack(self.server_video_stream_offer)

                    # Attach video from server to QLabel
                    if self.server_video_track is None:
                        self.server_video_track = WebCamera(self.server_video_stream_offer,self.to_emitter)
                    if self.server_video_blackholde is None:
                        self.server_video_blackholde = MediaBlackhole()
                        self.server_video_blackholde.addTrack(self.server_video_track)
                        await self.server_video_blackholde.start()





                    @self.pcs[call_number]["pc"].on("track")
                    async def on_track(track):
                        if track.kind == "audio":
                            self.pcs[call_number]["audio_track"] = track
                            # audio from client (server use)
                            self.pcs[call_number]["audio_track_for_local_use"] = ClientTrack(track, self, self.to_emitter,call_number)
                            self.pcs[call_number]["audio_blackhole"] = MediaBlackhole()
                            self.pcs[call_number]["audio_blackhole"].addTrack(
                                self.pcs[call_number]["audio_track_for_local_use"])
                            await self.pcs[call_number]["audio_blackhole"].start()
                        else:
                            self.pcs[call_number]["video_track"] = track
                            # video from client (server use)
                            self.pcs[call_number]["video_track_for_local_use"] = ClientWebCamera(track, self.to_emitter,
                                                                                                 call_number, self)
                            self.pcs[call_number]["video_blackhole"] = MediaBlackhole()
                            self.pcs[call_number]["video_blackhole"].addTrack(
                                self.pcs[call_number]["video_track_for_local_use"])
                            await self.pcs[call_number]["video_blackhole"].start()

                    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

                    # handle offer
                    await self.pcs[call_number]["pc"].setRemoteDescription(offer)

                    # send answer
                    answer = await self.pcs[call_number]["pc"].createAnswer()
                    await self.pcs[call_number]["pc"].setLocalDescription(answer)

                    # loop = asyncio.get_event_loop()
                    task = asyncio.ensure_future(self.manage_call_end(peer_connection["uid"]))
                    self.pcs[call_number]["manage_call_end_thread"] = task

                    # asyncio.ensure_future(self.statistics(peer_connection["pc"]))
                    return web.Response(content_type="application/json", text=json.dumps(
                        {"sdp": self.pcs[call_number]["pc"].localDescription.sdp,
                         "type": self.pcs[call_number]["pc"].localDescription.type}))
                else:
                    # reject call
                    while not self.ip_calls_queue.empty():
                        self.ip_calls_queue.get()
                    if call_number == 1:
                        self.to_emitter.send({"type": "call-1-status", "status": "closed-by-server"})
                    elif call_number == 2:
                        self.to_emitter.send({"type": "call-2-status", "status": "closed-by-server"})
                    else:
                        self.to_emitter.send({"type": "call-3-status", "status": "closed-by-server"})
                    await self.stop_peer_connection(peer_connection["uid"])
                    return web.Response(content_type="application/json", text=json.dumps({"sdp": "", "type": ""}))
        except:
            error = traceback.format_exc()
            print(error)
            self.to_emitter.send({"type":"error","error_message":error})


    async def stop_peer_connection(self, uid):
        try:
            counter = 0
            for pc_call_number in self.pcs.keys():
                if self.pcs[pc_call_number]["uid"] == uid:
                    call_number = pc_call_number
                    break
            self.to_emitter.send({"type":"stop-peer-connection","call_number":call_number})
            if self.pcs[call_number]["pc"] is None:
                try:
                    self.pcs[call_number]["offer_in_progress"] = False
                    self.pcs[call_number]["call_answered"] = True
                except:
                    pass

                del self.pcs[call_number]
                return None
            if self.pcs[call_number]["is_closed"]:
                return None
            self.pcs[call_number]["is_closed"] = True

            data_from_mother = self.call_queues[call_number - 1]

            if self.pcs[call_number]["stop_in_progress"]:
                return None
            else:
                self.pcs[call_number]["stop_in_progress"] = True
            try:
                if self.pcs[call_number]["pc"] is not None:
                    try:
                        await self.pcs[call_number]["pc"].close()
                        del self.pcs[call_number]["pc"]
                    except Exception as e:
                        pass
                if self.pcs[call_number]["call_answered"] == True:
                    try:
                        self.pcs[call_number]["dc"].close()
                    except:
                        pass
                if self.server_audio_stream_offer is not None:
                    if len(list(self.pcs.keys())) == 1:
                        self.server_audio_stream_offer.stop()
                        self.server_audio_stream_offer.stop_offering()
                        del self.server_audio_stream_offer
                        self.server_audio_stream_offer = None
                try:
                    if self.pcs[call_number]["audio_blackhole"] is not None:
                        await self.pcs[call_number]["audio_blackhole"].stop()
                        self.pcs[call_number]["audio_blackhole"] = None
                        del self.pcs[call_number]["audio_blackhole"]
                except:
                    pass
                try:
                    if self.pcs[call_number]["audio_track_for_local_use"] is not None:
                        del self.pcs[call_number]["audio_track_for_local_use"]
                except:
                    pass

                try:
                    if len(list(self.pcs.keys())) == 1:
                        try:
                            self.webcam.video.stop()
                            self.server_video_track.stop()
                            await self.server_video_blackholde.stop()
                            self.server_video_track = None
                            self.server_video_blackholde = None
                        except:
                            pass
                except:
                    pass
                if call_number == 1:
                    self.to_emitter.send({"type": "call-1-status", "status": "closed-by-client"})
                elif call_number == 2:
                    self.to_emitter.send({"type": "call-2-status", "status": "closed-by-client"})
                else:
                    self.to_emitter.send({"type": "call-3-status", "status": "closed-by-client"})

                try:
                    self.pcs[call_number]["video_track_for_local_use"].stop()
                    await self.pcs[call_number]["video_blackhole"].stop()
                except:
                    pass

                try:
                    del self.pcs[call_number]["video_track_for_local_use"]
                    del self.pcs[call_number]["video_blackhole"]
                except:
                    pass

                try:
                    self.pcs[call_number]["call_answered"] = False
                except:
                    pass

                try:
                    del self.pcs[call_number]["dc"]
                except:
                    pass

                try:
                    self.pcs[call_number]["offer_in_progress"] = False
                    del self.pcs[call_number]["manage_call_end_thread"]
                except:
                    pass
                try:
                    if len(list(self.pcs.keys())) == 1:
                        self.to_emitter.send({"type": "hide_server_web_camera"})
                        self.server_video_stream_offer.stop()
                        self.server_video_stream_offer = None

                    del self.pcs[call_number]["audio_track"]
                    del self.pcs[call_number]["video_track"]
                except:
                    pass
            except Exception as e:
                pass

            while not data_from_mother.empty():
                data_from_mother.get()

            del self.pcs[call_number]
        except:
            error = traceback.format_exc()
            self.to_emitter.send({"type":"error","error_message":error})


    async def manage_call_end(self, uid):
        try:
            for pc_call_number in self.pcs:
                if self.pcs[pc_call_number]["uid"] == uid:
                    call_number = pc_call_number
                    break
            data_from_mother = self.call_queues[call_number - 1]
            # asyncio.set_event_loop(loop)
            try:
                while (self.pcs[call_number]["offer_in_progress"]):
                    #print(await self.pcs[call_number]["pc"].getStats())
                    qsize = data_from_mother.qsize()
                    if qsize == 0:
                        await asyncio.sleep(1)
                    else:
                        data = data_from_mother.get()
                        while not data_from_mother.empty():
                            _ = data_from_mother.get()

                        try:
                            self.pcs[call_number]["dc"].send('{"type":"closing","uid":\"' + str(uid) + '\"}')
                        except:
                            pass
                        await self.stop_peer_connection(uid)
                        break
            except:
                pass
        except:
            error = traceback.format_exc()
            self.to_emitter.send({"type":"error","error_message":error})


    async def on_shutdown(self, app):
        try:
            for pc_call_number in self.pcs:
                await self.stop_peer_connection(self.pcs[pc_call_number]["uid"])
            raise GracefulExit()
        except:
            error = traceback.format_exc()
            self.to_emitter.send({"type":"error","error_message":error})


    async def shutdown_aiohttp(self, request):
        try:
            await self.on_shutdown(self.app)
            return web.Response(content_type="text/html", text="")
        except:
            error = traceback.format_exc()
            self.to_emitter.send({"type":"error","error_message":error})


class Server_Audio_Stream_Offer(MediaStreamTrack):
    kind = "audio"

    def __init__(self, q):
        super().__init__()

        self.speackers_deck_queue = q
        self.q = Simple_Queue()

        self.codec = av.CodecContext.create('pcm_s16le', 'r')
        self.codec.sample_rate = 8000
        self.codec.channels = 2

        self.audio_samples = 0
        self.run = True
        self.mp3_q = AudioSegment.empty()

        # Start packetization in a separate thread for concurrency
        self.packetize_correct_thread = threading.Thread(target=self.packetize_correct)
        self.packetize_correct_thread.daemon = True
        self.packetize_correct_thread.start()

    async def recv(self):
        """Receives audio frames from the queue, decodes, and prepares for sending."""
        try:
            packet = av.Packet(self.q.get())
            frame = self.codec.decode(packet)[0]
            frame.pts = self.audio_samples
            frame.time_base = fractions.Fraction(1, self.codec.sample_rate)
            self.audio_samples += frame.samples
            return frame
        except Exception as e:
            self.run = False  # Stop the offering if we hit an error
            print(f"Error in recv: {e}")
            return None

    def packetize_correct(self):
        """Splits the audio slices into smaller packets suitable for Opus."""
        while self.run:
            try:
                # Get the next slice from the speakers deck queue
                slice_125 = self.speackers_deck_queue.get()["slice"].set_frame_rate(8000)
                slice_full = self.mp3_q + slice_125
                len_slice_full = len(slice_full)
                desired_slice_len = 20  # WebRTC prefers 20ms packets

                # Split the full slice into smaller packets of 20ms duration
                packets = int(len_slice_full / desired_slice_len)
                for i in range(0, packets):
                    self.q.put(slice_full[i * desired_slice_len:(i + 1) * desired_slice_len].raw_data)

                # Remaining data that wasn't fully packetized
                self.mp3_q = slice_full[packets * desired_slice_len:]

            except Exception as e:
                print(f"Error in packetize_correct: {e}")
                self.run = False  # Stop the packetization if we hit an error

    def stop_offering(self):
        """Stop the audio stream offering process."""
        try:
            self.run = False
            self.packetize_correct_thread.join()
        except Exception as e:
            print(f"Error in stop_offering: {e}")


class CameraTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self,to_emitter, device_id=0):
        super().__init__()  # Initialize the base class
        self.cap = cv2.VideoCapture(device_id)
        self.to_emitter = to_emitter
        if not self.cap.isOpened():
            raise ValueError("Could not access the camera.")

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to read frame.")
        # Convert frame to a format compatible with WebRTC (YUV420P)
        # This may require additional processing
        # Convert the frame from BGR (OpenCV default) to RGB (pyav format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a pyav video frame
        video_frame = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')
        pil_image = video_frame.to_image()
        self.to_emitter.send({"type": "server-web-camera-frame", "pil_image": [pil_image]})
        return video_frame

    def convert_bgr_to_yuv420p(frame_bgr):
        # First, convert BGR (OpenCV format) to YUV (standard format)
        frame_yuv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2YUV_I420)
        return frame_yuv

    def stop(self):
        self.cap.release()

class WebCamera(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, to_emitter):
        super().__init__()  # don't forget this!
        self.track = track
        self.to_emitter = to_emitter

    async def recv(self):
        frame = await self.track.recv()
        pil_image = frame.to_image()
        self.to_emitter.send({"type": "server-web-camera-frame", "pil_image": [pil_image]})
        return None


class ClientWebCamera(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, to_emitter, call_number, parent_self):
        super().__init__()  # don't forget this!
        self.track = track
        self.to_emitter = to_emitter
        self.call_number = call_number
        self.parent_self = parent_self

    async def recv(self):
        try:
            frame = await self.track.recv()
            pil_image = frame.to_image()
            if self.call_number == 1:
                self.to_emitter.send({"type": "client-1-web-camera-frame", "pil_image": [pil_image]})
            elif self.call_number == 2:
                self.to_emitter.send({"type": "client-2-web-camera-frame", "pil_image": [pil_image]})
            else:
                self.to_emitter.send({"type": "client-3-web-camera-frame", "pil_image": [pil_image]})
            return None
        except:
            raise MediaStreamError


class ClientTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self, track, parent_self, to_emitter,call_number):
        super().__init__()
        self.track = track
        self.parent_self = parent_self
        self.to_emitter = to_emitter
        self.call_number = call_number

    async def recv(self):
        try:
            frame = await self.track.recv()
            packet_bytes = frame.planes[0].to_bytes()  # Direct access to plane bytes to avoid ndarray conversion
            self.to_emitter.send({"type": "ip-call-packet", "call-number": self.call_number, "frame": [packet_bytes]})
        except MediaStreamError:
            raise

    '''
    async def recv(self):
        # Get a new PyAV frame
        try:
            frame = await self.track.recv()
            packet_bytes = frame.to_ndarray().tobytes()
            self.to_emitter.send({"type":"ip-call-packet","call-number":self.call_number,"frame":[packet_bytes]})
        except:
            raise MediaStreamError
            return None
    '''