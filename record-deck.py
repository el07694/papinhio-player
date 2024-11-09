from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from multiprocessing import Process, Queue, Pipe
import sys
from datetime import datetime, timedelta
import time
import traceback
import pyaudio
from pydub import AudioSegment, effects, utils, generators
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
import wave
import os
from pathvalidate import is_valid_filename
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")

import importlib
icons = importlib.import_module('compiled-ui.icons')
database_functions = importlib.import_module("python+.lib.sqlite3-functions")
convert_time_function = importlib.import_module("python+.lib.convert-time-function")


class Record_Deck:
    def __init__(self,main_self):
        try:
            self.main_self = main_self

            self.deck_status = "stopped"
            self.main_self.final_slice_instance.put_to_record = False

            self.duration_str = "00:00:00"

            #manage record deck buttons

            # start button
            self.main_self.ui.record_deck_start.clicked.connect(lambda:self.start_clicked())

            # pause button
            self.main_self.ui.record_deck_pause.clicked.connect(lambda:self.pause_clicked())
            self.main_self.ui.menu_record_pause.triggered.connect(lambda action:self.pause_clicked())
            self.main_self.ui.action_pause_record.triggered.connect(lambda action:self.pause_clicked())

            # stop button
            self.main_self.ui.record_deck_stop.clicked.connect(lambda:self.stop_clicked())
            self.main_self.ui.menu_record_stop.triggered.connect(lambda action:self.stop_clicked())
            self.main_self.ui.action_stop_record.triggered.connect(lambda action:self.stop_clicked())

            # create process
            self.process_number = 100
            self.record_deck_mother_pipe, self.record_deck_child_pipe = Pipe()
            self.record_deck_queue = Queue()
            self.record_deck_emitter = Record_Deck_Emitter(self.record_deck_mother_pipe)
            self.record_deck_emitter.error_signal.connect(lambda error_message: self.main_self.open_record_deck_error_window(error_message))
            self.record_deck_emitter.current_duration_signal.connect(lambda duration_str: self.display_current_duration(duration_str))
            self.record_deck_emitter.record_end.connect(lambda: self.record_end())


            self.record_deck_emitter.start()
            self.record_deck_child_process = Record_Deck_Child_Proc(self.record_deck_child_pipe, self.record_deck_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.record_deck_child_process.start()
            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.record_deck_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})

            #self.put_to_record = True
            self.close_program = False
            self.restart_program = False
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def record_end(self):
        try:
            self.deck_status = "stopped"
            self.main_self.final_slice_instance.put_to_record = False
            time.sleep(0.250)
            if self.close_program:
                self.close()
                self.main_self.MainWindow.close()
            else:
                if self.restart_program:
                    self.close()
                    self.main_self.restart_app()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def stop_and_close(self):
        try:
            if self.close_program:
                return None
            self.close_program = True
            self.record_deck_queue.put({"type":"new-status","status":"stopped"})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def stop_and_restart(self):
        try:
            if self.restart_program:
                return None
            self.restart_program = True
            self.record_deck_queue.put({"type":"new-status","status":"stopped"})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)


    def display_current_duration(self,duration_str):
        try:
            if self.deck_status == "recording":
                self.duration_str = duration_str
                self.main_self.ui.record_deck_start.setText("Έναρξη ηχογράφησης ("+duration_str+")")
                self.main_self.ui.menu_record_start.setText("Έναρξη ηχογράφησης ("+duration_str+")")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def start_clicked(self):
        try:
            if self.deck_status == "stopped":
                filename = self.main_self.ui.record_deck_filename_lineEdit.text()
                if filename.strip()=="" or is_valid_filename(filename+".mp3") == False:
                    self.main_self.open_record_deck_filename_error_window(filename)
                else:
                    now = datetime.now()
                    now_str = now.strftime("%Y-%m-%d %H_%M_%S")
                    self.filename = filename+"_"+now_str
                    self.deck_status = "recording"
                    self.main_self.ui.record_deck_filename_lineEdit.setEnabled(False)
                    self.main_self.ui.record_deck_start.setEnabled(False)
                    self.main_self.ui.record_deck_pause.setEnabled(True)
                    self.main_self.ui.record_deck_stop.setEnabled(True)

                    self.main_self.ui.menu_record_start.setEnabled(False)
                    self.main_self.ui.menu_record_pause.setEnabled(True)
                    self.main_self.ui.menu_record_stop.setEnabled(True)

                    self.main_self.ui.action_start_record.setEnabled(False)
                    self.main_self.ui.action_pause_record.setEnabled(True)
                    self.main_self.ui.action_stop_record.setEnabled(True)

                    self.record_deck_queue.put({"type":"new-status","status":self.deck_status,"filename":self.filename})
                    self.main_self.final_slice_instance.put_to_record = True
            else:
                self.deck_status = "recording"
                self.main_self.ui.record_deck_start.setEnabled(False)
                self.main_self.ui.record_deck_pause.setEnabled(True)
                self.main_self.ui.record_deck_stop.setEnabled(True)

                self.main_self.ui.menu_record_start.setEnabled(False)
                self.main_self.ui.menu_record_pause.setEnabled(True)
                self.main_self.ui.menu_record_stop.setEnabled(True)

                self.main_self.ui.action_start_record.setEnabled(False)
                self.main_self.ui.action_pause_record.setEnabled(True)
                self.main_self.ui.action_stop_record.setEnabled(True)

                self.record_deck_queue.put({"type": "new-status", "status": self.deck_status})
                self.main_self.final_slice_instance.put_to_record = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def pause_clicked(self):
        try:
            self.deck_status = "paused"
            self.record_deck_queue.put({"type": "new-status", "status": self.deck_status})


            self.main_self.ui.record_deck_start.setEnabled(True)
            self.main_self.ui.record_deck_pause.setEnabled(False)
            self.main_self.ui.record_deck_stop.setEnabled(True)

            self.main_self.ui.menu_record_start.setEnabled(True)
            self.main_self.ui.menu_record_pause.setEnabled(False)
            self.main_self.ui.menu_record_stop.setEnabled(True)

            self.main_self.ui.action_start_record.setEnabled(True)
            self.main_self.ui.action_pause_record.setEnabled(False)
            self.main_self.ui.action_stop_record.setEnabled(True)

            self.main_self.final_slice_instance.put_to_record = False
            self.main_self.ui.record_deck_start.setText("Συνέχιση ηχογράφησης (" + str(self.duration_str) +")")
            self.main_self.ui.record_deck_start.setStatusTip("Πατήστε εδώ για συνέχιση της ηχογράφησης")
            self.main_self.ui.menu_record_start.setText("Συνέχιση ηχογράφησης (" + str(self.duration_str) +")")

            self.main_self.ui.action_start_record.setStatusTip("Συνέχιση ηχογράφησης")
            self.main_self.ui.menu_record_start.setStatusTip("Συνέχιση ηχογράφησης του τελικού σήματος εξόδου")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def stop_clicked(self):
        try:
            #self.deck_status = "stopped"

            self.main_self.ui.record_deck_filename_lineEdit.setEnabled(True)
            self.main_self.ui.record_deck_start.setEnabled(True)
            self.main_self.ui.record_deck_pause.setEnabled(False)
            self.main_self.ui.record_deck_stop.setEnabled(False)

            self.main_self.ui.menu_record_start.setEnabled(True)
            self.main_self.ui.menu_record_pause.setEnabled(False)
            self.main_self.ui.menu_record_stop.setEnabled(False)

            self.main_self.ui.action_start_record.setEnabled(True)
            self.main_self.ui.action_pause_record.setEnabled(False)
            self.main_self.ui.action_stop_record.setEnabled(False)


            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.set_btn_text())
            self.timer.setSingleShot(True)
            self.timer.start(300)



            self.record_deck_queue.put({"type": "new-status", "status": "stopped"})
            self.main_self.final_slice_instance.put_to_record = False
            self.main_self.ui.record_deck_start.setStatusTip("Πατήστε εδώ για έναρξη της ηχογράφησης (απαιτείτε να έχει συμπληρωθεί ο τίτλος του αρχείου ηχογράφησης)")
            self.main_self.ui.action_start_record.setStatusTip("Έναρξη ηχογράφησης")
            self.main_self.ui.menu_record_start.setStatusTip("Έναρξη ηχογράφησης του τελικού σήματος εξόδου")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def set_btn_text(self):
        try:
            self.main_self.ui.record_deck_start.setText("Έναρξη ηχογράφησης")
            self.main_self.ui.menu_record_start.setText("Έναρξη ηχογράφησης")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

    def close(self):
        try:
            if self.deck_status == "recording":
                self.deck_status = "stopped"
                self.record_deck_queue.put({"type":"new-status","status":self.deck_status})
                time.sleep(0.250)
            self.record_deck_queue.put({"type": "close"})
            time.sleep(0.250)
            try:
                if self.record_deck_child_process is not None:
                    self.record_deck_child_process.terminate()
                    self.record_deck_child_process.close()
            except:
                pass
                #print(traceback.format_exc())
            try:
                if self.record_deck_emitter is not None:
                    self.record_deck_emitter.quit()
            except:
                pass
                #print(traceback.format_exc())
            self.main_self.final_slice_instance.put_to_record = False
            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter]["pid"] = None
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = None
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "stopped"
                        self.main_self.manage_processes_instance.processes[counter]["cpu"] = 0
                        self.main_self.manage_processes_instance.processes[counter]["ram"] = 0
                counter += 1
            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_record_deck_error_window(error_message)

