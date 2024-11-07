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

            self.ip_calls = []
            for i in range(0,3):
                ip_call = {
                    "call_number":i+1,
                    "call-number":i+1,
                    "deck_status":"stopped",
                    "name":"",
                    "surname":"",
                    "is_local":None
                }
                self.ip_calls.append(ip_call)

            self.main_self.final_slice_instance.put_to_ip_record = False
            self.main_self.secondary_slice_instance.put_to_ip_record = False

            # create process
            self.process_number = 110
            self.record_deck_mother_pipe, self.record_deck_child_pipe = Pipe()
            self.record_deck_queue = Queue()
            self.final_slice_queue = Queue()
            self.secondary_slice_queue = Queue()
            self.record_deck_emitter = Record_Deck_Emitter(self.record_deck_mother_pipe)
            self.record_deck_emitter.error_signal.connect(lambda error_message: self.main_self.open_ip_calls_record_deck_error_window(error_message))
            self.record_deck_emitter.all_records_end.connect(lambda: self.all_records_end())


            self.record_deck_emitter.start()
            self.record_deck_child_process = Record_Deck_Child_Proc(self.record_deck_child_pipe, self.record_deck_queue,self.final_slice_queue,self.secondary_slice_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
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

            self.close_program = False
            self.restart_program = False
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    #called when all records end and before close or restart
    def all_records_end(self):
        try:
            for i in range(0,3):
                self.ip_calls[i]["deck_status"] = "stopped"

            self.main_self.final_slice_instance.put_to_ip_record = False
            self.main_self.secondary_slice_instance.put_to_ip_record = False

            if self.close_program:
                self.main_self.MainWindow.close()
            else:
                if self.restart_program:
                    self.main_self.restart_app()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    # stop all after close program requested
    def stop_and_close(self):
        try:
            if self.close_program:
                return None
            self.close_program = True
            self.record_deck_queue.put({"type":"new-status","status":"stopped"})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    # stop all after restart program requested
    def stop_and_restart(self):
        try:
            if self.restart_program:
                return None
            self.restart_program = True
            self.record_deck_queue.put({"type":"new-status","status":"stopped"})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    #Called when an ip call is started
    def start_record(self,call_number,name,surname,is_local):
        try:
            self.ip_calls[call_number-1]["deck_status"] = "recording"
            self.ip_calls[call_number-1]["name"] = name
            self.ip_calls[call_number-1]["surname"] = surname
            self.ip_calls[call_number-1]["is_local"] = is_local
            self.record_deck_queue.put({"type":"new-status","status":"recording","details":self.ip_calls[call_number-1]})
            if is_local:
                self.main_self.secondary_slice_instance.put_to_ip_record = True
            else:
                self.main_self.final_slice_instance.put_to_ip_record = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    def stop_record(self,call_number):
        try:
            self.record_deck_queue.put({"type": "new-status", "status": "stopped","call-number":call_number})
            total_locals = 0
            total_public = 0
            for ip_call in self.ip_calls:
                if ip_call["call_number"]!=call_number:
                    if ip_call["deck_status"] == "recording":
                        if ip_call["is_local"]:
                            total_locals += 1
                        else:
                            total_public += 1
            if total_locals == 0:
                self.main_self.secondary_slice_instance.put_to_ip_record = False
            if total_public == 0:
                self.main_self.final_slice_instance.put_to_ip_record = False
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    #call when active ip call is forwarded
    def set_is_local(self,call_number,is_local):
        try:
            self.ip_calls[call_number-1]["is_local"] = is_local
            self.record_deck_queue.put({"type":"update-is-local","is_local":is_local,"call-number":call_number})
            if is_local:
                self.main_self.secondary_slice_instance.put_to_ip_record = True
            else:
                self.main_self.final_slice_instance.put_to_ip_record = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

    def close(self):
        try:
            for i in range(0,3):
                if self.ip_calls[i]["deck_status"] == "recording":
                    self.ip_calls[i]["deck_status"] = "stopped"
                    self.record_deck_queue.put({"type": "new-status", "status": "stopped", "call-number": i+1})
            self.record_deck_queue.put({"type": "close"})
            time.sleep(0.125)
            try:
                if self.record_deck_child_process is not None:
                    self.record_deck_child_process.terminate()
                    self.record_deck_child_process.close()
            except:
                pass
            try:
                if self.record_deck_emitter is not None:
                    self.record_deck_emitter.quit()
            except:
                pass

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
            self.main_self.open_ip_calls_record_deck_error_window(error_message)

class Record_Deck_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        all_records_end = pyqtSignal()
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
                elif data["type"] == "all-records-end":
                    self.all_records_end.emit()
                elif data["type"] == "close":
                    break
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)


