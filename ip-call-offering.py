import time

from PyQt5.QtCore import pyqtSignal, QThread, Qt
from multiprocessing import Process, Queue, Pipe
import os
import traceback
from pydub import AudioSegment,generators
import pyaudio
import sys
from datetime import datetime
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


class Support_Ui_Dialog:

    def __init__(self, main_self, call_number,name,surname):
        try:
            self.main_self = main_self
            self.call_number = call_number
            self.name = name
            self.surname = surname

            self.call_answered = False

            # apply theme
            self.main_self.ip_call_offering_window.setStyleSheet(
                "*{font-family:" + self.main_self.default_font + ";font-size:" + self.main_self.default_font_size + "px;color:" + self.main_self.default_font_color + ";}QDialog{background:" + self.main_self.default_background_color + "}QPushButton, QComboBox{background:" + self.main_self.default_buttons_background + ";color:" + self.main_self.default_buttons_font_color + "}")

            self.main_self.ui_ip_call_offering_window.label.setText("Έχετε τηλεφωνική κλήση από τον ακροατή "+str(name)+" "+str(surname)+" .\nΠαρακαλώ διαχειριστείτε την κλήση με τους ακόλουθους τρόπους:")
            self.main_self.ui_ip_call_offering_window.local_answer.clicked.connect(lambda :self.local_answer())
            self.main_self.ui_ip_call_offering_window.public_answer.clicked.connect(lambda :self.public_answer())
            self.main_self.ui_ip_call_offering_window.ignore_call.clicked.connect(lambda :self.ignore_call())

            # create process
            self.process_number = 105
            self.ip_call_offering_mother_pipe, self.ip_call_offering_child_pipe = Pipe()
            self.ip_call_offering_queue = Queue()
            self.ip_call_offerring_emitter = Ip_Call_Offering_Emitter(self.ip_call_offering_mother_pipe)
            self.ip_call_offerring_emitter.error_signal.connect(lambda error_message: self.main_self.open_ip_calls_error_window(error_message))
            self.ip_call_offerring_emitter.close.connect(lambda: self.main_self.ip_call_offering_window.close())

            self.ip_call_offerring_emitter.start()
            self.ip_call_offering_child_process = Ip_Call_Offering_Child_Proc(
                self.ip_call_offering_child_pipe, self.ip_call_offering_queue)
            self.ip_call_offering_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.ip_call_offering_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})


            self.main_self.ip_call_offering_window.closeEvent = lambda event: self.closeEvent(event)
        except:
            error = traceback.format_exc()
            print(error)
            self.main_self.ip_call_offering_window.close()
            self.main_self.open_ip_calls_error_window(error)

    def local_answer(self):
        try:
            self.ip_call_offering_queue.put({"type": "stop-process"})
            time.sleep(0.125)
            self.main_self.ip_calls_instance.local_answer(self.call_number, self.name, self.surname)
            self.call_answered = True
            self.main_self.ip_call_offering_window.close()
        except:
            error = traceback.format_exc()
            print(error)
            self.main_self.ip_call_offering_window.close()
            self.main_self.open_ip_calls_error_window(error)


    def public_answer(self):
        try:
            self.ip_call_offering_queue.put({"type": "stop-process"})
            time.sleep(0.125)
            self.main_self.ip_calls_instance.public_answer(self.call_number,self.name,self.surname)
            self.call_answered = True
            self.main_self.ip_call_offering_window.close()
        except:
            error = traceback.format_exc()
            print(error)
            self.main_self.ip_call_offering_window.close()
            self.main_self.open_ip_calls_error_window(error)

    def ignore_call(self):
        try:
            self.ip_call_offering_queue.put({"type": "stop-process"})
            time.sleep(0.125)
            self.main_self.ip_calls_instance.reject_call(self.call_number,None)
            self.call_answered = True
            self.main_self.ip_call_offering_window.close()
        except:
            error = traceback.format_exc()
            print(error)
            self.main_self.ip_call_offering_window.close()
            self.main_self.open_ip_calls_error_window(error)

    def closeEvent(self, event):
        try:
            if self.call_answered == False:
                self.ip_call_offering_queue.put({"type":"stop-process"})
                time.sleep(0.125)
                self.main_self.ip_calls_instance.reject_call(self.call_number, None)
            try:
                if self.ip_call_offering_child_process is not None:
                    self.ip_call_offering_child_process.terminate()
                    self.ip_call_offering_child_process.close()
            except:
                pass
            try:
                if self.ip_call_offerring_emitter is not None:
                    self.ip_call_offerring_emitter.quit()
            except:
                pass

            try:
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
                pass
        except:
            print(traceback.format_exc())

        self.main_self.ip_call_offering_window_is_open = False
        event.accept()

class Ip_Call_Offering_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        close = pyqtSignal()
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
                elif data["type"] == "close":
                    self.close.emit()
                    break
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.error_signal.emit(error_message)


