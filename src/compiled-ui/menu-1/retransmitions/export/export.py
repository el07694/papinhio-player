# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/chris/Documents/papinhio-player/ui/menu-1/retransmitions/export/export.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(777, 169)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rest-windows/assets/images/rest-windows/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_6 = QtWidgets.QFrame(Dialog)
        self.frame_6.setStyleSheet("QFrame{border:none;}")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.convert_and_export = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.convert_and_export.sizePolicy().hasHeightForWidth())
        self.convert_and_export.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/rest-windows/assets/images/rest-windows/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.convert_and_export.setIcon(icon1)
        self.convert_and_export.setObjectName("convert_and_export")
        self.horizontalLayout_4.addWidget(self.convert_and_export)
        self.cancel = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)
        self.cancel.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_4.addWidget(self.cancel)
        self.gridLayout.addWidget(self.frame_6, 5, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.choose_folder = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/rest-windows/assets/images/rest-windows/select-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.choose_folder.setIcon(icon2)
        self.choose_folder.setObjectName("choose_folder")
        self.gridLayout.addWidget(self.choose_folder, 3, 1, 1, 1)
        self.playlist_type = QtWidgets.QComboBox(Dialog)
        self.playlist_type.setObjectName("playlist_type")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.playlist_type.addItem("")
        self.gridLayout.addWidget(self.playlist_type, 1, 1, 2, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 2, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setStyleSheet("QLabel{\n"
"    font-weight:bold;\n"
"    color:green;\n"
"}")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.title = QtWidgets.QLineEdit(Dialog)
        self.title.setDragEnabled(True)
        self.title.setClearButtonEnabled(True)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.title, self.playlist_type)
        Dialog.setTabOrder(self.playlist_type, self.choose_folder)
        Dialog.setTabOrder(self.choose_folder, self.convert_and_export)
        Dialog.setTabOrder(self.convert_and_export, self.cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Εξαγωγή αναμετάδοσης ως λίστα αναπαραγωγής"))
        self.convert_and_export.setText(_translate("Dialog", "Μετατροπή και εξαγωγή"))
        self.cancel.setText(_translate("Dialog", "Ακύρωση"))
        self.label_2.setText(_translate("Dialog", "Τύπος λίστας αναπαραγωγής:"))
        self.label.setText(_translate("Dialog", "Τίτλος αναμετάδοσης - εξαγώμενου αρχείου playlist:"))
        self.choose_folder.setText(_translate("Dialog", "Επιλογή θέσης αποθήκευσης"))
        self.playlist_type.setItemText(0, _translate("Dialog", "Επιλογή τύπου λίστας αναπαραγωγής"))
        self.playlist_type.setItemText(1, _translate("Dialog", "aimppl"))
        self.playlist_type.setItemText(2, _translate("Dialog", "aimppl4"))
        self.playlist_type.setItemText(3, _translate("Dialog", "asx"))
        self.playlist_type.setItemText(4, _translate("Dialog", "atom"))
        self.playlist_type.setItemText(5, _translate("Dialog", "b4s"))
        self.playlist_type.setItemText(6, _translate("Dialog", "hypetape"))
        self.playlist_type.setItemText(7, _translate("Dialog", "kpl"))
        self.playlist_type.setItemText(8, _translate("Dialog", "kpl (xml version)"))
        self.playlist_type.setItemText(9, _translate("Dialog", "m3u"))
        self.playlist_type.setItemText(10, _translate("Dialog", "m3u8"))
        self.playlist_type.setItemText(11, _translate("Dialog", "mpcpl"))
        self.playlist_type.setItemText(12, _translate("Dialog", "plc"))
        self.playlist_type.setItemText(13, _translate("Dialog", "plist"))
        self.playlist_type.setItemText(14, _translate("Dialog", "plp"))
        self.playlist_type.setItemText(15, _translate("Dialog", "pls"))
        self.playlist_type.setItemText(16, _translate("Dialog", "ram"))
        self.playlist_type.setItemText(17, _translate("Dialog", "rms"))
        self.playlist_type.setItemText(18, _translate("Dialog", "rss"))
        self.playlist_type.setItemText(19, _translate("Dialog", "smil"))
        self.playlist_type.setItemText(20, _translate("Dialog", "vlc"))
        self.playlist_type.setItemText(21, _translate("Dialog", "wax"))
        self.playlist_type.setItemText(22, _translate("Dialog", "wpl"))
        self.playlist_type.setItemText(23, _translate("Dialog", "wvx"))
        self.playlist_type.setItemText(24, _translate("Dialog", "xml"))
        self.playlist_type.setItemText(25, _translate("Dialog", "xspf"))
        self.playlist_type.setItemText(26, _translate("Dialog", "zpl"))
        self.playlist_type.setItemText(27, _translate("Dialog", "zpl (xml version)"))
        self.label_3.setText(_translate("Dialog", "Επιλογή θέσης αποθήκευσης:"))
        self.label_4.setText(_translate("Dialog", "Σημείωση: Όλα τα πεδία είναι υποχρεωτικά."))
        self.title.setPlaceholderText(_translate("Dialog", "Πληκτρολογήστε εδώ το επιθυμητό όνομα αρχείου"))
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
