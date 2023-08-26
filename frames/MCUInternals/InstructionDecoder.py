import tkinter as tk
from tkinter import ttk
from my_constants import *
from my_enums import Instruction as Inst

class InstructionDecoder():
    def __init__(self, parent, intruction_set, program_counter):

        # properties

        # split the instructions
        self.mnumonic = ""
        self.operand_1 = "0x00"
        self.operand_2 = 1

        self.parent = parent
        self.instruction_set = intruction_set
        self.program_counter = program_counter
    

    ## InstructionDecoder methods

    def get_new_program_address(self, instruction):
        # split the instruction
        self._split_instruction(instruction)

        # see if INSTRUCTION Mnumonic in set
        if self.mnumonic not in self.instruction_set:
            self._add_to_log(f"'{self.mnumonic}' is an unrecognised mnumonic.")
            # advance to next program line
            self.program_counter.advance_one()

        ## BYTE-ORIENTATED FILE REGISTER OPERATIONS - only act on File Registers
        
        # ADDWF Add the contents of w reg and file reg, storing result in either
        elif self.mnumonic == Inst.ADDWL.name:
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
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"ADDWF; W_REG value ({w}) + FILE REG 0x{self.operand_1:02X} value ({f_value}) --> {loc_string}")

        # ANDWF Add the contents of w reg and file reg, storing result in either
        elif self.mnumonic == Inst.ANDWF.name:
            w = self._get_w_reg_value()
            f_value = self._get_file_reg_value(self.operand_1)
            result = w & f_value

            # set Z bit according to result
            self._handle_Z_bit(result)

            # store value of reg in w or f (0 or 1)
            loc_string = self._where_to_store_result(result, self.operand_1, self.operand_2)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"ANDWF; W_REG value ({w}) bitwise & with FILE REG 0x{self.operand_1:02X} value ({f_value}) --> {loc_string}\n w: {w:08b}\n l: {f_value:08b}&\n  = {result:08b}")


        # CLRF clear value of file register given
        elif self.mnumonic == Inst.CLRF.name:
            self._set_file_reg_value(self.operand_1, 0)
           
            # always set in CLRF
            self._handle_Z_bit(0)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"CLRF; FILE REG addr. 0x{self.operand_1:02X} cleared")
        
        # CLRW clear value of W reg
        elif self.mnumonic == Inst.CLRW.name:
            self._set_w_reg_value(0)

            # always set in CLRW
            self._handle_Z_bit(0)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"CLRW; W_REG cleared")

        # MOVF move file register of address given (to 0 - W reg, or 1 - file reg) 
        elif self.mnumonic == Inst.MOVF.name:
            result = self._get_file_reg_value(self.operand_1)

            # Z bit
            self._handle_Z_bit(result)

            # store value of reg in w or f (0 or 1)
            loc_string = self._where_to_store_result(result, self.operand_1, self.operand_2)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"MOVF; FILE REG addr. 0x{self.operand_1:02X} value ({result}) --> {loc_string}")

        # move W reg to file register given
        elif self.mnumonic == Inst.MOVWF.name:
            w = self._get_w_reg_value()

            self._set_file_reg_value(self.operand_1, w)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"MOVWF; W_REG value({w}) --> FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}]")


        # No operation - do nothing but advance program counter
        elif self.mnumonic == Inst.NOP.name:
            # advance to next program line
            self.program_counter.advance_one()
            # log
            self._add_to_log(f"NOP; No operation executed")


        ## BIT-ORIENTATED FILE REGISTER OPERATIONS - only act on File Registers
        
        # Bit Clear File reg
        elif self.mnumonic == Inst.BCF.name:

            # clear bit
            self._clear_file_reg_bit(self.operand_1, self.operand_2)

            # advance to next program line
            self.program_counter.advance_one()
            # log
            self._add_to_log(f"BCF; FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}] bit {self.operand_2} cleared to 0.")

        # Bit Set File reg
        elif self.mnumonic == Inst.BSF.name:
            
            # set bit
            self._set_file_reg_bit(self.operand_1, self.operand_2)

            # advance to next program line
            self.program_counter.advance_one()
            # log
            self._add_to_log(f"BSF; FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}] bit {self.operand_2} set to 1.")

        # Bit Test File reg Skip if Clear
        elif self.mnumonic == Inst.BTFSC.name:
            # get bit value
            file_reg_bit_value = self._get_file_reg_bit_value(self.operand_1, self.operand_2)
            # log outcome
            self._add_to_log(f"BTFSC; FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}] bit {self.operand_2} = {file_reg_bit_value}.")

            # test bit
            if file_reg_bit_value == 0:
                # SKIPPED next line; next cycle to be an NOP - 2 instruction cycles
                self.parent.set_next_cycle_NOP()
                # skip a program line
                self.program_counter.advance_two()
                self._add_to_log(f"NEXT INSTRUCTION SKIPPED")

            elif file_reg_bit_value == 1:
                # advance to next program line
                self.program_counter.advance_one()
                self._add_to_log(f"NEXT INSTRUCTION EXECUTED")

                # Bit Test File reg Skip if Clear

        # Bit Test File reg Skip if Set 
        elif self.mnumonic == Inst.BTFSS.name:
            # get bit value
            file_reg_bit_value = self._get_file_reg_bit_value(self.operand_1, self.operand_2)
            # log outcome
            self._add_to_log(f"BTFSS; FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}] bit {self.operand_2} = {file_reg_bit_value}.")

            # test bit
            if file_reg_bit_value == 1:
                # SKIPPED next line; next cycle to be an NOP - 2 instruction cycles
                self.parent.set_next_cycle_NOP()
                # skip a program line
                self.program_counter.advance_two()
                self._add_to_log(f"NEXT INSTRUCTION SKIPPED")

            elif file_reg_bit_value == 0:
                # advance to next program line
                self.program_counter.advance_one()
                self._add_to_log(f"NEXT INSTRUCTION EXECUTED")


        ## LITERAL AND CONTROL OPERATIONS

        # ADDLW Add lieral value with W Reg
        elif self.mnumonic == Inst.ADDLW.name:
            w = self._get_w_reg_value()
            total = w + self.operand_1

            # handle C bit
            self._handle_C_bit(total)
        
            # handle byte wrap-around
            result = total % 256 # 8-bit number

            # handle Z bit
            self._handle_Z_bit(result)

            #set result
            self._set_w_reg_value(result)

            # advance to next program line
            self.program_counter.advance_one()
            # log
            self._add_to_log(f"ADDLW; literal value ({self.operand_1}) + W_REG value ({w}) --> W_REG (result: {self._get_w_reg_value()})")
        
        # AND W Reg with literal value, store in w reg
        elif self.mnumonic == Inst.ANDLW.name:
            literal = self.operand_1
            w = self._get_w_reg_value()

            # bitwise and the two values
            result = literal & w

            # set Z bit according to result
            self._handle_Z_bit(result)

            # set new w reg value
            self._set_w_reg_value(result)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"ANDWF; W_REG value ({w}) bitwise & with literal value {literal} = {result}\n w: {w:08b}\n l: {literal:08b}&\n  = {result:08b}")

        # CALL a subroutine - push return address (PC + 1) onto stack then GOTO given address
        elif self.mnumonic == Inst.CALL.name:
            # advance to next program line
            self.program_counter.advance_one()
            
            # then push current PC address to stack
            self._push_stack(self.program_counter.get_value())
            
            # set program counter to new address - like GOTO
            self.program_counter.set_value(self.operand_1)

            # set next cycle to be an NOP as GOTO uses 2 instruction cycles
            self.parent.set_next_cycle_NOP()

            # log
            self._add_to_log(f"CALL; subroutine at address 0x{self.operand_1:02X} [{self.operand_1}]; takes 2 instruction cycles")

        # GOTO a given address
        elif self.mnumonic == Inst.GOTO.name:
            # set program counter to new address
            self.program_counter.set_value(self.operand_1)

            # set next cycle to be an NOP as GOTO uses 2 instruction cycles
            self.parent.set_next_cycle_NOP()

            # log
            self._add_to_log(f"GOTO; address 0x{self.operand_1:02X} [{self.operand_1}]; takes 2 instruction cycles")

        # MOVE a literal value to w reg
        elif self.mnumonic == Inst.MOVLW.name:
            # set new w reg value
            self._set_w_reg_value(self.operand_1)

            # advance to next program line
            self.program_counter.advance_one()

            # log
            self._add_to_log(f"MOVLW; literal value ({self.operand_1}) --> W_REG addr.")

        # RETURN from a subroutine using stack
        elif self.mnumonic == Inst.RETURN.name:
            # get return address - most recent stack item
            return_address = self._pop_stack()

            # set PC to return address
            self.program_counter.set_value(return_address)

            # set next cycle to be an NOP as GOTO uses 2 instruction cycles
            self.parent.set_next_cycle_NOP()

            # log
            self._add_to_log(f"RETURN; Return to address 0x{return_address:02X} [{self.operand_1}]; takes 2 instruction cycles")
        
        # catch-all to log if instruction not understood
        else:
            # advance to next program line
            self.program_counter.advance_one()
            # log uncaught instruction
            self._add_to_log(f"Instruction error; {instruction}")



    ## InstructionDecoder internal methods

    # stack methods
    def _push_stack(self, return_address):
        self.parent.push_stack(return_address)

    def _pop_stack(self):
        return self.parent.pop_stack()

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
            self._add_to_log(f"Second operand needs to be either 0 or 1; value given was '{operand_2}', defaulted to 1.")
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
    def _get_file_reg_bit_value(self, file_reg, bit):
        return self.parent.get_byte_by_address(file_reg).get_bit(bit)

    def _set_file_reg_bit(self, file_reg, bit):
        self.parent.set_file_reg_bit(file_reg, bit)

    def _clear_file_reg_bit(self, file_reg, bit):
        self.parent.clear_file_reg_bit(file_reg, bit)

    # add message to log through parents
    def _add_to_log(self, message):
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
