import tkinter as tk
from tkinter import ttk
from my_constants import *

class StackDisplayFrame(ttk.Frame):
    def __init__(self, parent, stack, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5, width=50)
        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")

        # properties
        self.parent = parent
        self.stack = stack
        self.stack_display = []

        # tkinter widgets
        # heading
        self.stack_label = ttk.Label(self, text="STACK", style='MainWindowInner3.TLabel')
        self.stack_label.grid(column=0, row=0, pady=(0,0), padx=(0, 0), sticky="W")

        # populate empty values on stack
        for stack_index in range(0, STACK_SIZE):
            stack_element = ttk.Label(  self,
                                        text=f"{stack_index+1}: empty",
                                        width=8, 
                                        style="MCUBit.TLabel"      )
            stack_element.grid(column=0, row=stack_index+1, padx=0, pady=0, sticky="W")

            self.stack_display.append(stack_element)

        

    # Stack methods
    def update_stack(self):
        for stack_index in self.stack_display:
            if stack_index < len(self.stack):
                stack_index.configure(text=f"{stack_index+1}: 0x{self.stack[stack_index]:02X}")
            else:
                stack_index.configure(text=f"{stack_index+1}: -n/a-")




