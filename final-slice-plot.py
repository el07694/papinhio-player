import time
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5 import QtCore
from multiprocessing import Process, Queue, Pipe
from datetime import datetime, timedelta
import traceback
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.dates import num2date
from matplotlib.ticker import FuncFormatter
import numpy as np


class Final_Slice_Plot:

    def __init__(self, main_self):
        try:
            self.main_self = main_self

            # chart
            self.chart = Canvas(self)
            self.chart.ax.set_facecolor((1, 1, 1))
            self.chart.ax.tick_params(labelcolor='white')

            # create process
            self.process_number = 94
            self.final_slice_plot_mother_pipe, self.final_slice_plot_child_pipe = Pipe()
            self.final_slice_plot_queue = Queue()
            self.final_slice_plot_emitter = Final_Slice_Plot_Emitter(self.final_slice_plot_mother_pipe)
            self.final_slice_plot_emitter.error_signal.connect(lambda error_message: self.main_self.open_final_slice_plot_error_window(error_message))
            self.final_slice_plot_emitter.plot_data_signal.connect(lambda x,y: self.plot(x,y))

            self.final_slice_plot_emitter.start()
            self.final_slice_plot_child_process = Final_Slice_Plot_Child_Proc(self.final_slice_plot_child_pipe, self.final_slice_plot_queue,self.main_self.condition, self.main_self.frame, self.main_self.quit_event)
            self.final_slice_plot_child_process.start()

            counter = 0
            for process in self.main_self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"] == self.process_number:
                        self.main_self.manage_processes_instance.processes[counter][
                            "pid"] = self.final_slice_plot_child_process.pid
                        self.main_self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                        self.main_self.manage_processes_instance.processes[counter]["status"] = "in_progress"
                counter += 1

            if self.main_self.manage_proccesses_window_is_open:
                self.main_self.manage_proccesses_window_support_code.manage_proccesses_queue.put(
                    {"type": "table-update", "processes": self.main_self.manage_processes_instance.processes})

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.start_plot())
            self.timer.setSingleShot(True)
            self.timer.start(1200)
        except:
            error_message = traceback.format_exc()
            print("ERROR")
            self.main_self.open_final_slice_plot_error_window(error_message)

    def start_plot(self):
        try:
            self.main_self.final_slice_instance.put_to_plot = True
        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_plot_error_window(error_message)

    def clearLayout(self,layout):
        try:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_plot_error_window(error_message)

    def close(self):
        try:
            self.final_slice_plot_queue.put({"type":"close"})
            try:
                if self.final_slice_plot_child_process is not None:
                    self.final_slice_plot_child_process.terminate()
                    self.final_slice_plot_child_process.close()
            except Exception as e:
                pass
            try:
                if self.final_slice_plot_emitter is not None:
                    self.final_slice_plot_emitter.quit()
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
            self.clear_plot()
        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_plot_error_window(error_message)

    # signal for plot_data_signal
    def plot(self, x_vals,y_vals):
        try:
            self.chart.li.set_xdata(x_vals)
            self.chart.li.set_ydata(y_vals)

            x_ticks = []
            if (len(x_vals) > 0):
                for i in range(499, 2500 + 1, 1000):
                    tick = x_vals[0] + timedelta(milliseconds=i)
                    x_ticks.append(tick)
                plt.xticks(x_ticks)

            self.chart.ax.set_xlim(x_vals[0], x_vals[0] + timedelta(milliseconds=3000))
            self.chart.ax.xaxis.set_major_formatter(FuncFormatter(self.date_formatter_1))

            self.chart.fig.canvas.draw()
            self.chart.fig.canvas.flush_events()

        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_plot_error_window(error_message)

# Clear the matplotlib plot
    def clear_plot(self):
        try:
            x_vals = [datetime.now()]
            y_vals = [0]

            self.chart.li.set_xdata(x_vals)
            self.chart.li.set_ydata(y_vals)

            x_ticks = []
            if (len(x_vals) > 0):
                for i in range(499, 2500 + 1, 1000):
                    tick = x_vals[0] + timedelta(milliseconds=i)
                    x_ticks.append(tick)
                plt.xticks(x_ticks)

                self.chart.ax.set_xlim(x_vals[0], x_vals[0] + timedelta(milliseconds=3000))

            self.chart.ax.xaxis.set_major_formatter(FuncFormatter(self.date_formatter_1))

            self.chart.fig.canvas.draw()
            self.chart.fig.canvas.flush_events()

        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_plot_error_window(error_message)

    # Formats the x-axis of matplotlib plot
    def date_formatter_1(self, a, b):
        try:
            t = num2date(a)
            ms = str(t.microsecond)[:1]
            res = f"{t.hour:02}:{t.minute:02}:{t.second:02}.{ms}"
            # res = f"{t.hour:02}:{t.minute:02}:{t.second:02}"
            return res
        except:
            error_message = traceback.format_exc()
            self.main_self.open_final_slice_plot_error_window(error_message)

