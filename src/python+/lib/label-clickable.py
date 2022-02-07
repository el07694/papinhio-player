from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import pyqtSignal, QTimer

class QLabelClickable(QLabel):
	clicked = pyqtSignal(str)
	
	def __init__(self, parent=None):
		super(QLabelClickable, self).__init__(parent)

	def mousePressEvent(self, event):
		self.ultimo = "Clic"
    
	def mouseReleaseEvent(self, event):
		if self.ultimo == "Clic":
			QTimer.singleShot(QApplication.instance().doubleClickInterval(),self.performSingleClickAction)
		else:
			# Realizar acción de doble clic.
			self.clicked.emit(self.ultimo)
    
	def mouseDoubleClickEvent(self, event):
		self.ultimo = "Doble Clic"
    
	def performSingleClickAction(self):
		if self.ultimo == "Clic":
			self.clicked.emit(self.ultimo)