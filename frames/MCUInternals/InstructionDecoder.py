import tkinter as tk
from tkinter import ttk
from my_constants import*


class InstructionDecoder():
    def __init__(self, parent, program_counter):

        # properties

        # split the instructions
        self.mnumonic = ""
        self.operand_1 = "0x00"
        self.operand_2 = 1

        self.parent = parent
        self.program_counter = program_counter
    

    # InstructionDecoder methods

    def get_new_program_address(self, instruction):
        # split the instruction
        self._split_instruction(instruction)

        # BYTE-ORIENTATED FILE REGISTER OPERATIONS - only act on File Registers
        if self.mnumonic == "ADDWF":
            w = self._get_w_reg_value()
            f_value = self._get_file_reg_value(self.operand_1)
            total = w + f_value

            # set C bit according to carry over
            self._handle_C_bit(total)
        
            # handle byte wrap-around
            result = total % 256

            # set Z bit according to result
            self._handle_Z_bit(result)

            # store value of reg in w or f (0 or 1)
            loc_string = self._where_to_store_result(result, self.operand_1, self.operand_2)
            # advance to next program line

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self.add_to_log(f"ADDWF; W_REG value ({w}) + FILE REG 0x{self.operand_1:02X} value ({f_value}) --> {loc_string}")


        # clear value of file register given
        elif self.mnumonic == "CLRF":
            self._set_file_reg_value(self.operand_1, 0)
           
            # always set in CLRF
            self._handle_Z_bit(0)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self.add_to_log(f"CLRF; FILE REG addr. 0x{self.operand_1:02X} cleared")
        
        # clear value of W reg
        elif self.mnumonic == "CLRW":
            self._set_w_reg_value(0)

            # always set in CLRW
            self._handle_Z_bit(0)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self.add_to_log(f"CLRW; W_REG cleared")

        # move file register of address given (to 0 - W reg, or 1 - file reg) 
        elif self.mnumonic == "MOVF":
            result = self._get_file_reg_value(self.operand_1)

            # Z bit
            self._handle_Z_bit(result)

            # store value of reg in w or f (0 or 1)
            loc_string = self._where_to_store_result(result, self.operand_1, self.operand_2)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self.add_to_log(f"MOVF; FILE REG addr. 0x{self.operand_1:02X} value ({result}) --> {loc_string}")

        # move W reg to file register given
        elif self.mnumonic == "MOVWF":
            w = self._get_w_reg_value()

            self._set_file_reg_value(self.operand_1, w)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self.add_to_log(f"MOVWF; W_REG value({w}) --> FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}]")


        # No operation - do nothing but advance program counter
        elif self.mnumonic == "NOP":
            # advance to next program line
            self.program_counter.advance_one()
            # log
            self.add_to_log(f"NOP; No operation executed")


        # BIT-ORIENTATED FILE REGISTER OPERATIONS - only act on File Registers

        # LITERAL AND CONTROL OPERATIONS
        elif self.mnumonic == "ADDLW":
            w = self._get_w_reg_value()
            total = w + self.operand_1

            # handle C bit
            self._handle_C_bit(total)
        
            # handle byte wrap-around
            result = total % 256

            # handle Z bit
            self._handle_Z_bit(result)

            #set result
            self._set_w_reg_value(result)

            # advance to next program line
            self.program_counter.advance_one()
            # log
            self.add_to_log(f"ADDLW; literal value ({self.operand_1}) + W_REG value ({w}) --> W_REG (result: {self._get_w_reg_value()})")

        elif self.mnumonic == "GOTO":
            # set program counter to new address
            self.program_counter.set_value(self.operand_1)
            # set next cycle to be an NOP as GOTO uses 2 instruction cycles
            self.parent.set_next_cycle_NOP()
            # log
            self.add_to_log(f"GOTO; address 0x{self.operand_1:02X} [{self.operand_1}]; takes 2 instruction cycles")

        elif self.mnumonic == "CALL":
            # advance to next program line
            self.program_counter.set_value(self.operand_1)
            # then push current PCL to stack

        elif self.mnumonic == "MOVLW":
            self._set_w_reg_value(self.operand_1)
            # advance to next program line
            self.program_counter.advance_one()
            # log
            self.add_to_log(f"MOVLW; literal value ({self.operand_1}) --> W_REG addr.")

        else:
            self.program_counter.advance_one()
            self.add_to_log(f"Unrecognised instruction; {instruction}")
            # advance to next program line


    ## InstructionDecoder internal methods

    # get numerical address location by name
    def _get_address_by_name(self, name):
        return self.parent.SFR_dict[name]

    # access to named registers
    def _get_w_reg_value(self):
        return self.parent.get_w_register().get_dec_value()
        
    def _set_w_reg_value(self, value=0):
        self.parent.set_w_register(value)

    # access to file registers with address
    def _get_file_reg_value(self, file_reg):
        return self.parent.get_byte_by_address(file_reg).get_dec_value()

    def _set_file_reg_value(self, file_reg, value=0):
        return self.parent.set_byte_by_address(file_reg, value)

    # determine where to store result (w or f)
    def _where_to_store_result(self, result, operand_1, operand_2):
        if operand_2 == 0:
            self._set_w_reg_value(result)
            loc_string = f"W_REG (result: {result})"
        elif operand_2 == 1:
            self._set_file_reg_value(operand_1, result)
            loc_string = f"FILE REG addr. 0x{operand_1:02X} (result: {result})"
        else:
            self.add_to_log(f"Second operand needs to be either 0 or 1; value given was '{operand_2}', defaulted to 1.")
        # return string of location
        return loc_string

    # set C bit in STATUS if results in carry over, clear if not
    def _handle_C_bit(self, total):
            if total >= 256:
                self.parent.set_C_bit_status()
            else:
                self.parent.clear_C_bit_status()

    # set Z bit STATUS if result is 0, clear if not
    def _handle_Z_bit(self, result):
            if result == 0:
                self.parent.set_Z_bit_status()
            else:
                self.parent.clear_Z_bit_status()

    # set/clear bit from file register
    def _set_file_reg_value_bit(self, file_reg, bit):
        self.parent.set_file_reg_bit(file_reg, bit)
    def _clear_file_reg_bit(self, file_reg, bit):
        self.parent.clear_file_reg_bit(file_reg, bit)

    # add message to log through parents
    def add_to_log(self, message):
        self.parent.parent.add_to_log(message)

    # formatting the instructions
    def _split_instruction(self, instruction):
        # get the mnumonic string
        self.mnumonic = instruction[0]

        op1 = 0
        # get the 1st operand - needs to be able to accept empty argument
        try:
            op1 = int(instruction[1], 16) # convert to decimal for use with data and prog memory lists
        except Exception:
            op1 = 0
        self.operand_1 = op1
        
        op2 = 1
        # get the 2nd operand - needs to be either 1 or 0 (for destination of a calculation), or 1-7 (for bit address)
        try:
            if instruction[2] != '':
                op2 = int(instruction[2])
        except Exception:
            op2 = 1

        self.operand_2 = op2