class Final_Slice_Plot_Emitter(QThread):
    try:
        error_signal = pyqtSignal(str)
        plot_data_signal = pyqtSignal(np.ndarray,np.ndarray)
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
                '''if self.data_from_process.poll():
                    data = self.data_from_process.recv()
                else:
                    time.sleep(0.1)
                    continue
                '''
                data = self.data_from_process.recv()
                if data["type"] == "error":
                    self.error_signal.emit(data["error_message"])
                elif data["type"] == "plot_data":
                    self.plot_data_signal.emit(data["x"], data["y"])
                elif data["type"]=="close":
                    break
        except Exception as e:
            error_message = traceback.format_exc()
            self.error_signal.emit(error_message)

class Final_Slice_Plot_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother,condition, frame_number, quit_event):
        try:
            super().__init__()
            self.daemon = False
            self.to_emitter = to_emitter
            self.condition = condition
            self.frame_number = frame_number
            self.quit_event = quit_event
            self.data_from_mother = from_mother

        except Exception as e:
            try:
                error_message = str(traceback.format_exc())
                to_emitter.put({"type": "error", "error_message": error_message})
            except Exception as e:
                pass

    def run(self):
        try:
            self.TIME_WINDOW = 3000
            self.chunk_number = 0
            self.current_duration_milliseconds = 0
            self.now = datetime.now()
            self.x_vals = np.array([])
            self.y_vals = np.array([])
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
            if data["type"] == "slice":
                slice = data["slice"]
            elif data["type"] == "close":
                self.to_emitter.send({"type": "close"})
                self.chunk_number = 0
                self.current_duration_milliseconds = 0
                self.x_vals = np.array([])
                self.y_vals = np.array([])
                return "break"
                #self.quit_event.set()
            else:
                #self.quit_event.set()
                pass

            chunk_time = len(slice)
            samples = slice.get_array_of_samples()
            left_samples = samples[::2]
            right_samples = samples[1::2]
            left_audio_data = np.frombuffer(left_samples, np.int16)[::128]  # down sampling
            right_audio_data = np.frombuffer(right_samples, np.int16)[::128]  # down sampling
            audio_data = np.vstack((left_audio_data, right_audio_data)).ravel('F')

            time_data = np.array([])
            for i in range(0, len(audio_data)):
                time_data = np.append(time_data, self.now)
                self.now = self.now + timedelta(milliseconds=chunk_time / len(audio_data))

            self.x_vals = np.concatenate((self.x_vals, time_data))
            self.y_vals = np.concatenate((self.y_vals, audio_data))

            if (self.x_vals.size > audio_data.size * (self.TIME_WINDOW / chunk_time)):
                self.x_vals = self.x_vals[audio_data.size:]
                self.y_vals = self.y_vals[audio_data.size:]

            self.to_emitter.send({"type": "plot_data", "x": self.x_vals, "y": self.y_vals})
            self.now = datetime.now()

            self.chunk_number += 1
            self.current_duration_milliseconds += chunk_time
        except:
            error_message = str(traceback.format_exc())
            self.to_emitter.send({"type": "error", "error_message": error_message})

class Canvas(FigureCanvas):

    def __init__(self, parent):
        try:
            self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
            super().__init__(self.fig)

            self.fig.patch.set_facecolor((6 / 255, 21 / 255, 154 / 255))

            self.ax.set_position([0., 0, 1., 0.8])
            self.ax.xaxis.tick_top()
            self.ax.tick_params(axis='both', which='major', pad=1, length=2.4, width=0.5, color=(1, 1, 1))

            parent.clearLayout(parent.main_self.ui.verticalLayout_3)
            parent.main_self.ui.verticalLayout_3.addWidget(self)

            self.now = datetime.now()
            self.chart_stop = self.now + timedelta(milliseconds=3000)

            plt.cla()

            plt.gca().xaxis.set_major_formatter(FuncFormatter(parent.date_formatter_1))

            plt.xticks(fontsize=3)
            self.ax.grid(False)

            self.ax.set_ylim(-32768, 32768)

            x_ticks = []
            for i in range(499, 2500 + 1, 1000):
                tick = self.now + timedelta(milliseconds=i)
                x_ticks.append(tick)
            plt.xticks(x_ticks)

            self.ax.set_xlim(self.now, self.now + timedelta(milliseconds=3000))


            self.li, = self.ax.plot([self.now, self.now + timedelta(milliseconds=3000)], [0, 0], color=(0, 1, 0.29),
                                    linestyle='solid', marker=",")

            self.show()
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.parent.main_self.open_final_slice_plot_error_window(error_message)