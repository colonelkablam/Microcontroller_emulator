import tkinter as tk
from tkinter import ttk
from my_constants import *

class ByteDisplayFrame(ttk.Frame):
    def __init__(self, parent, bytes_tuple, display_bits=8, title="Unnamed", byte_heading=None, display_dec=True, display_hex=True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent

        # tuple of bytes
        self.bytes = bytes_tuple
        self.byte_value = bytes_tuple[0]

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
            byte_label = ttk.Label(self, text=f"{byte_heading}", style='MainWindowInner3.TLabel')
            byte_label.grid(column=0, row=0, columnspan=2, pady=(0,0), padx=(0,6), sticky="E")

        mem_label = ttk.Label(self, text=f"{title}", style='ByteDisplayHeading.TLabel')
        mem_label.grid(column=0, row=0, pady=(0,0), padx=(5, 15), sticky="EW")

        self.bit_frame = ttk.Frame(self, style="MCUByte.TFrame")
        self.bit_frame.grid(column=1, row=1, padx=(0,3), sticky="E")

        byte_value_frame = ttk.Frame(self, style="MCUByteValues.TFrame", padding=5)
        byte_value_frame.grid(column=0, row=1, padx=(0,0), pady=(0,0), sticky="EW")

        if display_dec:
            self.dec_label = ttk.Label(byte_value_frame, text="dec.", style='MainWindowInner3.TLabel')
            self.dec_label.grid(column=0, row=0, padx=(10,0), pady=(0,0), sticky="EW")

            self.dec_value = ttk.Label(byte_value_frame, width=3, textvariable=self.byte_value.get_dec(), style="MCUBit.TLabel")
            self.dec_value.grid(column=1, row=0, padx=(0,5), pady=(0,0), sticky="EW")

        if display_hex:
            self.hex_label = ttk.Label(byte_value_frame, text="hex.", style='MainWindowInner3.TLabel')
            self.hex_label.grid(column=2, row=0, padx=(0,0), pady=(0,0), sticky="EW")

            self.hex_value = ttk.Label(byte_value_frame, width=3, textvariable=self.byte_value.get_hex(), style="MCUBit.TLabel")
            self.hex_value.grid(column=3, row=0, padx=(0,10), pady=(0,0), sticky="EW")


        # populate bits from left to right (MSB to LSB)
        nth_byte = 0
        for bit_index in range(self.msb, -1, -1):
            bit = ttk.Label(self.bit_frame,
                            text=str(self.bytes[nth_byte].get_bit(bit_index % 8)), 
                            width=1, 
                            style="MCUBit.TLabel"                           )
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
