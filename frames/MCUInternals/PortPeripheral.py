import tkinter as tk
from tkinter import ttk
from my_constants import *
from my_enums import *
from frames.MCUInternals import PortPin


# port peripheral class - will read and write directly to PORT and TRIS registers
class PortPeripheral():
    def __init__(self, port_register, tris_register, num_io_pins):

        # properties
        self.name = port_register.get_name()
        self.port_register = port_register
        self.tris_register = tris_register
        self.num_io_pins = num_io_pins

        self.port_pins = []

        # populate the port io pins
        for pin in range(0, self.num_io_pins):
            # give name (using the name format given on the MICROCHIP PIC16C712 data sheet)
            self.port_pins.append(PortPin(f"R{self.name[4]}{pin}"))

        
    # Port methods
    def update_registers(self):
        # read TRIS registers
        for bit, port_pin in enumerate(self.port_pins):
            port_pin.set_direction(self.tris_register.get_bit(bit))

        for bit, port_pin in enumerate(self.port_pins):
            # if set to input read chip pin input
            if port_pin.pin_direction == PinDir.INPUT:
                # if port pin set to input change value accordingly
                if port_pin.pin_input == PinVal.ON:
                    self.port_register.set_bit(bit)
                else:
                    self.port_register.clear_bit(bit)
            else:
                pass
                

    # return port pin object
    def get_port_pin_by_name(self, name):
        for port_pin in self.port_pins:
            if port_pin.get_name() == name:
                return port_pin
        return None # return None type if not found

    def update_port(self):
        for port_pin in self.pins:
            
            pass

    def read_pins(self):
        pass

    def write_pins(self):
        pass

    def initialise_port(self):
        pass
    

            


        






