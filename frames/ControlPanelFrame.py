import tkinter as tk
from tkinter import ttk
from my_constants import*


class ControlPanelFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # configure layout of internal Frames
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # properties
        self.parent = parent
        self.clock_running = False
        self.clock_speed = tk.IntVar(value=1000)
        self.code_window_open = False
        self.log_window_open = False
        

        # tkinter widgets

        # panel label
        self.frame_label = ttk.Label(self, text="Control Panel", style='MainWindowOuter.TLabel')
        self.frame_label.grid(column=0, row=0, padx=(50,0), sticky="W")

        # button frame
        self.button_frame = ttk.Frame(self, style='MainWindowOuter.TFrame', relief='flat')
        self.button_frame.grid(column=0, row=1)
        # buttons
        self.button1 = ttk.Button(self.button_frame, text="Advance", command=self.MCU_advance_cycle)
        self.button2 = ttk.Button(self.button_frame, text="Run", command=self.start_clock)
        self.button3 = ttk.Button(self.button_frame, text="Stop", command=self.stop_clock)
        self.button4 = ttk.Button(self.button_frame, text="View Log Messages", command=self.open_log_window)
        self.button5 = ttk.Button(self.button_frame, text="Pin Out")
        self.button6 = ttk.Button(self.button_frame, text="Code Editor", command=self.open_code_window)
        self.button7 = ttk.Button(self.button_frame, text="Reset MCU", command=self.reset_MCU)

        # grid the buttons
        self.button1.grid(column=0, row=0, columnspan=2, sticky="EW")
        self.button2.grid(column=0, row=1)
        self.button3.grid(column=1, row=1)
        self.button4.grid(column=3, row=0)
        self.button5.grid(column=4, row=0)
        self.button6.grid(column=5, row=0)
        self.button7.grid(column=5, row=1)      

        # apply padding to all widgets in self
        for child in self.button_frame.winfo_children():
            child.configure(style="MainWindow.TButton")
            child.grid(padx=10, pady=10)

    # ControlPanelFrame methods

    def MCU_advance_cycle(self):
        self.parent.MCU_frame.advance_cycle()

    def start_clock(self):
        self.clock_running = True
        while clock_running:
            self.after(self.clock_speed.get(), self.MCU_advance_cycle)

    def stop_clock(self):
        self.clock_running = False
    
    def reset_MCU(self):
        self.parent.MCU_frame.reset_MCU()

    def open_code_window(self):
        if self.code_window_open == False:
           self.parent.open_code_window()
           self.code_window_open = True

    def close_code_window(self):
        self.code_window_open = False

    def open_log_window(self):
        if self.log_window_open == False:
            self.parent.open_log_window()
            self.log_window_open = True

    def close_log_window(self):
        self.log_window_open = False
