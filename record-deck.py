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
from enum import Enum
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


class DeckStatus(Enum):
    STOPPED = "stopped"
    RECORDING = "recording"


class Record_Deck_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother, final_slice_queue, secondary_slice_queue, condition, frame_number,
                 quit_event):
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

            self.ip_calls = [
                {"call_number": i + 1, "deck_status": DeckStatus.STOPPED, "name": "", "surname": "", "is_local": None}
                for i in range(3)]

        except Exception as e:
            error_message = f"Initialization error: {str(e)}"
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def run(self):
        try:
            current_frame = 0
            while True:
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return None
                result = self.one_chunk()
                if result == "break":
                    return None
                current_frame += 1
        except Exception as e:
            error_message = f"Run loop error: {str(e)}"
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def one_chunk(self):
        try:
            data = self._get_data_from_mother()
            if data:
                return self._process_data(data)

            final_slice = self._get_final_slice()
            secondary_slice = self._get_secondary_slice()

            self._write_to_files(final_slice, secondary_slice)

        except Exception as e:
            error_message = f"Error processing chunk: {str(e)}"
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def _get_data_from_mother(self):
        if self.data_from_mother.qsize() > 0:
            return self.data_from_mother.get()
        return None

    def _process_data(self, data):
        if data["type"] == "close":
            self.to_emitter.send({"type": "close"})
            return "break"
        elif data["type"] == "new-status":
            return self._process_new_status(data)
        elif data["type"] == "update-is-local":
            return self._update_is_local(data)

    def _process_new_status(self, data):
        status = data["status"]
        if status == DeckStatus.STOPPED.value:
            self._stop_all_or_specific(data)
        else:
            self._start_recording(data)

    def _stop_all_or_specific(self, data):
        if "call-number" not in data:
            self.stop_recording(1)
            self.stop_recording(2)
            self.stop_recording(3)
            self.to_emitter.send({"type": "all-records-end"})
        else:
            self.stop_recording(data["call-number"])

    def _start_recording(self, data):
        call_number = data["details"]["call-number"]
        name = data["details"]["name"]
        surname = data["details"]["surname"]
        self.ip_calls[call_number - 1]["deck_status"] = DeckStatus.RECORDING
        self.ip_calls[call_number - 1]["name"] = name
        self.ip_calls[call_number - 1]["surname"] = surname
        self.ip_calls[call_number - 1]["is_local"] = data["details"]["is_local"]

        now = datetime.now()
        start_datetime_str = now.strftime("%d-%m-%Y %H:%M:%S")
        self.ip_calls[call_number - 1]["start_datetime_str"] = start_datetime_str
        title = f"Ηχητική κλήση από τον ακροατή: {name} {surname} ({now.strftime('%d-%m-%Y %H-%M-%S')})"
        self.ip_calls[call_number - 1]["title"] = title
        filename = title.replace(":", "_") + ".wav"

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = os.path.abspath(os.path.join("files", "ip-calls", filename))
        else:
            filename = os.path.abspath("files/ip-calls/" + filename)

        self.ip_calls[call_number - 1]["filename"] = filename
        self._initialize_file_handle(call_number, filename)

    def _initialize_file_handle(self, call_number, filename):
        p = pyaudio.PyAudio()
        self.ip_calls[call_number - 1]["file_handle"] = wave.open(filename, 'wb')
        self.ip_calls[call_number - 1]["file_handle"].setnchannels(2)
        self.ip_calls[call_number - 1]["file_handle"].setsampwidth(p.get_sample_size(pyaudio.paInt16))
        self.ip_calls[call_number - 1]["file_handle"].setframerate(44100)

    def _update_is_local(self, data):
        call_number = data["call-number"]
        self.ip_calls[call_number - 1]["is_local"] = data["is_local"]

    def _get_final_slice(self):
        return self.final_slice_queue.get()["slice"] if self.final_slice_queue.qsize() > 0 else AudioSegment.empty()

    def _get_secondary_slice(self):
        return self.secondary_slice_queue.get()[
            "slice"] if self.secondary_slice_queue.qsize() > 0 else AudioSegment.empty()

    def _write_to_files(self, final_slice, secondary_slice):
        for i in range(3):
            if self.ip_calls[i]["deck_status"] == DeckStatus.RECORDING:
                slice_to_write = secondary_slice if self.ip_calls[i]["is_local"] else final_slice
                self.ip_calls[i]["file_handle"].writeframes(slice_to_write.raw_data)

    def stop_recording(self, call_number):
        try:
            if self.ip_calls[call_number - 1]["deck_status"] != DeckStatus.RECORDING.value:
                return None

            self.ip_calls[call_number - 1]["deck_status"] = DeckStatus.STOPPED.value
            self.ip_calls[call_number - 1]["file_handle"].close()
            del self.ip_calls[call_number - 1]["file_handle"]

            self._convert_to_mp3(call_number)

        except Exception as e:
            error_message = f"Error stopping recording: {str(e)}"
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def _convert_to_mp3(self, call_number):
        try:
            slice = AudioSegment.from_file(self.ip_calls[call_number - 1]["filename"])
            duration_ms = len(slice)
            duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_ms)
            mp3_filename = self.ip_calls[call_number - 1]["filename"].replace(".wav", ".mp3")
            slice.export(mp3_filename, format="mp3")

            ip_call_item = {
                "is_const": 1,
                "title": self.ip_calls[call_number - 1]["title"],
                "name": self.ip_calls[call_number - 1]["name"],
                "surname": self.ip_calls[call_number - 1]["surname"],
                "real_start_datetime": self.ip_calls[call_number - 1]["start_datetime_str"],
                "duration": duration_human,
                "filename": mp3_filename,
            }
            self.to_emitter.send({"type": "add-to-list", "ip_call_item": ip_call_item})
        except Exception as e:
            error_message = f"Error during MP3 conversion: {str(e)}"
            self.to_emitter.send({"type": "error", "error_message": error_message})