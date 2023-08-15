import tkinter as tk
from tkinter import ttk
from my_constants import *

class StackDisplayFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super.__init__(parent, *args, *kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # properties
        self.parent = parent
        #self.stack = stack

    # Stack methods
