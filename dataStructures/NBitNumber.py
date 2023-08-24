import tkinter as tk
from tkinter import ttk
from my_constants import*
import math

class NBitNumber():
    def __init__(self, n_bits, dec_value, hex_value, bin_value, name=" - "):

        # properties
        self.number_of_bits = n_bits

        # tk.IntVar()
        self.dec_value_obj = dec_value
        # tk.StringVar()
        self.hex_value_obj = hex_value
        self.bin_value_obj = bin_value

        self.name = name
    
    # Byte methods
    def set_value(self, new_value):
        self.dec_value_obj.set(new_value)
        self.update_byte()


    # need to increment all three base numbers
    def increment_value(self, step=1):
        self.dec_value_obj.set(self.dec_value_obj.get() + step)
        self.update_byte()

    # need to update other values using the existing dec value
    def update_byte(self):
        # calculating formatting (hex to be in bytes)
        max_value = (2**self.number_of_bits) - 1
        num_digits_hex = 0
        if max_value <= 255:
            num_digits_hex = 2
        elif max_value <= 65535:
            num_digits_hex = 4
        # arguably no necessary
        elif max_value <= 16777215:
            num_digits_hex = 6
        else:
            num_digits_hex = 8

        # handle larger numbers than can be stored with wrap-around
        self.dec_value_obj.set(self.dec_value_obj.get()  % (max_value + 1)) # store up to n-bit binary number
        # formatting number of digits to display
        self.hex_value_obj.set(f"{self.dec_value_obj.get() :0{num_digits_hex}X}h")
        self.bin_value_obj.set(f"{self.dec_value_obj.get() :0{self.number_of_bits}b}")

    # return int value
    def get_dec_value(self):
        return self.dec_value_obj.get()

    # return hex string
    def get_hex_value(self):
        return f"{self.dec_value_obj.get() :0{num_digets_hex}X}"
        
    # return tkinter value object - needed to update memory panels
    def get_dec(self): 
        return self.dec_value_obj

    def get_bin(self):
        return self.bin_value_obj

    def get_hex(self):
        return self.hex_value_obj

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
            self.set_value(((1 << bit) | self.dec_value_obj.get()))

    def clear_bit(self, bit):
        if bit >= 0 and bit < self.number_of_bits:
            self.set_value(self.dec_value_obj.get() & (~(1 << bit)))

    def get_number_of_bits(self):
        return self.number_of_bits
    
    def print_values(self):
        print(self.dec.get(), self.hex.get(), self.bin.get())