class Record_Deck_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,final_slice_queue,secondary_slice_queue,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
            self.final_slice_queue = final_slice_queue
            self.secondary_slice_queue = secondary_slice_queue
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event

            self.ip_calls = []
            for i in range(0, 3):
                ip_call = {
                    "call_number": i + 1,
                    "deck_status": "stopped",
                    "name": "",
                    "surname": "",
                    "is_local": None
                }
                self.ip_calls.append(ip_call)

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
                    return None
                current_frame += 1
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def one_chunk(self):
        try:
            q_size = self.data_from_mother.qsize()
            if q_size > 0:
                data = self.data_from_mother.get()
            else:
                data = None
            if data is not None:
                if data["type"] == "close":
                    self.to_emitter.send({"type": "close"})
                    return "break"
                elif data["type"] == "new-status":
                    status = data["status"]
                    if status == "stopped":
                        if "call-number" not in data:
                            #stop all
                            self.stop_recording(1)
                            self.stop_recording(2)
                            self.stop_recording(3)
                            self.to_emitter.send({"type":"all-records-end"})
                            return None
                        else:
                            #stop certain
                            call_number = data["call-number"]
                            self.stop_recording(call_number)
                    else:
                        #start recording
                        call_number = data["details"]["call-number"]
                        name = data["details"]["name"]
                        surname = data["details"]["surname"]
                        details = data["details"]
                        self.ip_calls[call_number-1]["deck_status"] = "recording"
                        self.ip_calls[call_number-1]["name"] = name
                        self.ip_calls[call_number-1]["surname"] = surname
                        self.ip_calls[call_number-1]["is_local"] = details["is_local"]

                        now = datetime.now()
                        start_datetime_str = now.strftime("%d-%m-%Y %H:%M:%S")
                        self.ip_calls[call_number - 1]["start_datetime_str"] = start_datetime_str
                        title = "Ηχητική κλήση από τον ακροατή: " + str(name) + " " + str(surname) + " (" + now.strftime("%d-%m-%Y %H-%M-%S") + ")"
                        self.ip_calls[call_number - 1]["title"] = title
                        data["filename"] = title.replace(":","_")
                        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                            filename = os.path.abspath(os.path.join("files","ip-calls",data["filename"]+".wav"))
                        else:
                            filename = os.path.abspath(os.path.join("../","../","../","files", "ip-calls", data["filename"] + ".wav"))
                        self.ip_calls[call_number - 1]["filename"] = filename
                        self.ip_calls[call_number - 1]["file_handle"] = wave.open(self.ip_calls[call_number - 1]["filename"], 'wb')
                        p = pyaudio.PyAudio()
                        self.ip_calls[call_number - 1]["file_handle"].setnchannels(2)
                        self.ip_calls[call_number - 1]["file_handle"].setsampwidth(p.get_sample_size(pyaudio.paInt16))
                        self.ip_calls[call_number - 1]["file_handle"].setframerate(44100)
                elif data["type"] == "update-is-local":
                    call_number = data["call-number"]
                    self.ip_calls[call_number-1]["is_local"] = data["is_local"]
            final_q_size = self.final_slice_queue.qsize()
            if final_q_size > 0:
                final_slice = self.final_slice_queue.get()["slice"]
            else:
                final_slice = AudioSegment.empty()

            secondary_q_size = self.secondary_slice_queue.qsize()
            if secondary_q_size > 0:
                secondary_slice = self.secondary_slice_queue.get()["slice"]
            else:
                secondary_slice = AudioSegment.empty()

            for i in range(0,3):
                if self.ip_calls[i]["deck_status"] == "recording":
                    if self.ip_calls[i]["is_local"]:
                        self.ip_calls[i]["file_handle"].writeframes(secondary_slice.raw_data)
                    else:
                        self.ip_calls[i]["file_handle"].writeframes(final_slice.raw_data)
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def stop_recording(self,call_number):
        try:
            if self.ip_calls[call_number-1]["deck_status"] != "recording":
                return None
            else:
                try:
                    self.ip_calls[call_number-1]["deck_status"] = "stopped"
                    self.ip_calls[call_number-1]["file_handle"].close()
                    del self.ip_calls[call_number-1]["file_handle"]
                except:
                    pass

                # convert to mp3
                slice = AudioSegment.from_file(self.ip_calls[call_number-1]["filename"])
                dt = len(slice)
                dt_human = convert_time_function.convert_duration_from_milliseconds_to_human(dt)
                saved_path = self.ip_calls[call_number-1]["filename"].replace(".wav", ".mp3")
                export_file_handle = slice.export(saved_path, format="mp3")
                # just for backup don't delete wav file
                # os.remove(self.filename)

                ip_call_item = {
                    "is_const": 1,
                    "title": self.ip_calls[call_number-1]["title"],
                    "name": self.ip_calls[call_number-1]["name"],
                    "surname": self.ip_calls[call_number-1]["surname"],
                    "scheduled_start_datetime": "",
                    "scheduled_duration_milliseconds": "",
                    "scheduled_duration_human": "",
                    "real_start_datetime": self.ip_calls[call_number-1]["start_datetime_str"],
                    "real_duration_milliseconds": dt,
                    "real_duration_human": dt_human,
                    "call_connection_password": "",
                    "volume": 20,
                    "normalize": 0,
                    "pan": 0,
                    "low_frequency": 20,
                    "high_frequency": 20000,
                    "saved_path": saved_path,
                    "vote": 10
                }
                ip_call_item = database_functions.import_ip_call_item(ip_call_item)
                del self.ip_calls[call_number-1]["start_datetime_str"]
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})
