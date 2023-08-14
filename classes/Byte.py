import tkinter as tk
from tkinter import ttk
from my_constants import*

class Byte():
    def __init__(self, dec_value, hex_value, bin_value, name=" - "):

        self.dec_value = dec_value
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
        self.hex_value.set(f"{self.dec_value.get() :02X}")
        self.bin_value.set(f"{self.dec_value.get() :08b}")

    # return int value
    def get_dec_value(self):
        return self.dec_value.get()

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

    # Bit methods
    def set_bit(self, bit):
        print("set bit3")
        self.set_value(((1 << bit) | self.dec_value.get()))

    def clear_bit(self, bit=0):
        self.set_value(self.dec_value.get() & (~(1 << bit)))
    
    def print_values(self):
        print(self.dec.get(), self.hex.get(), self.bin.get())