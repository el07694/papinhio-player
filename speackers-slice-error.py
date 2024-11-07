import traceback
import pyperclip
import importlib
from PyQt5 import QtCore
import sys

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append('../../compiled-ui/')
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")


### speackers deck ###
speackers_deck_secondary_class = importlib.import_module("python+.menu-1.ip-calls.speackers-deck-secondary")


class Support_Ui_Dialog:

    def __init__(self, main_self, error_message):
        self.main_self = main_self

        self.no_action = True
        self.main_self.speackers_deck_secondary_instance.put_to_q = False

        # apply theme
        self.main_self.manage_speackers_deck_secondary_error_window.setStyleSheet(
            "*{font-family:" + self.main_self.default_font + ";font-size:" + self.main_self.default_font_size + "px;color:" + self.main_self.default_font_color + ";}QDialog{background:" + self.main_self.default_background_color + "}QPushButton, QComboBox{background:" + self.main_self.default_buttons_background + ";color:" + self.main_self.default_buttons_font_color + "}")

        self.main_self.ui_manage_speackers_deck_secondary_error_window.details.setPlainText(str(error_message))
        self.main_self.ui_manage_speackers_deck_secondary_error_window.copy_error.clicked.connect(lambda state: self.copy_error(state))
        self.main_self.ui_manage_speackers_deck_secondary_error_window.restart_proccess.clicked.connect(lambda state: self.restart_proccess(state))
        self.main_self.ui_manage_speackers_deck_secondary_error_window.restart_program.clicked.connect(lambda state: self.restart_program(state))
        self.main_self.ui_manage_speackers_deck_secondary_error_window.close_program.clicked.connect(lambda state: self.close_program(state))

        self.main_self.manage_speackers_deck_secondary_error_window.closeEvent = lambda event: self.closeEvent(event)

    def copy_error(self, state):
        pyperclip.copy(self.main_self.ui_manage_speackers_deck_secondary_error_window.details.toPlainText())

    def restart_proccess(self, state):
        try:
            self.no_action = False

            #1. close error window
            self.main_self.manage_speackers_deck_secondary_error_window.close()

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.restart_the_process())
            self.timer.setSingleShot(True)
            self.timer.start(200)  # set it to timeout in 200 ms
        except:
            print(traceback.format_exc())

    def restart_the_process(self):
        try:
            #2. terminate speackers deck process
            self.main_self.speackers_deck_secondary_instance.close()

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.restart_the_process_end())
            self.timer.setSingleShot(True)
            self.timer.start(200)  # set it to timeout in 200 ms
        except:
            print(traceback.format_exc())

    def restart_the_process_end(self):
        try:
            #3. re-instantiate speackers_deck_instance!
            self.main_self.speackers_deck_secondary_instance = speackers_deck_secondary_class.Speackers_Deck_Secondary(self.main_self)
        except:
            print(traceback.format_exc())


    def restart_program(self,state):
        self.no_action = False
        #1. close error window
        self.main_self.manage_speackers_deck_secondary_error_window.close()

        #2. Restart the program
        self.main_self.restart_app()


    def close_program(self,state):
        self.no_action = False
        # 1. close error window
        self.main_self.manage_speackers_deck_secondary_error_window.close()

        # 2. close program
        self.main_self.MainWindow.close()

    def closeEvent(self, event):
        if self.no_action:
            self.no_action = False
            self.restart_proccess(None)
            return None
        self.main_self.manage_speackers_deck_secondary_error_window_is_open = False
        event.accept()