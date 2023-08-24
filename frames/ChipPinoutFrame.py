import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import *
from my_enums import *

# frame for each chip pin in the ChipPinoutFrame - ChipPinoutFrame below
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
            self.direction.set("INPUT ")

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
            self.direction.set(" ---- ")

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
                self.direction.set("INPUT ")
                self.input_toggle.configure(state="normal")
                self.output_toggle.configure(state="disabled")
                # get input value and set to port pin
                pin.set_input(PinVal(self.input_value.get()))

            # if set to OUTPUT
            elif pin.get_direction() == PinDir.OUTPUT:
                self.direction.set("OUTPUT")
                self.input_toggle.configure(state="disabled")
                self.output_toggle.configure(state="normal")
                # get output value and set to chip pin
                print("output val.", pin.get_output().value)
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
        else:
            pass


    def reset(self):
        if self.port_pin_object != None:
            self.input_value.set(0)
            self.output_value.set(0)
            self.direction.set(" INPUT")
            self.update()

    def toggle_pin_input(self):
        # toggle between 0 / 1
        if self.input_value.get() == 0:
            self.input_value.set(1)
        else:
            self.input_value.set(0)

        self.update()
        
        print(f"Pin {self.pin_number} value input now {self.input_value.get()}.")

# frame to contain all the pins needed for the pinout
class ChipPinoutFrame(ttk.Frame):
    def __init__(self, parent, port_pins_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # configure layout of internal Frames
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(style='PinOutBackground.TFrame', padding=20)

        # properties
        self.parent = parent
        self.port_pins_dict = port_pins_dict

        ## tkinter widgets

        # left side of chip
        self.left_pin_label = ttk.Label(self, text="pin state    name", style="PinOutHeading.TLabel", anchor="e")
        self.left_pin_label.grid(column=0, row=0, sticky="E", pady=(0,5))
        self.left_pin_frame = ttk.Frame(self, style='PinOutBackground2.TFrame')
        self.left_pin_frame.grid(column=0, row=1 )
        
        # center of chip
        self.center_pin_frame = ttk.Frame(self, style='PinOutChip.TFrame', width=210, height=320, padding=10)
        self.center_pin_frame.grid(column=1, row=1)
        self.center_pin_frame.grid_propagate(0)
        self.center_pin_frame.columnconfigure(1, weight=1)
        self.center_pin_label = ttk.Label(self.center_pin_frame, text="PIC16172", anchor="center", style="PinOutChip.TLabel")
        self.center_pin_label.grid(column=1, row=0, rowspan=8, sticky="EW")
       
       # right side of chip
        self.left_pin_label = ttk.Label(self, text="name    pin state", style="PinOutHeading.TLabel", anchor="w")
        self.left_pin_label.grid(column=2, row=0, sticky="W", pady=(0,5))
        self.right_pin_frame = ttk.Frame(self, style='PinOutBackground2.TFrame')
        self.right_pin_frame.grid(column=2, row=1 )

        # create list to store pin_frames for access when updating
        self.pin_frame_list = []
        # initialise chip pins with port_pin_dict to give access to port pins
        self.initialise_chip_pins()


    # ChipPinoutFrame methods

    def initialise_chip_pins(self):

    # populate left side chip pins 1 to 9
        for pin_num in range(1, 10):

            # maps port pins to chip pins
            pin = self.port_pins_dict[pin_num]
            # row to place pin in (according to physical pinout of PIC16C712)
            row_num = pin_num - 1

            # ChipPinFrames
            if pin != None:
                pin_frame = ChipPinFrame(self.left_pin_frame, pin_num, Side.LEFT, pin)
                pin_frame.grid(column=0, row=row_num)
                self.pin_frame_list.append(pin_frame)
            else:   # if no port assigned
                pin_frame = ChipPinFrame(self.left_pin_frame, pin_num, Side.LEFT)
                pin_frame.grid(column=0, row=row_num)
                self.pin_frame_list.append(pin_frame)

            # chip pin numbers
            pin_num_label = ttk.Label(self.center_pin_frame, width=2, text=pin_num, style="PinOutChip.TLabel")
            pin_num_label.grid(column=0, row=row_num, pady=6)

    # populate right side chip pins 18 to 9
        for pin_num in range(18, 9, -1):

            # maps port pins to chip pins
            pin = self.port_pins_dict[pin_num]
            # row to place pin in (according to physical pinout of PIC16C712)
            row_num = 18 - pin_num

            if pin != None:
                pin_frame = ChipPinFrame(self.right_pin_frame, pin_num, Side.RIGHT, pin)
                pin_frame.grid(column=0, row=row_num)
                self.pin_frame_list.append(pin_frame)
            else:   # if no port assigned
                pin_frame = ChipPinFrame(self.right_pin_frame, pin_num, Side.RIGHT)
                pin_frame.grid(column=0, row=row_num)
                self.pin_frame_list.append(pin_frame)

            # chip pin numbers
            pin_num_label = ttk.Label(self.center_pin_frame, width=2, text=pin_num, style="PinOutChip.TLabel")
            pin_num_label.grid(column=2, row=row_num, pady=6)

    def update(self):
        for pin in self.pin_frame_list:
            pin.update()

    def reset(self):
        for pin_frame in self.pin_frame_list:
            pin_frame.reset()

