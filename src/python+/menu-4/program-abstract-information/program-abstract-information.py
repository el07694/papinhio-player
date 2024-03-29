from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess
import traceback

class Support_Ui_Dialog:

    def __init__(self,main_self):
        try:
            self.main_self = main_self
            
            #apply theme
            self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
            self.main_self.programm_abstract_information_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
            self.main_self.programm_abstract_information_window.showMaximized()
            self.main_self.programm_abstract_information_window.update()

            self.main_self.programm_abstract_information_window.show()
            self.main_self.programm_abstract_information_window.hide()

            self.main_self.ui_programm_abstract_information_window.ok.clicked.connect(lambda state:self.close_window(state))
            self.main_self.ui_programm_abstract_information_window.open_manual.clicked.connect(lambda state:self.open_manual(state))
            
            self.main_self.programm_abstract_information_window.closeEvent = lambda event:self.closeEvent(event)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_programm_abstract_information_error_window(error_message)
  
    def close_window(self,state):
        try:
            self.main_self.programm_abstract_information_window.close()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_programm_abstract_information_error_window(error_message)
        
    def open_manual(self,state):
        try:
            manual_pdf_path = os.path.abspath("")
            subprocess.Popen('explorer /select,"'+manual_pdf_path+'"', shell=False)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_programm_abstract_information_error_window(error_message)
        self.close_window(None)

    def closeEvent(self,event):
        try:
            self.main_self.programm_abstract_information_window_is_open = False
            event.accept()        
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_programm_abstract_information_error_window(error_message)
        
        	