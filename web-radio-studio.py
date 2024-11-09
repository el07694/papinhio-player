import traceback
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
#sys.coinit_flags = 0
import os
import importlib
from multiprocessing import freeze_support, Queue
import pyuac
import subprocess

import threading
from multiprocessing import Condition, Value, Process, Event

sys.path.append("src")
sys.path.append("src/python+/")
sys.path.append("src/compiled-ui/")
sys.path.append("src/python+/main-window")
sys.path.append("src/python+/main-window/ngrok.exe")

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append('../../compiled-ui/')
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")

### import main ui class ###
web_radio_studio_ui = importlib.import_module("compiled-ui.main-window.web-radio-studio")

### import database functions ###
database_functions = importlib.import_module("python+.lib.sqlite3-functions")

### import manage processes class ###
manage_processes_class = importlib.import_module("python+.main-window.manage-procceses")

### ip call 1 ###
ip_call_1_class = importlib.import_module("python+.menu-1.ip-calls.ip-call-1")

### ip call 2 ###
ip_call_2_class = importlib.import_module("python+.menu-1.ip-calls.ip-call-2")

### ip call 3 ###
ip_call_3_class = importlib.import_module("python+.menu-1.ip-calls.ip-call-3")


### deck 1 ###
deck_1_class = importlib.import_module("python+.main-window.deck-1")

### deck 2 ###
deck_2_class = importlib.import_module("python+.main-window.deck-2")

### music clip deck ###
music_clip_deck_class = importlib.import_module("python+.main-window.music-clip-deck")

### speackers deck ###
speackers_deck_class = importlib.import_module("python+.main-window.speackers-deck")

### speackers deck secondary ###
speackers_deck_secondary_class = importlib.import_module("python+.menu-1.ip-calls.speackers-deck-secondary")

### final slice ###
final_slice_class = importlib.import_module("python+.main-window.final-slice")

### aiortc ###
ip_calls_class = importlib.import_module("python+.menu-1.ip-calls.ip-calls")

# secondary slice class
secondary_slice_class = importlib.import_module("python+.menu-1.ip-calls.secondary-slice")

### information frame ###
information_frame_class = importlib.import_module("python+.main-window.information-frame")

### final slice plot ###
final_slice_plot_class = importlib.import_module("python+.main-window.final-slice-plot")

### final slice pyaudio ###
final_slice_pyaudio_class = importlib.import_module("python+.main-window.final-slice-pyaudio")

### secondary slice pyaudio ###
secondary_slice_pyaudio_class = importlib.import_module("python+.menu-1.ip-calls.secondary-slice-pyaudio")

### record_deck ###
record_deck_class = importlib.import_module("python+.main-window.record-deck")

### ip calls record_deck ###
ip_calls_record_deck_class = importlib.import_module("python+.menu-1.ip-calls.record-deck")


### make the stackedwidget movable! ###
stacked_widget_class = importlib.import_module("python+.main-window.stacked-widget")

### player list ###
player_list_class = importlib.import_module("python+.main-window.page-4.player-list")

