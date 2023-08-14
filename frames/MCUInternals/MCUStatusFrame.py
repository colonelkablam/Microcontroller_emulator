import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames.MCUInternals.MCUStatusFrames import ByteDisplayFrame


class MCUStatusFrame(ttk.Frame):
    def __init__(self, parent, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((4), weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent

        # tkinter widgets

        # panel label
        self.control_panel_label = ttk.Label(self, text=title, style='MainWindowInner.TLabel')
        self.control_panel_label.grid(column=0, row=0, sticky="N")

        # PROGRAM COUNTER
        self.PCL_display = ByteDisplayFrame(self, self.parent.get_byte_by_name("PCL"), "Program Counter", style='MainWindowInner.TLabel')
        self.PCL_display.grid(column=0, row=1, sticky="EW")
        # STATUS REG
        self.STATUS_display = ByteDisplayFrame(self, self.parent.get_byte_by_name("STATUS"), "Status Register", style='MainWindowInner.TLabel')
        self.STATUS_display.grid(column=0, row=2, sticky="EW")
        # WORKING REG
        self.WREG_display = ByteDisplayFrame(self, self.parent.get_w_register(), "Working Register", style='MainWindowInner.TLabel')
        self.WREG_display.grid(column=0, row=3, sticky="EW")

    def update_display(self):
        for widget in self.winfo_children():
            widget.update()






        








