import tkinter as tk
from tkinter import ttk
import threading
from my_constants import *
from dataStructures import NBitNumber
from frames.ScrollableCanvasFrame import ScrollableCanvasFrame


class DataMemoryFrame(ttk.Frame):
    def __init__(self, parent, SFR_dict, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)  # want canvas to fill all available space
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        # strores the 'bytes' of memory
        self.memory = []

        # list to store intruction labels
        self.rows = [] # allows access for formatting later
        
        self.accessed_registers_in_cycle = []   # list per cycle (used for highlighting)
        self.prev_accessed_registers_in_cycle = []  # to undo highlighting (avoiding iterating through whole memory)
        self.accessed_registers = set() # set of accessed addresses (used to reset quicker + watch option)
        
        self.watching_selected_registers = tk.BooleanVar(value=False) # toggle value to see only see ticked registers
        self.watching_accessed_registers = tk.BooleanVar(value=False) # toggle value to see only changed registers

        # Special Function Registers (SFR) look-up address by name dictionary (rom MCU)
        self.SFR_dict = SFR_dict

        # tkinter widgets

        # panel label
        control_panel_label = ttk.Label(self, text=f"{title}\n{DATA_MEMORY_SIZE} bytes", style='MainWindowInner.TLabel')
        control_panel_label.grid(column=0, row=0, columnspan=2, padx=(5,0), pady=(0,5), sticky="NW")

        mem_label = ttk.Label(      self, 
                                    text="[    address    ][   byte value   ]",
                                    style='MainWindowInner2.TLabel'                     )
        mem_label.grid(column=0, row=1, columnspan=2, padx=(17,0), pady=(0,0), sticky="NW")

        mem_label_2 = ttk.Label(    self,
                                    text="  hex     SFR     dec hex  binary ",
                                    style='MainWindowInner2.TLabel'                     )
        mem_label_2.grid(column=0, row=2, columnspan=2, padx=(15,0), pady=(0,0), sticky="NW")

        # create a scrollable canvas object
        scroll_canvas_frame = ScrollableCanvasFrame(self, DATA_MEMORY_WINDOW_WIDTH, DATA_MEMORY_WINDOW_HEIGHT)
        scroll_canvas_frame.grid(column=0, row=3, sticky="NS")
        scroll_canvas_frame.rowconfigure(0, weight=1)


        # get it's inner frame to mount the memory display on
        inner_frame = scroll_canvas_frame.get_inner_frame()

        # populate the data memory list with default values
        self.initialise_data_memory()

        # define style
        label_style = "MCUmemory.TLabel"
        
        # add memory display to row list
        for mem_address in range(0, DATA_MEMORY_SIZE):
            # create a watching 0/1 variable (stored as 1st element of list)
            watch_bool = tk.BooleanVar(value=False) 
            # checkbox to toggle above bool
            watch_box = ttk.Checkbutton(    inner_frame,
                                            variable=watch_bool,
                                            onvalue=True,
                                            offvalue=False,
                                            style="MCUTickbox.TCheckbutton",
                                            takefocus=False         )
            watch_box.grid(column=0, row=mem_address, pady=(0,5), padx=(3,0), sticky="W")

            addr = ttk.Label(inner_frame, text=f"{mem_address:04X}h", width=5, style=label_style)
            addr.grid(column=1, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            name = ttk.Label(inner_frame, text=self.memory[mem_address].get_name(), width=9, style=label_style)
            name.grid(column=2, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            dec_value = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_dec(), width=3, style=label_style, anchor="e")
            dec_value.grid(column=3, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            hex_value = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_hex(), width=3, style=label_style)
            hex_value.grid(column=4, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            bin_value = ttk.Label(inner_frame, textvariable=self.memory[mem_address].get_bin(), width=8, style=label_style)
            bin_value.grid(column=5, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            # add 'columns' to rows of data
            column = [watch_bool, watch_box, addr, name, dec_value, hex_value, bin_value]

            # append to main list
            self.rows.append(column)

        # test to see if PCL/PCLATH SFR and adjust bg style accordingly
        self._SFRs_background_set()
        
        # add watched reg. display tickbox
        # user can toggle between watched and all registers
        self.toggle_watching_registers = ttk.Checkbutton(   self,
                                                            text="Display only selected registers",
                                                            variable=self.watching_selected_registers,
                                                            onvalue=True,
                                                            offvalue=False,
                                                            style="MCUTickbox2.TCheckbutton",
                                                            takefocus=False,
                                                            command=self._toggle_watching_selected_registers      )
        self.toggle_watching_registers.grid(column=0, row=4, pady=(5,0), padx=(3,3), sticky="EW")

        # user can toggle between watching accessed and all registers
        self.toggle_accessed_registers = ttk.Checkbutton(   self,
                                                            text="Display only accessed registers",
                                                            variable=self.watching_accessed_registers,
                                                            onvalue=True,
                                                            offvalue=False,
                                                            style="MCUTickbox2.TCheckbutton",
                                                            takefocus=False,
                                                            command=self._toggle_watching_accessed_registers      )
        self.toggle_accessed_registers.grid(column=0, row=5, pady=(0,0), padx=(3,3), sticky="EW")


    # MemoryFrame methods
    # keep list of reg's accessed per cycle for highlighting
    def add_accessed_register_cycle(self, new_reg_address):
        self.accessed_registers_in_cycle.append(new_reg_address)

    def highlight_accessed_registers_cycle(self):
        # unhighlight previously accessed registers
        for address in self.prev_accessed_registers_in_cycle:
            for element in self.rows[address][1:]:
                if element.winfo_class() == "TLabel":
                    element.config(background=VISITED_DATA_ADDRESS)
                    
        # highlight accessed registers
        for address in self.accessed_registers_in_cycle:
            for element in self.rows[address][1:]:
                if element.winfo_class() == "TLabel":
                    element.config(background=DATA_MEMORY_HIGHLIGHT)
        
        # manage lists - keep previous cycle list to reset highlights
        self.prev_accessed_registers_in_cycle.clear()
        self.prev_accessed_registers_in_cycle = self.accessed_registers_in_cycle.copy()
        for item in self.accessed_registers_in_cycle:
            self.accessed_registers.add(item)
        self.accessed_registers_in_cycle.clear()

    def _toggle_watching_accessed_registers(self):
        for address, row in enumerate(self.rows):
            if self.watching_accessed_registers.get() == True:
                self.toggle_watching_registers.configure(state="disabled") # disable other watching checkbox
                if address not in self.accessed_registers:  # hide if row not been accessed
                    for element in row[1:]:
                        element.grid_remove()
            else:
                self.toggle_watching_registers.configure(state="normal") # enable other watching checkbox
                for element in self.rows[address][1:]:  # add back if stopped watching
                        element.grid()

        
    def _toggle_watching_selected_registers(self):
        for row in self.rows:
            if self.watching_selected_registers.get() == True:
                self.toggle_accessed_registers.configure(state="disabled") # disable other watching checkbox
                if row[0].get() == False: # access the watch_bool variable#
                    for element in row[1:]:     # romove only grid widgets
                        element.grid_remove()
            else:
                self.toggle_accessed_registers.configure(state="normal") # enable other watching checkbox
                for element in row[1:]:     # add back if stopped watching
                    element.grid()


    # takes a list of SFR names to change bg colour
    def _SFRs_background_set(self):
        for mem_address in self.SFR_dict.values():
            for element in self.rows[mem_address][1:]:
                if element.winfo_class() == "TLabel":
                    element.config(background=PCL_PCLATH_HIGHLIGHT)

    # fill data memory with Byte objects and name accordingly (using the SFR dict)
    def initialise_data_memory(self):
        self.memory.clear()
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
            
        # TRIS registers start as input by default
        self.set_byte_by_name("TRISA", 31)
        self.set_byte_by_name("TRISB", 255)

    # clear all values in data registers and reset highlighting
    def reset_data_memory_frame(self):
        # reset memory and highlighting - using set of accessed addresses to speed it up
        for register in self.accessed_registers:
            # reset memory
            self.memory[register].set_value(0) # sets all accessed registers to zero
            # reset highlighting
            for element in self.rows[register][1:]:
                if element.winfo_class() == "TLabel" : # miss the Checkbox object
                    element.configure(background="white")

        # TRIS registers start as input by default
        self.set_byte_by_name("TRISA", 31)
        self.set_byte_by_name("TRISB", 255)
        self.set_byte_by_name("PORTA", 0)
        self.set_byte_by_name("PORTB", 0)
        self.set_byte_by_name("STATUS", 0)


        self._SFRs_background_set()
        self.prev_accessed_registers_in_cycle.clear()
        self.accessed_registers_in_cycle.clear()
        self.accessed_registers.clear()

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
        address = 0
        #try:
        address = self.SFR_dict[byte_name]
        self.memory[address].set_value(value)
        self.add_accessed_register_cycle(address)
        set_successful = True
        #except:
            #set_successful = False
        return set_successful

    def set_byte_by_address(self, byte_addr, value):
        #try:
        self.memory[byte_addr].set_value(value)
        self.add_accessed_register_cycle(byte_addr)
        set_successful = True
        #except:
            #set_successful = False
        return set_successful


    # bit-wise methods
    # set/clear file reg bit
    def set_file_reg_bit(self, mem_address, bit):
        self.memory[mem_address].set_bit(bit)
        self.add_accessed_register_cycle(mem_address)

    def clear_file_reg_bit(self, mem_address, bit):
        self.memory[mem_address].clear_bit(bit)

    # set/clear status bit 2 (Z); result of ALU gives a zero 
    def set_Z_bit_status(self):
        self.memory[self.SFR_dict["STATUS"]].set_bit(2)
        
    def clear_Z_bit_status(self):
        self.memory[self.SFR_dict["STATUS"]].clear_bit(2)

    # set/clear status bit 0 (C); result of ALU carry over/borrow 
    def set_C_bit_status(self):
        self.memory[self.SFR_dict["STATUS"]].set_bit(0)
        
    def clear_C_bit_status(self):
        self.memory[self.SFR_dict["STATUS"]].clear_bit(0)






