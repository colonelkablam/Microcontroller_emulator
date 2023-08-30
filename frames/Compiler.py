import tkinter as tk
from tkinter import ttk
from enum import Enum
from my_constants import *
from my_enums import *
import re
from frames import LogDisplayFrame


class Compiler():
    def __init__(self, SFR_dict, instruction_set):

        self.whole_text = ""
        self.compiled_program = []
        self.SFR_dict = SFR_dict
        self.instruction_set = instruction_set
        self.error_log = []

    def get_instructions(self, whole_text):

        
        # split the lines into words - removes comments and blanks and sets to uppercase
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
               
                # determine format of hex (CALL and GOTO need to address Program mem (13-bit), others are 8-bit)
                hex_digits = 2
                if instruction[0] == "CALL" or instruction[0] == "GOTO":
                    hex_digits = 4

                for i, part_instruction in enumerate(instruction):
                    # MNUMONIC
                    if i == 0:
                        instruction_line.append(part_instruction)
                    # 1st operand
                    elif i == 1: # can be literal value or address
                        if self._is_hex(part_instruction):              # is already in hex format; make sure 4 digit long
                            instruction_line.append(self._string_to_hex_string(part_instruction, 16, hex_digits))
                        elif self._is_decimal(part_instruction):        # else if decimal string turn into hex string
                            instruction_line.append(self._string_to_hex_string(part_instruction, 10, hex_digits))
                        elif part_instruction in self.SFR_dict.keys():  # or named SFR get address from dict (and format to hex string)
                            instruction_line.append(self._int_to_hex_string(self.SFR_dict[part_instruction], hex_digits))
                        elif part_instruction in var_sub_dict.keys():   # else if in var_sub dict as already defined in code
                            instruction_line.append(var_sub_dict[part_instruction])
                        elif self._is_valid_variable(part_instruction):
                            instruction_line.append(part_instruction)   # will be used as a prog section later
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

                # add empty instruction parts to program if none in code (correct format for MCU upload)
                if len(instruction) == 2:
                    instruction_line.append("")
                elif len(instruction) == 1:
                    instruction_line.append("")
                    instruction_line.append("") 

                # insert in the correct program address
                temp_compiled_program[PC] = instruction_line
                # move to next line
                PC += 1


            ## ELSE if PROGRAM SECTION or SUBROUTINE definition
            
            # check 1st part ENDS with a ':' i.e. 'main:' or 'loop:'
            elif self._is_valid_subroutine(instruction[0]):
                # if only part PC remains unchanged, no PSECT address given
                if len(instruction) == 1:
                    prog_sect = instruction[0][:-1] # remove colon
                    var_sub_dict.update({prog_sect : self._int_to_hex_string(PC, 4)})

                # else if 3 parts and 2nd part is 'PSECT' and 3rd valid hex address then use address as location
                elif len(instruction) == 3 and self._is_hex(instruction[2]):
                    if instruction[1] == "PSECT":
                        # store location in subroutine dict - format hex
                        prog_sect = instruction[0][:-1]
                        var_sub_dict.update({prog_sect : self._string_to_hex_string(instruction[2], 16, 4)})

                        # move to inserting lines past address given by PSECT instruction
                        PC = int(instruction[2], 16)
                else:
                    self.error_log.append(f"Error creating subroutine/program section from instruction '{instruction}' on line {code_line}.")


            # ELSE IF VARIABLE - single word not beginning with a number
            # if three parts (needed to define a variable address location), add variable to dictionary
            elif len(instruction) == 3 and self._is_valid_variable(instruction[0]):
                if instruction[1] == "EQU":
                    if self._is_hex(instruction[2]): # is already in hex format; make sure 4 digit long
                            var_sub_dict.update({instruction[0] : self._string_to_hex_string(instruction[2], 16, 2)})
                    else:
                        self.error_log.append(f"Error creating variable from instruction '{instruction}' on line {code_line}.")
                else:
                    self.error_log.append(f"Error creating variable from instruction '{instruction}' on line {code_line}.")

        # replace any subroutines and PSECT definitions with address
        for line in temp_compiled_program:
            if line[1] in var_sub_dict.keys():
                line[1] = var_sub_dict[line[1]]

        # shorten program to compiled length
        self.compiled_program = temp_compiled_program[:PC]

        self._display_assembled_code()

        # return compiled program
        return self.compiled_program

    # create a pop-up window showing code and any errors raised
    def _display_assembled_code(self):
        prog_display_window = tk.Toplevel()
        prog_display_window.title("Compiled Code Display")
        prog_display_window.geometry("250x350+20+20")

        prog_display_window.columnconfigure(0, weight=1)
        prog_display_window.rowconfigure(0, weight=1)


        # iterate through error log
        text = "ERROR LOG:\n"
        for line in self.error_log:
            text = (text + line + '\n')

        text = text + '\nPROGRAM:\n\n'

        # iterate through program
        for instruction in self.compiled_program:
            line_text = ""
            for part in instruction:
                line_text = line_text + part + '\t'
            text = text + line_text + '\n'

        compile_text = tk.StringVar(value=text)
        compile_log_frame = LogDisplayFrame(prog_display_window, compile_text)
        compile_log_frame.grid(column=0, row=0, sticky="NSEW")


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
                    word_list.append(word.upper())
            # add word list to line list if any words
            if len(word_list) != 0:
                word_list_per_line.append(word_list)
        
        return word_list_per_line

    # formatting hex for program
    def _string_to_hex_string(self, string, base, digits):
        return f"0x{int(string, base):0{digits}X}"

    def _int_to_hex_string(self, int, digits):
        return f"0x{int:0{digits}X}"

    # testing input string
    def _is_hex(self, string):
        return re.search('^0[Xx][a-fA-F0-9]+$', string)

    def _is_decimal(self, string):
        return re.search('^[0-9]*$', string)

    def _is_one_char(self, string):
        return re.search('^[0-9WwFf]{1}$', string)
    
    def _is_valid_subroutine(self, string):
        return re.search('^[^0-9]{1}\w*:$', string)

    def _is_valid_variable(self, string):
        return re.search('^[^0-9]{1}\w*$', string)


