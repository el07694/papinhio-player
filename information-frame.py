from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5 import QtCore
from multiprocessing import Process, Queue, Pipe
from datetime import datetime, timedelta
import traceback
import sys
import pyaudio
import psutil
import wmi

sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
sys.path.append("../../../../")
sys.path.append("../../../../../")
sys.path.append("../../../../../../")
sys.path.append("../../../../../../..")

import importlib

database_functions = importlib.import_module("python+.lib.sqlite3-functions")

class Information_Frame:

    def __init__(self, main_self):
        try:
            self.main_self = main_self

            # create process
            self.process_number = 97
            self.information_frame_mother_pipe, self.information_frame_child_pipe = Pipe()
            self.information_frame_queue = Queue()
            self.information_frame_emitter = Information_Frame_Emitter(self.information_frame_mother_pipe)
            self.information_frame_emitter.error_signal.connect(lambda error_message: self.main_self.open_information_frame_error_window(error_message))
            self.information_frame_emitter.visitors_signal.connect(lambda value: self.display_visitors(value))
            self.information_frame_emitter.cpu_percentage.connect(lambda value: self.display_cpu(value))
            self.information_frame_emitter.current_datetime.connect(lambda value: self.display_datetime(value))
            self.information_frame_emitter.temperature.connect(lambda value: self.display_temperature(value))
            self.information_frame_emitter.ram.connect(lambda value: self.display_ram(value))

            self.information_frame_emitter.start()
            self.information_frame_child_process = Information_Frame_Child_Proc(self.information_frame_child_pipe, self.information_frame_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.information_frame_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.information_frame_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})
        except:
            error_message = traceback.format_exc()
            self.main_self.open_information_frame_error_window(error_message)

    def display_visitors(self,value):
        try:
            self.main_self.ui.label_2.setText("Σύνολο ακροατών: "+str(value))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_information_frame_error_window(error_message)

    def display_cpu(self,value):
        try:
            self.main_self.ui.label_3.setText("CPU: "+str(value)+" %")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_information_frame_error_window(error_message)

    def display_datetime(self,value):
        try:
            self.main_self.ui.label.setText(str(value))
        except:
            error_message = traceback.format_exc()
            self.main_self.open_information_frame_error_window(error_message)

    def display_temperature(self,value):
        try:
            self.main_self.ui.label_4.setText("Θερμοκρασία CPU: "+str(value)+" °C")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_information_frame_error_window(error_message)

    def display_ram(self,value):
        try:
            self.main_self.ui.label_5.setText("RAM: "+str(value)+" %")
        except:
            error_message = traceback.format_exc()
            self.main_self.open_information_frame_error_window(error_message)

    def close(self):
        try:
            self.information_frame_queue.put({"type":"close"})
            try:
                if self.information_frame_child_process is not None:
                    #self.information_frame_child_process.join()
                    self.information_frame_child_process.terminate()
                    self.information_frame_child_process.close()
            except Exception as e:
                pass
            try:
                if self.information_frame_emitter is not None:
                    self.information_frame_emitter.quit()
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
            self.main_self.open_information_frame_error_window(error_message)

class Information_Frame_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        visitors_signal = pyqtSignal(int)
        cpu_percentage = pyqtSignal(int)
        current_datetime = pyqtSignal(str)
        temperature = pyqtSignal(int)
        ram = pyqtSignal(float)
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
                    self.data_from_process.close()
                    break
                elif data["type"] == "visitors_signal":
                    self.visitors_signal.emit(data["value"])
                elif data["type"] == "cpu_percentage":
                    self.cpu_percentage.emit(int(data["value"]))
                elif data["type"] == "current_datetime":
                    self.current_datetime.emit(data["value"])
                elif data["type"] == "temperature":
                    self.temperature.emit(data["value"])
                elif data["type"] == "ram":
                    self.ram.emit(data["value"])
        except Exception as e:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)

