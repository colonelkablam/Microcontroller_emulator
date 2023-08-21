import tkinter as tk
import tkinter.font as font
from datetime import datetime
from my_constants import *
from tkinter import ttk
from frames import ControlPanelFrame, MCUFrame
from windows import LogWindow, CodeWindow
from styling import MainStyle


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # MainWindow properties
        self.title("MCU Emulator")
        #self.geometry("%dx%d+%d+%d" % (MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, 100, 100))
        self.resizable(height = True, width = False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # log window
        self.log_window = None 
        # var to contain log text (will populate log window when open)
        self.log_text = tk.StringVar()
        self.log_text.trace_add('write', self.update_log_window_display)
        
        self.log_commit_list = [] # list of text to add to log_text when cycle/event complete
        self.event_count_per_cycle = 0

        # code window
        self.code_window = None

        # style
        self["background"] = COLOUR_MAIN_BACKGROUND

        # tkinter Widgets

        # main MCU_frame - contains MCUInternals, data and program memory
        self.create_MCU_frame()

        # control panel frame for app - contained within main window
        self.control_panel_frame = ControlPanelFrame(self, style='MainWindowOuter.TFrame', padding=10)
        self.control_panel_frame.grid(column=0, row=1, sticky="NSEW")


    # MainWindow Methods

    def create_MCU_frame(self):
        self.MCU_frame = MCUFrame(self, style='MainWindowOuter.TFrame', padding=10)
        self.MCU_frame.grid(column=0, row=0, sticky="NSEW")

    def reset_MCU_frame(self):
        self.MCU_frame.destroy()
        self.MCU_frame = MCUFrame(self, style='MainWindowOuter.TFrame', padding=10)
        self.MCU_frame.grid(column=0, row=0, sticky="NSEW")

    def open_code_window(self):
        self.code_window = CodeWindow(self)

    # clear code_window var after window close
    def clear_code_window(self):
        self.control_panel_frame.close_code_window()
        self.code_window = None

    def open_log_window(self):
        self.log_window = LogWindow(self)

    # clear log_window var after window close
    def close_log_window(self):
        self.control_panel_frame.close_log_window()
        self.log_window = None

    # add to log - calling .set calls traceback function 'update_log_window_display'
    # needed as no textvariable in text box and log wanted as a string
    def add_to_log(self, message):
        self.log_commit_list.append(f"[{self.event_count_per_cycle}] {message}")
        self.log_commit_list.append('\n')
        self.event_count_per_cycle += 1

    def system_message(self, system_message):
        # self.log_commit_list.append('\n')
        self.log_text.set(f"{self.get_time()} - SYSTEM MESSAGE: {system_message}\n{self.log_text.get()}")

    def log_commit(self):
        self.log_commit_list.append('\n')
        self.log_commit_list.insert(0, f"\t\t----- Instruction Cycle: {self.MCU_frame.get_instruction_cycle()} -----\n")
        text_to_commit = ''.join(self.log_commit_list)
        self.log_text.set(f"{text_to_commit}{self.log_text.get()}")
        self.log_commit_list = []
        self.event_count_per_cycle = 0


    # update log window
    def update_log_window_display(self, var, index, mode):
        # text if window exists
        if self.log_window != None:
            self.log_window.update_window()
        else:
            pass # no window open to update display

    # get time
    def get_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    # initialise log text
    def clear_log_text(self):
        self.log_text.set(value="")
