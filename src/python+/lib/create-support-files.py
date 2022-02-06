import os
import sys

compiled_ui_folder = os.path.abspath("../../compiled-ui")
python_support_folder = os.path.abspath("../../python+")

def parse_directory(path):
	path_contents = os.listdir(path)
	if os.path.exists(path.replace(compiled_ui_folder,python_support_folder))==False:
		os.mkdir(path.replace(compiled_ui_folder,python_support_folder))
	for path_content in path_contents:
		if os.path.isdir(path+"/"+path_content):
			parse_directory(path+"/"+path_content)
		else:
			print(path+"/"+path_content)
			support_template_code = '''
from PyQt5 import QtCore, QtGui, QtWidgets

class Support_Ui_Dialog:

    def __init__(self,main_self):
        self.main_self = main_self
        
        #apply theme
        self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
        self.main_self.edit_radio_stations_window.setStyleSheet("*{font-family:\""+self.main_self.default_font+"\";font-size:"+self.main_self.default_font_size+"px;color:\""+self.main_self.default_font_color+"\";}QFrame{border:0px;}QDialog{background:\""+self.main_self.default_background_color+"\"}QPushButton, QComboBox{background:\""+self.main_self.default_buttons_background+"\";color:\""+self.main_self.default_buttons_font_color+"\"}")
        self.main_self.edit_radio_stations_window.showMaximized()
        self.main_self.edit_radio_stations_window.update()
        
        self.main_self.'********_window'.closeEvent = lambda event:self.closeEvent(event)
        
    def closeEvent(self,event):
        self.main_self.'********_window_is_open' = False
        event.accept()        
        	'''
			saved_path = (path+"/"+path_content).replace(compiled_ui_folder,python_support_folder)
			if "icons.py" not in saved_path:
				fin = open(saved_path, "x")
				fin.write(support_template_code)
				fin.close()

parse_directory(compiled_ui_folder)