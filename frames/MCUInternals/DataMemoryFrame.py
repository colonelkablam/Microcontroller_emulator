import tkinter as tk
from tkinter import ttk
from my_constants import *


class DataMemoryFrame(ttk.Frame):
    def __init__(self, parent, memory, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)  # want canvas to fill all available space
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.memory = memory

        # list to store intruction labels
        self.rows = [] # allows access for formatting later
        self.previous_reg_address = -1

        # tkinter widgets

        # panel label
        self.control_panel_label = ttk.Label(self, text=f"{title}\n{DATA_MEMORY_SIZE} bytes", style='MainWindowInner.TLabel')
        self.control_panel_label.grid(column=0, row=0, columnspan=2, padx=(5,0), pady=(0,5), sticky="NW")

        self.mem_label = ttk.Label(     self, 
                                        text="[    address    ][   byte value   ]",
                                        style='MainWindowInner2.TLabel'                     )
        self.mem_label.grid(column=0, row=1, columnspan=2, pady=(0,0), sticky="NW")

        self.mem_label_2 = ttk.Label(   self,
                                        text="  hex     SFR     dec hex  binary ",
                                        style='MainWindowInner2.TLabel'                     )
        self.mem_label_2.grid(column=0, row=2, columnspan=2, pady=(0,0), sticky="NW")

        # canvas
        self.scroll_canvas = tk.Canvas(self, width=DATA_MEMORY_WINDOW_WIDTH, height=DATA_MEMORY_WINDOW_HEIGHT)
        self.scroll_canvas.grid(column=0, row=3, sticky="NS")
        self.scroll_canvas.columnconfigure(0, weight=1)
        self.scroll_canvas.rowconfigure(0, weight=1)

        # scrollbars
        self.code_scroll = ttk.Scrollbar(self, orient='vertical', command=self.scroll_canvas.yview)
        self.code_scroll.grid(column=1, row=3, sticky="NS")

        # configure canvas
        self.scroll_canvas.configure(yscrollcommand=self.code_scroll.set)
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.scroll_canvas.bind('<Leave>', self._unbound_to_mousewheel)

        # create ANOTHER inner frame inside canvas
        self.inner_frame = ttk.Frame(self.scroll_canvas, style="MCUmemory.TFrame")

        # add INNER FRAME to a window in the canvas
        self.scroll_canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

        # add memory display
        for mem_address in range(0, DATA_MEMORY_SIZE):
            addr = ttk.Label(self.inner_frame, text=f"{mem_address:04X}h", width=5, style="MCUmemory.TLabel")
            addr.grid(column=0, row=mem_address, pady=(0,5), padx=5, sticky="W")

            name = ttk.Label(self.inner_frame, text=self.memory[mem_address].get_name(), width=9, style="MCUmemory.TLabel")
            name.grid(column=1, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            dec_value = ttk.Label(self.inner_frame, textvariable=self.memory[mem_address].get_dec(), width=3, style="MCUmemory.TLabel", anchor="e")
            dec_value.grid(column=2, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            hex_value = ttk.Label(self.inner_frame, textvariable=self.memory[mem_address].get_hex(), width=3, style="MCUmemory.TLabel")
            hex_value.grid(column=3, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            bin_value = ttk.Label(self.inner_frame, textvariable=self.memory[mem_address].get_bin(), width=8, style="MCUmemory.TLabel")
            bin_value.grid(column=4, row=mem_address, pady=(0,5), padx=(0,5), sticky="W")

            # add 'columns' to rows of data
            self.rows.append([addr, name, dec_value, hex_value, bin_value])


    # MemoryFrame methods
    def highlight_current_register(self, new_reg_address):

        if new_reg_address != -1:
            for label in self.rows[new_reg_address]:
                label.config(background=DATA_MEMORY_HIGHLIGHT)

        if self.previous_reg_address != -1:
            for label in self.rows[self.previous_reg_address]:
                label.config(background=VISITED_DATA_ADDRESS)

        self.previous_reg_address = new_reg_address



    # canvas scrolling behaviour
    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bound_to_mousewheel(self, event):
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.scroll_canvas.unbind_all("<MouseWheel>")






