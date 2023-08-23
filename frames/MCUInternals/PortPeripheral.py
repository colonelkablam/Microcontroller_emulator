import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames.MCUInternals import PortPin


# port peripheral class - will read and write directly to PORT and TRIS registers
class PortPeripheral():
    def __init__(self, port_register, tris_register, num_io_pins):

        # properties
        self.name = port_register.get_name()
        self.port_register = port_register
        self.tris_register = tris_register
        self.num_io_pins = num_io_pins

        self.pins = []

        # populate the port io pins
        for pin in range(0, self.num_io_pins):
            # give name (using the name format given on the MICROCHIP PIC16C712 data sheet)
            self.pins.append(PortPin(f"R{self.name[4]}{pin}"))

        # print out test
        print(self.name)

        for i, pin in enumerate(self.pins):
            print(pin.get_name(), "", end="")
        print(" ")

        for i, pin in enumerate(self.pins):
            print(pin.get_direction(), end="")
        print(" ")

        for i, pin in enumerate(self.pins):
            print(pin.get_output(), end="")
        print(" ")
        
        for i, pin in enumerate(self.pins):
            print(pin.get_input(), end="")
        print("\n")
        
    # Port methods
    def update_register(self):
        for pin in self.pins:
            if pin.pin_direction == PinDir.INPUT:
                pass

    # return port pin object
    def get_port_pin_by_name(self, name):
        for pin in self.pins:
            if pin.get_name() == name:
                return pin
        return None # return None type if not found

    def clear_port(self):
        pass

    def read_pins(self):
        pass

    def write_pins(self):
        pass

    def initialise_port(self):
        pass
    

            


        






