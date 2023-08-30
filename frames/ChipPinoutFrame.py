import tkinter as tk
from tkinter import ttk
from enum import Enum
from frames import ChipPinFrame
from my_constants import *
from my_enums import *

# frame to contain all the chip pins needed for the chip's pinout
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
        self.left_pin_label.grid(column=0, row=0, sticky="E", pady=(0,7))
        self.left_pin_frame = ttk.Frame(self, style='PinOutBackground2.TFrame')
        self.left_pin_frame.grid(column=0, row=1 )
        
        # center of chip
        self.center_pin_frame = ttk.Frame(self, style='PinOutChip.TFrame', width=210, height=320, padding=10)
        self.center_pin_frame.grid(column=1, row=1)
        self.center_pin_frame.grid_propagate(0)
        self.center_pin_frame.columnconfigure(1, weight=1)
        self.center_pin_label = ttk.Label(self.center_pin_frame, text="PIC16c172", anchor="center", style="PinOutChip.TLabel")
        self.center_pin_label.grid(column=1, row=0, rowspan=8, sticky="EW")
       
        # right side of chip
        self.left_pin_label = ttk.Label(self, text="name    pin state", style="PinOutHeading.TLabel", anchor="w")
        self.left_pin_label.grid(column=2, row=0, sticky="W", pady=(0,7))
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

