from PyQt5 import QtCore, QtGui, QtWidgets

class Support_Ui_Dialog:

    def __init__(self,main_self,error_message):
        self.main_self = main_self
        
        #apply theme
        self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
        self.main_self.visible_programm_components_error_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
        self.main_self.visible_programm_components_error_window.showMaximized()
        self.main_self.visible_programm_components_error_window.update()
        
        self.main_self.visible_programm_components_error_window.hide()
        self.main_self.visible_programm_components_error_window.show()

        self.main_self.ui_visible_programm_components_error_window.details.setPlainText(str(error_message))

        self.main_self.ui_visible_programm_components_error_window.restart_proccess.clicked.connect(lambda state:self.restart_proccess(state))
        self.main_self.ui_visible_programm_components_error_window.ok.clicked.connect(lambda state:self.close_window(state))
        
        self.main_self.visible_programm_components_error_window.closeEvent = lambda event:self.closeEvent(event)

        
    def restart_proccess(self,state):
        if self.main_self.select_visible_programm_components_save_question_window_is_open:
            self.main_self.select_visible_programm_components_save_question_window_support_code.close_window(None)
            self.main_self.select_visible_programm_components_save_question_window_is_open = False

        self.main_self.visible_programm_components_window_support_code.need_save = False
        self.main_self.visible_programm_components_window_support_code.save_in_progress = False
        if self.main_self.visible_program_components_window_is_open:
            self.main_self.visible_programm_components_window_support_code.close_window(None)
            self.main_self.visible_program_components_window_is_open = False

        self.main_self.visible_programm_components_error_window.close()
        self.main_self.open_programm_components_window(None)

    def close_window(self,state):
        if self.main_self.select_visible_programm_components_save_question_window_is_open:
            self.main_self.select_visible_programm_components_save_question_window_support_code.close_window(None)

        self.main_self.visible_programm_components_window_support_code.need_save = False
        self.main_self.visible_programm_components_window_support_code.save_in_progress = False
        if self.main_self.visible_program_components_window_is_open:
            self.main_self.visible_programm_components_window_support_code.close_window(None)

        self.main_self.visible_programm_components_error_window.close()
        
    def closeEvent(self,event):
        if self.main_self.select_visible_programm_components_save_question_window_is_open:
            self.main_self.select_visible_programm_components_save_question_window_support_code.close_window(None)

        self.main_self.visible_programm_components_window_support_code.need_save = False
        self.main_self.visible_programm_components_window_support_code.save_in_progress = False
        if self.main_self.visible_program_components_window_is_open:
            self.main_self.visible_programm_components_window_support_code.close_window(None)

        self.main_self.visible_programm_components_error_window_is_open = False
        event.accept()