class Web_Radio_Studio:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        #self.MainWindow.EXIT_CODE_REBOOT = -123456789
        self.ui = web_radio_studio_ui.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()

        # manage_processes_class
        self.manage_processes_instance = manage_processes_class.Manage_Processes(self)

        # make the stacked widget movable
        self.stacked_widget_instance = stacked_widget_class.Stacked_Widget(self)

        # apply theme settings
        self.apply_theme_settings()

        # boolean declaration for window states
        self.window_states()

        # main-menu actions triggers
        self.link_menus()

        # synchronize primary processes
        self.condition = Condition()
        self.frame = Value('q', lock=False)
        self.quit_event = Event()
        self.tr = threading.Thread(target=self.infinite_heartbreat)
        self.tr.start()

        # deck 1 manage
        self.deck_1_instance = deck_1_class.Deck_1(self)

        # deck 2 manage
        self.deck_2_instance = deck_2_class.Deck_2(self)

        # music clip deck manage
        self.music_clip_deck_instance = music_clip_deck_class.Music_Clip_Deck(self)

        # speackers deck
        self.speackers_deck_instance = speackers_deck_class.Speackers_Deck(self)

        # speackers deck secondary
        self.speackers_deck_secondary_instance = speackers_deck_secondary_class.Speackers_Deck_Secondary(self)

        # final slice
        self.final_slice_instance = final_slice_class.Final_Slice(self)

        # ip call 1
        self.ip_call_1_instance = ip_call_1_class.Ip_Call_1(self)

        # ip call 2
        self.ip_call_2_instance = ip_call_2_class.Ip_Call_2(self)

        # ip call 3
        self.ip_call_3_instance = ip_call_3_class.Ip_Call_3(self)

        # ip calls (aiortc)
        self.ip_calls_instance = ip_calls_class.Ip_Calls(self)

        # secondary slice
        self.secondary_slice_instance = secondary_slice_class.Secondary_Slice(self)

        # information frame
        self.information_frame_instance = information_frame_class.Information_Frame(self)

        # final slice plot
        self.final_slice_plot_instance = final_slice_plot_class.Final_Slice_Plot(self)

        # final slice pyaudio
        self.final_slice_pyaudio_instance = final_slice_pyaudio_class.Final_Slice_PyAudio(self)

        # secondary slice pyaudio
        self.secondary_slice_pyaudio_instance = secondary_slice_pyaudio_class.Secondary_Slice_PyAudio(self)

        # record deck
        self.record_deck_instance = record_deck_class.Record_Deck(self)

        # ip calls record deck
        self.ip_calls_record_deck_instance = ip_calls_record_deck_class.Record_Deck(self)

        # player list
        self.player_list_instance = player_list_class.Player_List(self)

        # close action
        self.MainWindow.closeEvent = lambda event: self.closeEvent(event)

        sys.exit(self.app.exec())

    #synchronize primary processes
    def infinite_heartbreat(self):
        next_beat = time.time()
        while True:
            next_beat += 0.125
            time_to_sleep = next_beat - time.time()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            with self.condition:
                self.frame.value += 1
                self.condition.notify_all()
                if self.quit_event.is_set():
                    return

    def apply_theme_settings(self):
        self.default_font = database_functions.read_setting("default_font")["value"]
        self.default_font_size = database_functions.read_setting("default_font_size")["value"]
        self.default_font_color = database_functions.read_setting("default_font_color")["value"]
        self.default_background_color = database_functions.read_setting("default_background_color")["value"]
        self.default_buttons_background = database_functions.read_setting("default_button_background")["value"]
        self.default_buttons_font_color = database_functions.read_setting("default_button_font_color")["value"]
        self.default_style = database_functions.read_setting("default_style")["value"]
        self.default_custome_theme = database_functions.read_setting("default_custome_theme")["value"]

        self.app.setStyle(self.default_style)
        self.MainWindow.setStyleSheet("*{font-family:"+self.default_font+";font-size:"+self.default_font_size+"px;color:"+self.default_font_color+";}QMainWindow{background:"+self.default_background_color+"}QPushButton, QComboBox{background:"+self.default_buttons_background+";color:"+self.default_buttons_font_color+"}")

    def window_states(self):
        ### menu-1 ###

        ### manage input and output devices ###

        ### microphone-input-device-settings ###
        self.manage_input_device_error_window_is_open = False
        self.manage_input_device_window_is_open = False
        self.manage_input_device_save_question_window_is_open = False

        ### camera-input-device-settings ###
        self.manage_camera_input_device_error_window_is_open = False
        self.manage_camera_input_device_window_is_open = False
        self.manage_camera_input_device_save_question_window_is_open = False

        ### sound-output-devices-settings ###
        self.manage_output_device_error_window_is_open = False
        self.manage_output_device_save_question_window_is_open = False
        self.manage_output_device_window_is_open = False

        ### manage-procceses ###
        self.manage_proccesses_error_window_is_open = False
        self.manage_proccesses_window_is_open = False

        ### speackers deck error window
        self.manage_speackers_deck_error_window_is_open = False

        ### speackers deck secondary error window
        self.manage_speackers_deck_secondary_error_window_is_open = False

        ### music clip deck error window
        self.manage_music_clip_deck_error_window_is_open = False

        ### deck 1 error window
        self.manage_deck_1_error_window_is_open = False

        ### deck 1 web error window
        self.manage_deck_1_web_error_window_is_open = False

        ### deck 2 error window
        self.manage_deck_2_error_window_is_open = False

        ### deck 2 web error window
        self.manage_deck_2_web_error_window_is_open = False

        # final slice error window
        self.final_slice_error_window_is_open = False

        # player list error window
        self.player_list_error_window_is_open = False

        # empty player list error window
        self.player_list_empty_error_window_is_open = False

        # player list delete all window
        self.player_list_delete_all_window_is_open = False

        # player list delete one window
        self.player_list_delete_one_window_is_open = False

        # secondary slice error window
        self.secondary_slice_error_window_is_open = False

        # record deck error window
        self.record_deck_error_window_is_open = False

        # ip calls record error window
        self.ip_calls_record_deck_error_window_is_open = False

        # record deck filename error window
        self.record_deck_filename_error_window_is_open = False

        # start record error window
        self.record_start_error_window_is_open = False

        # record filename error window
        self.record_filename_error_window_is_open = False

        # record select filename window
        self.record_select_filename_window_is_open = False

        # information frame error window
        self.information_frame_error_window_is_open = False

        # final slice plot error window
        self.final_slice_plot_error_window_is_open = False

        # final slice pyaudio error window
        self.final_slice_pyaudio_error_window_is_open = False

        # ip calls error window
        self.ip_calls_error_window_is_open = False

        # ip calls offering window
        self.ip_call_offering_window_is_open = False

    def link_menus(self):
        ### menu-1 ###

        ### manage input and output devices ###
        self.ui.menu_manage_output_devices.triggered.connect(lambda action: self.open_manage_output_device_window())
        self.ui.action_manage_output_devices.triggered.connect(lambda action: self.open_manage_output_device_window())
        self.ui.menu_manage_input_device.triggered.connect(lambda action: self.open_manage_input_device_window())
        self.ui.action_manage_input_device.triggered.connect(lambda action: self.open_manage_input_device_window())
        self.ui.menu_select_camera.triggered.connect(lambda action: self.open_manage_camera_input_device_window())
        self.ui.action_select_camera.triggered.connect(lambda action: self.open_manage_camera_input_device_window())

        ### menu-3 ###
        self.ui.menu_record_start.triggered.connect(lambda action:self.open_record_select_filename_window())
        self.ui.action_start_record.triggered.connect(lambda action:self.action_start_record_clicked())


    def action_start_record_clicked(self):
        if self.record_deck_instance.deck_status == "paused":
            self.record_deck_instance.start_clicked()
        else:
            self.open_record_select_filename_window()

    ### manage-input-and-output-sound-devices ###

    ### microphone-input-device-settings ###
    def open_manage_input_device_error_window(self, error_message):  # to be fixed
        variables = dir(self)
        if "manage_input_device_error_ui" not in variables:
            self.manage_input_device_error_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.error")
            self.manage_input_device_error_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.error")
        if self.manage_input_device_error_window_is_open == False:
            if self.manage_input_device_save_question_window_is_open == True:
                self.manage_input_device_error_window = CustomQDialog(self,True,
                                                                      self.manage_input_device_save_question_window,
                                                                      QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            if self.manage_input_device_window_is_open == True:
                self.manage_input_device_error_window = CustomQDialog(self,True, self.manage_input_device_window,
                                                                      QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            else:
                self.manage_input_device_error_window = CustomQDialog(self,True, self.MainWindow,
                                                                      QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

            self.ui_manage_input_device_error_window = self.manage_input_device_error_ui.Ui_Dialog()
            self.ui_manage_input_device_error_window.setupUi(self.manage_input_device_error_window)
            self.manage_input_device_error_window_is_open = True
            self.manage_input_device_error_window_support_code = self.manage_input_device_error_support_ui.Support_Ui_Dialog(
                self, error_message)
            self.manage_input_device_error_window.exec()


    def open_manage_input_device_window(self):
        variables = dir(self)
        if "manage_input_device_ui" not in variables:
            self.manage_input_device_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.microphone-input-device-setting")
            self.manage_input_device_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.microphone-input-device-setting")
        if self.manage_input_device_window_is_open == False:
            self.manage_input_device_window = CustomQDialog(self,True,self.MainWindow,
                                                            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            self.ui_manage_input_device_window = self.manage_input_device_ui.Ui_Dialog()
            self.ui_manage_input_device_window.setupUi(self.manage_input_device_window)
            self.manage_input_device_window_is_open = True
            self.manage_input_device_window_support_code = self.manage_input_device_support_ui.Support_Ui_Dialog(self)
            self.manage_input_device_window.exec()

    def open_manage_input_device_save_question_window(self):
        variables = dir(self)
        if "manage_input_device_save_question_ui" not in variables:
            self.manage_input_device_save_question_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.save-question")
            self.manage_input_device_save_question_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.save-question")
        if self.manage_input_device_save_question_window_is_open == False:
            self.manage_input_device_save_question_window = CustomQDialog(self,False, self.MainWindow,
                                                                          QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            self.ui_manage_input_device_save_question_window = self.manage_input_device_save_question_ui.Ui_Dialog()
            self.ui_manage_input_device_save_question_window.setupUi(self.manage_input_device_save_question_window)
            self.manage_input_device_save_question_window_is_open = True
            self.manage_input_device_save_question_window_support_code = self.manage_input_device_save_question_support_ui.Support_Ui_Dialog(
                self)
            self.manage_input_device_save_question_window.exec()


    ### camera-input-device-settings ###
    def open_manage_camera_input_device_error_window(self, error_message):  # to be fixed
        variables = dir(self)
        if "manage_camera_input_device_error_ui" not in variables:
            self.manage_camera_input_device_error_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.camera-input-device-settings.error")
            self.manage_camera_input_device_error_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.camera-input-device-settings.error")
        if self.manage_camera_input_device_error_window_is_open == False:
            if self.manage_camera_input_device_save_question_window_is_open == True:
                self.manage_camera_input_device_error_window = CustomQDialog(self,True,
                                                                      self.manage_camera_input_device_save_question_window,
                                                                      QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            if self.manage_camera_input_device_window_is_open == True:
                self.manage_camera_input_device_error_window = CustomQDialog(self,True, self.manage_camera_input_device_window,
                                                                      QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            else:
                self.manage_camera_input_device_error_window = CustomQDialog(self,True, self.MainWindow,
                                                                      QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

            self.ui_manage_camera_input_device_error_window = self.manage_camera_input_device_error_ui.Ui_Dialog()
            self.ui_manage_camera_input_device_error_window.setupUi(self.manage_camera_input_device_error_window)
            self.manage_camera_input_device_error_window_is_open = True
            self.manage_camera_input_device_error_window_support_code = self.manage_camera_input_device_error_support_ui.Support_Ui_Dialog(
                self, error_message)
            self.manage_camera_input_device_error_window.exec()


    def open_manage_camera_input_device_window(self):
        variables = dir(self)
        if "manage_camera_input_device_ui" not in variables:
            self.manage_camera_input_device_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.camera-input-device-settings.camera-input-device-setting")
            self.manage_camera_input_device_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.camera-input-device-settings.camera-input-device-setting")
        if self.manage_camera_input_device_window_is_open == False:
            self.manage_camera_input_device_window = CustomQDialog(self,True,self.MainWindow,
                                                            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            self.ui_manage_camera_input_device_window = self.manage_camera_input_device_ui.Ui_Dialog()
            self.ui_manage_camera_input_device_window.setupUi(self.manage_camera_input_device_window)
            self.manage_camera_input_device_window_is_open = True
            self.manage_camera_input_device_window_support_code = self.manage_camera_input_device_support_ui.Support_Ui_Dialog(self)
            self.manage_camera_input_device_window.exec()

    def open_manage_camera_input_device_save_question_window(self):
        variables = dir(self)
        if "manage_camera_input_device_save_question_ui" not in variables:
            self.manage_camera_input_device_save_question_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.camera-input-device-settings.save-question")
            self.manage_camera_input_device_save_question_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.camera-input-device-settings.save-question")
        if self.manage_camera_input_device_save_question_window_is_open == False:
            self.manage_camera_input_device_save_question_window = CustomQDialog(self,False, self.MainWindow,
                                                                          QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            self.ui_manage_camera_input_device_save_question_window = self.manage_camera_input_device_save_question_ui.Ui_Dialog()
            self.ui_manage_camera_input_device_save_question_window.setupUi(self.manage_camera_input_device_save_question_window)
            self.manage_camera_input_device_save_question_window_is_open = True
            self.manage_camera_input_device_save_question_window_support_code = self.manage_camera_input_device_save_question_support_ui.Support_Ui_Dialog(
                self)
            self.manage_camera_input_device_save_question_window.exec()


    ### sound-output-devices-settings ###
    def open_manage_output_device_error_window(self, error_message):  # to be fixed
        variables = dir(self)
        if "manage_output_device_error_ui" not in variables:
            self.manage_output_device_error_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.error")
            self.manage_output_device_error_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.error")
        if self.manage_output_device_error_window_is_open == False:
            if self.manage_output_device_save_question_window_is_open == True:
                self.manage_output_device_error_window = CustomQDialog(self,True,
                                                                       self.manage_output_device_save_question_window,
                                                                       QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            if self.manage_output_device_window_is_open == True:
                self.manage_output_device_error_window = CustomQDialog(self,True, self.manage_output_device_window,
                                                                       QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            else:
                self.manage_output_device_error_window = CustomQDialog(self,True, self.MainWindow,
                                                                       QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

            self.ui_manage_output_device_error_window = self.manage_output_device_error_ui.Ui_Dialog()
            self.ui_manage_output_device_error_window.setupUi(self.manage_output_device_error_window)
            self.manage_output_device_error_window_is_open = True
            self.manage_output_device_error_window_support_code = self.manage_output_device_error_support_ui.Support_Ui_Dialog(
                self, error_message)
            self.manage_output_device_error_window.exec()

    def open_manage_output_device_save_question_window(self):
        variables = dir(self)
        if "manage_output_device_save_question_ui" not in variables:
            self.manage_output_device_save_question_ui = importlib.import_module(
                "compiled-ui.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.save-question")
            self.manage_output_device_save_question_support_ui = importlib.import_module(
                "python+.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.save-question")
        if self.manage_output_device_save_question_window_is_open == False:
            self.manage_output_device_save_question_window = CustomQDialog(self,False,self.MainWindow,
                                                                           QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            self.ui_manage_output_device_save_question_window = self.manage_output_device_save_question_ui.Ui_Dialog()
            self.ui_manage_output_device_save_question_window.setupUi(self.manage_output_device_save_question_window)
            self.manage_output_device_save_question_window_is_open = True
            self.manage_output_device_save_question_window_support_code = self.manage_output_device_save_question_support_ui.Support_Ui_Dialog(
                self)
            self.manage_output_device_save_question_window.exec()

    def open_manage_output_device_window(self):
        try:
            variables = dir(self)
            if "manage_output_device_ui" not in variables:
                self.manage_output_device_ui = importlib.import_module(
                    "compiled-ui.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.sound-output-devices-settings")
                self.manage_output_device_support_ui = importlib.import_module(
                    "python+.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.sound-output-devices-settings")
            if self.manage_output_device_window_is_open == False:
                self.manage_output_device_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_output_device_window = self.manage_output_device_ui.Ui_Dialog()
                self.ui_manage_output_device_window.setupUi(self.manage_output_device_window)
                self.manage_output_device_window_is_open = True
                self.manage_output_device_window_support_code = self.manage_output_device_support_ui.Support_Ui_Dialog(self)
                self.manage_output_device_window.exec()
        except:
            print(traceback.format_exc())

    # speackers deck error window
    def open_speackers_deck_error_window(self,error_message):
        try:
            variables = dir(self)
            if "manage_speackers_deck_error_ui" not in variables:
                self.manage_speackers_deck_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.speackers-slice-error")
                self.manage_speackers_deck_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.speackers-slice-error")
            if self.manage_speackers_deck_error_window_is_open == False:
                self.manage_speackers_deck_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_speackers_deck_error_window = self.manage_speackers_deck_error_ui.Ui_Dialog()
                self.ui_manage_speackers_deck_error_window.setupUi(self.manage_speackers_deck_error_window)
                self.manage_speackers_deck_error_window_is_open = True
                self.manage_speackers_deck_error_window_support_code = self.manage_speackers_deck_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.manage_speackers_deck_error_window.exec()
        except:
            print(traceback.format_exc())

    # speackers deck error window
    def open_speackers_deck_secondary_error_window(self,error_message):
        try:
            variables = dir(self)
            if "manage_speackers_deck_secondary_error_ui" not in variables:
                self.manage_speackers_deck_secondary_error_ui = importlib.import_module("compiled-ui.menu-1.ip-calls.speackers-slice-error")
                self.manage_speackers_deck_secondary_error_support_ui = importlib.import_module("python+.menu-1.ip-calls.speackers-slice-error")
            if self.manage_speackers_deck_secondary_error_window_is_open == False:
                self.manage_speackers_deck_secondary_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_speackers_deck_secondary_error_window = self.manage_speackers_deck_secondary_error_ui.Ui_Dialog()
                self.ui_manage_speackers_deck_secondary_error_window.setupUi(self.manage_speackers_deck_secondary_error_window)
                self.manage_speackers_deck_secondary_error_window_is_open = True
                self.manage_speackers_deck_secondary_error_window_support_code = self.manage_speackers_deck_secondary_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.manage_speackers_deck_secondary_error_window.exec()
        except:
            print(traceback.format_exc())

    # music clip deck error window
    def open_music_clip_deck_error_window(self,error_message):
        try:
            variables = dir(self)
            if "manage_music_clip_deck_error_ui" not in variables:
                self.manage_music_clip_deck_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.music-clip-deck-slice-error")
                self.manage_music_clip_deck_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.music-clip-deck-slice-error")
            if self.manage_music_clip_deck_error_window_is_open == False:
                self.manage_music_clip_deck_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_music_clip_deck_error_window = self.manage_music_clip_deck_error_ui.Ui_Dialog()
                self.ui_manage_music_clip_deck_error_window.setupUi(self.manage_music_clip_deck_error_window)
                self.manage_music_clip_deck_error_window_is_open = True
                self.manage_music_clip_deck_error_window_support_code = self.manage_music_clip_deck_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.manage_music_clip_deck_error_window.exec()
        except:
            print(traceback.format_exc())

    # deck 1 error window
    def open_deck_1_error_window(self,error_message):
        try:
            variables = dir(self)
            if "manage_deck_1_error_ui" not in variables:
                self.manage_deck_1_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.deck-1-slice-error")
                self.manage_deck_1_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.deck-1-slice-error")
            if self.manage_deck_1_error_window_is_open == False:
                self.manage_deck_1_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_deck_1_error_window = self.manage_deck_1_error_ui.Ui_Dialog()
                self.ui_manage_deck_1_error_window.setupUi(self.manage_deck_1_error_window)
                self.manage_deck_1_error_window_is_open = True
                self.manage_deck_1_error_window_support_code = self.manage_deck_1_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.manage_deck_1_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_deck_1_web_error_window(self,tmp_item):
        try:
            variables = dir(self)
            if "manage_deck_1_web_error_ui" not in variables:
                self.manage_deck_1_web_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.deck-1-web-error")
                self.manage_deck_1_web_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.deck-1-web-error")
            if self.manage_deck_1_web_error_window_is_open == False:
                self.manage_deck_1_web_error_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_deck_1_web_error_window = self.manage_deck_1_web_error_ui.Ui_Dialog()
                self.ui_manage_deck_1_web_error_window.setupUi(self.manage_deck_1_web_error_window)
                self.manage_deck_1_web_error_window_is_open = True
                self.manage_deck_1_web_error_window_support_code = self.manage_deck_1_web_error_support_ui.Support_Ui_Dialog(self,tmp_item)
                self.manage_deck_1_web_error_window.exec()
        except:
            print(traceback.format_exc())

    # deck 2 error window
    def open_deck_2_error_window(self,error_message):
        try:
            variables = dir(self)
            if "manage_deck_2_error_ui" not in variables:
                self.manage_deck_2_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.deck-2-slice-error")
                self.manage_deck_2_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.deck-2-slice-error")
            if self.manage_deck_2_error_window_is_open == False:
                self.manage_deck_2_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_deck_2_error_window = self.manage_deck_2_error_ui.Ui_Dialog()
                self.ui_manage_deck_2_error_window.setupUi(self.manage_deck_2_error_window)
                self.manage_deck_2_error_window_is_open = True
                self.manage_deck_2_error_window_support_code = self.manage_deck_2_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.manage_deck_2_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_deck_2_web_error_window(self,tmp_item):
        try:
            variables = dir(self)
            if "manage_deck_2_web_error_ui" not in variables:
                self.manage_deck_2_web_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.deck-2-web-error")
                self.manage_deck_2_web_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.deck-2-web-error")
            if self.manage_deck_2_web_error_window_is_open == False:
                self.manage_deck_2_web_error_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_manage_deck_2_web_error_window = self.manage_deck_2_web_error_ui.Ui_Dialog()
                self.ui_manage_deck_2_web_error_window.setupUi(self.manage_deck_2_web_error_window)
                self.manage_deck_2_web_error_window_is_open = True
                self.manage_deck_2_web_error_window_support_code = self.manage_deck_2_web_error_support_ui.Support_Ui_Dialog(self,tmp_item)
                self.manage_deck_2_web_error_window.exec()
        except:
            print(traceback.format_exc())



    #final slice error window
    def open_final_slice_error_window(self,error_message):
        try:
            variables = dir(self)
            if "final_slice_error_ui" not in variables:
                self.final_slice_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.final-slice-error")
                self.final_slice_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.final-slice-error")
            if self.final_slice_error_window_is_open == False:
                self.final_slice_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_final_slice_error_window = self.final_slice_error_ui.Ui_Dialog()
                self.ui_final_slice_error_window.setupUi(self.final_slice_error_window)
                self.final_slice_error_window_is_open = True
                self.final_slice_error_window_support_code = self.final_slice_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.final_slice_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_player_list_error_window(self,error_message):
        try:
            variables = dir(self)
            if "player_list_error_ui" not in variables:
                self.player_list_error_ui = importlib.import_module("compiled-ui.main-window.page-4.player-list-error")
                self.player_list_error_support_ui = importlib.import_module("python+.main-window.page-4.player-list-error")
            if self.player_list_error_window_is_open == False:
                self.player_list_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_player_list_error_window = self.player_list_error_ui.Ui_Dialog()
                self.ui_player_list_error_window.setupUi(self.player_list_error_window)
                self.player_list_error_window_is_open = True
                self.player_list_error_window_support_code = self.player_list_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.player_list_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_player_list_empty_error_window(self):
        try:
            variables = dir(self)
            if "player_list_empty_error_ui" not in variables:
                self.player_list_empty_error_ui = importlib.import_module("compiled-ui.main-window.page-4.empty-player-list")
                self.player_list_empty_error_support_ui = importlib.import_module("python+.main-window.page-4.empty-player-list")
            if self.player_list_empty_error_window_is_open == False:
                self.player_list_empty_error_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_player_list_empty_error_window = self.player_list_empty_error_ui.Ui_Dialog()
                self.ui_player_list_empty_error_window.setupUi(self.player_list_empty_error_window)
                self.player_list_empty_error_window_is_open = True
                self.player_list_empty_error_window_support_code = self.player_list_empty_error_support_ui.Support_Ui_Dialog(self)
                self.player_list_empty_error_window.exec()
        except:
            print(traceback.format_exc())


    def open_player_list_delete_all_window(self):
        try:
            variables = dir(self)
            if "player_list_delete_all_ui" not in variables:
                self.player_list_delete_all_ui = importlib.import_module("compiled-ui.main-window.page-4.delete-all")
                self.player_list_delete_all_support_ui = importlib.import_module("python+.main-window.page-4.delete-all")
            if self.player_list_delete_all_window_is_open == False:
                self.player_list_delete_all_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_player_list_delete_all_window = self.player_list_delete_all_ui.Ui_Dialog()
                self.ui_player_list_delete_all_window.setupUi(self.player_list_delete_all_window)
                self.player_list_delete_all_window_is_open = True
                self.player_list_delete_all_window_support_code = self.player_list_delete_all_support_ui.Support_Ui_Dialog(self)
                self.player_list_delete_all_window.exec()
        except:
            print(traceback.format_exc())

    def open_player_list_delete_one_window(self,player_list_item,edit=False):
        try:
            variables = dir(self)
            if "player_list_delete_one_ui" not in variables:
                self.player_list_delete_one_ui = importlib.import_module("compiled-ui.main-window.page-4.delete-one")
                self.player_list_delete_one_support_ui = importlib.import_module("python+.main-window.page-4.delete-one")
            if self.player_list_delete_one_window_is_open == False:
                self.player_list_delete_one_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_player_list_delete_one_window = self.player_list_delete_one_ui.Ui_Dialog()
                self.ui_player_list_delete_one_window.setupUi(self.player_list_delete_one_window)
                self.player_list_delete_one_window_is_open = True
                self.player_list_delete_one_window_support_code = self.player_list_delete_one_support_ui.Support_Ui_Dialog(self,player_list_item)
                self.player_list_delete_one_window.exec()
        except:
            print(traceback.format_exc())


    # final slice error window
    def open_ip_calls_error_window(self, error_message):
        try:
            variables = dir(self)
            if "ip_calls_error_ui" not in variables:
                self.ip_calls_error_ui = importlib.import_module(
                    "compiled-ui.menu-1.ip-calls.aiortc-error")
                self.ip_calls_error_support_ui = importlib.import_module(
                    "python+.menu-1.ip-calls.aiortc-error")
            if self.ip_calls_error_window_is_open == False:
                self.ip_calls_error_window = CustomQDialog(self, True, self.MainWindow,
                                                              QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_ip_calls_error_window = self.ip_calls_error_ui.Ui_Dialog()
                self.ui_ip_calls_error_window.setupUi(self.ip_calls_error_window)
                self.ip_calls_error_window_is_open = True
                self.ip_calls_error_window_support_code = self.ip_calls_error_support_ui.Support_Ui_Dialog(
                    self, error_message)
                self.ip_calls_error_window.exec()
        except:
            print(traceback.format_exc())


    #secondary slice error window
    def open_secondary_slice_error_window(self,error_message):
        try:
            variables = dir(self)
            if "secondary_slice_error_ui" not in variables:
                self.secondary_slice_error_ui = importlib.import_module("compiled-ui.menu-1.ip-calls.secondary-slice-error")
                self.secondary_slice_error_support_ui = importlib.import_module("python+.menu-1.ip-calls.secondary-slice-error")
            if self.secondary_slice_error_window_is_open == False:
                self.secondary_slice_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_secondary_slice_error_window = self.secondary_slice_error_ui.Ui_Dialog()
                self.ui_secondary_slice_error_window.setupUi(self.secondary_slice_error_window)
                self.secondary_slice_error_window_is_open = True
                self.secondary_slice_error_window_support_code = self.secondary_slice_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.secondary_slice_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_record_deck_error_window(self, error_message):
        try:
            variables = dir(self)
            if "record_deck_error_ui" not in variables:
                self.record_deck_error_ui = importlib.import_module(
                    "compiled-ui.main-window.helpfull-windows.record-deck-error")
                self.record_deck_error_support_ui = importlib.import_module(
                    "python+.main-window.helpfull-windows.record-deck-error")
            if self.record_deck_error_window_is_open == False:
                self.record_deck_error_window = CustomQDialog(self, True, self.MainWindow,
                                                              QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_record_deck_error_window = self.record_deck_error_ui.Ui_Dialog()
                self.ui_record_deck_error_window.setupUi(self.record_deck_error_window)
                self.record_deck_error_window_is_open = True
                self.record_deck_error_window_support_code = self.record_deck_error_support_ui.Support_Ui_Dialog(self,
                                                                                                                 error_message)
                self.record_deck_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_ip_calls_record_deck_error_window(self,error_message):
        try:
            variables = dir(self)
            if "ip_calls_record_deck_error_ui" not in variables:
                self.ip_calls_record_deck_error_ui = importlib.import_module("compiled-ui.menu-1.ip-calls.record-deck-error")
                self.ip_calls_record_deck_error_support_ui = importlib.import_module("python+.menu-1.ip-calls.record-deck-error")
            if self.ip_calls_record_deck_error_window_is_open == False:
                self.ip_calls_record_deck_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_ip_calls_record_deck_error_window = self.ip_calls_record_deck_error_ui.Ui_Dialog()
                self.ui_ip_calls_record_deck_error_window.setupUi(self.ip_calls_record_deck_error_window)
                self.ip_calls_record_deck_error_window_is_open = True
                self.ip_calls_record_deck_error_window_support_code = self.ip_calls_record_deck_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.ip_calls_record_deck_error_window.exec()
        except:
            print(traceback.format_exc())

    ### microphone-input-device-settings ###
    def open_record_start_errow_window(self, error_message):  # to be fixed
        try:
            print("Open")
            variables = dir(self)
            if "record_start_error_ui" not in variables:
                self.record_start_error_ui = importlib.import_module(
                    "compiled-ui.menu-3.error")
                self.record_start_error_support_ui = importlib.import_module(
                    "python+.menu-3.error")
            if self.record_start_error_window_is_open == False:
                if self.record_filename_error_window_is_open == True:
                    self.record_start_error_window = CustomQDialog(self,True,
                                                                          self.record_filename_error_window,
                                                                          QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                if self.record_select_filename_window_is_open == True:
                    self.record_start_error_window = CustomQDialog(self,True, self.record_select_filename_window,
                                                                          QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                else:
                    self.record_start_error_window = CustomQDialog(self,True, self.MainWindow,
                                                                          QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

                self.ui_record_start_error_window = self.record_start_error_ui.Ui_Dialog()
                self.ui_record_start_error_window.setupUi(self.record_start_error_window)
                self.record_start_error_window_is_open = True
                self.record_start_error_window_support_code = self.record_start_error_support_ui.Support_Ui_Dialog(
                    self, error_message)
                print("Opening error window")
                self.record_start_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_record_deck_filename_error_window(self,filename):
        try:
            variables = dir(self)
            if "record_deck_filename_error_ui" not in variables:
                self.record_deck_filename_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.record-deck-filename-error")
                self.record_deck_filename_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.record-deck-filename-error")
            if self.record_deck_filename_error_window_is_open == False:
                self.record_deck_filename_error_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_record_deck_filename_error_window = self.record_deck_filename_error_ui.Ui_Dialog()
                self.ui_record_deck_filename_error_window.setupUi(self.record_deck_filename_error_window)
                self.record_deck_filename_error_window_is_open = True
                self.record_deck_filename_error_window_support_code = self.record_deck_filename_error_support_ui.Support_Ui_Dialog(self,filename)
                self.record_deck_filename_error_window.exec()
        except:
            print(traceback.format_exc())

    def open_record_select_filename_window(self):
        try:
            if self.record_deck_instance.deck_status == "paused":
                self.record_deck_instance.start_clicked()
                return None
            variables = dir(self)
            if "record_select_filename_ui" not in variables:
                self.record_select_filename_ui = importlib.import_module("compiled-ui.menu-3.start-record")
                self.record_select_filename_support_ui = importlib.import_module("python+.menu-3.start-record")
            if self.record_select_filename_window_is_open == False:
                self.record_select_filename_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_record_select_filename_window = self.record_select_filename_ui.Ui_Dialog()
                self.ui_record_select_filename_window.setupUi(self.record_select_filename_window)
                self.record_select_filename_window_is_open = True
                self.record_select_filename_window_support_code = self.record_select_filename_support_ui.Support_Ui_Dialog(self)
                self.record_select_filename_window.exec()
        except:
            print(traceback.format_exc())

    def open_record_filename_error_window(self,filename):
        try:
            variables = dir(self)
            if "record_filename_error_ui" not in variables:
                self.record_filename_error_ui = importlib.import_module("compiled-ui.menu-3.record-filename-error")
                self.record_filename_error_support_ui = importlib.import_module("python+.menu-3.record-filename-error")
            if self.record_filename_error_window_is_open == False:
                self.record_filename_error_window = CustomQDialog(self,False,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_record_filename_error_window = self.record_filename_error_ui.Ui_Dialog()
                self.ui_record_filename_error_window.setupUi(self.record_filename_error_window)
                self.record_filename_error_window_is_open = True
                self.record_filename_error_window_support_code = self.record_filename_error_support_ui.Support_Ui_Dialog(self,filename)
                self.record_filename_error_window.exec()
        except:
            print(traceback.format_exc())

    #information frame error window
    def open_information_frame_error_window(self,error_message):
        try:
            variables = dir(self)
            if "information_frame_error_ui" not in variables:
                self.information_frame_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.information-frame-error")
                self.information_frame_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.information-frame-error")
            if self.information_frame_error_window_is_open == False:
                self.information_frame_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_information_frame_error_window = self.information_frame_error_ui.Ui_Dialog()
                self.ui_information_frame_error_window.setupUi(self.information_frame_error_window)
                self.information_frame_error_window_is_open = True
                self.information_frame_error_window_support_code = self.information_frame_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.information_frame_error_window.exec()
        except:
            print(traceback.format_exc())

    #final slice error window
    def open_final_slice_plot_error_window(self,error_message):
        try:
            variables = dir(self)
            if "final_slice_plot_error_ui" not in variables:
                self.final_slice_plot_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.final-slice-plot-error")
                self.final_slice_plot_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.final-slice-plot-error")
            if self.final_slice_plot_error_window_is_open == False:
                self.final_slice_plot_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_final_slice_plot_error_window = self.final_slice_plot_error_ui.Ui_Dialog()
                self.ui_final_slice_plot_error_window.setupUi(self.final_slice_plot_error_window)
                self.final_slice_plot_error_window_is_open = True
                self.final_slice_plot_error_window_support_code = self.final_slice_plot_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.final_slice_plot_error_window.exec()
        except:
            print(traceback.format_exc())

    #final slice pyaudio error window
    def open_final_slice_pyaudio_error_window(self,error_message):
        try:
            variables = dir(self)
            if "final_slice_pyaudio_error_ui" not in variables:
                self.final_slice_pyaudio_error_ui = importlib.import_module("compiled-ui.main-window.helpfull-windows.final-slice-pyaudio-error")
                self.final_slice_pyaudio_error_support_ui = importlib.import_module("python+.main-window.helpfull-windows.final-slice-pyaudio-error")
            if self.final_slice_pyaudio_error_window_is_open == False:
                self.final_slice_pyaudio_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_final_slice_pyaudio_error_window = self.final_slice_pyaudio_error_ui.Ui_Dialog()
                self.ui_final_slice_pyaudio_error_window.setupUi(self.final_slice_pyaudio_error_window)
                self.final_slice_pyaudio_error_window_is_open = True
                self.final_slice_pyaudio_error_window_support_code = self.final_slice_pyaudio_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.final_slice_pyaudio_error_window.exec()
        except:
            print(traceback.format_exc())

    # ip calls error window
    def open_ip_call_error_window(self,error_message):
        try:
            variables = dir(self)
            if "ip_calls_error_ui" not in variables:
                self.ip_calls_error_ui = importlib.import_module("compiled-ui.menu-1.ip-calls.ip-calls-error")
                self.ip_calls_error_support_ui = importlib.import_module("python+.menu-1.ip-calls.ip-calls-error")
            if self.ip_calls_error_window_is_open == False:
                if self.ip_call_offering_window_is_open:
                    self.ip_calls_error_window = CustomQDialog(self,True,self.ip_call_offering_window,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                else:
                    self.ip_calls_error_window = CustomQDialog(self,True,self.MainWindow,
                                                                 QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

                self.ui_ip_calls_error_window = self.ip_calls_error_ui.Ui_Dialog()
                self.ui_ip_calls_error_window.setupUi(self.ip_calls_error_window)
                self.ip_calls_error_window_is_open = True
                self.ip_calls_error_window_support_code = self.ip_calls_error_support_ui.Support_Ui_Dialog(self,error_message)
                self.ip_calls_error_window.exec()
        except:
            print(traceback.format_exc())

    # ip calls error window
    def open_ip_call_offering_window(self, call_number,name,surname):
        try:
            variables = dir(self)
            if "ip_call_offering_ui" not in variables:
                self.ip_call_offering_ui = importlib.import_module(
                    "compiled-ui.menu-1.ip-calls.ip-call-offering")
                self.ip_call_offering_support_ui = importlib.import_module(
                    "python+.menu-1.ip-calls.ip-call-offering")
            #only one offer in progress at a time
            if self.ip_call_offering_window_is_open == False:
                self.ip_call_offering_window = CustomQDialog(self, False, self.MainWindow,QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                self.ui_ip_call_offering_window = self.ip_call_offering_ui.Ui_Dialog()
                self.ui_ip_call_offering_window.setupUi(self.ip_call_offering_window)
                self.ip_call_offering_window_is_open = True
                self.ip_call_offering_window_support_code = self.ip_call_offering_support_ui.Support_Ui_Dialog(self,call_number,name,surname)
                self.ip_call_offering_window.exec()
        except:
            print(traceback.format_exc())

    def restart_app(self):
        try:
            if self.record_deck_instance.deck_status != "stopped":
                self.record_deck_instance.stop_and_restart()
                return None
            #'''
            return_None = False
            for i in range(0,3):
                if self.ip_calls_record_deck_instance.ip_calls[i]["deck_status"] == "recording":
                    self.ip_calls_record_deck_instance.stop_and_restart()
                    return_None = True
            if return_None:
                return None
            #'''
            self.close_processes()

            try:
                self.MainWindow.close()
            except:
                pass
            QtCore.QProcess.startDetached(sys.executable, sys.argv)

            #if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            #    Popen(["web-radio-studio.exe"])
            #else:
            #    Popen(["python","web-radio-studio.py"])
            #    #os.spawnl(os.P_DETACH, os.path.abspath("python.exe"),os.path.abspath("python.exe"),"web-radio-studio.py")

            sys.exit(0)
            '''
            self.close_processes()

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.restart_end())
            self.timer.setSingleShot(True)
            self.timer.start(1000)  # set it to timeout in 200 ms
            '''
        except:
            #print(traceback.format_exc())
            pass

    def restart_end(self):
        try:
            #os.execl(sys.executable, sys.executable, *['"'+sys.argv[0]+'"', "-t", '2'])
            QtCore.QCoreApplication.quit()
            QtCore.QProcess.startDetached(sys.executable, sys.argv)
        except:
            print(traceback.format_exc())

    def closeEvent(self,event):
        try:
            if self.ui.ip_call_1_frame.isVisible():
                self.ui.ip_call_1_dismiss.click()
                time.sleep(0.25)
            if self.ui.ip_call_2_frame.isVisible():
                self.ui.ip_call_2_dismiss.click()
                time.sleep(0.25)
            if self.ui.ip_call_3_frame.isVisible():
                self.ui.ip_call_3_dismiss.click()
                time.sleep(0.25)

            if self.record_deck_instance.deck_status != "stopped":
                self.record_deck_instance.stop_and_close()
                event.ignore()
                return None
            return_None = False
            #'''
            for i in range(0, 3):
                if self.ip_calls_record_deck_instance.ip_calls[i]["deck_status"] == "recording":
                    self.ip_calls_record_deck_instance.stop_and_close()
                    return_None = True
            #'''
            if return_None:
                event.ignore()
                return None
            else:
                self.close_processes()
                # stop ngrok proccess
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                # si.wShowWindow = subprocess.SW_HIDE # default
                subprocess.call('taskkill /f /im ngrok.exe', startupinfo=si)
                time.sleep(0.5)
                event.accept()
        except Exception as e:
            print(traceback.format_exc())
            sys.exit()

    def close_processes(self):
        try:
            self.final_slice_instance.put_to_ip_record = False
            self.final_slice_instance.put_to_plot = False
            self.final_slice_instance.put_to_pyaudio = False
            self.secondary_slice_instance.put_to_pyaudio = False
            self.final_slice_pyaudio_instance.final_slice_pyaudio_queue.put({"type":"close"})
            self.secondary_slice_pyaudio_instance.secondary_slice_pyaudio_queue.put({"type":"close"})
            self.final_slice_plot_instance.final_slice_plot_queue.put({"type":"close"})
            self.secondary_slice_instance.put_to_ip_record = False

            self.ip_call_1_instance.put_to_q = False
            self.ip_call_2_instance.put_to_q = False
            self.ip_call_3_instance.put_to_q = False


            self.player_list_instance.player_list_queue.put({"type":"close"})
            self.ip_calls_instance.ip_calls_queue.put({"type":"close"})
            #self.record_deck_instance.record_deck_queue.put({"type": "close"})
            time.sleep(0.125)
            self.speackers_deck_instance.put_to_q = False
            while (self.final_slice_instance.speackers_deck_queue.qsize() > 0):
                tmp = self.final_slice_instance.speackers_deck_queue.get()
            self.speackers_deck_instance.manage_speackers_deck_queue.put({"type": "new-status", "status": "stopped"})
            time.sleep(0.125)
            self.speackers_deck_secondary_instance.put_to_q = False
            while (self.secondary_slice_instance.speackers_deck_secondary_queue.qsize() > 0):
                tmp = self.secondary_slice_instance.speackers_deck_secondary_queue.get()
            self.speackers_deck_secondary_instance.manage_speackers_deck_secondary_queue.put({"type": "new-status", "status": "stopped"})
            time.sleep(0.125)
            self.music_clip_deck_instance.put_to_q = False
            while (self.final_slice_instance.music_clip_deck_queue.qsize() > 0):
                tmp = self.final_slice_instance.music_clip_deck_queue.get()
            self.music_clip_deck_instance.stop_button_clicked()
            time.sleep(0.125)
            self.deck_1_instance.put_to_q = False
            while (self.final_slice_instance.deck_1_queue.qsize() > 0):
                tmp = self.final_slice_instance.deck_1_queue.get()
            self.deck_1_instance.stop_button_clicked()
            time.sleep(0.125)
            self.deck_2_instance.put_to_q = False
            while (self.final_slice_instance.deck_2_queue.qsize() > 0):
                tmp = self.final_slice_instance.deck_2_queue.get()
            self.deck_2_instance.stop_button_clicked()
            time.sleep(0.125)
            self.record_deck_instance.put_to_record = False
            #self.record_deck_instance.record_deck_queue.put({"type": "new-status", "status": "stopped"})
            self.ip_calls_record_deck_instance.record_deck_queue.put({"type": "new-status", "status": "stopped"})
            #time.sleep(0.150)

            # record deck
            self.record_deck_instance.close()

            # player list
            self.player_list_instance.close()

            self.quit_event.set()
            self.tr.join()
            # deck 1 manage
            self.deck_1_instance.close()
            # deck 2 manage
            self.deck_2_instance.close()
            # music clip deck manage
            self.music_clip_deck_instance.close()
            # speackers deck
            self.speackers_deck_instance.close()
            # speackers deck secondary
            self.speackers_deck_secondary_instance.close()
            # final slice
            self.final_slice_instance.close()
            # ip call 1
            self.ip_call_1_instance.close()
            # ip call 2
            self.ip_call_2_instance.close()
            # ip call 3
            self.ip_call_3_instance.close()
            # ip calls (aiortc)
            self.ip_calls_instance.close()
            # secondary slice
            self.secondary_slice_instance.close()
            # information frame
            self.information_frame_instance.close()
            # final slice plot
            self.final_slice_plot_instance.close()
            # final slice pyaudio
            self.final_slice_pyaudio_instance.close()
            # secondary slice pyaudio
            self.secondary_slice_pyaudio_instance.close()

            # ip calls record deck
            self.ip_calls_record_deck_instance.close()

        except:
            print(traceback.format_exc())

class CustomQDialog(QtWidgets.QDialog):

    def __init__(self,main_self,resize,*args, **kwards):
        self.main_self = main_self
        super().__init__(*args, **kwards)
        self.setModal(True)
        if resize:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.resize_and_center())
            self.timer.setSingleShot(True)
            self.timer.start(50)
            #self.resize_and_center()
        else:

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.center_qdialog())
            self.timer.setSingleShot(True)
            self.timer.start(50)
            #self.center_qdialog()

    def resize_and_center(self):
        try:
            title_bar_height = QtWidgets.QApplication.style().pixelMetric(QtWidgets.QStyle.PM_TitleBarHeight)
            central_widget_width = int(self.main_self.ui.centralwidget.frameSize().width())
            central_widget_height = int(self.main_self.ui.centralwidget.frameSize().height())
            self.setFixedSize(int(0.95*central_widget_width),int(1.0*(central_widget_height-title_bar_height)))

            central_widget_top_x = int(self.main_self.ui.centralwidget.frameGeometry().x())
            central_widget_top_y = int(self.main_self.ui.centralwidget.frameGeometry().y())
            central_widget_width = int(self.main_self.ui.centralwidget.frameGeometry().width())
            central_widget_height = int(self.main_self.ui.centralwidget.frameGeometry().height())

            qdialog_width = self.frameGeometry().width()
            qdialog_height = self.frameGeometry().height()
            qdialog_new_x = central_widget_top_x + (central_widget_width-qdialog_width)/2
            qdialog_new_y = central_widget_top_y + (central_widget_height-qdialog_height)/2
            self.move(self.main_self.MainWindow.mapToGlobal(QtCore.QPoint(int(qdialog_new_x),int(qdialog_new_y))))


        except:
            print(traceback.format_exc())

    def center_qdialog(self):
        central_widget_top_x = int(self.main_self.ui.centralwidget.frameGeometry().x())
        central_widget_top_y = int(self.main_self.ui.centralwidget.frameGeometry().y())
        central_widget_width = int(self.main_self.ui.centralwidget.frameGeometry().width())
        central_widget_height = int(self.main_self.ui.centralwidget.frameGeometry().height())

        qdialog_width = self.frameGeometry().width()
        qdialog_height = self.frameGeometry().height()
        qdialog_new_x = central_widget_top_x + (central_widget_width - qdialog_width) / 2
        qdialog_new_y = central_widget_top_y + (central_widget_height - qdialog_height) / 2
        self.move(self.main_self.MainWindow.mapToGlobal(QtCore.QPoint(int(qdialog_new_x), int(qdialog_new_y))))


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    '''
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            freeze_support()
        program = Web_Radio_Studio()
    '''
    #'''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        freeze_support()
    program = Web_Radio_Studio()