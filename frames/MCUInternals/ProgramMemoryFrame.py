import tkinter as tk
from tkinter import ttk
from my_constants import *
from dataStructures import Instruction
from frames.ScrollableCanvasFrame import ScrollableCanvasFrame


class ProgramMemoryFrame(ttk.Frame):
    def __init__(self, parent, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1) # row 3 has canvas which we want to fill available space
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.memory = []

        # list to store intruction labels
        self.rows = [] # allows access for formatting tkinter objects later
        self.visited_rows = set()   # track visited addresses to reset labels when needed
        self.previous_address = 0
        self.program_length = 0


        # tkinter widgets

        # panel labels
        control_panel_label = ttk.Label(self, text=f"{title}\n{PROGRAM_MEMORY_SIZE} x 14-bit words", style='MainWindowInner.TLabel')
        control_panel_label.grid(column=0, row=0, columnspan=2, padx=(5,0), pady=(0,5), sticky="NW")

        mem_label = ttk.Label(      self,
                                    text="[  address  ] [  instruction  ]",
                                    style='MainWindowInner2.TLabel'             )
        mem_label.grid(column=0, row=1, columnspan=2, pady=(0,0), sticky="NW")
        mem_label_2 = ttk.Label(    self,
                                    text="  dec   hex    mnum.  operands",
                                    style='MainWindowInner2.TLabel'             )
        mem_label_2.grid(column=0, row=2, columnspan=2, pady=(0,0), sticky="NW")

        # create a scrollable canvas object
        scroll_canvas_frame = ScrollableCanvasFrame(self, PROG_MEMORY_WINDOW_WIDTH, PROG_MEMORY_WINDOW_HEIGHT)
        scroll_canvas_frame.grid(column=0, row=3, sticky="NS")
        scroll_canvas_frame.rowconfigure(0, weight=1)

        # get it's inner frame to mount the memory display on
        inner_frame = scroll_canvas_frame.get_inner_frame()
           
        # initialise program memory - clear and create list of default instructions
        self.initialise_program_memory()

        # add memory display - using the variables stored in the memory list
        for mem_address in range(0, PROGRAM_MEMORY_SIZE):
            # display the program memory locations
            dec_addr = ttk.Label(inner_frame, text=f"[{mem_address :03}]", width=5, style="MCUmemory.TLabel")
            dec_addr.grid(column=0, row=mem_address, pady=(0,5), padx=5, sticky="W")

            hex_addr = ttk.Label(inner_frame, text=f"{mem_address :04X}h", width=5, style="MCUmemory.TLabel")
            hex_addr.grid(column=1, row=mem_address, pady=(0,5), padx=(0,10), sticky="W")

            # create the labels to display the instructions ('dissassembly')
            instruction_mnemonic = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_mnumonic(), width=6, style="MCUmemory.TLabel")
            instruction_mnemonic.grid(column=2, row=mem_address, pady=(0,5), padx=(0,5), sticky="E")

            instruction_operand_1 = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_operand_1(), width=6, style="MCUmemory.TLabel")
            instruction_operand_1.grid(column=3, row=mem_address, pady=(0,5), padx=(0,5), sticky="E")

            instruction_operand_2 = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_operand_2(), width=1, style="MCUmemory.TLabel")
            instruction_operand_2.grid(column=4, row=mem_address, pady=(0,5), padx=(0,5), sticky="E")

            self.rows.append([dec_addr, hex_addr, instruction_mnemonic, instruction_operand_1, instruction_operand_2])

        # hightlight the program starting position (0x00h)
        self.highlight_current_instruction(0)


    # MemoryFrame methods

    # fill program memory with empty Instruction objects
    def initialise_program_memory(self):
        for mem_address in range(0, PROGRAM_MEMORY_SIZE):
            # add Instruction
            self.memory.append(Instruction())

    # clear all values in program data
    def reset_program_memory_frame(self):
        # reset memory
        for i, instruction in enumerate(self.memory):
            
            # saves looping through entire program memory
            if i >= self.program_length:
                break
            instruction.set_instruction() # sets all instructions to DEFAULT_INSTRUCTION

        self.previous_address = 0   # back to starting state

        # reset highlighting - only visited addresses to save in iterating through whole memory
        for address in self.visited_rows:
            for element in self.rows[address]:
                element.configure(background="white")

        self.highlight_current_instruction(0)
        self.visited_rows.clear()

    # load program into program memory (code editor uses this to populate memory)
    def upload_program(self, program):
        self.program_length = len(program)
        if self.program_length <= PROGRAM_MEMORY_SIZE | self.program_length > 0:
            for mem_address in range(0, self.program_length):
                self.memory[mem_address].set_mnumonic(program[mem_address][0])
                self.memory[mem_address].set_operand_1(program[mem_address][1])
                self.memory[mem_address].set_operand_2(program[mem_address][2])

            return True
        else:
            self.program_length = 0
            return False

    # retrieve an instruction - none if out of range
    def get_instruction(self, address):
        if address < PROGRAM_MEMORY_SIZE:
            return self.memory[address].get_instruction() # gets tuple of intruction
        else:
            return None

    # used for highlighting current PC address
    def highlight_current_instruction(self, new_prog_address):
        # add visited row to set
        self.visited_rows.add(new_prog_address)
        
        # reset previous instruction row highlight
        for label in self.rows[self.previous_address]:
            label.config(background=VISITED_DATA_ADDRESS)
       
       # update previous address with current
        self.previous_address = new_prog_address
        
        # highlight current row instruction
        for label in self.rows[new_prog_address]:
            label.config(background=PROGRAM_MEMORY_HIGHLIGHT)






