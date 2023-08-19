import tkinter as tk
from tkinter import ttk
from my_constants import*
from dataStructures import NBitNumber


class ProgramCounter():
    def __init__(self, data_memory):
        
        # properties
        self.data_memory = data_memory
        self.counter = NBitNumber(  13, 
                                    tk.IntVar(value=0), 
                                    tk.StringVar(value="0000h"), 
                                    tk.StringVar(value="0000000000000"), 
                                    "PC"        )

        self.previous_value = 0

    def get(self):
        return self.counter

    def set_value(self, new_address):
        # save previous value
        self.previous_value = self.get_value()
        # wrap value within the program memory size (can different to max no. a 13-bit can represent)
        address = new_address %  PROGRAM_MEMORY_SIZE
        self.counter.set_value(address)

        # split the address into lower and upper bytes (as PC stored in PCL and PCLATH)
        lower_byte = self._get_n_byte_int(address, 0, 8)
        upper_byte = self._get_n_byte_int(address, 1, 8)
        # take only the lower 5-bits of the 2nd byte - PCLATH not addressable; last 3 bits '0'
        upper_5_bits = self._get_n_byte_int(upper_byte, 0, 5)

        # store the values in the registers
        self.data_memory.set_byte_by_name("PCL", lower_byte)
        self.data_memory.set_byte_by_name("PCLATH", upper_5_bits)


    # get the nth byte value
    def _get_n_byte_int(self, target, n, bit_length=8):
        mask = 255 << (n * bit_length)
        and_result = mask & target
        byte = and_result >> (n * bit_length)
        return byte

    def get_value(self):
        return self.counter.get_dec_value()

    def get_previous(self):
        return self.previous_value

    def set_previous(self, value=0):
        self.previous_value = value

    def advance_one(self):
        self.set_value(self.counter.get_dec_value() + 1)
    
    # likely handled by the instruction decoder
    def advance_two(self):
        self.set_value(self.counter.get_dec_value() + 2)

