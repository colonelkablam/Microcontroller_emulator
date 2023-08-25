import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import *
from my_enums import *

# frame for each chip pin in the ChipPinoutFrame
class ChipPinFrame(ttk.Frame):
    def __init__(self, parent, pin_number, side, port_pin=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # configure layout of internal Frames
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(style='Pin.TFrame')

        # properties
        self.parent = parent
        self.pin_number = pin_number
        self.port_pin_object = port_pin
        self.input_value = tk.IntVar()
        self.output_value = tk.IntVar()
        self.direction = tk.StringVar()

        # handle placing widgets when on either left or right of chip 
        # (reverses order of tk grid column placement)
        index_start = 0
        index_step = 1
        if side == Side.LEFT:
            index = 0
            index_step = 1
            self.input_text = "INPUT  "
            self.output_text = " OUTPUT"
        elif side == Side.RIGHT:
            index = 3
            index_step = -1
            self.input_text = "  INPUT"
            self.output_text = "OUTPUT "


        # if peripheral port pin assigned to chip pin populate with values of port pins
        if self.port_pin_object != None:
            self.name = self.port_pin_object.get_name()
            self.direction.set(self.input_text)

            self.input_toggle = ttk.Button(self, width=1, textvariable=self.input_value, command=self.toggle_pin_input)
            self.input_toggle.grid(column=index, row=0)
            index += index_step
            self.dir_label = ttk.Label(self, textvariable=self.direction)
            self.dir_label.grid(column=index, row=0)
            index += index_step
            self.output_toggle = ttk.Button(self, textvariable=self.output_value)
            self.output_toggle.grid(column=index, row=0)
            self.output_toggle.configure(state="disabled")
            index += index_step
            self.name_label = ttk.Label(self, text=self.name)
            self.name_label.grid(column=index, row=0)

        # else populate with default unassigned values
        else:
            self.name = " - "
            self.direction.set(" ----- ")

            self.input_toggle = ttk.Button(self, textvariable=self.input_value, command=self.toggle_pin_input)
            self.input_toggle.grid(column=index, row=0)
            self.input_toggle.configure(state="disabled")
            index += index_step
            self.dir_label = ttk.Label(self, textvariable=self.direction)
            self.dir_label.grid(column=index, row=0)
            index += index_step
            self.output_toggle = ttk.Button(self, textvariable=self.output_value)
            self.output_toggle.grid(column=index, row=0)
            self.output_toggle.configure(state="disabled")
            index += index_step
            self.name_label = ttk.Label(self, text=self.name)
            self.name_label.grid(column=index, row=0)

        for widget in self.winfo_children():
            if widget.winfo_class() == "TButton":
                widget.configure(style="PinOutOFF.TButton", width=1)
            if widget.winfo_class() == "TLabel":
                widget.configure(style="PinOut.TLabel", anchor="center")

    # update pin display and set port pin input
    def update(self):
        pin = self.port_pin_object
        # if a port object connected to pin
        if pin != None:
            # if set to INPUT
            if pin.get_direction() == PinDir.INPUT:
                self.direction.set(self.input_text)
                self.input_toggle.configure(state="normal")
                self.output_toggle.configure(state="disabled")
                # get input value and set to port pin
                pin.set_input(PinVal(self.input_value.get()))

            # if set to OUTPUT
            elif pin.get_direction() == PinDir.OUTPUT:
                self.direction.set(self.output_text)
                self.input_toggle.configure(state="disabled")
                self.output_toggle.configure(state="normal")
                # get output value and set to chip pin
                self.output_value.set(pin.get_output().value)

            ## highlight if bit set 
            #input
            if self.input_value.get() == 1:
                self.input_toggle.config(style="PinOutON.TButton")
            else:
                self.input_toggle.configure(style="PinOutOFF.TButton")
            # output
            if self.output_value.get() == 1:
                self.output_toggle.configure(style="PinOutON.TButton")
            else:
                self.output_toggle.configure(style="PinOutOFF.TButton")

        # if object None then no action
        # upgradable to deal with new peripherals pin interactions when needed
        else:
            pass

    ## ChipPinFrame methods
    
    # reset to default values
    def reset(self):
        if self.port_pin_object != None:
            self.input_value.set(0)
           # self.output_value.set(0)
            self.direction.set(" INPUT")
            # refresh display
            self.update()

    # handle user input - changing digital pin input
    def toggle_pin_input(self):
        # toggle between 0 / 1
        if self.input_value.get() == 0:
            self.input_value.set(1)
        else:
            self.input_value.set(0)
        # refresh display
        self.update()