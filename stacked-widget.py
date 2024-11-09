import importlib
import sys
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../../../../")
sys.path.append("../../../../../")
from custom_qstacked_widgets import *
import time

class Stacked_Widget:
    def __init__(self,main_self):
        self.main_self = main_self
        loadJsonStyle(self.main_self.ui,"src/python+/main-window/custom_qstacked_widgets.json")


        self.currentIndex = 0
        self.main_self.ui.stackedWidget.currentChanged.connect(lambda index:self.current_index_changed(index))

        self.main_self.ui.action_go_to_page_1.triggered.connect(lambda action: self.go_to_page(0))
        self.main_self.ui.action_go_to_page_2.triggered.connect(lambda action: self.go_to_page(1))
        self.main_self.ui.action_go_to_page_3.triggered.connect(lambda action: self.go_to_page(2))
        self.main_self.ui.action_go_to_page_4.triggered.connect(lambda action: self.go_to_page(3))

        self.hide_page_3()

    def hide_page_3(self):
        self.main_self.ui.stackedWidget.hide_3 = True
        self.main_self.ui.action_go_to_page_3.setEnabled(False)

    def show_page_3(self):
        self.main_self.ui.stackedWidget.hide_3 = False
        self.main_self.ui.action_go_to_page_3.setEnabled(True)

    def current_index_changed(self,index):
        if index != self.currentIndex:
            self.currentIndex = index
        for i in range(0,4):
            eval("self.main_self.ui.action_go_to_page_" + str(i+1) + ".setChecked(False)")
        eval("self.main_self.ui.action_go_to_page_" + str(index+1) + ".setChecked(True)")

    def go_to_page(self,page_id):
        currentIndex = self.main_self.ui.stackedWidget.currentIndex()
        if currentIndex != self.currentIndex:
            self.currentIndex = currentIndex

        if currentIndex == page_id:
            eval("self.main_self.ui.action_go_to_page_"+str(page_id+1)+".setChecked(True)")
            return None
        else:
            eval("self.main_self.ui.action_go_to_page_" + str(currentIndex + 1) + ".setChecked(False)")
            widgetPage = self.main_self.ui.stackedWidget.widget(page_id)
            self.main_self.ui.stackedWidget.setCurrentWidget(widgetPage)