import tkinter as tk
from tkinter import ttk
from my_constants import*

# stores tk.StringVar objects with the instructions 
class Instruction():
    def __init__(self, mnumonic="ADDLW", operand_1="0xFF", operand_2="-"):

        # list of tk.StringVar() to store intruction
        self.mnumonic = tk.StringVar(value=mnumonic)
        self.operand_1 = tk.StringVar(value=operand_1)
        self.operand_2 = tk.StringVar(value=operand_2)

    #  methods
    # set
    def set_mnumonic(self, new_value):
        self.mnumonic.set(new_value)

    def set_operand_1(self, new_value):
        self.operand_1.set(new_value)
    
    def set_operand_2(self, new_value):
        self.operand_2.set(new_value)

    def set_instruction(self, mnumonic="ADDLW", operand_1="0xFF", operand_2="-"):
         self.mnumonic.set(mnumonic)
         self.operand_1.set(operand_1)
         self.operand_2.set(operand_2)

    # get
    # return tuple of the instruction as strings
    def get_instruction(self):
        return (self.mnumonic.get(), self.operand_1.get(), self.operand_2.get())

    def get_mnumonic(self):
        return self.mnumonic

    def get_operand_1(self):
        return self.operand_1
    
    def get_operand_2(self):
        return self.operand_2


    