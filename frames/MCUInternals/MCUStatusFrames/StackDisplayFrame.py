import tkinter as tk
from tkinter import ttk
from my_constants import *

class StackDisplayFrame(ttk.Frame):
    def __init__(self, parent, stack, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")

        # properties
        self.parent = parent
        self.stack = stack
        self.stack_display_list = []
        self.previous_length = 0

        # tkinter widgets
        # heading
        self.stack_label = ttk.Label(self, text=" STACK:\n-  top  -", style='MainWindowInner3.TLabel')
        self.stack_label.grid(column=0, row=0, pady=(0,0), padx=(0, 0), sticky="EW")

        # frame for list of stack elements
        self.list_frame = ttk.Frame(self, style='MainWindowInner3.TLabel')
        self.list_frame.grid(column=0, row=1, pady=(0,0), padx=(0, 0), sticky="NSEW")

        # initialise the stack display
        self.initialise_stack_display_list()

        
    # STACK methods

    def update(self):
        print(self.stack)
        stack_length = len(self.stack)

        for i, element in enumerate(self.stack_display_list, 1):
            if stack_length == 0:
                element.configure(text="  empty  ", style="Stack.TLabel")
                element.grid()
                break
            elif i <= stack_length:
                element.configure(text=f"{i} - {self.stack[i-1]:04X}h", style="Stack.TLabel" )
                element.grid()
            elif i == stack_length + 1:
                element.configure(text="-bottom-", style='MainWindowInner3.TLabel')
                element.grid()
            else:
                element.grid_remove()


    def initialise_stack_display_list(self):
        for stack_level in range(0, STACK_SIZE + 1): # +1 to store last status label
            stack_element = ttk.Label(  self.list_frame,
                                        width=9, 
                                        style="Stack.TLabel"      )
            stack_element.grid(column=0, row=stack_level, padx=0, pady=(0,3), sticky="EW")
            stack_element.grid_remove()
            self.stack_display_list.append(stack_element)
        
        # add empty 'backstop to stack'
        self.stack_display_list[0].configure(text="  empty  ", style="Stack.TLabel")
        self.stack_display_list[0].grid()
        self.stack_display_list[1].configure(text="-  end  -", style='MainWindowInner3.TLabel')
        self.stack_display_list[1].grid()
            


        






