from __future__ import print_function

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import sys
import smtplib 

import sys

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../..")

import importlib
import requests

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from zipfile import ZipFile
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import os
import shutil

import pickle


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from mimetypes import guess_type as guess_mime_type

import base64
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from multiprocessing import Process, Queue, Pipe
from PyQt5.QtCore import pyqtSignal, QThread
from datetime import datetime

import traceback

class Support_Ui_Dialog:

    def __init__(self,main_self):
        try:
            self.main_self = main_self
            
            #apply theme
            self.font = QtGui.QFont(self.main_self.default_font, int(self.main_self.default_font_size))
            self.main_self.contact_window.setStyleSheet("*{font-family:""+self.main_self.default_font+"";font-size:"+self.main_self.default_font_size+"px;color:""+self.main_self.default_font_color+"";}QFrame{border:0px;}QDialog{background:""+self.main_self.default_background_color+""}QPushButton, QComboBox{background:""+self.main_self.default_buttons_background+"";color:""+self.main_self.default_buttons_font_color+""}")
            self.main_self.contact_window.showMaximized()
            self.main_self.contact_window.update()

            self.main_self.contact_window.hide()
            self.main_self.contact_window.show()

            self.attachements_filenames = []

            self.main_self.ui_contact_window.add_attachment.clicked.connect(lambda state: self.add_attachment(state))
            self.main_self.ui_contact_window.remove_attachment.clicked.connect(lambda state: self.remove_attachment(state))
            self.main_self.ui_contact_window.send.clicked.connect(lambda state: self.send_email(state))
            self.main_self.ui_contact_window.cancel.clicked.connect(lambda state: self.close_window(state))

            #create proccess for send e-mail
            self.proccess_number = 23
            self.send_email_mother_pipe, self.send_email_child_pipe = Pipe()
            self.send_email_queue = Queue()
            self.send_email_emitter = Send_Email_Emitter(self.send_email_mother_pipe)
            self.send_email_emitter.start()
            self.send_email_child_process = Send_Email_Child_Proc(self.send_email_child_pipe, self.send_email_queue)
            self.send_email_child_process.start()
            self.send_email_emitter.email_send.connect(self.email_send)
            self.send_email_emitter.error_signal.connect(lambda error_message:self.main_self.open_contact_error_window(error_message))


            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.proccess_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = self.send_email_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1
     
            

            
            self.main_self.contact_window.closeEvent = lambda event:self.closeEvent(event)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)

        
    def closeEvent(self,event):
        try:
            self.main_self.contact_window_is_open = False
            event.accept()        
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)


    def add_attachment(self,state):
        try:
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.AnyFile)
            filenames = []

            if dlg.exec_():
                filenames = dlg.selectedFiles()
                for filename in filenames:
                    self.attachements_filenames.append(filename)
                    base=os.path.basename(filename)
                    item = QtWidgets.QListWidgetItem()
                    self.main_self.ui_contact_window.attachment_list.addItem(item)
                    item.setText(base)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)

        
    def remove_attachment(self,state):
        try:
            current_index = self.main_self.ui_contact_window.attachment_list.currentRow()
            if current_index!=-1:
                if current_index+1<=len(self.attachements_filenames):
                    self.main_self.ui_contact_window.attachment_list.takeItem( current_index )
                    del self.attachements_filenames[current_index]
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)

    
    def send_email(self,state):
        try:
            subject = self.main_self.ui_contact_window.subject.text()
            email = self.main_self.ui_contact_window.email.text()
            body = "Μήνυμα από: "+self.main_self.ui_contact_window.name.text()+"("+str(email)+"). \n"+self.main_self.ui_contact_window.message.toPlainText()
            self.main_self.ui_contact_window.name.setEnabled(False)
            self.main_self.ui_contact_window.subject.setEnabled(False)
            self.main_self.ui_contact_window.message.setEnabled(False)
            self.main_self.ui_contact_window.attachment_list.setEnabled(False)
            self.main_self.ui_contact_window.add_attachment.setEnabled(False)
            self.main_self.ui_contact_window.remove_attachment.setEnabled(False)
            self.main_self.ui_contact_window.send.setEnabled(False)
            self.send_email_queue.put({"type":"send","subject":subject,"body":body,"filenames":self.attachements_filenames})
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)


        
    def email_send(self):
        try:
            self.close_window(None)
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)

        
    def close_window(self,state):
        try:
            self.main_self.contact_window.close()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)


    def closeEvent(self,event):
        try:
            if self.send_email_child_process is not None:
                self.send_email_child_process.terminate()
                self.send_email_emitter.terminate()
                self.send_email_child_process = None
                self.send_email_emitter = None
                
            self.main_self.contact_window_is_open = False
            event.accept()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.main_self.open_contact_error_window(error_message)



