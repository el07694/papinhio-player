from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from multiprocessing import Process, Queue, Pipe
import sys
from datetime import datetime, timedelta
import time
import traceback
from pydub import AudioSegment, effects, utils, generators
import math
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
from io import BytesIO
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


class Secondary_Slice:
    def __init__(self, main_self):
        try:
            self.main_self = main_self

            self.put_to_pyaudio = False

            # create process
            self.process_number = 102
            self.secondary_slice_mother_pipe, self.secondary_slice_child_pipe = Pipe()
            self.secondary_slice_queue = Queue()
            self.speackers_deck_secondary_queue = Queue()
            self.ip_call_1_queue = Queue()
            self.ip_call_2_queue = Queue()
            self.ip_call_3_queue = Queue()
            self.secondary_slice_emitter = Secondary_Slice_Emitter(self.secondary_slice_mother_pipe)
            self.secondary_slice_emitter.error_signal.connect(lambda error_message: self.main_self.open_secondary_slice_error_window(error_message))
            self.secondary_slice_emitter.secondary_slice_ready.connect(lambda slice: self.secondary_slice_ready(slice))


            self.secondary_slice_emitter.start()
            self.secondary_slice_child_process = Secondary_Slice_Child_Proc(
                self.secondary_slice_child_pipe, self.secondary_slice_queue,self.speackers_deck_secondary_queue,self.ip_call_1_queue,self.ip_call_2_queue,self.ip_call_3_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.secondary_slice_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.secondary_slice_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_secondary_slice_error_window(error_message)


    def secondary_slice_ready(self,slice):
        try:
            try:
                if "put_to_ip_record" in dir(self):
                    if self.put_to_ip_record:
                        self.main_self.ip_calls_record_deck_instance.secondary_slice_queue.put({"type":"slice","slice":slice})
                if self.put_to_pyaudio:
                    self.main_self.secondary_slice_pyaudio_instance.secondary_slice_pyaudio_queue.put(
                        {"type": "slice", "slice": slice})
            except RuntimeError as e:
                print(e)
            except:
                print(traceback.format_exc())
        except:
            error_message = traceback.format_exc()
            self.main_self.open_secondary_slice_error_window(error_message)

    def close(self):
        try:
            self.secondary_slice_queue.put({"type": "close"})
            try:
                if self.secondary_slice_child_process is not None:
                    self.secondary_slice_child_process.terminate()
                    self.secondary_slice_child_process.close()
            except:
                pass
            try:
                if self.secondary_slice_emitter is not None:
                    self.secondary_slice_emitter.quit()
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
            self.main_self.open_secondary_slice_error_window(error_message)

#CAUTION: no error window for final slice in this class!
class Custom_QFrame(QtWidgets.QFrame):
    def __init__(self, parent, *args, **kwargs):
        super(QtWidgets.QFrame, self).__init__(parent, *args, **kwargs)

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            return True
        return super(QtWidgets.QFrame, self).eventFilter(obj, event)


class Secondary_Slice_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        secondary_slice_ready = pyqtSignal(AudioSegment)
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
                elif data["type"] == "secondary_slice":
                    self.secondary_slice_ready.emit(data["slice"])
                elif data["type"] == "close":
                    break
        except:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)


class Secondary_Slice_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,speackers_deck_secondary_queue,ip_call_1_queue,ip_call_2_queue,ip_call_3_queue,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.speackers_deck_secondary_queue = speackers_deck_secondary_queue
            self.ip_call_1_queue = ip_call_1_queue
            self.ip_call_2_queue = ip_call_2_queue
            self.ip_call_3_queue = ip_call_3_queue

            self.packet_time = 125

            sine_segment = generators.Sine(1000).to_audio_segment()
            sine_segment = sine_segment.set_frame_rate(44100)
            sine_segment = sine_segment[(1000 - int(125)) / 2:125 + (1000 - int(125)) / 2]
            self.silent_segment = sine_segment - 200

        except:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.send({"type": "error", "error_message": error_message})
            except:
                pass

    def run(self):
        try:
            self.database_functions = database_functions

            current_frame = 0
            while (True):
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return
                self.one_chunk()
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

            q_size = self.speackers_deck_secondary_queue.qsize()
            if q_size > 0:
                data = self.speackers_deck_secondary_queue.get()
                speackers_deck_slice = data["slice"]
            else:
                data = None
                speackers_deck_slice = AudioSegment.empty()

            q_size = self.ip_call_1_queue.qsize()
            if q_size > 0:
                data = self.ip_call_1_queue.get()
                ip_call_1_slice = data["slice"]
            else:
                data = None
                ip_call_1_slice = AudioSegment.empty()

            q_size = self.ip_call_2_queue.qsize()
            if q_size > 0:
                data = self.ip_call_2_queue.get()
                ip_call_2_slice = data["slice"]
            else:
                data = None
                ip_call_2_slice = AudioSegment.empty()

            q_size = self.ip_call_3_queue.qsize()
            if q_size > 0:
                data = self.ip_call_3_queue.get()
                ip_call_3_slice = data["slice"]
            else:
                data = None
                ip_call_3_slice = AudioSegment.empty()

            slice = AudioSegment.empty()
            if slice == AudioSegment.empty():
                slice = speackers_deck_slice
            else:
                slice = slice.overlay(speackers_deck_slice)

            if slice == AudioSegment.empty():
                slice = ip_call_1_slice
            else:
                slice = slice.overlay(ip_call_1_slice)
            if slice == AudioSegment.empty():
                slice = ip_call_2_slice
            else:
                slice = slice.overlay(ip_call_2_slice)
            if slice == AudioSegment.empty():
                slice = ip_call_3_slice
            else:
                slice = slice.overlay(ip_call_3_slice)
            if slice == AudioSegment.empty():
                slice = self.silent_segment

            self.to_emitter.send({"type": "secondary_slice", "slice": slice})
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})

    # Use pydub effect to normalize the volume of a sound file
    def normalize_method(self, seg, headroom):
        try:
            peak_sample_val = seg.max

            # if the max is 0, this audio segment is silent, and can't be normalized
            if peak_sample_val == 0:
                return seg

            target_peak = seg.max_possible_amplitude * utils.db_to_float(-headroom)
            # target_peak = seg.max_possible_amplitude * (percent_headroom)

            needed_boost = utils.ratio_to_db(target_peak / peak_sample_val)
            return seg.apply_gain(needed_boost)
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.to_emitter.send({"type": "error", "error_message": error_message})
            return seg