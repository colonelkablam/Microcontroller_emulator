import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import*

class Side(Enum):
    LEFT = 0
    RIGHT = 1

class PinFrame(ttk.Frame):
    def __init__(self, parent, pin_number,  name="none", direction=0, output=0, side=Side.LEFT, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # configure layout of internal Frames
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # properties
        self.parent = parent
        self.pin_number = pin_number
        self.name = name
        self.input_value = tk.IntVar(value=0)

        self.input_toggle = tk.Button(self, textvariable=self.input_value, command=self.toggle_pin_input)
        self.input_toggle.grid(column=0, row=0)
        self.name_label = ttk.Label(self, text=name)
        self.name_label.grid(column=1, row=0)
        self.dir_label = ttk.Label(self, text=direction)
        self.dir_label.grid(column=2, row=0)


    def toggle_pin_input(self):
        # toggle between 0 / 1
        if self.input_value.get() == 0:
            self.input_value.set(1)
        else:
            self.input_value.set(0)
        
        print(f"Pin {self.pin_number} value input now {self.input_value.get()}.")


class PinoutFrame(ttk.Frame):
    def __init__(self, parent, port_a, port_b, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # configure layout of internal Frames
        #self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.configure(style='MainWindowOuter.TFrame')

        # properties
        self.parent = parent
        self.port_a = port_a
        self.port_b = port_b

        self.chip_pin_dict = {  "RA0" : [17, 0],
                                "RA1" : [18, 0],
                                "RA2" : [1,  0],
                                "RA3" : [2,  0],
                                "RA4" : [3,  0],
                                "RB0" : [6,  0],
                                "RB1" : [7,  0],
                                "RB2" : [8,  0],
                                "RB3" : [9,  0],
                                "RB4" : [10, 0],
                                "RB5" : [11, 0],
                                "RB6" : [12, 0],
                                "RB7" : [13, 0]     }


        # tkinter widgets

        self.left_pin_frame = ttk.Frame(self, style='MainWindowOuter.TFrame')
        self.left_pin_frame.grid(column=0, row=0, )
        self.center_pin_frame = ttk.Frame(self, style='MainWindowOuter.TFrame', width=150, height=240)
        self.center_pin_frame.grid(column=1, row=0, )
        self.right_pin_frame = ttk.Frame(self, style='MainWindowOuter.TFrame')
        self.right_pin_frame.grid(column=2, row=0, )

        self.pins = []

        for pin_num in range(1, 10):
            pin = PinFrame(self.left_pin_frame, pin_number=pin_num)
            pin.grid(column=0, row=pin_num-1)
            self.pins.append(pin)

        for pin_num in range(18, 9, -1):
            pin = PinFrame(self.right_pin_frame, pin_number=pin_num)
            pin.grid(column=0, row=18 - pin_num)
            self.pins.append(pin)


    # PinoutFrame methods

