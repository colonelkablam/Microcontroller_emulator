import tkinter as tk
from tkinter import ttk
from my_constants import*

class InstructionDecoder():
    def __init__(self, parent):

        # properties

        # split the instructions
        self.mnumonic = ""
        self.operand_1 = "0x00"
        self.operand_2 = 1

        self.parent = parent
        self.new_program_address = 0
        self.altered_register_address = 0
    

    # InstructionDecoder methods

    def get_new_program_address(self, instruction):
        # split the instruction
        self._split_instruction(instruction)

        # BYTE-ORIENTATED FILE REGISTER OPERATIONS - only act on File Registers
        if self.mnumonic == "ADDWF":
            w = self.get_w_reg_value()
            f = self.get_file_reg_value(self.operand_1)
            loc_string = ""

            # handle byte wrap-around
            result = (w + f) % 256

            # set Z bit in STATUS reg if result 0, clear if not
            if result == 0:
                self.set_Z_bit_status()
            else:
                self.clear_Z_bit_status()

            # determin where to store result (W or f)
            if self.operand_2 == 0:
                self.set_w_reg_value(result)
                loc_string = f"W_REG (result: {result})"
                # record altered register address
                self.altered_register_address = -1 # W_REG not in data_mem
            elif self.operand_2 == 1:
                self.set_file_reg_value(self.operand_1, result)
                loc_string = f"FILE REG addr. 0x{self.operand_1:02X} (result: {result})"
                # record altered register address
                self.altered_register_address = self.operand_1
            else:
                self.add_to_log(f"Second operand needs to be either 1 or 0; value given = {self.operand_2}")

            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1

            # log
            self.add_to_log(f"ADDWF; W_REG value ({w}) + FILE REG 0x{self.operand_1:02X} value ({f}) --> {loc_string}")


        # clear value of file register given
        elif self.mnumonic == "CLRF":
            self.set_file_reg_value(self.operand_1, 0)
            # record altered register address
            self.altered_register_address = self.operand_1
            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1
            # log
            self.add_to_log(f"CLRF; FILE REG addr. 0x{self.operand_1:02X} cleared")
        
        # clear value of W reg
        elif self.mnumonic == "CLRW":
            self.set_w_reg_value(0)
            # record altered register address (-1 if no reg altered)
            self.altered_register_address = -1
            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1
            # log
            self.add_to_log(f"CLRW; W_REG cleared")


        # move W reg to file register given
        elif self.mnumonic == "MOVWF":
            w = self.get_w_reg_value()
            self.set_file_reg_value(self.operand_1, w)
            # record altered register address
            self.altered_register_address = self.operand_1
            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1
            # log
            self.add_to_log(f"MOVWF; W_REG value({w}) --> FILE REG addr. 0x{self.operand_1:02X} [{self.operand_1}]")


        # No operation - do nothing but advance program counter
        elif self.mnumonic == "NOP":
            # record altered register address (-1 if no reg altered)
            self.altered_register_address = -1
            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1
            # log
            self.add_to_log(f"NOP; No operation executed")


        # BIT-ORIENTATED FILE REGISTER OPERATIONS - only act on File Registers

        # LITERAL AND CONTROL OPERATIONS
        elif self.mnumonic == "ADDLW":
            w = self.get_w_reg_value()
            result = w + self.operand_1
            self.set_w_reg_value(result)
            # record altered register address (-1 if no reg altered)
            self.altered_register_address = -1
            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1
            # log
            self.add_to_log(f"ADDLW; literal value ({self.operand_1}) + W_REG value ({w}) --> W_REG (result: {self.get_w_reg_value()})")

        elif self.mnumonic == "GOTO":
            # record altered register address (-1 if no reg altered)
            self.altered_register_address = -1
            self.new_program_address = self.operand_1
            # set next cycle to be an NOP as GOTO uses 2 instruction cycles
            self.parent.set_next_cycle_NOP()
            # log
            self.add_to_log(f"GOTO; address 0x{self.operand_1:02X} [{self.operand_1}]; takes 2 instruction cycles")

        elif self.mnumonic == "CALL":
            # record altered register address (-1 if no reg altered)
            self.altered_register_address = -1
            self.new_program_address = self.operand_1
            # then push current PCL to stack

        elif self.mnumonic == "MOVLW":
            self.set_w_reg_value(self.operand_1)
            # advance to next program line
            self.new_program_address = self.parent.get_current_PC_value() + 1
            # log
            self.add_to_log(f"MOVLW; literal value ({self.operand_1}) --> W_REG addr.")

        else:
            # record altered register address (-1 if no reg altered)
            self.altered_register_address = -1
            self.new_program_address = self.parent.get_current_PC_value() + 1
            self.add_to_log(f"Unrecognised instruction; {instruction}")
            # advance to next program line

        # return the new program address (handle wrap-around with %)
        return ((self.new_program_address  % PROGRAM_MEMORY_SIZE), self.altered_register_address)

    # get numerical address location by name
    def get_address_by_name(self, name):
        return self.parent.SFR_dict[name]

    # access to named registers
    def get_w_reg_value(self):
        return self.parent.get_w_register().get_dec_value()
        
    def set_w_reg_value(self, value=0):
        self.parent.set_w_register(value)

    # access to file registers with address
    def get_file_reg_value(self, file_reg):
        return self.parent.data_memory[file_reg].get_dec_value()

    def set_file_reg_value(self, file_reg, value=0):
        self.parent.data_memory[file_reg].set_value(value)

    # set/clear status bit
    def set_Z_bit_status(self):
        self.parent.set_Z_bit_status()
    def clear_Z_bit_status(self):
        self.parent.clear_Z_bit_status()

    # set/clear bit from file register
    def set_file_reg_value_bit(self, file_reg, bit):
        self.parent.set_file_reg_bit(file_reg, bit)
    def clear_file_reg_bit(self, file_reg, bit):
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

        print(instruction)
        print(self.mnumonic, self.operand_1, self.operand_2)

