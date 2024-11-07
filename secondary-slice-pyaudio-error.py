import traceback
import pyperclip
import importlib

import sys
from PyQt5 import QtCore
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append('../../compiled-ui/')
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")


### secondary slice pyaudio ###
secondary_slice_pyaudio_class = importlib.import_module("python+.menu-1.ip-calls.secondary-slice-pyaudio")


class Support_Ui_Dialog:

    def __init__(self, main_self, error_message):
        self.main_self = main_self

        self.no_action = True
        self.main_self.secondary_slice_instance.put_to_pyaudio = False

        # apply theme
        self.main_self.secondary_slice_pyaudio_error_window.setStyleSheet(
            "*{font-family:" + self.main_self.default_font + ";font-size:" + self.main_self.default_font_size + "px;color:" + self.main_self.default_font_color + ";}QDialog{background:" + self.main_self.default_background_color + "}QPushButton, QComboBox{background:" + self.main_self.default_buttons_background + ";color:" + self.main_self.default_buttons_font_color + "}")

        self.main_self.ui_secondary_slice_pyaudio_error_window.details.setPlainText(str(error_message))

        self.main_self.ui_secondary_slice_pyaudio_error_window.copy_error.clicked.connect(lambda state: self.copy_error(state))
        self.main_self.ui_secondary_slice_pyaudio_error_window.restart_proccess.clicked.connect(lambda state: self.restart_proccess(state))
        self.main_self.ui_secondary_slice_pyaudio_error_window.restart_program.clicked.connect(lambda state: self.restart_program(state))
        self.main_self.ui_secondary_slice_pyaudio_error_window.close_program.clicked.connect(lambda state: self.close_program(state))


        self.main_self.secondary_slice_pyaudio_error_window.closeEvent = lambda event: self.closeEvent(event)

    def copy_error(self, state):
        pyperclip.copy(self.main_self.ui_secondary_slice_pyaudio_error_window.details.toPlainText())

    def restart_proccess(self, state):
        try:
            self.no_action = False

            #2. terminate final slice plot process
            self.main_self.secondary_slice_pyaudio_instance.close()

            #3. re-instantiate final slice plot instance!
            self.main_self.secondary_slice_pyaudio_instance = secondary_slice_pyaudio_class.Secondary_Slice_Pyaudio(self.main_self)

            #1. close error window
            self.main_self.secondary_slice_pyaudio_error_window.close()
        except:
            print(traceback.format_exc())

    def restart_the_process(self):
        try:
            #2. terminate final slice plot process
            self.main_self.secondary_slice_pyaudio_instance.close()

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.restart_the_process_end())
            self.timer.setSingleShot(True)
            self.timer.start(1000)  # set it to timeout in 200 ms
        except:
            print(traceback.format_exc())

    def restart_program(self,state):
        self.no_action = False
        #1. close error window
        self.main_self.secondary_slice_pyaudio_error_window.close()

        #2. Restart the program
        self.main_self.restart_app()

    def restart_the_process_end(self):
        try:
            #3. re-instantiate final slice plot instance!
            del self.main_self.secondary_slice_pyaudio_instance.secondary_slice_pyaudio_queue
            del self.main_self.secondary_slice_pyaudio_instance
            ### secondary slice pyaudio ###
            secondary_slice_pyaudio_class = importlib.import_module("python+.menu-1.ip-calls.secondary-slice-pyaudio")
            self.main_self.secondary_slice_pyaudio_instance = secondary_slice_pyaudio_class.Secondary_Slice_Pyaudio(self.main_self)
        except:
            print(traceback.format_exc())

    def close_program(self,state):
        self.no_action = False
        # 1. close error window
        self.main_self.secondary_slice_pyaudio_error_window.close()

        # 2. close program
        self.main_self.MainWindow.close()

    def closeEvent(self, event):
        if self.no_action:
            self.no_action = False
            self.restart_proccess(None)
            return None

        self.main_self.secondary_slice_pyaudio_error_window_is_open = False
        event.accept()