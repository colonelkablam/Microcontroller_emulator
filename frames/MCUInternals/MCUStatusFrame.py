import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames.MCUInternals.MCUStatusFrames import ByteDisplayFrame, StackDisplayFrame


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
        self.PCL_display = ByteDisplayFrame(    self, 
                                                (self.parent.get_byte_by_name("PCLATH"), self.parent.get_byte_by_name("PCL")),
                                                display_bits=13, 
                                                title="Program Counter",
                                                byte_heading="12 -PCLATH-  7 ----- PCL ---- 0", 
                                                style='MainWindowInner.TLabel'                  )
        
        self.PCL_display.grid(column=0, row=1, columnspan=2, sticky="EW")

        # STACK - displayed within the MCU status frame
     
        # STATUS REG
        self.STATUS_display = ByteDisplayFrame( self,
                                                (self.parent.get_byte_by_name("STATUS"), ),
                                                title="Status Register",
                                                byte_heading=              "7           z dc c", 
                                                style='MainWindowInner.TLabel'                  )

        self.STATUS_display.grid(column=1, row=2, sticky="EW")
        
        # WORKING REG
        self.WREG_display =     ByteDisplayFrame(self,
                                                (self.parent.get_w_register(), ),
                                                title="Working Register",
                                                byte_heading=              "7                0", 
                                                style='MainWindowInner.TLabel'                  )
        self.WREG_display.grid(column=1, row=3, sticky="EW")

        # PORTA
        self.PORTA_display =    ByteDisplayFrame(self,
                                                (self.parent.get_byte_by_name("PORTA"), ),
                                                title="PORTA",
                                                byte_heading=              "7                0", 
                                                style='MainWindowInner.TLabel'                  )
        self.PORTA_display.grid(column=1, row=4, pady=(10,0), sticky="EW")

        # PORTB
        self.PARTB_display =     ByteDisplayFrame(self,
                                                (self.parent.get_byte_by_name("PORTB"), ),
                                                title="PORTB",
                                                #byte_heading=              "7 6 5 4 3 2 1 0                 0", 
                                                style='MainWindowInner.TLabel'                  )
        self.PARTB_display.grid(column=1, row=5, sticky="EW")

        # MCU status info
        self.status_info_frame = ttk.Frame(self, style="MainWindowInner2.TFrame", padding=10)
        self.status_info_frame.grid(column=0, row=6)

        self

    def update_display(self):
        for widget in self.winfo_children():
            widget.update()

    def highlight_byte(self, byte):
        if byte == W_REG:
            self.WREG_display.highlight()
        elif byte == STATUS:
            self.STATUS_display.highlight()






        








