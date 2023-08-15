import tkinter as tk
from tkinter import ttk
from my_constants import *


class ByteDisplayFrame(ttk.Frame):
    def __init__(self, parent, bytes_tuple, display_bits=8, title="Unnamed", byte_heading=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent

        # tuple of bytes
        self.bytes = bytes_tuple

        # msb of combined bytes to display from
        num_of_bits = 8 * len(self.bytes)
        if display_bits > num_of_bits or display_bits < 1:
            self.msb = num_of_bits - 1
        else:
            self.msb = display_bits - 1

        # list for bits
        self.bits = []

        # highlighting
        self.highlighted = False

        # tkinter widgets

        # panel label
        if byte_heading != None:
            self.byte_label = ttk.Label(self, text=f"{byte_heading}", style='MainWindowInner3.TLabel')
            self.byte_label.grid(column=0, row=0, columnspan=2, pady=(0,0), padx=(0,6), sticky="E")

        self.mem_label = ttk.Label(self, text=f"{title}", style='MainWindowInner3.TLabel')
        self.mem_label.grid(column=0, row=1, pady=(0,0), padx=(5, 0), sticky="W")

        self.bit_frame = ttk.Frame(self, style="MCUByte.TFrame")
        self.bit_frame.grid(column=1, row=1, padx=(0,3), sticky="E")

        # populate bits from left to right (MSB to LSB)
        nth_byte = 0
        for bit_index in range(self.msb, -1, -1):
            bit = ttk.Label(self.bit_frame, text=str(self.bytes[nth_byte].get_bit(bit_index % 8)), width=1, style="MCUBit.TLabel")
            bit.grid(column=self.msb-bit_index, row=0, padx=2, pady=2)
            if bit_index % 8 == 0:
                nth_byte += 1
            self.bits.insert(0, bit) # store in a list for updating as needed

    # update method rather than using tkinter value objects with textvariable
    # (would need one for each bit in every byte in memory otherwise!)
    def update(self):
        nth_byte = 0
        bit_index = self.msb
        # iterate through bits of combined bytes
        for bit_index in range(self.msb, -1, -1): # got through bit list
            bit_value = self.bytes[nth_byte].get_bit(bit_index % 8) # get bit value
            # test to get correct highlight
            if bit_value == 0:
                style = "MCUBit.TLabel"
            else :
                style = "MCUBitHighlight.TLabel"
            # apply update
            self.bits[bit_index].configure(text=str(bit_value), style=style)
            # adjust byte index
            if bit_index % 8 == 0:
                nth_byte += 1
        # if self.highlighted == True:
        #     self.unhighlight()

    def highlight(self):
        self.bit_frame.configure( style="MCUByteHighlight.TFrame")

    def unhighlight(self):
        self.bit_frame.configure(style="MCUByte.TFrame")
