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

### ip call 1 ###
ip_call_1_class = importlib.import_module("python+.menu-1.ip-calls.ip-call-1")

### ip call 2 ###
ip_call_2_class = importlib.import_module("python+.menu-1.ip-calls.ip-call-2")

### ip call 3 ###
ip_call_3_class = importlib.import_module("python+.menu-1.ip-calls.ip-call-3")


### ip calls ###
ip_calls_class = importlib.import_module("python+.menu-1.ip-calls.ip-calls")


class Support_Ui_Dialog:

    def __init__(self, main_self, error_message):
        self.main_self = main_self

        self.no_action = True
        self.main_self.ip_calls_instance.put_to_q = False
        self.main_self.ip_call_1_instance.put_to_q = False
        self.main_self.ip_call_2_instance.put_to_q = False
        self.main_self.ip_call_3_instance.put_to_q = False

        # apply theme
        self.main_self.ip_calls_error_window.setStyleSheet(
            "*{font-family:" + self.main_self.default_font + ";font-size:" + self.main_self.default_font_size + "px;color:" + self.main_self.default_font_color + ";}QDialog{background:" + self.main_self.default_background_color + "}QPushButton, QComboBox{background:" + self.main_self.default_buttons_background + ";color:" + self.main_self.default_buttons_font_color + "}")

        self.main_self.ui_ip_calls_error_window.details.setPlainText(str(error_message))

        self.main_self.ui_ip_calls_error_window.copy_error.clicked.connect(lambda state: self.copy_error(state))
        self.main_self.ui_ip_calls_error_window.restart_proccess.clicked.connect(lambda state: self.restart_proccess(state))
        self.main_self.ui_ip_calls_error_window.restart_program.clicked.connect(lambda state: self.restart_program(state))
        self.main_self.ui_ip_calls_error_window.close_program.clicked.connect(lambda state: self.close_program(state))


        self.main_self.ip_calls_error_window.closeEvent = lambda event: self.closeEvent(event)

    def copy_error(self, state):
        pyperclip.copy(self.main_self.ui_ip_calls_error_window.details.toPlainText())

    def restart_proccess(self, state):
        try:
            self.no_action = False

            self.main_self.ip_calls_instance.close()
            self.main_self.ip_call_1_instance.close()
            self.main_self.ip_call_2_instance.close()
            self.main_self.ip_call_3_instance.close()

            self.main_self.ip_calls_instance = ip_calls_class.Ip_Calls(self.main_self)
            self.main_self.ip_call_1_instance = ip_call_1_class.Ip_Call_1(self.main_self)
            self.main_self.ip_call_2_instance = ip_call_1_class.Ip_Call_2(self.main_self)
            self.main_self.ip_call_3_instance = ip_call_1_class.Ip_Call_3(self.main_self)

            #1. close error window
            self.main_self.ip_calls_error_window.close()
        except:
            print(traceback.format_exc())


    def restart_program(self,state):
        self.no_action = False
        #1. close error window
        self.main_self.ip_calls_error_window.close()

        #2. Restart the program
        self.main_self.restart_app()

    def close_program(self,state):
        self.no_action = False
        # 1. close error window
        self.main_self.ip_calls_error_window.close()

        # 2. close program
        self.main_self.MainWindow.close()

    def closeEvent(self, event):
        if self.no_action:
            self.no_action = False
            self.restart_proccess(None)
            return None

        self.main_self.ip_calls_error_window_is_open = False
        event.accept()