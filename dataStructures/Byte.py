import tkinter as tk
from tkinter import ttk
from my_constants import*

class Byte():
    def __init__(self, dec_value, hex_value, bin_value, name=" - "):

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
        self.dec_value.set(self.dec_value.get()  % 256) # can only store an 8-bit number
        self.hex_value.set(f"{self.dec_value.get() :02X}h")
        self.bin_value.set(f"{self.dec_value.get() :08b}")

    # return int value
    def get_dec_value(self):
        return self.dec_value.get()

    # return hex string
    def get_hex_value(self):
        return f"{self.dec_value.get() :02X}"
        

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
        if bit >= 0 and bit < 8:
            bit_value = (self.get_dec_value() >> bit) & 1
        else:
            bit_value = None
        return bit_value

    def set_bit(self, bit):
        if bit >= 0 and bit < 8:
            self.set_value(((1 << bit) | self.dec_value.get()))

    def clear_bit(self, bit=0):
        if bit >= 0 and bit < 8:
            self.set_value(self.dec_value.get() & (~(1 << bit)))
    
    def print_values(self):
        print(self.dec.get(), self.hex.get(), self.bin.get())