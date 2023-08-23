import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import *
from my_enums import *


class PinFrame(ttk.Frame):
    def __init__(self, parent, pin_number, side, port_pin=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # configure layout of internal Frames
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # properties
        self.parent = parent
        self.pin_number = pin_number
        self.port_pin_object = port_pin
        self.input_value = tk.IntVar()
        self.output_value = tk.IntVar()
        self.direction = tk.StringVar()

        # handle placing widgets when on either left or right of chip (reverses order of grid placement)
        index_start = 0
        index_step = 1
        if side == Side.LEFT:
            index = 0
            index_step = 1
        elif side == Side.RIGHT:
            index = 3
            index_step = -1

        # if peripheral port pin assigned populate with values of port pins
        if self.port_pin_object != None:
            self.name = self.port_pin_object.get_name()
            self.direction.set(" INPUT")

            self.input_toggle = tk.Button(self, textvariable=self.input_value, command=self.toggle_pin_input)
            self.input_toggle.grid(column=index, row=0)
            index += index_step
            self.dir_label = ttk.Label(self, text=self.direction.get(), style="PinOut.TLabel")
            self.dir_label.grid(column=index, row=0)
            index += index_step
            self.output_toggle = tk.Button(self, textvariable=self.output_value)
            self.output_toggle.grid(column=index, row=0)
            self.output_toggle.configure(state="disabled")
            index += index_step
            self.name_label = ttk.Label(self, text=self.name, style="PinOut.TLabel")
            self.name_label.grid(column=index, row=0)

        # else populate with default unassigned values
        else:
            self.name = "n/a"
            self.direction.set("------")

            self.input_toggle = tk.Button(self, textvariable=self.input_value, command=self.toggle_pin_input)
            self.input_toggle.grid(column=index, row=0)
            self.input_toggle.configure(state="disabled")
            index += index_step
            self.dir_label = ttk.Label(self, text=self.direction.get(), style="PinOut.TLabel")
            self.dir_label.grid(column=index, row=0)
            index += index_step
            self.output_toggle = tk.Button(self, textvariable=self.output_value)
            self.output_toggle.grid(column=index, row=0)
            self.output_toggle.configure(state="disabled")
            index += index_step
            self.name_label = ttk.Label(self, text=self.name, style="PinOut.TLabel")
            self.name_label.grid(column=index, row=0)

    # update pin display and set port pin input
    def update(self):
        pin = self.port_pin_object
        if pin != None:
            if pin.get_direction() == PinDir.INPUT:
                self.direction.set(" INPUT")
                self.input_toggle.configure(state="normal")
                self.output_toggle.configure(state="disabled")
            elif pin.get_direction() == PinDir.OUTPUT:
                self.direction.set("OUTPUT")
                self.input_toggle.configure(state="disabled")
                self.output_toggle.configure(state="normal")

            pin.set_input(PinVal(self.input_value.get()))
            print(self.input_value.get())


    def toggle_pin_input(self):
        # toggle between 0 / 1
        if self.input_value.get() == 0:
            self.input_value.set(1)
        else:
            self.input_value.set(0)
        
        print(f"Pin {self.pin_number} value input now {self.input_value.get()}.")


class PinoutFrame(ttk.Frame):
    def __init__(self, parent, port_pins_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # configure layout of internal Frames
        #self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.configure(style='MainWindowOuter.TFrame')

        # properties
        self.parent = parent


        # tkinter widgets

        self.left_pin_frame = ttk.Frame(self, style='MainWindowOuter.TFrame')
        self.left_pin_frame.grid(column=0, row=0, )
        self.center_pin_frame = ttk.Frame(self, style='MainWindowOuter.TFrame', width=150, height=260)
        self.center_pin_frame.grid(column=1, row=0, )
        self.right_pin_frame = ttk.Frame(self, style='MainWindowOuter.TFrame')
        self.right_pin_frame.grid(column=2, row=0, )

        self.pins = []

        # populate left side chip pins 1 to 9
        for pin_num in range(1, 10):
            
            pin = port_pins_dict[pin_num]

            if pin != None:
                pin_frame = PinFrame(self.left_pin_frame, pin_num, Side.LEFT, pin)
                pin_frame.grid(column=0, row=pin_num-1)
                self.pins.append(pin_frame)
            else:   # if no port assigned
                pin_frame = PinFrame(self.left_pin_frame, pin_num, Side.LEFT)
                pin_frame.grid(column=0, row=pin_num-1)
                self.pins.append(pin_frame)

        # populate right side chip pins 18 to 9
        for pin_num in range(18, 9, -1):
            pin = port_pins_dict[pin_num]

            if pin != None:
                pin_frame = PinFrame(self.right_pin_frame, pin_num, Side.RIGHT, pin)
                pin_frame.grid(column=0, row=18 - pin_num)
                self.pins.append(pin_frame)
            else:   # if no port assigned
                pin_frame = PinFrame(self.right_pin_frame, pin_num, Side.RIGHT)
                pin_frame.grid(column=0, row=18 - pin_num)
                self.pins.append(pin_frame)


    # PinoutFrame methods
    def update(self):
        for pin in self.pins:
            pin.update()

