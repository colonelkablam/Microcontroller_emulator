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
        self.rows = []# allows access for formatting later
        self.previous_address = 0


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
           
        # initialise program memory
        self.initialise_program_memory()

        # add memory display
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
        self.highlight_current_instruction(self.previous_address)


    # MemoryFrame methods

    # fill program memory with empty Instruction objects
    def initialise_program_memory(self):
        for mem_address in range(0, PROGRAM_MEMORY_SIZE):
            # add Instruction
            self.memory.append(Instruction(tk.StringVar(value="ADDLW"), tk.StringVar(value="0xFF"), tk.StringVar(value="-")))

    # load program into program memory (code editor uses this to populate memory)
    def upload_program(self, program):
        prog_len = len(program)
        if prog_len <= PROGRAM_MEMORY_SIZE | prog_len > 0:
            for mem_address in range(0, prog_len):
                self.memory[mem_address].set_mnumonic(program[mem_address][0])
                self.memory[mem_address].set_operand_1(program[mem_address][1])
                self.memory[mem_address].set_operand_2(program[mem_address][2])

            return True
        else:
            return False

    # retrieve an instruction - none if out of range
    def get_instruction(self, address):
        if address < PROGRAM_MEMORY_SIZE:
            return self.memory[address].get_instruction() # gets tuple of intruction
        else:
            return None

    # used for highlighting current PC address
    def highlight_current_instruction(self, new_prog_address):
        for label in self.rows[self.previous_address]:
            label.config(background=VISITED_DATA_ADDRESS)

        self.previous_address = new_prog_address

        for label in self.rows[new_prog_address]:
            label.config(background=PROGRAM_MEMORY_HIGHLIGHT)






