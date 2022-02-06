
from PyQt5 import QtCore, QtGui, QtWidgets

class Support_Ui_Dialog:

    def __init__(self,main_self):
        self.main_self = main_self
        
        #apply theme
        self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
        self.main_self.edit_radio_stations_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
        self.main_self.edit_radio_stations_window.showMaximized()
        self.main_self.edit_radio_stations_window.update()
        
        self.main_self.export_retransmition_window.closeEvent = lambda event:self.closeEvent(event)
        
    def closeEvent(self,event):
        self.main_self.export_retransmition_window_is_open = False
        event.accept()        
        	