class Ip_Call_Offering_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.data_from_mother = from_mother
        except:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.send({"type": "error", "error_message": error_message})
            except:
                pass

    def run(self):
        try:
            self.fetch_output_devices()

            self.bit_rate = 128 * 1024  # 128 kb/sec
            # self.packet_time = 744
            self.packet_time = 125
            self.packet_size = 1024
            self.new_sample_rate = 44800
            self.TIME_WINDOW = 3000

            self.format = pyaudio.paInt16
            self.channels = 2

            self.stream = None
            if self.secondary_output_device_number !="Καμία συσκευή αναπαραγωγής ήχου":
                for output_device in self.output_devices:
                    if (self.secondary_output_device_name == output_device[2]):
                        self.output_device_index = output_device[1]
                        self.stream = self.p.open(format=pyaudio.paInt16, channels=self.channels,
                                                  rate=self.new_sample_rate, output=True,
                                                  output_device_index=self.output_device_index,
                                                  frames_per_buffer=self.packet_size)
                        self.stream.start_stream()
                        self.play_status = "playing"
                        self.chunk_number = 0
                        self.current_duration_milliseconds = 0

            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                self.www_root_folder = os.path.abspath("extra-files/ip_calls")
            else:
                self.www_root_folder = os.path.abspath("../../../exe/extra-files/ip_calls")

            intro_path = os.path.join(self.www_root_folder, "telephone_calls.mp3")

            self.audio_segment = AudioSegment.from_file(intro_path, format="mp3").set_frame_rate(
                self.new_sample_rate)
            self.total_duration_milliseconds = len(self.audio_segment)

            sine_segment = generators.Sine(1000).to_audio_segment()
            sine_segment = sine_segment.set_frame_rate(self.new_sample_rate)
            sine_segment = sine_segment[
                           (1000 - int(self.packet_time)) / 2:self.packet_time + (1000 - int(self.packet_time)) / 2]
            self.silent_segment = sine_segment - 200
            self.process_stopped = False

            while (self.process_stopped == False):
                q_size = self.data_from_mother.qsize()
                if q_size > 0:
                    data = self.data_from_mother.get()
                else:
                    data = None
                if data is not None:
                    if data["type"] == "stop-process":
                        self.process_stopped = True

                        self.play_status = "stopped"
                        self.chunk_number = 0
                        self.current_duration_milliseconds = 0
                        try:
                            self.stream.stop_stream()
                            self.stream.close()
                        except:
                            pass
                        return 1

                if ((self.chunk_number + 1) * (self.packet_time) <= self.total_duration_milliseconds):
                    slice = self.audio_segment[
                            self.chunk_number * (self.packet_time):(self.chunk_number + 1) * (self.packet_time)]
                else:
                    if ((self.chunk_number) * (self.packet_time) < self.current_duration_milliseconds):
                        slice = self.audio_segment[self.chunk_number * (self.packet_time):]
                    else:
                        slice = self.silent_segment
                        self.chunk_number = 0
                if self.stream is not None:
                    self.stream.write(slice.raw_data)
                self.chunk_number += 1
                self.current_duration_milliseconds += self.packet_time
                if self.current_duration_milliseconds>=1000*30:
                    self.to_emitter.send({"type":"close"})
                    return None
        except:
            error_message = str(traceback.format_exc())
            print(error_message)
            self.to_emitter.send({"type": "error", "error_message": error_message})

    # Gets from database the output device settings
    def fetch_output_devices(self):
        try:
            sys.path.append("../../../..")
            self.database_functions = database_functions
            # self.database_functions = importlib.import_module("Αρχεία κώδικα python (Python files).Συναρτήσεις sqlite3 (Sqlite3 functions)")

            self.primary_output_device_name = self.database_functions.read_setting("primary_output_device_name")[
                "value"]
            self.primary_output_device_number = int(
                self.database_functions.read_setting("primary_output_device_number")["value"])
            self.secondary_output_device_name = self.database_functions.read_setting("secondary_output_device_name")[
                "value"]
            self.secondary_output_device_number = int(
                self.database_functions.read_setting("secondary_output_device_number")["value"])

            self.p = pyaudio.PyAudio()
            self.info = self.p.get_host_api_info_by_index(0)
            self.numdevices = self.info.get('deviceCount')

            self.output_devices = [[0, -1, "Καμία συσκευή αναπαραγωγής ήχου"]]

            api_info, api_index = self.get_api_info(self.p)
            api_name = api_info['name']
            PREFERRED_HOST_API_NAME = 'Windows WASAPI'
            if api_name != PREFERRED_HOST_API_NAME:
                print(f'[WARNING] "{PREFERRED_HOST_API_NAME}" not available on this system, '
                      f'going with "{api_name}" instead')

            numdevices = api_info.get('deviceCount')

            counter = 1
            for i in range(0, self.numdevices):
                dev_info = self.p.get_device_info_by_host_api_device_index(0, i)
                if dev_info.get('maxOutputChannels') > 0:
                    device_name_cropped = str(dev_info.get('name'))
                    for j in range(0, numdevices):
                        one_dev_info = self.p.get_device_info_by_host_api_device_index(api_index, j)
                        if one_dev_info.get('maxOutputChannels') > 0:
                            one_device_name = str(one_dev_info.get('name'))
                            if device_name_cropped in one_device_name:
                                device_name_cropped = one_device_name
                                break

                    self.output_devices.append([counter, i, device_name_cropped])
                    counter += 1

            self.to_emitter.send({"type": "available_devices", "devices": self.output_devices,
                                  "primary_device_index": self.primary_output_device_number,
                                  "secondary_device_index": self.secondary_output_device_number})
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def get_api_info(self, p):
        PREFERRED_HOST_API_NAME = 'Windows WASAPI'
        api_info, api_index = None, 0
        for i in range(p.get_host_api_count()):
            current_api_info = p.get_host_api_info_by_index(i)
            if i == 0:
                api_info = current_api_info
            else:
                if current_api_info['name'] == PREFERRED_HOST_API_NAME:
                    api_info, api_index = current_api_info, i
                    break
        return api_info, api_index