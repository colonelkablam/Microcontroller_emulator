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
        self.stack_display_list = []

        # tkinter widgets
        # heading
        self.stack_label = ttk.Label(self, text="STACK", style='MainWindowInner3.TLabel')
        self.stack_label.grid(column=0, row=0, pady=(0,0), padx=(0, 0), sticky="W")

        # initialise the stack display so will show a holding label
        # add empty 'backstop to stack'
        self.initialise_stack_display_list("- empty -")

        
    # STACK methods

    def update(self):
        print(self.stack)
        stack_length = len(self.stack)
        # test to see if empty
        if stack_length == 0:
            self.stack_display_list[0].configure(text="- empty -")
            self.stack_display_list[0].grid()
        else:
            i = 1
            for element in self.stack_display_list:
                if i <= stack_length:
                    element.configure(text=f"{i} - {self.stack[i-1]:04X}h")
                    element.grid()
                else:
                    element.grid_remove()
                i+=1

            self.stack_display_list[i+1].grid()
            self.stack_display_list[i+1].configure(text="-  end  -")



    def initialise_stack_display_list(self, text):
        for stack_level in range(0, STACK_SIZE):
            stack_element = ttk.Label(  self,
                                        width=9, 
                                        style="Stack.TLabel"      )
            stack_element.grid(column=0, row=stack_level, padx=0, pady=(0,3), sticky="W")
            stack_element.grid_remove()
            self.stack_display_list.append(stack_element)

            self.stack_display_list[0].configure(text=text)
            self.stack_display_list[0].grid()
            
            # add empty 'backstop to stack'

        






