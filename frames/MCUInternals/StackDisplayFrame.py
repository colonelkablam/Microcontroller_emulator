import tkinter as tk
from tkinter import ttk
from collections import deque
from my_constants import *

class StackDisplayFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner2.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")

        # properties
        self.parent = parent
        self.stack = deque(maxlen=STACK_SIZE) # keep stack to * elements
        self.stack_display_list = []
        self.previous_stack_length = 0

        # tkinter widgets
        # heading
        stack_label = ttk.Label(self, text="STACK\n-top-", style='MainWindowInner3.TLabel')
        stack_label.grid(column=0, row=0, pady=(0,0), padx=(0, 0), sticky="EW")

        # frame for list of stack elements
        self.list_frame = ttk.Frame(self, style='MainWindowInner3.TLabel', height=190)
        self.list_frame.grid(column=0, row=1, pady=(0,0), padx=(0, 0), sticky="NSEW")
        self.list_frame.grid_propagate(0)

        # bottom
        stack_label = ttk.Label(self, text="-end-", style='MainWindowInner3.TLabel')
        stack_label.grid(column=0, row=3, pady=(0,0), padx=(0, 0), sticky="EW")

        # initialise the stack display
        self.initialise_stack_display_list()

        
    # STACK methods

    def update(self):
        stack_length = len(self.stack)
        # check to see if need to highlight a stack increase
        if self.previous_stack_length < stack_length:
            stack_increased = True
        else:
            stack_increased = False
        # record prev value
        self.previous_stack_length = stack_length

        style = "Stack.TLabel"
        # go through list of labels and populate according to the stack contents
        for i, element in enumerate(self.stack_display_list):
            # populate labels - removing any that are empty
            if i < stack_length:
                # highlight new element
                if stack_increased and i == 0:
                    style = "StackHighlighted.TLabel"
                element.configure(text=f"{self.stack[i-1]:04X}h", style=style )
                element.grid()
                style = "Stack.TLabel"

            else:
                element.grid_remove() # hide

        if stack_length == 0:
            self._add_empty_label() # show stack is empty

    # clear stack and display
    def clear_stack(self):
        for element in self.stack_display_list:
            element.grid_remove()
        self.stack.clear()

    # access to the stack data structure
    def get_stack(self):
        return self.stack

    # return top element
    def pop_stack(self):
        if len(self.stack) != 0:
            first_in_queue = self.stack.pop()
        else:
            first_in_queue = None
        return first_in_queue

    # add to stack - 8 deep
    def push_stack(self, new_address=17):
        # **some logic** to implement an 8 deep stack to be added
        self.stack.append(new_address)

    def initialise_stack_display_list(self):
        for stack_level in range(0, STACK_SIZE):
            stack_element = ttk.Label(  self.list_frame,
                                        width=5, 
                                        style="Stack.TLabel"      )
            stack_element.grid(column=0, row=stack_level, padx=0, pady=(0,3), sticky="EW")
            stack_element.grid_remove()
            self.stack_display_list.append(stack_element)
            self._add_empty_label() # show stack is empty
    
    # add empty 'backstop to stack'
    def _add_empty_label(self):
        self.stack_display_list[0].configure(text="empty", style="Stack.TLabel")
        self.stack_display_list[0].grid()

            


        






