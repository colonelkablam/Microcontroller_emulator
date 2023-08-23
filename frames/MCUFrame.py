import tkinter as tk
from tkinter import ttk
import threading
import multiprocessing
from my_constants import*
from dataStructures import NBitNumber
from frames import ControlPanelFrame, CodeDisplayFrame, PinoutFrame
from frames.MCUInternals import ProgramCounter, ProgramMemoryFrame,\
                                DataMemoryFrame, MCUStatusFrame,\
                                StackDisplayFrame, InstructionDecoder, \
                                PortPeripheral


class MCUFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # configure layout of internal Frames
        #self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        # properties
        self.parent = parent

        # running sim
        self.simulation_running = False
        self.simulation_speed = 1000
        # clock information
        self.clock_frequency = 20.0 # Mhz
        self.Q_cycles_per_instruction = 4
        self.num_instruction_cycles = 0
        self.num_instructions_executed = 0
        self.time_duration = 0

        # Working register - not in data_memory
        self.w_reg = NBitNumber(    8,
                                    tk.IntVar(value=0),
                                    tk.StringVar(value="00h"),
                                    tk.StringVar(value=f"00000000"),
                                    "WREG"      )
        

        ## tkinter widgets

        # panel label
        #frame_label = ttk.Label(self, text="MCU Panel", style='MainWindowOuter.TLabel')
        #frame_label.grid(column=0, row=0, padx=(50,0), pady=(0,10), sticky="W")

        # set-up MCU
        # MCU 'views'
        # program memory - contains the program memory logic/control
        self.prog_memory_frame = ProgramMemoryFrame(self, "Program Memory")
        self.prog_memory_frame.grid(column=0, row=1, padx=(10,10))

        # data memory - contains the data memory logic/control
        self.data_memory_frame = DataMemoryFrame(self, "Data Memory / registers")
        self.data_memory_frame.grid(column=1, row=1)

        # 13-bit number needed for Program Counter
        self.program_counter = ProgramCounter(self.data_memory_frame)

        # logic
        self.instruction_decoder = InstructionDecoder(self, self.program_counter)
        self.is_next_cycle_NOP = False

        # MCU Status Information display - frame to display key information/status from the MCU/memory
        self.MCU_status_frame = MCUStatusFrame(self, "MCU Status Display")
        self.MCU_status_frame.grid(column=2, row=1, padx=(20,10))

        # stack to be shown in MCU status frame above - contains the stack logic/control
        self.stack_frame = StackDisplayFrame(self.MCU_status_frame, style='MainWindowInner.TLabel')
        self.stack_frame.grid(column=0, row=2, rowspan=6, sticky="NSEW")


        ## peripherals

        # port A
        self.port_a = PortPeripheral(   self.data_memory_frame.get_byte_by_name("PORTA"),
                                        self.data_memory_frame.get_byte_by_name("TRISA"),
                                        5       )
        # port B
        self.port_b = PortPeripheral(   self.data_memory_frame.get_byte_by_name("PORTB"),
                                        self.data_memory_frame.get_byte_by_name("TRISB"),
                                        8       )

        # look-up chip pin object or input value by port pin
        # basically represtents the physical chip and any digital values on the pin
        self.peripheral_pin_dict = {17 : self.port_a.get_port_pin_by_name("RA0"),
                                    18 : self.port_a.get_port_pin_by_name("RA1"),
                                    1 :  self.port_a.get_port_pin_by_name("RA2"),
                                    2 :  self.port_a.get_port_pin_by_name("RA3"),
                                    3 :  self.port_a.get_port_pin_by_name("RA4"),
                                    6 :  self.port_b.get_port_pin_by_name("RB0"),
                                    7 :  self.port_b.get_port_pin_by_name("RB1"),
                                    8 :  self.port_b.get_port_pin_by_name("RB2"),
                                    9 :  self.port_b.get_port_pin_by_name("RB3"),
                                    10 : self.port_b.get_port_pin_by_name("RB4"),
                                    11 : self.port_b.get_port_pin_by_name("RB5"),
                                    12 : self.port_b.get_port_pin_by_name("RB6"),
                                    13 : self.port_b.get_port_pin_by_name("RB7"),
                                    4  : None,
                                    5  : None,
                                    14 : None,
                                    15 : None,
                                    16 : None     }

        # create a pinout_frame - contains the state of the chip pins - contained in the pinout window
        self.pinout_frame = PinoutFrame(self.parent.pinout_window.window, self.peripheral_pin_dict)
        self.pinout_frame.grid(column=0, row=0, sticky="NSEW")


    # MCUFrame methods
    # fill program memory with empty Instruction objects ("ADDLW 0xFF 0")
    def initialise_program_memory(self):
        self.prog_memory_frame.initialise_program_memory()

    def reset_MCU(self, keepprogram=True):        
        self.prog_memory_frame.reset_program_memory_frame(keepprogram)
        self.data_memory_frame.reset_data_memory_frame()
        self.stack_frame.clear_stack()
        self.w_reg.set_value(0)
        self.set_PC(0)

        self.port_a.reset()
        self.port_b.reset()
        self.pinout_frame.reset()

        self.reset_clock_info()
        self.MCU_status_frame.reset_display()

    # load program into program memory (code editor uses this to populate memory)
    def upload_program(self, program):
        prog_len = len(program)
        upload_successful = self.prog_memory_frame.upload_program(program)
        if upload_successful:
            self.parent.system_message(f"{prog_len} x 14-bit word program successfully loaded into Program Memory")
        else:
            self.parent.system_message(f"FAILED TO LOAD PROGRAM: {prog_len} word program too large for MCU's {PROGRAM_MEMORY_SIZE} word program memory")
    
    # fill data memory with Byte objects and name accordingly (using the SFR dict)
    def initialise_data_memory(self):
        self.data_memory_frame.initialise_data_memory()
        self.parent.system_message(f"DATA MEMORY INITIALISED")


    # retrieve bytes from data memory by name (if SFR) or address
    def get_byte_by_name(self, byte_name):
        byte = self.data_memory_frame.get_byte_by_name(byte_name)
        if byte == None:
            self.parent.system_message(f"FAILED TO RETRIEVE BYTE: {byte_name}; SFR name not defined")
        return byte

    def get_byte_by_address(self, byte_addr):
        byte = self.data_memory_frame.get_byte_by_address(byte_addr)
        if byte == None:
            self.parent.system_message(f"FAILED TO RETRIEVE BYTE: @ address {byte_addr}; not within data memory")
        return byte

    # set bytes in data memory by name (if SFR) or address
    def set_byte_by_name(self, byte_name, value):
        set_successful = self.data_memory_frame.set_byte_by_name(byte_name, value)
        if set_successful == False:
            self.parent.system_message(f"FAILED TO SET BYTE: value of {value} @ '{byte_name}'; SFR name not defined")

    def set_byte_by_address(self, byte_addr, value):
        set_successful = self.data_memory_frame.set_byte_by_address(byte_addr, value)
        if set_successful == False:
            self.parent.system_message(f"FAILED TO SET BYTE: value of {value} @ address {byte_addr}")

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
        return self.num_instruction_cycles

    # handling the Instruction Cycle
    # main advance method - calls instruction decoder (logic of MCU) and updates PCL
    def advance_cycle(self):
        # get new PC address and altered reg address from the instruction decoder object (and handle wrapping around of max prog mem size)
        self.pinout_frame.update()
        self.port_a.update_registers()
        self.port_b.update_registers()
        self.instruction_decoder.get_new_program_address(self.get_current_instruction())
        self.prog_memory_frame.highlight_current_instruction(self.program_counter.get_value())
        self.data_memory_frame.highlight_accessed_registers_cycle()
        self.num_instruction_cycles += 1
        self.num_instructions_executed += 1

        # test to see if next instruction a NOP
        if self.is_next_cycle_NOP == True:
            self.advance_NOP()
            self.is_next_cycle_NOP = False

        self.MCU_status_frame.update_display() # update focused byte displays

        self.parent.log_commit()




    # advance if NOP called by InstructionDecoder
    def advance_NOP(self):
        self.parent.add_to_log(f"NOP after a 2 cycle instruction")
        self.num_instruction_cycles += 1
        self.parent.log_commit()


    # methods for running simulation
    def start_simulation(self, sim_speed):
        # set sim to running
        self.simulation_running = True
        # local fuction to use with threading
        def run_loop(sim_speed):
            if self.simulation_running == True:
                self.advance_cycle()    # advance cycle
                self.after(sim_speed, run_loop, sim_speed)  # time to wait before running loop again
            else:
                return
        # use a thread to run the advance cycle loop
        threading.Thread(target=run_loop, args=(sim_speed,)).start()
        
    def stop_simulation(self):
        self.simulation_running = False

    def set_sim_speed(self, speed):
        self.simulation_speed = speed

    def set_next_cycle_NOP(self):
        self.is_next_cycle_NOP = True

    # program counter is 13-bit value (can address up to 8192 14-bit instructions words)
    # use the current program counter value to get the current instruction
    def get_current_instruction(self):
        return self.prog_memory_frame.get_instruction(self.get_current_PC_value())

    def get_previous_instruction(self):
        return self.prog_memory_frame.get_instruction(self.get_previous_PC_value())

    # get the value of the program counter (PC)
    def get_current_PC_value(self):
        return self.program_counter.get_value()
    def get_previous_PC_value(self):
        return self.program_counter.get_previous()

    # returns the program counter object
    def get_PC_13bit_representation(self):
        return self.program_counter.get()

    # set the value of the program counter (PC)
    def set_PC(self, new_address):
        # store the new address in PC object - for PC display in MCU status
        # this will store to the PCL (lower byte) and PCLATH (upper 5 bits)
        self.program_counter.set_value(new_address)
        # log it
        prev_val = self.program_counter.get_previous()
        self.parent.add_to_log(f"Program Counter (PC); changed from 0x{prev_val:04X} [{prev_val}] --> 0x{new_address:04X} [{new_address}]")

    # get status info for MCU status frame display
    def get_status_info(self):
        previous_instruction = self.get_previous_instruction()
        next_instruction = self.get_current_instruction()
        num_cycles = self.num_instruction_cycles
        num_instructions = self.num_instructions_executed
        # return tuple of status information
        return (previous_instruction, next_instruction, num_cycles, num_instructions)

    # reset status info
    def reset_clock_info(self):
        self.num_instruction_cycles = 0
        self.num_instructions_executed = 0

    # bit-wise methods
    # set/clear file reg bit
    def set_file_reg_bit(self, mem_address, bit):
        self.data_memory_frame(mem_address).set_bit(bit)

    def clear_file_reg_bit(self, mem_address, bit):
        self.data_memory_frame(mem_address).clear_bit(bit)

    # set/clear status bit 2 (Z); result of ALU gives a zero 
    def set_Z_bit_status(self):
        self.data_memory_frame.set_Z_bit_status()
        
    def clear_Z_bit_status(self):
        self.data_memory_frame.clear_Z_bit_status()




    

    
    