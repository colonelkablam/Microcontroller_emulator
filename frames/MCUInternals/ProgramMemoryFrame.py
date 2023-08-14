import tkinter as tk
from tkinter import ttk
from my_constants import *


class ProgramMemoryFrame(ttk.Frame):
    def __init__(self, parent, memory, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.memory = memory

        # list to store intruction labels
        self.rows = []# allows access for formatting later
        self.previous_address = 0


        # tkinter widgets

        # panel labels
        self.control_panel_label = ttk.Label(self, text=f"{title}\n{PROGRAM_MEMORY_SIZE} x 14-bit words", style='MainWindowInner.TLabel')
        self.control_panel_label.grid(column=0, row=0, columnspan=2, pady=(0,10), sticky="W")

        self.mem_label = ttk.Label(self, text="  addr.      instruction", style='MainWindowInner2.TLabel')
        self.mem_label.grid(column=0, row=1, columnspan=2, pady=(0,5), sticky="W")

        # canvas
        self.scroll_canvas = tk.Canvas(self, width=MEMORY_WINDOW_WIDTH, height=MEMORY_WINDOW_HEIGHT)
        self.scroll_canvas.grid(column=0, row=2, sticky="NS")
        self.scroll_canvas.columnconfigure(0, weight=1)
        self.scroll_canvas.rowconfigure(0, weight=1)

        # scrollbars
        self.code_scroll = ttk.Scrollbar(self, orient='vertical', command=self.scroll_canvas.yview)
        self.code_scroll.grid(column=1, row=2, sticky="NSW")

        # configure canvas
        self.scroll_canvas.configure(yscrollcommand=self.code_scroll.set)
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.scroll_canvas.bind('<Leave>', self._unbound_to_mousewheel)

        # create ANOTHER inner frame inside canvas
        self.inner_frame = ttk.Frame(self.scroll_canvas, style="MCUmemory.TFrame")
        #self.inner_frame.columnconfigure(0, weight=1)

        # add INNER FRAME to a window in the canvas
        self.scroll_canvas.create_window((0,0), window=self.inner_frame, anchor="nw", width=MEMORY_WINDOW_WIDTH)
           
        # add memory display
        for mem_address in range(0, PROGRAM_MEMORY_SIZE):
            # display the program memory locations
            dec_addr = ttk.Label(self.inner_frame, text=f"{mem_address :03}", width=3, style="MCUmemory.TLabel")
            dec_addr.grid(column=0, row=mem_address, pady=(0,5), padx=5, sticky="W")

            hex_addr = ttk.Label(self.inner_frame, text=f"{mem_address :04X}h", width=5, style="MCUmemory.TLabel")
            hex_addr.grid(column=1, row=mem_address, pady=(0,5), padx=(0,10), sticky="W")

            # create the labels to display the instructions ('dissassembly')
            instruction_mnemonic = ttk.Label(self.inner_frame, textvariable=self.memory[mem_address].get_mnumonic(), width=6, style="MCUmemory.TLabel")
            instruction_mnemonic.grid(column=2, row=mem_address, pady=(0,5), padx=(0,5), sticky="E")

            instruction_operand_1 = ttk.Label(self.inner_frame, textvariable=self.memory[mem_address].get_operand_1(), width=6, style="MCUmemory.TLabel")
            instruction_operand_1.grid(column=3, row=mem_address, pady=(0,5), padx=(0,5), sticky="E")

            instruction_operand_2 = ttk.Label(self.inner_frame, textvariable=self.memory[mem_address].get_operand_2(), width=1, style="MCUmemory.TLabel")
            instruction_operand_2.grid(column=4, row=mem_address, pady=(0,5), padx=(0,5), sticky="E")

            column = [dec_addr, hex_addr, instruction_mnemonic, instruction_operand_1, instruction_operand_2]
            self.rows.append(column)

        # hightlight the program starting position (0x00h)
        self.highlight_current_instruction(self.previous_address)


    # MemoryFrame methods

    def highlight_current_instruction(self, new_prog_address):
        for label in self.rows[self.previous_address]:
            label.config(background="white")

        self.previous_address = new_prog_address

        for label in self.rows[new_prog_address]:
            label.config(background=PROGRAM_MEMORY_HIGHLIGHT)



            



    # canvas scrolling behaviour

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bound_to_mousewheel(self, event):
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.scroll_canvas.unbind_all("<MouseWheel>")






