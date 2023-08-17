import tkinter as tk
from tkinter import ttk
from my_constants import*
from frames import ControlPanelFrame, CodeDisplayFrame
from frames.MCUInternals import ProgramMemoryFrame, DataMemoryFrame, MCUStatusFrame, StackDisplayFrame, InstructionDecoder
#from frames.MCUInternals.MCUStatusFrames import StackDisplayFrame
from dataStructures import Byte, Instruction



class MCUFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # properties
        self.parent = parent
        # memory 
        self.data_memory = []       # list of Byte objects
        # logic
        self.instruction_decoder = InstructionDecoder(self)
        self.is_next_cycle_NOP = False
        # clock
        self.clock_frequency = 4.0 # Mhz
        self.cycles_per_instruction = 4
        self.instruction_cycle = 0
        self.time_duration = 0
        # Working register - not in data_memory
        self.w_reg = Byte(tk.IntVar(value=0), tk.StringVar(value="00"), tk.StringVar(value=f"00000000"), "WREG")
        # PC - store previous program counter value
        self.prev_PC_value = 0
        self.bit_to_set = 0
        # Special Function Registers (SFR) look-up address by name dictionary
        self.SFR_dict = {   "INDF" :    int("0x00", 16),
                            "TMRO" :    int("0x01", 16),
                            "PCL" :     int("0x02", 16),
                            "STATUS" :  int("0x03", 16),
                            "FSR" :     int("0x04", 16),  
                            "PORTA" :   int("0x05", 16),
                            "PORTB" :   int("0x06", 16),
                            "PCLATH" :  int("0x0A", 16),
                            "TRISA" :   int("0x85", 16),
                            "TRISB" :   int("0x86", 16)   }

        # set-up MCU
        self.initialise_data_memory()

        # tkinter widgets

        # configure layout of internal Frames
        #self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        # panel label
        self.frame_label = ttk.Label(self, text="MCU Panel", style='MainWindowOuter.TLabel')
        self.frame_label.grid(column=0, row=0, padx=(50,0), pady=(0,10), sticky="W")

        # MCU 'views'
        # program memory - contains the program memory logic/control
        self.prog_memory_frame = ProgramMemoryFrame(self, "Program Memory")
        self.prog_memory_frame.grid(column=0, row=1, padx=(10,10))

        # data memory - contains the data memory logic/control
        self.data_memory_frame = DataMemoryFrame(self, self.data_memory, "Data Memory / registers")
        self.data_memory_frame.grid(column=1, row=1)

        # MCU Status Information display - frame to display key information/status from the MCU/memory
        self.MCU_status_frame = MCUStatusFrame(self, "MCU Status Display")
        self.MCU_status_frame.grid(column=2, row=1, padx=(20,10))

        # stack to be shown in MCU status frame above - contains the stack logic/control
        self.stack_frame = StackDisplayFrame(   self.MCU_status_frame,
                                                style='MainWindowInner.TLabel'                  )
        self.stack_frame.grid(column=0, row=2, rowspan=4, sticky="NSEW")   


    # MCUFrame methods
    # fill program memory with empty Instruction objects
    def initialise_program_memory(self):
        self.prog_memory_frame.initialise_program_memory()

    # load program into program memory (code editor uses this to populate memory)
    def upload_program(self, program):
        upload_successful = self.prog_memory_frame.upload_program(program)
        if upload_successful:
            self.parent.system_message(f"{prog_len} x 14-bit word program successfully loaded into Program Memory")
        else:
            self.parent.system_message(f"FAILED TO LOAD PROGRAM: {prog_len} word program too large for MCU's {PROGRAM_MEMORY_SIZE} word program memory")
    
    # fill data memory with Byte objects and name accordingly (using the SFR dict)
    def initialise_data_memory(self):
        for mem_address in range(0, DATA_MEMORY_SIZE):
            # get SFR name (if one assigned) - look through SFR dictionary
            for SFR_name, SFR_addr in self.SFR_dict.items():
                if SFR_addr == mem_address:
                    name = SFR_name
                    break
                else:
                    name = " -"
            # add Byte
            self.data_memory.append(Byte(tk.IntVar(value=0), tk.StringVar(value="00h"), tk.StringVar(value=f"00000000"), name))

    # retrieve bytes from data memory by name (if SFR) or address
    def get_byte_by_name(self, byte_name):
        return self.data_memory[self.SFR_dict[byte_name]]
    def get_byte_by_address(self, byte_addr):
        return self.data_memory[byte_addr]

    # handle the working register (exists outside the data memory list)
    def get_w_register(self):
        return self.w_reg
    def set_w_register(self, new_value):
        self.w_reg.set_value(new_value)

    # STACK methods
    # access to the stack data structure
    def get_stack(self):
        return self.stack_frame.get_stack()

    # return top element
    def pop_stack(self):
        first_in_queue = self.stack_frame.pop_stack()
        if first_in_queue == None:
            self.parent.add_to_log(f"Stack empty; unable tp pop MCU stack")
            return None
        else:
            self.parent.add_to_log(f"Stack popped; returning 0x{first_in_queue:04X}")
            return first_in_queue

    # add to stack - 8 deep
    def push_stack(self, new_address=0):
        self.stack_frame.push_stack(new_address)
        self.parent.add_to_log(f"Stack pushed; 0x{new_address:04X} added to top")


    # initialise log text
    def clear_log_text(self):
        self.parent.clear_log_text()

    # instruction cycle
    def get_instruction_cycle(self):
        return self.instruction_cycle

    # handling the Instruction Cycle
    # main advance method - calls instruction decoder (logic of MCU) and updates PCL
    def advance_cycle(self):
        # get new PC address and altered reg address from the instruction decoder object (and handle wrapping around of max prog mem size)
        new_PC_address_and_register = self.instruction_decoder.get_new_program_address(self.get_current_instruction())
        new_PC_address = new_PC_address_and_register[0] 
        altered_reg_address = new_PC_address_and_register[1]
        
        self.set_PC(new_PC_address)
        self.prog_memory_frame.highlight_current_instruction(new_PC_address)
        self.data_memory_frame.highlight_current_register(altered_reg_address)

        self.MCU_status_frame.update_display() # update focused byte displays

        self.instruction_cycle += 1
        self.parent.log_commit()
        
        # test to see if next instruction a NOP
        if self.is_next_cycle_NOP == True:
            self.advance_NOP()
            self.is_next_cycle_NOP = False

    # advance if NOP called by InstructionDecoder
    def advance_NOP(self):
        self.parent.add_to_log(f"NOP after a 2 cycle instruction")
        self.instruction_cycle += 1
        self.parent.log_commit()

    def set_next_cycle_NOP(self):
        self.is_next_cycle_NOP = True

    # use the current program counter value to get the current instruction
    def get_current_instruction(self):
        return self.prog_memory_frame.get_instruction(self.get_current_PC_value())

    # program counter is 13-bit value (can address up to 8192 14-bit instructions words)
    # get the value of the program counter (PC) from the PCL (lower byte) and PCLATH (upper 5 bits)
    def get_current_PC_value(self):
        lower_byte = self.data_memory[self.SFR_dict["PCL"]].get_dec_value()
        upper_byte = self.data_memory[self.SFR_dict["PCLATH"]].get_dec_value()
        # combine the two bytes (NOT ADD - used to represent a 13-bit prog address!)
        return (upper_byte << 8) | lower_byte

    # set the value of the program counter (PC)
    def set_PC(self, new_address):
        print("new addr.", new_address)
        # store current PC value
        self.prev_PC_value = self.get_current_PC_value()
        # split the address into lower and upper bytes (as PC stored in PCL and PCLATH)

        lower_byte = self._get_n_byte_int(new_address, 0, 8)
        upper_byte = self._get_n_byte_int(new_address, 1, 8)
        # take only the lower 5-bits of the 2nd byte - PCLATH not addressable; last 3 bits '0'
        upper_5_bits = self._get_n_byte_int(upper_byte, 0, 5)

        # store the values in the registers
        self.data_memory[self.SFR_dict["PCL"]].set_value(lower_byte)
        self.data_memory[self.SFR_dict["PCLATH"]].set_value(upper_5_bits)
        # log it
        self.parent.add_to_log(f"Program Counter (PC); changed from 0x{self.prev_PC_value:04X} [{self.prev_PC_value}] --> 0x{new_address:04X} [{new_address}]")
    
    # get the nth byte value
    def _get_n_byte_int(self, target, n, bit_length=8):
        mask = 255 << (n * bit_length)
        and_result = mask & target
        byte = and_result >> (n * bit_length)
        return byte

    # bit-wise methods
    # set/clear file reg bit
    def set_file_reg_bit(self, mem_address, bit):
        self.data_memory[mem_address].set_bit(bit)

    def clear_file_reg_bit(self, mem_address, bit):
        self.data_memory[mem_address].clear_bit(bit)

    # set/clear status bit
    def set_Z_bit_status(self):
        self.data_memory[self.SFR_dict["STATUS"]].set_bit(2)
        
    def clear_Z_bit_status(self):
        self.data_memory[self.SFR_dict["STATUS"]].clear_bit(2)




    

    
    