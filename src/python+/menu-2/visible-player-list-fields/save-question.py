
from PyQt5 import QtCore, QtGui, QtWidgets

class Support_Ui_Dialog:

    def __init__(self,main_self):
        try:
            self.main_self = main_self
            
            #apply theme
            self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
            self.main_self.select_player_list_fields_save_question_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
            self.main_self.select_player_list_fields_save_question_window.showMaximized()
            self.main_self.select_player_list_fields_save_question_window.update()

            self.main_self.select_player_list_fields_save_question_window.show()
            self.main_self.select_player_list_fields_save_question_window.hide()
            
            self.main_self.select_player_list_fields_save_question_window.closeEvent = lambda event:self.closeEvent(event)

            #Αποθήκευση
            self.main_self.ui_select_player_list_fields_save_question_window.save.clicked.connect(lambda state:self.save(state))
            
            #Απόρριψη
            self.main_self.ui_select_player_list_fields_save_question_window.no_save.clicked.connect(lambda state:self.no_save(state))

            #Ακύρωση
            self.main_self.ui_select_player_list_fields_save_question_window.cancel.clicked.connect(lambda state:self.cancel(state))
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
        
    def closeEvent(self,event):
        try:
            self.main_self.select_player_list_fields_save_question_window_is_open = False
            event.accept()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)

    def close_window(self,state):
        try:
            self.main_self.select_player_list_fields_save_question_window.close()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
            
    def save(self,state):
        try:
            self.main_self.visible_player_list_fields_window_support_code.save(None)
            self.close_window(None)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
            
    def no_save(self,state):
        try:
            self.main_self.visible_player_list_fields_window_support_code.need_save = False
            self.main_self.visible_player_list_fields_window.close()
            self.close_window(None)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
            
    def cancel(self,state):
        try:
            self.main_self.visible_player_list_fields_window_support_code.need_save = True
            self.close_window(None)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_select_player_list_fields_error_window(error_message)
        	