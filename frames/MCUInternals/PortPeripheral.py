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
        # read TRIS register and update port pins accordingly
        for bit, port_pin in enumerate(self.port_pins):
            port_pin.set_direction(self.tris_register.get_bit(bit))

        # decide pins to set
        for bit, port_pin in enumerate(self.port_pins):

            # if set to INPUT read CHIP pin input and set PORT register accordingly
            if port_pin.pin_direction == PinDir.INPUT:
                # if port pin set to input change value accordingly
                if port_pin.pin_input == PinVal.ON:
                    self.port_register.set_bit(bit)
                else:
                    self.port_register.clear_bit(bit)

            # if set to OUTPUT read PORT pin input and set CHIP pin accordingly
            elif port_pin.pin_direction == PinDir.OUTPUT:
                # if port pin set to output change output value according to PORT reg. bit value
                if self.port_register.get_bit(bit) == 0:
                    port_pin.set_output(PinVal.OFF)
                elif self.port_register.get_bit(bit) == 1:
                    port_pin.set_output(PinVal.ON)

    # return port pin object
    def get_port_pin_by_name(self, name):
        for port_pin in self.port_pins:
            if port_pin.get_name() == name:
                return port_pin
        return None # return None type if not found

    # reset all values
    def reset(self):
        for pin in self.port_pins:
            pin.reset()
    

            


        