class Record_Deck_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        current_duration_signal = pyqtSignal(str)
        record_end = pyqtSignal()
    except:
        pass

    def __init__(self, from_process: Pipe):
        try:
            super().__init__()
            self.data_from_process = from_process
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)

    def run(self):
        try:
            while True:
                data = self.data_from_process.recv()
                if data["type"] == "error":
                    self.error_signal.emit(data["error_message"])
                elif data["type"] == "current-duration":
                    self.current_duration_signal.emit(data["duration"])
                elif data["type"] == "record-end":
                    self.record_end.emit()
                elif data["type"]=="close":
                    break
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)


class Record_Deck_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.deck_status = "stopped"
        except:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.send({"type": "error", "error_message": error_message})
            except:
                pass

    def run(self):
        try:
            current_frame = 0
            while (True):
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return None
                w = self.one_chunk()
                if w == "break":
                    break
                current_frame += 1
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def one_chunk(self):
        try:
            slice = None
            q_size = self.data_from_mother.qsize()
            if q_size > 0:
                data = self.data_from_mother.get()
            else:
                data = None
            if data is not None:
                if data["type"] == "close":
                    self.to_emitter.send({"type": "close"})
                    return "break"
                if data["type"] == "slice":
                    slice = data["slice"]
                elif data["type"] == "new-status":
                    old_deck_status = self.deck_status
                    self.deck_status = data["status"]
                    if self.deck_status == "recording" and old_deck_status=="stopped":
                        self.start_datetime_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        self.title = data["filename"].split("_")[0]
                        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                            self.filename = os.path.abspath(os.path.join("files","records",data["filename"]+".wav"))
                        else:
                            self.filename = os.path.abspath(os.path.join("files", "records", data["filename"] + ".wav"))
                        self.chunk_number = 0
                        self.current_duration_milliseconds = 0

                        self.file_handle = wave.open(self.filename, 'wb')
                        p = pyaudio.PyAudio()
                        self.file_handle.setnchannels(2)
                        self.file_handle.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                        self.file_handle.setframerate(44100)
                    elif self.deck_status == "stopped":
                        if old_deck_status != "stopped":
                            try:
                                self.file_handle.close()
                                del self.file_handle
                            except:
                                pass
                            self.chunk_number = 0
                            self.current_duration_milliseconds = 0

                            #convert to mp3
                            slice = AudioSegment.from_file(self.filename)
                            dt = len(slice)
                            dt_human = convert_time_function.convert_duration_from_milliseconds_to_human(dt)
                            saved_path = self.filename.replace(".wav",".mp3")
                            export_file_handle = slice.export(saved_path,format="mp3")
                            #just for backup don't delete wav file
                            #os.remove(self.filename)
                            record = {
                                "start_datetime":self.start_datetime_str,
                                "title":self.title,
                                "description":self.title,
                                "volume":100,
                                "normalize":0,
                                "pan":0,
                                "low_frequency":20,
                                "high_frequency":20000,
                                "duration_milliseconds":dt,
                                "duration_human":dt_human,
                                "saved_path":saved_path,
                                "vote":10
                            }
                            record = database_functions.import_record_file(record)
                            del self.start_datetime_str
                        self.to_emitter.send({"type":"record-end"})
            if self.deck_status == "recording":
                if slice is not None:
                    self.file_handle.writeframes(slice.raw_data)

                    self.chunk_number += 1
                    self.current_duration_milliseconds += 125
                    self.current_duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(self.current_duration_milliseconds)
                    self.to_emitter.send({"type":"current-duration","duration":self.current_duration_human})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})