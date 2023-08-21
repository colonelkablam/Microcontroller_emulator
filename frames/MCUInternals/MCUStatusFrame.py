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
        self.cycle_count = tk.IntVar()
        self.num_instructions_executed = tk.IntVar()

        # info to calculate time elapsed
        self.q_cycles_per_instruction = self.parent.Q_cycles_per_instruction
        self.clock_mhz = self.parent.clock_frequency
        self.time_per_cycle = 1 / ((self.clock_mhz/1000) / self.q_cycles_per_instruction) # nano seconds 
        self.time_elapsed_microsecond = tk.IntVar()




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
                                                title = "      PORTA"                 )
        self.PORTA_display.grid(column=1, row=4, padx=(10,0), pady=(10,0), sticky="NEW")
        
        # TRISA
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("TRISA"),
                                                display_dec = False,
                                                display_hex = False,
                                                title = "      TRISA"                   )
        self.PARTB_display.grid(column=1, row=5, padx=(10,0), pady=(0,5), sticky="NEW")
        
        # PORTB
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("PORTB"),
                                                display_dec=False,
                                                display_hex=False,
                                                title = "      PORTB"                      )
        self.PARTB_display.grid(column=1, row=6, padx=(10,0), pady=(5,0), sticky="NEW")

        # TRISB
        self.PARTB_display = BinaryDisplayFrame(self,
                                                self.parent.get_byte_by_name("TRISB"),
                                                display_dec=False,
                                                display_hex=False,
                                                title = "      TRISB"                      )
        self.PARTB_display.grid(column=1, row=7, padx=(10,0), pady=(0,10), sticky="NEW")

        ## MCU status info 
        # instructions
        self.status_info_frame = ttk.Frame(self, style="MainWindowInner2.TFrame", padding=5)
        self.status_info_frame.grid(column=0, row=8, sticky="EW", columnspan=2)
        self.status_info_frame.columnconfigure(1, weight=1)

        self.last_instruction_label = ttk.Label(self.status_info_frame, text="Prev. Instruction:", anchor="e", style="StatusHeading.TLabel")
        self.last_instruction_label.grid(column=0, row=0, padx=(10,10), pady=(5,5), sticky="EW")

        self.last_instruction = ttk.Label(self.status_info_frame, textvariable=self.previous_instruction, anchor="center", style= "Instruction.TLabel")
        self.last_instruction.grid(column=1, row=0, padx=(5,10), pady=(5,5), sticky="EW")

        self.next_instruction_label = ttk.Label(self.status_info_frame, text="Next Instruction:", anchor="e", style="StatusHeading.TLabel")
        self.next_instruction_label.grid(column=0, row=1, padx=(10,10), pady=(0,5), sticky="EW")

        self.next_instruction_label = ttk.Label(self.status_info_frame, textvariable=self.next_instruction, anchor="center", style= "Instruction.TLabel")
        self.next_instruction_label.grid(column=1, row=1, padx=(5,10), pady=(0,5), sticky="EW")

        # time frame - goes inside status information frame
        self.time_frame = ttk.Frame(self.status_info_frame, style="MainWindowInner2.TFrame", padding=5)
        self.time_frame.grid(column=0, row=2, columnspan=2, sticky="EW")
        self.time_frame.columnconfigure((1,2), weight=1)

        # display times
        self.cycle_count_label = ttk.Label(self.time_frame, text="Cycle Count:", anchor="e", style="StatusHeading.TLabel")
        self.cycle_count_label.grid(column=0, row=0, padx=(0,0), pady=(0,0), sticky="EW")

        self.cycle_count_display = ttk.Label(self.time_frame, width=5, textvariable=self.cycle_count, anchor="center", style= "Instruction.TLabel")
        self.cycle_count_display.grid(column=1, row=0, padx=(0,0), pady=(0,0), sticky="EW")

        self.instruction_count_label = ttk.Label(self.time_frame, text="Instruction Count:", anchor="e", style="StatusHeading.TLabel")
        self.instruction_count_label.grid(column=0, row=1, padx=(0,0), pady=(0,0), sticky="EW")

        self.instruction_count = ttk.Label(self.time_frame, width=5, textvariable=self.num_instructions_executed, anchor="center", style= "Instruction.TLabel")
        self.instruction_count.grid(column=1, row=1, padx=(0,0), pady=(0,0), sticky="EW")

        self.elapsed_time_label = ttk.Label(self.time_frame, text="Time (μs):", anchor="e", style="StatusHeading.TLabel")
        self.elapsed_time_label.grid(column=2, row=0, padx=(0,0), pady=(0,0), sticky="EW")

        self.elapsed_time = ttk.Label(self.time_frame, width=7, textvariable=self.time_elapsed_microsecond, anchor="center", style= "Instruction.TLabel")
        self.elapsed_time.grid(column=3, row=0, padx=(0,0), pady=(0,0), sticky="EW")

        self.mhz_label = ttk.Label(self.time_frame, text="MCU MHz:", anchor="e", style="StatusHeading.TLabel")
        self.mhz_label.grid(column=2, row=1, padx=(0,0), pady=(0,0), sticky="EW")

        self.mhz = ttk.Label(self.time_frame, width=7, text=self.clock_mhz, anchor="center", style= "Instruction.TLabel")
        self.mhz.grid(column=3, row=1, padx=(0,0), pady=(0,0), sticky="EW")


    def update_display(self):
        # get tuple of information from parent (MCUFrame)
        status_info = self.parent.get_status_info()
        # set the tkinter variable objects
        self.previous_instruction.set("  ".join(status_info[0]))
        self.next_instruction.set("  ".join(status_info[1]))
        self.cycle_count.set(status_info[2])
        self.num_instructions_executed.set(status_info[3])
        self.time_elapsed_microsecond.set((self.time_per_cycle * self.cycle_count.get()) / 1000)

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
        self.cycle_count.set(0)
        self.num_instructions_executed.set(0)
        self.time_elapsed_microsecond.set(0)

        # update each TFrame
        for widget in self.winfo_children():
            if widget.winfo_class() == "TFrame":
                widget.update()






        








