import tkinter as tk
from tkinter import ttk
from my_constants import*
import math

class NBitNumber():
    def __init__(self, n_bits, dec_value, hex_value, bin_value, name=" - "):

        # properties
        self.number_of_bits = n_bits

        # tk.IntVar()
        self.dec_value = dec_value
        # tk.StringVar()
        self.hex_value = hex_value
        self.bin_value = bin_value

        self.name = name

    # Byte methods
    def set_value(self, new_value):
        self.dec_value.set(new_value)
        self.update_byte()


    # need to increment all three base numbers
    def increment_value(self, step=1):
        self.dec_value.set(self.dec_value.get() + step)
        self.update_byte()

    def update_byte(self):
        max_value = 2**self.number_of_bits
        num_digets_hex = int(math.log10(max_value)) + 1
        self.dec_value.set(self.dec_value.get()  % max_value) # can only store up to n-bit number


        self.hex_value.set(f"{self.dec_value.get() :0{num_digets_hex}X}h")
        self.bin_value.set(f"{self.dec_value.get() :0{self.number_of_bits}b}")

    # return int value
    def get_dec_value(self):
        return self.dec_value.get()

    # return hex string
    def get_hex_value(self):
        return f"{self.dec_value.get() :0{num_digets_hex}X}"
        

    # return tkinter value object - needed to update memory panels
    def get_dec(self): 
        return self.dec_value

    def get_bin(self):
        return self.bin_value

    def get_hex(self):
        return self.hex_value

    # get the name string
    def get_name(self):
        return self.name

    # Bit methods - 
    def get_bit(self, bit):
        if bit >= 0 and bit < self.number_of_bits:
            bit_value = (self.get_dec_value() >> bit) & 1
        else:
            bit_value = None
        return bit_value

    def set_bit(self, bit):
        if bit >= 0 and bit < self.number_of_bits:
            self.set_value(((1 << bit) | self.dec_value.get()))

    def clear_bit(self, bit=0):
        if bit >= 0 and bit < self.number_of_bits:
            self.set_value(self.dec_value.get() & (~(1 << bit)))
    
    def print_values(self):
        print(self.dec.get(), self.hex.get(), self.bin.get())