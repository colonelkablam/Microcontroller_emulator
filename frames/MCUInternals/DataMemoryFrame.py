import tkinter as tk
from tkinter import ttk
from my_constants import *
from dataStructures import NBitNumber
from frames.ScrollableCanvasFrame import ScrollableCanvasFrame


class DataMemoryFrame(ttk.Frame):
    def __init__(self, parent, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)  # want canvas to fill all available space
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.memory = []

        # list to store intruction labels
        self.rows = [] # allows access for formatting later
        self.previous_reg_address = -1 # starts as non-existant address
        self.watch_list = []    # stores registers to watch
        self.watch_registers = tk.IntVar(value=0) # toggle value to see if to ticked registers

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

        # tkinter widgets

        # panel label
        control_panel_label = ttk.Label(self, text=f"{title}\n{DATA_MEMORY_SIZE} bytes", style='MainWindowInner.TLabel')
        control_panel_label.grid(column=0, row=0, columnspan=2, padx=(5,0), pady=(0,5), sticky="NW")

        mem_label = ttk.Label(     self, 
                                        text="[    address    ][   byte value   ]",
                                        style='MainWindowInner2.TLabel'                     )
        mem_label.grid(column=0, row=1, columnspan=2, pady=(0,0), sticky="NW")

        mem_label_2 = ttk.Label(   self,
                                        text="  hex     SFR     dec hex  binary ",
                                        style='MainWindowInner2.TLabel'                     )
        mem_label_2.grid(column=0, row=2, columnspan=2, pady=(0,0), sticky="NW")

        # create a scrollable canvas object
        scroll_canvas_frame = ScrollableCanvasFrame(self, DATA_MEMORY_WINDOW_WIDTH, DATA_MEMORY_WINDOW_HEIGHT)
        scroll_canvas_frame.grid(column=0, row=3, sticky="NS")
        scroll_canvas_frame.rowconfigure(0, weight=1)


        # get it's inner frame to mount the memory display on
        inner_frame = scroll_canvas_frame.get_inner_frame()

        self.initialise_data_memory()

        # define style
        label_style = "MCUmemory.TLabel"
        # add memory display
        for mem_address in range(0, DATA_MEMORY_SIZE):

            addr = ttk.Label(inner_frame, text=f"{mem_address:04X}h", width=5, style=label_style)
            addr.grid(column=0, row=mem_address, pady=(0,5), padx=5, sticky="W")

            name = ttk.Label(inner_frame, text=self.memory[mem_address].get_name(), width=9, style=label_style)
            name.grid(column=1, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            dec_value = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_dec(), width=3, style=label_style, anchor="e")
            dec_value.grid(column=2, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            hex_value = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_hex(), width=3, style=label_style)
            hex_value.grid(column=3, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            bin_value = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_bin(), width=8, style=label_style)
            bin_value.grid(column=4, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")
            
            watch = tk.IntVar(value=0) # create a watching 0/1 variable
            watch_box = ttk.Checkbutton(inner_frame, variable=watch, onvalue=1, offvalue=0)#, bg=COLOUR_MEMORY_FRAME_BACKGROUND)
            watch_box.grid(column=5, row=mem_address, pady=(0,0), padx=(0,0), sticky="W")
            self.watch_list.append(watch) # add watch variable to watch_list

            # add 'columns' to rows of data
            column = [addr, name, dec_value, hex_value, bin_value]
            
            # test to see if PC byte - adjust style accor
            if mem_address == self.SFR_dict["PCL"] or mem_address == self.SFR_dict["PCLATH"]:
                for label in column:
                    label.config(background=PCL_PCLATH_HIGHLIGHT)

            # append to main list
            self.rows.append(column)
        
        # add watched reg. display tickbox
        # user can toggle between watched and all registers
        toggle_watch_registers = tk.Checkbutton(    self,
                                                    variable=self.watch_registers,
                                                    onvalue=1,
                                                    offvalue=0,
                                                    bg=COLOUR_MEMORY_FRAME_BACKGROUND,
                                                    command=self._toggle_watching_reg      )
        toggle_watch_registers.grid(column=0, row=4, pady=(0,0), padx=(0,0), sticky="W")





    # MemoryFrame methods
    def highlight_current_register(self, new_reg_address):

        if new_reg_address != -1:
            for label in self.rows[new_reg_address]:
                label.config(background=DATA_MEMORY_HIGHLIGHT)

        if self.previous_reg_address != -1:
            for label in self.rows[self.previous_reg_address]:
                label.config(background=VISITED_DATA_ADDRESS)

        self.previous_reg_address = new_reg_address

    def _toggle_watching_reg(self):
        for address, watch in enumerate(self.watch_list):
            if watch.get() == 0:
                for label in self.rows[address]:
                    label.grid_remove()

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
            self.memory.append(NBitNumber(8, tk.IntVar(value=0), tk.StringVar(value="00h"), tk.StringVar(value=f"00000000"), name))

    # retrieve bytes from data memory by name (if SFR) or address - return None if outside of index
    def get_byte_by_name(self, byte_name):
        try:
            byte = self.memory[self.SFR_dict[byte_name]]
        except:
            byte = None
        return byte

    def get_byte_by_address(self, byte_addr):
        try:
            byte = self.memory[byte_addr]
        except:
            byte = None
        return byte

    # set bytes by name or address - return False if outside of index/unable to set
    def set_byte_by_name(self, byte_name, value):
        try:
            self.memory[self.SFR_dict[byte_name]].set_value(value)
            set_successful = True
        except:
            set_successful = False
        return set_successful

    def set_byte_by_address(self, byte_addr, value):
        try:
            self.memory[byte_addr].set_value(value)
            set_successful = True
        except:
            set_success = False
        return set_successful


    # bit-wise methods
    # set/clear file reg bit
    def set_file_reg_bit(self, mem_address, bit):
        self.memory[mem_address].set_bit(bit)

    def clear_file_reg_bit(self, mem_address, bit):
        self.memory[mem_address].clear_bit(bit)

    # set/clear status bit 2 (Z); result of ALU gives a zero 
    def set_Z_bit_status(self):
        self.memory[self.SFR_dict["STATUS"]].set_bit(2)
        
    def clear_Z_bit_status(self):
        self.memory[self.SFR_dict["STATUS"]].clear_bit(2)






