import tkinter as tk
from tkinter import ttk
from my_constants import *
from my_enums import *

# pin class to store the state of each port pin and handle pin logic
class PortPin():
    def __init__(self, name):
        # properties
        self.name = name
        self.pin_direction = PinDir.INPUT
        self.pin_output = PinVal.OFF
        self.pin_input = PinVal.OFF


    # Pin methods
    # set direction by corrisponding TRIS register bit
    def set_direction(self, dir_bit):
        if dir_bit == 0:
            self.pin_direction = PinDir.OUTPUT
        elif dir_bit == 1:
            self.pin_direction = PinDir.INPUT
        else:
            pass # no change if invalid value

    # set by chip pin in pinout frame - external control
    def set_input(self, digital_value):
        if self.pin_direction == PinDir.INPUT:
            self.pin_input = digital_value
        else:
            pass # no change as pin not in correct state for INPUT
    
    # set output by corrisponding PORT register bit
    def set_output(self, digital_value):
        if self.pin_direction == PinDir.OUTPUT:
            self.pin_output = digital_value # PinVal enum ON or OFF
        else:
            pass # no change as pin not in correct state for OUTPUT

    def get_direction(self):
        return self.pin_direction.value

    def get_input(self):
        return self.pin_input.value

    def get_output(self):
        return self.pin_output.value

    def get_name(self):
        return self.name