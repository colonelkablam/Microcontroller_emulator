import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames.MCUInternals.MCUStatusFrames import BinaryDisplayFrame


class MCUStatusFrame(ttk.Frame):
    def __init__(self, parent, title ="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="MainWindowInner.TFrame", padding=10)
        self.columnconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent

        self.previous_instruction = tk.StringVar(value="n/a")
        self.next_instruction = tk.StringVar(value="  ".join(parent.get_current_instruction()))
        self.instruction_cycles = tk.IntVar()
        self.num_instructions_executed = tk.IntVar()

        self.q_cycles_per_instruction = self.parent.Q_cycles_per_instruction
        self.clock_frequency = self.parent.clock_frequency


        # tkinter widgets

        # panel label
        self.control_panel_label = ttk.Label(self, text=title, style='MainWindowInner.TLabel')
        self.control_panel_label.grid(column=0, row=0, columnspan=2, sticky="NE")

        # PROGRAM COUNTER - need to enter a tuple of the byte(s) being displayed
        self.PCL_display = BinaryDisplayFrame(  self, 
                                                self.parent.get_PC_13bit_representation(),
                                                title="Program Counter",
                                                bit_numbering="12 -PCLATH-  7 ----- PCL ---- 0",
                                                style='MainWindowInner.TLabel'                  )
        
        self.PCL_display.grid(column=0, row=1, columnspan=2, sticky="EW")

        # STACK - displayed within the MCU status frame but contained in MCUFrame as a data holder
     
        # STATUS REG
        self.STATUS_display = BinaryDisplayFrame(   self,
                                                    self.parent.get_byte_by_name("STATUS"),
                                                    title = "Status Register",
                                                    bit_numbering =              "7           z dc c"     )

        self.STATUS_display.grid(column=1, row=2, sticky="EW")
        
        # WORKING REG
        self.WREG_display = BinaryDisplayFrame( self,
                                                self.parent.get_w_register(),
                                                title = "Working Register",
                                                bit_numbering =              "7    -- bit --   0"     )
        self.WREG_display.grid(column=1, row=3, sticky="EW")

        # PORTA
        self.PORTA_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("PORTA"),
                                                display_dec = False,
                                                display_hex = False,
                                                title = "PORTA"                 )
        self.PORTA_display.grid(column=1, row=4, pady=(5,0), sticky="NEW")
        
        # TRISA
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("TRISA"),
                                                display_dec = False,
                                                display_hex = False,
                                                title = "TRISA"                   )
        self.PARTB_display.grid(column=1, row=5, pady=(0,5), sticky="NEW")
        
        # PORTB
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("PORTB"),
                                                display_dec=False,
                                                display_hex=False,
                                                title="PORTB"                      )
        self.PARTB_display.grid(column=1, row=6, pady=(5,0), sticky="NEW")

        # TRISB
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("TRISB"),
                                                display_dec=False,
                                                display_hex=False,
                                                title="TRISB"                      )
        self.PARTB_display.grid(column=1, row=7, pady=(0,0), sticky="NEW")

        # MCU status info 
        self.status_info_frame = ttk.Frame(self, style="MainWindowInner2.TFrame", padding=5)
        self.status_info_frame.grid(column=0, row=8, sticky="EW", columnspan=2)
        self.status_info_frame.columnconfigure(1, weight=1)

        self.last_instruction_label = ttk.Label(self.status_info_frame, text="Prev. Instruction:", anchor="e", style='ByteDisplayHeading.TLabel')
        self.last_instruction_label.grid(column=0, row=0, padx=(10,10), pady=(0,5))

        self.last_instruction = ttk.Label(self.status_info_frame, textvariable=self.previous_instruction, anchor="center", style= "Instruction.TLabel")
        self.last_instruction.grid(column=1, row=0, padx=(5,10), pady=(0,5))

        self.next_instruction_label = ttk.Label(self.status_info_frame, text="Next Instruction:", anchor="e", style='ByteDisplayHeading.TLabel')
        self.next_instruction_label.grid(column=0, row=1, padx=(10,10), pady=(0,0))

        self.next_instruction_label = ttk.Label(self.status_info_frame, textvariable=self.next_instruction, anchor="center", style= "Instruction.TLabel")
        self.next_instruction_label.grid(column=1, row=1, padx=(5,10), pady=(0,0))

        for label in self.status_info_frame.winfo_children():
            label.grid(sticky="EW")

    def update_display(self):
        # get tuple of information from parent (MCUFrame)
        status_info = self.parent.get_status_info()
        # set the tkinter variable objects
        self.previous_instruction.set("  ".join(status_info[0]))
        self.next_instruction.set("  ".join(status_info[1]))
        self.instruction_cycles.set(status_info[2])
        self.num_instructions_executed.set(status_info[3])
        # update each TFrame
        for widget in self.winfo_children():
            if widget.winfo_class() == "TFrame":
                widget.update()

    def reset_display(self):
        # get tuple of information from parent (MCUFrame)
        status_info = self.parent.get_status_info()
        # set the tkinter variable objects
        self.previous_instruction.set("n/a")
        self.next_instruction.set("  ".join(status_info[1]))
        self.instruction_cycles.set(0)
        self.num_instructions_executed.set(0)
        # update each TFrame
        for widget in self.winfo_children():
            if widget.winfo_class() == "TFrame":
                widget.update()






        








