import tkinter as tk
from tkinter import ttk
from my_constants import *

class BinaryDisplayFrame(ttk.Frame):
    def __init__(self, parent, n_bit_number, title="Unnamed", bit_numbering=None, display_dec=True, display_hex=True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent

        # binary number
        self.n_bit_number_obj = n_bit_number # object of number to display
        self.number_of_bits = n_bit_number.get_number_of_bits() # number of bits to diplay

        # msb of binary number
        self.msb = self.number_of_bits - 1


        # list for bits
        self.bits = []

        # highlighting
        self.highlighted = False

        # tkinter widgets

        # panel label
        if bit_numbering != None:
            byte_label = ttk.Label(self, text=f"{bit_numbering}", style="BitPosition.TLabel")
            byte_label.grid(column=0, row=0, columnspan=2, pady=(0,0), padx=(0,6), sticky="E")

        if display_dec and display_hex:
            title_row = 0
            byte_value_frame = ttk.Frame(self, style="MCUByteValues.TFrame", padding=5)
            byte_value_frame.grid(column=0, row=1, padx=(0,0), pady=(0,0), sticky="EW")
        else:
            title_row = 1

        mem_label = ttk.Label(self, text=f"{title}", style='ByteDisplayHeading.TLabel')
        mem_label.grid(column=0, row=title_row, pady=(0,0), padx=(5, 15), sticky="EW")

        self.bit_frame = ttk.Frame(self, style="MCUByte.TFrame")
        self.bit_frame.grid(column=1, row=1, padx=(0,3), sticky="E")

        if display_dec:
            dec_label = ttk.Label(byte_value_frame, text="dec.", style='MainWindowInner3.TLabel')
            dec_label.grid(column=0, row=0, padx=(10,0), pady=(0,0), sticky="EW")

            dec_value = ttk.Label(byte_value_frame, width=3, textvariable=self.n_bit_number_obj.get_dec(), style="MCUBit.TLabel")
            dec_value.grid(column=1, row=0, padx=(0,5), pady=(0,0), sticky="EW")

        if display_hex:
            hex_label = ttk.Label(byte_value_frame, text="hex.", style='MainWindowInner3.TLabel')
            hex_label.grid(column=2, row=0, padx=(0,0), pady=(0,0), sticky="EW")

            hex_value = ttk.Label(byte_value_frame, textvariable=self.n_bit_number_obj.get_hex(), style="MCUBit.TLabel")
            hex_value.grid(column=3, row=0, padx=(0,10), pady=(0,0), sticky="EW")


        # populate bits from left to right (MSB to LSB)
        for bit_index in range(self.msb, -1, -1):
            bit = ttk.Label(self.bit_frame,
                            text=str(self.n_bit_number_obj.get_bit(bit_index)), 
                            width=1, 
                            style="MCUBit.TLabel"                           )
            bit.grid(column=self.msb-bit_index, row=0, padx=2, pady=2)
            self.bits.insert(0, bit) # store in a list for updating as needed

    # update method rather than using tkinter value objects with textvariable
    # (would need one for each bit in every byte in memory otherwise!)
    def update(self):
        # iterate through bits of combined bytes
        for bit_index in range(self.msb, -1, -1): # got through bit list
            bit_value = self.n_bit_number_obj.get_bit(bit_index) # get bit value
            # test to get correct highlight
            if bit_value == 0:
                style = "MCUBit.TLabel"
            else :
                style = "MCUBitHighlight.TLabel"
            # apply update
            self.bits[bit_index].configure(text=str(bit_value), style=style)


    def highlight(self):
        self.bit_frame.configure( style="MCUByteHighlight.TFrame")

    def unhighlight(self):
        self.bit_frame.configure(style="MCUByte.TFrame")
