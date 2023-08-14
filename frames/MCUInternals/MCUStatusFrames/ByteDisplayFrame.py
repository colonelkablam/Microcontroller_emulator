import tkinter as tk
from tkinter import ttk
from my_constants import *


class ByteDisplayFrame(ttk.Frame):
    def __init__(self, parent, byte, title = " - ", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.byte = byte

        # tkinter widgets

        # panel label
        self.mem_label = ttk.Label(self, text=f"{title} ({self.byte.get_name()})", style='MainWindowInner3.TLabel')
        self.mem_label.grid(column=0, row=0, pady=(0,5), sticky="W")

        self.bit_frame = ttk.Frame(self, style="MainWindowInner2.TFrame")
        self.bit_frame.grid(column=1, row=0, sticky="E")

        # populate bits from left to right (MSB to LSB)
        for column in range(7, -1, -1):
            bit = ttk.Label(self.bit_frame, text=str(self.byte.get_bit(column)), width=1)
            bit.grid(column=7-column, row=0, padx=5, pady=2)

    # update method rather than using tkinter value objects with textvariable
    # (would need one for each bit in every byte in memory otherwise!)
    def update(self):
        bit_pos = 7
        for widget in self.bit_frame.winfo_children():
            widget.configure(text=str(self.byte.get_bit(bit_pos)))
            bit_pos -= 1