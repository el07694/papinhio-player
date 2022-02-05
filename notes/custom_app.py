import sys
from PyQt5 import QtWidgets

from qt_material import list_themes
from qt_material import apply_stylesheet
themes = list_themes()
#print(themes)

# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml')

# run
window.show()
app.exec_()