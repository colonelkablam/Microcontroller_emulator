import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import *
from my_enums import *
import re

class Compiler():
    def __init__(self, SFR_dict, instruction_set):

        self.whole_text = ""
        self.compiled_program = []
        self.SFR_dict = SFR_dict
        self.instruction_set = instruction_set
        self.error_log = []

    def get_instructions(self, whole_text):
        
        # split the lines into words - removes comments and blanks
        word_list_per_line = self._create_word_list_per_line(whole_text)

        # create empty program
        self.compiled_program.clear()
        temp_compiled_program = self._create_empty_program()
        
        # dictionary to store variable and subroutine address equivalents
        var_sub_dict = {}

        # keep track of instruction address
        PC = 0

        # iterate through code lines
        for code_line, instruction in enumerate(word_list_per_line):
            # empty instruction
            instruction_line = []

            ## IF INSTRUCTION from instruction set

            # if first part a recognised MNUMONIC then append next one or two parts into instruction code
            if instruction[0] in self.instruction_set:
                for i, part_instruction in enumerate(instruction):
                    # MNUMONIC
                    if i == 0:
                        instruction_line.append(part_instruction)
                    # 1st operand
                    elif i == 1: # can be literal value or address
                        if self._is_hex(part_instruction):              # is already in hex format; make sure 4 digit long
                            instruction_line.append(f"0x{int(part_instruction, 16):04X}")
                        elif self._is_decimal(part_instruction):        # else if decimal string turn into hex string
                            instruction_line.append(f"0x{int(part_instruction, 10):04X}")
                        elif part_instruction in self.SFR_dict.keys():  # or named SFR get address from dict (and format to hex string)
                            instruction_line.append(f"0x{self.SFR_dict[part_instruction]:04X}")
                        elif part_instruction in var_sub_dict.keys():   # else if in var_sub dict as already defined in code
                            instruction_line.append(var_sub_dict[part_instruction])
                        else:
                            instruction_line.append("") # operand 1 left empty if above criteria not met
                    # 2nd operand
                    elif i == 2: 
                        if self._is_one_char(part_instruction):         # one charcter only (defines destination or bit)
                            instruction_line.append(part_instruction)
                        else:
                            instruction_line.append("")                 # operand 2 left empty if above criteria not met

                    # stop instruction line; the rest can be ignored
                    elif i > 2:
                        break # if more parts ignore (no more than 3 parts needed)
                    else:
                        self.error_log.append(f"error compiling '{instruction}' on code editor line {code_line}; not recognised.")

                # insert in the correct program address
                temp_compiled_program[PC] = instruction_line
                # move to next line
                PC += 1


            ## ELSE if PROGRAM SECTION or SUBROUTINE definition
            
            # check 1st part ENDS with a ':' i.e. 'main:' or 'loop:'
            elif self._is_valid_subroutine(instruction[0]):
                # if only part PC remains unchanged, no CODE address given
                if len(instruction) == 1:
                    prog_sect = instruction[0][:-1] # remove colon
                    var_sub_dict.update({prog_sect : f"0x{PC:04X}"})

                # else if 3 parts and 2nd part is 'CODE' and 3rd valid hex address then use address as location
                elif len(instruction) == 3 and self._is_hex(instruction[2]) :
                    if instruction[1] == "CODE":
                        # store location in subroutine dict - format hex
                        prog_sect = instruction[0][:-1]
                        var_sub_dict.update({prog_sect : f"{int(instruction[2]):04X}"})
                else:
                    self.error_log.append(f"Error creating subroutine/program section from instruction '{instruction}' on line {code_line}.")

            # ELSE IF VARIABLE - single word not beginning with a number
            # if three parts (needed to define a variable address location), add variable to dictionary
            elif len(instruction) == 3 and re.search('^[^0-9]+\w+$', instruction[0]):
                if instruction[1] == "EQU":
                    if re.search('^0x[a-fA-F0-9]+$', instruction[2]): # is already in hex format; make sure 4 digit long
                            var_sub_dict.update({instruction[0] : f"0x{int(instruction[2], 16):04X}"})
                    elif re.search('^[0-9]*$', instruction[2]):  # else if decimal string turn into hex string
                            var_sub_dict.update({instruction[0] : f"0x{int(instruction[2], 10):04X}"})
                    else:
                        self.error_log.append(f"Error creating variable from instruction '{instruction}' on line {code_line}.")
                else:
                    self.error_log.append(f"Error creating variable from instruction '{instruction}' on line {code_line}.")

        # shorten program to compiled length
        self.compiled_program = temp_compiled_program[:PC]

        for i, instruction in enumerate(self.compiled_program):
            print(i, "-", instruction)

        for line in self.error_log:
            print(line)

        # return compiled program
        return self.compiled_program


    # create empty list for upload to MCU
    def _create_empty_program(self):
        compiled_program = []
        for empty_instruction in range(256):
            compiled_program.append(["ADDWF", "0xFF", "-"]) # list of 3 empty strings (MCU format)
        return compiled_program

    # removes blanks and comments and puts text into a list of word lists
    def _create_word_list_per_line(self, whole_text):
        word_list_per_line = []
        for line in whole_text.split("\n"):
            word_list = []
            # for each word in line
            for word in line.split():
                # check for ';' comment character to ignore whole/rest of line
                if word[0] == ";":
                    break
                else:
                    word_list.append(word)
            # add word list to line list if any words
            if len(word_list) != 0:
                word_list_per_line.append(word_list)
        
        return word_list_per_line

    def _is_hex(self, string):
        return re.search('^0x[a-fA-F0-9]+$', string)

    def _is_decimal(self, string):
        return re.search('^[0-9]*$', string)

    def _is_one_char(self, string):
        return re.search('^[0-9]{1}|[WwFf]{1}$', string)
    
    def _is_valid_subroutine(self, string):
        return re.search('^[^0-9]+\w+:$', string)

    def _is_valid_variable(self, string):
        return re.search('^[^0-9]+\w+$', string)


