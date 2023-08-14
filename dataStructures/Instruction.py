import tkinter as tk
from tkinter import ttk
from my_constants import*

class Instruction():
    def __init__(self, mnumonic, operand_1, operand_2):

        # list of tk.StringVar() to store intruction
        self.mnumonic = mnumonic
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    #  methods
    # set
    def set_mnumonic(self, new_value):
        self.mnumonic.set(new_value)

    def set_operand_1(self, new_value):
        self.operand_1.set(new_value)
    
    def set_operand_2(self, new_value):
        self.operand_2.set(new_value)

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


    