class Information_Frame_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.data_from_mother = from_mother
            self.total_visitors = None
            self.cpu_percent = None
            self.now_str = None
            self.temperature_value = None
            self.ram_value = None
        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.put({"type": "error", "error_message": error_message})
            except Exception as e:
                pass

    def run(self):
        try:
            current_frame = 0
            while (True):
                with self.condition:
                    self.condition.wait_for(lambda: current_frame <= self.frame_number.value)
                    if self.quit_event.is_set():
                        return None
                self.one_chunk()
                current_frame += 1

        except Exception as e:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def one_chunk(self):
        try:
            qsize = self.data_from_mother.qsize()
            if qsize>0:
                data = self.data_from_mother.get()
            else:
                data = None
            if data is not None:
                if data["type"] == "close":
                    self.to_emitter.send({"type": "close"})
                    #self.quit_event.set()

            self.count_visitors()
            self.cpu_percentage()
            self.current_datetime()
            #self.temperature()
            self.ram_usage()

        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def count_visitors(self):
        try:
            total_visitors = 0
            if total_visitors != self.total_visitors:
                self.total_visitors = total_visitors
                self.to_emitter.send({"type":"visitors_signal","value":self.total_visitors})
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def cpu_percentage(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent != self.cpu_percent:
                self.cpu_percent = cpu_percent
                self.to_emitter.send({"type":"cpu_percentage","value":self.cpu_percent})
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def current_datetime(self):
        try:
            now = datetime.now()
            month = int(now.strftime("%m"))
            if month == 1:
                month = "Ιανουαρίου"
            elif month == 2:
                month = "Φεβρουαρίου"
            elif month == 3:
                month = "Μαρτίου"
            elif month == 4:
                month = "Απριλίου"
            elif month == 5:
                month = "Μαϊου"
            elif month == 6:
                month = "Ιουνίου"
            elif month == 7:
                month = "Ιουλίου"
            elif month == 8:
                month = "Αυγούστου"
            elif month == 9:
                month = "Σεπτεμβρίου"
            elif month == 10:
                month = "Οκτωβρίου"
            elif month == 11:
                month = "Νοεμβρίου"
            elif month == 12:
                month = "Δεκεμβρίου"
            day = now.strftime("%d")
            week_day = now.strftime("%A")
            if week_day == "Monday":
                week_day = "Δευτέρα"
            elif week_day == "Tuesday":
                week_day = "Τρίτη"
            elif week_day == "Wednesday":
                week_day = "Τετάρτη"
            elif week_day == "Thursday":
                week_day = "Πέμπτη"
            elif week_day == "Friday":
                week_day = "Παρασκευή"
            elif week_day == "Saturday":
                week_day = "Σάββατο"
            elif week_day == "Sunday":
                week_day = "Κυριακή"

            year = now.strftime("%Y")
            hour = now.strftime("%H")
            minute = now.strftime("%M")
            second = now.strftime("%S")
            now_str = str(week_day)+" "+str(day)+" "+str(month)+" "+str(year)+" "+str(hour)+":"+str(minute)+":"+str(second)
            if now_str != self.now_str:
                self.now_str = now_str
                self.to_emitter.send({"type":"current_datetime","value":now_str})
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def temperature(self):
        try:
            #w = wmi.WMI(namespace='root\\wmi')
            #temperature = w.MSAcpi_ThermalZoneTemperature()[0]
            #temperature_value = int(temperature.CurrentTemperature / 10.0 - 273.15)
            temperature_value = 0
            if temperature_value!= self.temperature_value:
                self.temperature_value = temperature_value
                self.to_emitter.send({"type":"temperature","value":self.temperature_value})
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

    def ram_usage(self):
        try:
            ram_value = psutil.virtual_memory().percent
            if ram_value != self.ram_value:
                self.ram_value = ram_value
                self.to_emitter.send({"type": "ram", "value": self.ram_value})
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})
