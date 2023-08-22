import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import *

# locally used enums for pin direction/values
class PinDir(Enum):
    INPUT = 1
    OUTPUT = 0
class PinVal(Enum):
    ON = 1
    OFF = 0

# pin class to store the state of each port pin and handle pin logic
class PortPin():
    def __init__(self, name):
        # properties
        self.name = name
        self.pin_direction = PinDir.INPUT
        self.pin_output = PinVal.OFF
        self.pin_input = PinVal.OFF


    # Pin methods
    def set_direction(dir_bit):
        if dir_bit == 0:
            self.pin_direction = PinDir.OUTPUT
        elif dir_bit == 1:
            self.pin_direction = PinDir.INPUT
        else:
            pass # no change if invalid value

    def set_input(digital_value):
        if self.pin_direction == PinDir.INPUT:
            self.pin_input = digital_value # PinVal enum ON or OFF
        else:
            pass # no change as pin not in correct state
    
    def set_output(digital_value):
        if self.pin_direction == PinDir.OUTPUT:
            self.pin_output = digital_value # PinVal enum ON or OFF
        else:
            pass # no change as pin not in correct state

    def get_direction(self):
        return self.pin_direction.value

    def get_input(self):
        return self.pin_input.value

    def get_output(self):
        return self.pin_output.value

    def get_name(self):
        return self.name