class Send_Email_Emitter(QThread):
    try:
        email_send = pyqtSignal()
        error_signal = pyqtSignal(str)
    except Exception as e:
        pass

    def __init__(self, from_process: Pipe):
        try:
            super().__init__()
            self.data_from_process = from_process
        except Exception as e:
            pass

    def run(self):
        try:
            while True:
                data = self.data_from_process.recv()
                if data["type"]=="email_send":
                    self.email_send.emit()
                elif data["type"] == "error":
                    self.error_signal.emit(data["error_message"])
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.error_signal.emit(error_message)
            except Exception as e:
                pass

                
class Send_Email_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass
        
    def run(self):
        try:
            while(True):
                data = self.data_from_mother.get()
                if data["type"] == "send":
                    self.send_email(data["subject"],data["body"],data["filenames"])
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass

                    
    def send_email(self,subject,body,filenames):
        try:
            # Request all access (permission to read/send/receive emails, manage the inbox, and more)
            self.SCOPES = ['https://mail.google.com/']
            self.our_email = 'el07694@gmail.com'
            self.service = None
            self.subject = subject
            self.body = body
            self.attachements = filenames
            self.service = self.gmail_authenticate()
            self.send_message(self.service,"el07694@gmail.com", self.subject, self.body, self.attachements)

            self.to_emitter.send({"type":"email_send"})
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass
            
        
    def gmail_authenticate(self):
        try:
            #if os.path.exists('../menu-4/contact/token.pickle'):
            #    creds = Credentials.from_authorized_user_file(os.path.exists('../menu-4/contact/token.pickle'), SCOPES)
            #else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.abspath('../menu-4/contact/credentials.json'), self.SCOPES)
            creds = flow.run_local_server(port=0)
            
            # save the credentials for the next run
            with open(os.path.abspath("../menu-4/contact/token.pickle"), "wb") as token:
                pickle.dump(creds, token)
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass

        
    # Adds the attachment with the given filename to the given message
    def add_attachment_google(self,message, filename):
        try:
            content_type, encoding = guess_mime_type(filename)
            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(filename, 'rb')
                msg = MIMEText(fp.read().decode(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(filename, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(filename, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(filename, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()
            filename = os.path.basename(filename)
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(msg)
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass

        
    def build_message(self,destination, obj, body, attachments=[]):
        try:
            if not attachments: # no attachments given
                message = MIMEText(body)
                message['to'] = destination
                message['from'] = self.our_email
                message['subject'] = obj
            else:
                message = MIMEMultipart()
                message['to'] = destination
                message['from'] = self.our_email
                message['subject'] = obj
                message.attach(MIMEText(body))
                for filename in attachments:
                    self.add_attachment_google(message, filename)
            return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass

    
    def send_message(self,service, destination, obj, body, attachments=[]):
        try:
            return service.users().messages().send(userId="me",body=self.build_message(destination, obj, body, attachments)).execute()
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                self.to_emitter.send({"type":"error","error_message":error_message})
            except Exception as e:
                pass