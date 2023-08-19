import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames.MCUInternals.MCUStatusFrames import BinaryDisplayFrame


class MCUStatusFrame(ttk.Frame):
    def __init__(self, parent, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=10)
        self.columnconfigure(1, weight=1)
        #self.rowconfigure(2, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent

        # tkinter widgets

        # panel label
        self.control_panel_label = ttk.Label(self, text=title, style='MainWindowInner.TLabel')
        self.control_panel_label.grid(column=0, row=0, columnspan=2, sticky="NE")

        # PROGRAM COUNTER - need to enter a tuple of the byte(s) being displayed
        self.PCL_display = BinaryDisplayFrame(  self, 
                                                self.parent.get_PC_13bit_representation(),
                                                title="Program Counter",
                                                bit_numbering="12 -PCLATH-  7 ----- PCL ---- 0",
                                                style='MainWindowInner.TLabel'                  )
        
        self.PCL_display.grid(column=0, row=1, columnspan=2, sticky="EW")

        # STACK - displayed within the MCU status frame but contained in MCUFrame as a data holder
     
        # STATUS REG
        self.STATUS_display = BinaryDisplayFrame(   self,
                                                    self.parent.get_byte_by_name("STATUS"),
                                                    title = "Status Register",
                                                    bit_numbering =              "7           z dc c"     )

        self.STATUS_display.grid(column=1, row=2, sticky="EW")
        
        # WORKING REG
        self.WREG_display = BinaryDisplayFrame( self,
                                                self.parent.get_w_register(),
                                                title = "Working Register",
                                                bit_numbering =              "7                0"     )
        self.WREG_display.grid(column=1, row=3, sticky="EW")

        # PORTA
        self.PORTA_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("PORTA"),
                                                display_dec = False,
                                                display_hex = False,
                                                title = "PORTA",
                                                bit_numbering =              "7                0"   )
        self.PORTA_display.grid(column=1, row=4, pady=(10,0), sticky="NEW")
        
        # TRISA
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("TRISA"),
                                                display_dec = False,
                                                display_hex = False,
                                                title = "TRISA",
                                                bit_numbering =              "7  6  5  4  3  2  1  0"   )
        self.PARTB_display.grid(column=1, row=5, pady=(0,10), sticky="NEW")
        
        # PORTB
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("PORTB"),
                                                display_dec=False,
                                                display_hex=False,
                                                title="PORTB"                      )
        self.PARTB_display.grid(column=1, row=6, pady=(10,0), sticky="NEW")

        # TRISB
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("TRISB"),
                                                display_dec=False,
                                                display_hex=False,
                                                title="TRISB"                      )
        self.PARTB_display.grid(column=1, row=7, pady=(0,10), sticky="NEW")

        # MCU status info
        # self.status_info_frame = ttk.Frame(self, style="MainWindowInner2.TFrame", padding=10)
        # self.status_info_frame.grid(column=0, row=6)

        self

    def update_display(self):
        for widget in self.winfo_children():
            widget.update()

    def highlight_byte(self, byte):
        if byte == W_REG:
            self.WREG_display.highlight()
        elif byte == STATUS:
            self.STATUS_display.highlight()






        








