# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/chris/Documents/papinhio-player/ui/menu-1/sound-files/edit/wrong-image-file-type.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(573, 184)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rest-windows/assets/images/rest-windows/information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setStyleSheet("QFrame{border:0px;}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.image_label = QtWidgets.QLabel(self.frame)
        self.image_label.setMaximumSize(QtCore.QSize(117, 117))
        self.image_label.setText("")
        self.image_label.setPixmap(QtGui.QPixmap(":/rest-windows/assets/images/rest-windows/information.png"))
        self.image_label.setScaledContents(True)
        self.image_label.setObjectName("image_label")
        self.horizontalLayout.addWidget(self.image_label)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)
        self.ok = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/rest-windows/assets/images/rest-windows/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ok.setIcon(icon1)
        self.ok.setObjectName("ok")
        self.gridLayout.addWidget(self.ok, 1, 0, 1, 1)
        self.choose_another_file = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/main-window/assets/images/main-window/deck-image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.choose_another_file.setIcon(icon2)
        self.choose_another_file.setObjectName("choose_another_file")
        self.gridLayout.addWidget(self.choose_another_file, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Λάθος αρχείο εικόνας"))
        self.label.setText(_translate("Dialog", "Το εισαγώμενο αρχείο δεν υποστήριζεται από την εφαρμογή."))
        self.ok.setText(_translate("Dialog", "Εντάξει"))
        self.choose_another_file.setText(_translate("Dialog", "Επιλογή άλλου αρχείου εικόνας"))
import sys
sys.path.append('../../../')

import importlib
icons = importlib.import_module('compiled-ui.icons')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
