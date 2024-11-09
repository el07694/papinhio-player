import time
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5 import QtCore
from multiprocessing import Process, Queue, Pipe
from datetime import datetime, timedelta
import traceback
import sys
import pyaudio

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")

import importlib

database_functions = importlib.import_module("python+.lib.sqlite3-functions")


class Final_Slice_PyAudio:

    def __init__(self, main_self):
        try:
            self.main_self = main_self

            # create process
            self.process_number = 95
            self.final_slice_pyaudio_mother_pipe, self.final_slice_pyaudio_child_pipe = Pipe()
            self.final_slice_pyaudio_queue = Queue()
            self.final_slice_pyaudio_emitter = Final_Slice_PyAudio_Emitter(self.final_slice_pyaudio_mother_pipe)
            self.final_slice_pyaudio_emitter.error_signal.connect(lambda error_message: self.main_self.open_final_slice_pyaudio_error_window(error_message))

            self.final_slice_pyaudio_emitter.start()
            self.final_slice_pyaudio_child_process = Final_Slice_PyAudio_Child_Proc(self.final_slice_pyaudio_child_pipe, self.final_slice_pyaudio_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.final_slice_pyaudio_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.final_slice_pyaudio_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.start_pyaudio())
            self.timer.setSingleShot(True)
            self.timer.start(1200)
        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_pyaudio_error_window(error_message)

    def start_pyaudio(self):
        try:
            self.main_self.final_slice_instance.put_to_pyaudio = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_pyaudio_error_window(error_message)

    def close(self):
        try:
            self.final_slice_pyaudio_queue.put({"type":"close"})
            try:
                if self.final_slice_pyaudio_child_process is not None:
                    self.final_slice_pyaudio_child_process.terminate()
                    self.final_slice_pyaudio_child_process.close()
            except Exception as e:
                pass
            try:
                if self.final_slice_pyaudio_emitter is not None:
                    self.final_slice_pyaudio_emitter.quit()
            except Exception as e:
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
            self.main_self.open_final_slice_pyaudio_error_window(error_message)

class Final_Slice_PyAudio_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
    except Exception as e:
        pass

    def __init__(self, from_process: Pipe):
        try:
            super().__init__()
            self.data_from_process = from_process
        except Exception as e:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)

    def run(self):
        try:
            while True:
                data = self.data_from_process.recv()
                if data["type"] == "error":
                    self.error_signal.emit(data["error_message"])
                elif data["type"]=="close":
                    break
        except Exception as e:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)

class Final_Slice_PyAudio_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.data_from_mother = from_mother
            self.stream = None

        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.put({"type": "error", "error_message": error_message})
            except Exception as e:
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

            if self.primary_output_device_name != "Καμία συσκευή αναπαραγωγής ήχου":
                for output_device in self.output_devices:
                    if (self.primary_output_device_name == output_device[2]):
                        self.output_device_index = output_device[1]
                        self.stream = self.p.open(format=pyaudio.paInt16, channels=self.channels, rate=self.new_sample_rate,output=True, output_device_index=self.output_device_index,frames_per_buffer=self.packet_size)
                        self.stream.start_stream()

            current_frame = 0
            while (True):
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return None
                w = self.one_chunk()
                if w is None:
                    pass
                else:
                    return None
                current_frame += 1

        except Exception as e:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def one_chunk(self):
        try:
            data = self.data_from_mother.get()
            slice = None
            if data["type"] == "slice":
                slice = data["slice"]
            elif data["type"] == "close":
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
                except:
                    pass
                self.to_emitter.send({"type": "close"})
                return "break"
                #self.quit_event.set()
            elif data["type"] == "update-sound-device":
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
                except:
                    pass
                self.fetch_output_devices()
                if self.primary_output_device_name != "Καμία συσκευή αναπαραγωγής ήχου":
                    for output_device in self.output_devices:
                        if (self.primary_output_device_name == output_device[2]):
                            self.output_device_index = output_device[1]
                            self.stream = self.p.open(format=pyaudio.paInt16, channels=self.channels, rate=self.new_sample_rate,output=True, output_device_index=self.output_device_index,frames_per_buffer=self.packet_size)
                            self.stream.start_stream()
            else:
                self.quit_event.set()
            if slice is not None:
                if self.stream is not None:
                    self.stream.write(slice.raw_data)
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})


    # Gets from database the output device settings
    def fetch_output_devices(self):
        try:
            self.database_functions = database_functions
            self.primary_output_device_name = self.database_functions.read_setting("primary_output_device_name")["value"]
            self.primary_output_device_number = int(self.database_functions.read_setting("primary_output_device_number")["value"])

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


        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})


    def get_api_info(self, p):
        try:
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
        except:
            error_message = traceback.format_exc()
            self.to_emitter.send({"type": "error", "error_message": error_message})
