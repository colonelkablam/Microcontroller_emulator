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
        self.code_window_open = False
        self.log_window_open = False

        # tkinter widgets

        # panel label
        # self.frame_label = ttk.Label(self, text="Control Panel", style='MainWindowOuter.TLabel')
        # self.frame_label.grid(column=0, row=0, padx=(50,0), sticky="W")

        # main button frame
        self.button_frame = ttk.Frame(self, style='MainWindowOuter.TFrame', relief='flat')
        self.button_frame.grid(column=0, row=1, sticky="EW")
        self.button_frame.columnconfigure((0,1,2), weight=1, uniform=1)

        # button groups - run MCU
        self.running_MCU_frame = ttk.Frame(self.button_frame, style='MainWindowOuter.TFrame')
        self.running_MCU_frame.grid(column=0, row=0, sticky="EW")
        self.running_MCU_frame.columnconfigure((0,1), weight=1)

        # buttons + label and slider
        self.advance = ttk.Button(self.running_MCU_frame, text="Advance Instruction", command=self._MCU_advance_cycle)
        self.run = ttk.Button(self.running_MCU_frame, text="Run", command=self._start_simulation)
        self.stop = ttk.Button(self.running_MCU_frame, text="Stop", command=self._stop_simulation)
        self.slider_label = ttk.Label(  self.running_MCU_frame,
                                         text="slow   - simulation speed -   fast",
                                         anchor="center",
                                         style="MainWindowOuterSlider.TLabel"   )
        self.sim_speed_slider = ttk.Scale(  self.running_MCU_frame,
                                        name="run speed",
                                        takefocus=False,
                                        from_=1000,
                                        to=1,
                                        orient="horizontal"                      )
        self.sim_speed_slider.set(1000)
        # positions - control buttons
        self.advance.grid(column=0, row=0, columnspan=2, sticky="EW")
        self.run.grid(column=0, row=1, sticky="EW")
        self.stop.grid(column=1, row=1, sticky="EW")
        self.slider_label.grid(column=0, row=2, padx=(30,30), pady=(10,0), columnspan=2, sticky="SEW")
        self.sim_speed_slider.grid(column=0, row=3, padx=(30,30), columnspan=2, sticky="EW")

        # button groups - log and pin
        self.log_frame = ttk.Frame(self.button_frame, style='MainWindowOuter.TFrame')
        self.log_frame.grid(column=1, row=0, sticky="EW")
        self.log_frame.columnconfigure(0, weight=1)
        # buttons
        self.pin_out = ttk.Button(self.log_frame, text="Pinout Display", command=self._open_pinout_window)
        self.log = ttk.Button(self.log_frame, text="View Log Messages", command=self._open_log_window)
        self.log_clear = ttk.Button(self.log_frame, name="narrow1", text="Clear Log Messages", command=self.parent.clear_log_text)
        # positions log and pin
        self.pin_out.grid(column=0, row=0)
        self.log.grid(column=0, row=1)
        self.log_clear.grid(column=0, row=2)

        # button groups - program and reset 
        self.reset_frame = ttk.Frame(self.button_frame, style='MainWindowOuter.TFrame')
        self.reset_frame.grid(column=2, row=0, sticky="EW")
        self.reset_frame.columnconfigure(0, weight=1)
        # buttons
        self.code_editor = ttk.Button(self.reset_frame, text="Code Editor", command=self._open_code_window)
        self.restart_MCU_button = ttk.Button(self.reset_frame, name="narrow1", text="Restart MCU", command=self._restart_MCU)
        self.clear_program_button = ttk.Button(self.reset_frame, name="narrow2", text="Clear Program", command=self._clear_program)
        # positions program and reset
        self.code_editor.grid(column=0, row=0)
        self.restart_MCU_button.grid(column=0, row=1)
        self.clear_program_button.grid(column=0, row=2)    

        # apply padding and style to all buttons
        for frame in self.button_frame.winfo_children():
            frame.configure(relief='flat')
            frame.grid(sticky="NEW")
            for button in frame.winfo_children():
                if button.winfo_class() == 'TButton':
                    button.configure(style="MainWindow.TButton")
                    button.grid(sticky="NEW", padx=(15,15), pady=(5,0))
                    if button.winfo_name() == "narrow1":
                        button.grid(sticky="NEW", padx=(40,40), pady=(10,0))
                    elif button.winfo_name() == "narrow2":
                        button.grid(sticky="NEW", padx=(40,40), pady=(5,0))

        self.clear_program_button.configure(style="MainWindow2.TButton")
        self.stop.configure(style="MainWindow2.TButton")
        self.log_clear.configure(style="MainWindow2.TButton")
        self.run.configure(style="MainWindow3.TButton")
        self.restart_MCU_button.configure(style="MainWindow4.TButton")

    # ControlPanelFrame methods

    def _MCU_advance_cycle(self):
        self.parent.MCU_frame.advance_cycle()

    def _start_simulation(self):
        # disable other buttons
        self.advance.configure(state="disabled")
        self.run.configure(state="disabled")
        self.stop.configure(state="normal")
        # call method in MCU
        self.parent.MCU_frame.start_simulation(int(self.sim_speed_slider.get()))

    def _stop_simulation(self):
        # enable other buttons
        self.advance.configure(state="normal")
        self.run.configure(state="normal")
        self.stop.configure(state="disabled")
        # call method in MCU
        self.parent.MCU_frame.stop_simulation()
    
    def _restart_MCU(self):
        self._stop_simulation()
        self.parent.MCU_frame.reset_MCU(keepprogram=True)

    def _clear_program(self):
        self._stop_simulation()
        self.parent.MCU_frame.reset_MCU(keepprogram=False)

    # manage code window
    def _open_code_window(self):
        if self.code_window_open == False:
           self.parent.open_code_window()
           self.code_window_open = True
        else:
            self.parent.code_window.lift_window()

    def close_code_window(self):
        self.code_window_open = False

    # manage log window
    def _open_log_window(self):
        if self.log_window_open == False:
            self.parent.open_log_window()
            self.log_window_open = True
        else:
            self.parent.log_window.lift_window()

    def close_log_window(self):
        self.log_window_open = False

    # manage pinout window
    def _open_pinout_window(self):
        self.parent.open_pinout_window()

