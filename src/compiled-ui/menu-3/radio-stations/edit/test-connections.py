# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/chris/Documents/papinhio-player/ui/menu-3/radio-stations/edit/test-connections.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(793, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_31 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setStyleSheet("QLabel{border:none;}")
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 0, 0, 1, 1)
        self.http_test_result = QtWidgets.QLabel(Dialog)
        self.http_test_result.setStyleSheet("QLabel{border:none;}")
        self.http_test_result.setText("")
        self.http_test_result.setWordWrap(True)
        self.http_test_result.setObjectName("http_test_result")
        self.gridLayout.addWidget(self.http_test_result, 0, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setStyleSheet("QLabel{border:none;}")
        self.label_33.setObjectName("label_33")
        self.gridLayout.addWidget(self.label_33, 1, 0, 1, 1)
        self.ftp_test_result = QtWidgets.QLabel(Dialog)
        self.ftp_test_result.setStyleSheet("QLabel{border:none;}")
        self.ftp_test_result.setText("")
        self.ftp_test_result.setWordWrap(True)
        self.ftp_test_result.setObjectName("ftp_test_result")
        self.gridLayout.addWidget(self.ftp_test_result, 1, 1, 1, 1)
        self.label_35 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy)
        self.label_35.setStyleSheet("QLabel{border:none;}")
        self.label_35.setObjectName("label_35")
        self.gridLayout.addWidget(self.label_35, 2, 0, 1, 1)
        self.mysql_test_result = QtWidgets.QLabel(Dialog)
        self.mysql_test_result.setStyleSheet("QLabel{border:none;}")
        self.mysql_test_result.setText("")
        self.mysql_test_result.setWordWrap(True)
        self.mysql_test_result.setObjectName("mysql_test_result")
        self.gridLayout.addWidget(self.mysql_test_result, 2, 1, 1, 1)
        self.label_34 = QtWidgets.QLabel(Dialog)
        self.label_34.setStyleSheet("QLabel{border:none;}")
        self.label_34.setObjectName("label_34")
        self.gridLayout.addWidget(self.label_34, 3, 0, 1, 1)
        self.radio_server_status = QtWidgets.QLabel(Dialog)
        self.radio_server_status.setStyleSheet("QLabel{border:none;}")
        self.radio_server_status.setText("")
        self.radio_server_status.setWordWrap(True)
        self.radio_server_status.setObjectName("radio_server_status")
        self.gridLayout.addWidget(self.radio_server_status, 3, 1, 1, 1)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setMinimumSize(QtCore.QSize(0, 1))
        self.line.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line.setStyleSheet("Line{\n"
"    border:1px solid #ABABAB;\n"
"}")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)
        self.web_page_message = QtWidgets.QLabel(Dialog)
        self.web_page_message.setStyleSheet("QLabel{border:0px;}")
        self.web_page_message.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.web_page_message.setWordWrap(True)
        self.web_page_message.setObjectName("web_page_message")
        self.gridLayout.addWidget(self.web_page_message, 5, 0, 1, 2)
        self.radio_web_page_frame = QtWidgets.QFrame(Dialog)
        self.radio_web_page_frame.setMinimumSize(QtCore.QSize(0, 80))
        self.radio_web_page_frame.setMaximumSize(QtCore.QSize(16777215, 80))
        self.radio_web_page_frame.setStyleSheet("QFrame{border:1px solid #ABABAB;background:white;}")
        self.radio_web_page_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.radio_web_page_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.radio_web_page_frame.setObjectName("radio_web_page_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.radio_web_page_frame)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addWidget(self.radio_web_page_frame, 6, 0, 1, 2)
        self.test_complete = QtWidgets.QPushButton(Dialog)
        self.test_complete.setObjectName("test_complete")
        self.gridLayout.addWidget(self.test_complete, 7, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Δοκιμαστικός έλεγχος συνδέσεων"))
        self.label_31.setText(_translate("Dialog", "Κατάσταση κεντρικής σελίδας (http):"))
        self.label_33.setText(_translate("Dialog", "Ftp server:"))
        self.label_35.setText(_translate("Dialog", "Mysql server:"))
        self.label_34.setText(_translate("Dialog", "Radio server:"))
        self.web_page_message.setText(_translate("Dialog", "Παρακάτω παρουσιάζετε ενδεικτικά τμήμα της σελίδας ακρόασης με σκοπό τον δοκιμαστικό έλεγχό της (ενδεικτική αναμετάδοση: \"Ομιλία: Ειρήνη - Δώρο Θεού (Μέρος 1)\")"))
        self.test_complete.setText(_translate("Dialog", "Ολοκλήρωση δοκιμής"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
