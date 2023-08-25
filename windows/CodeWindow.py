import tkinter as tk
import os
import re
from tkinter import ttk
from frames import CodeDisplayFrame
from my_constants import *
from styling import MainStyle


class CodeWindow:
    def __init__(self, parent):
        
        # properties

        # starting position relative to parent window

        window_width = CODE_WINDOW_WIDTH
        window_height = CODE_WINDOW_HEIGHT
        window_xpos = parent.winfo_x() + 30
        window_ypos = parent.winfo_y() + 30

        self.parent = parent
        self.always_on_top = tk.BooleanVar(value=False)
        self.dark_theme = tk.BooleanVar(value=False)
        
        self.empty_file_text = "** No file loaded **"
        self.current_file_path = tk.StringVar(value=self.empty_file_text)
        self.current_file_name = tk.StringVar(value=self.empty_file_text)

        self.instruction_set = [    "GOTO",
                                    "ADDLW",
                                    "ADDWF"  ]

        # # test program 1
        # self.compiled_program = [   ["GOTO",   "0x05",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["MOVLW",  "0x08",  ""],
        #                             ["MOVWF",  "0x20",  ""],
        #                             ["MOVLW",  "0xA2",  ""],
        #                             ["ADDWF",  "0x20",  "0"],
        #                             ["NOP",   "",  ""],
        #                             ["ADDLW",  "0xA2",  ""],
        #                             ["ADDWF",  "0x21",  "1"],
        #                             ["GOTO",  "0x00",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],    ]

        # test program 2
        # self.compiled_program = [   ["GOTO",   "0x05",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["CLRW",   "0xFF",  ""],
        #                             ["CLRF",   "0x86",  ""],
        #                             ["MOVF",   "0x05",  "0"],
        #                             ["MOVWF",  "0x20",  ""],
        #                             ["NOP",    "",      ""],
        #                             ["ADDWF",  "0x06",  "1"],
        #                             ["GOTO",   "0x09",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],   ]

        # test program 3
        # self.compiled_program = [   ["GOTO",   "0x02",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["CALL",   "0x06",  ""], # 2
        #                             ["GOTO",   "0x10",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["ADDLW",  "0x02",  ""], # 6
        #                             ["ADDLW",  "0x10",  ""],
        #                             ["CALL",   "0x0A",  ""],
        #                             ["RETURN",   "",  ""],
        #                             ["MOVWF",  "0x20",  "1"], # A
        #                             ["RETURN",  "0xFF",  ""],
        #                             ["CALL",   "0x0D",  ""],
        #                             ["GOTO",   "0x00",  ""],
        #                             ["ADDLW",  "0xFF",  ""],
        #                             ["MOVF",   "0x05",  "0"], # F
        #                             ["GOTO",  "0x00",  ""],   
        #                             ["RETURN",  "",     ""],        ]

        # test program 4
        self.compiled_program = [   ["CALL",   "0x08",  ""],
                                    ["CLRF",   "0x85",  ""],
                                    ["MOVLW",  "0x0A",  ""],
                                    ["ANDWF",  "0x06",  "0"],
                                    ["MOVWF",  "0x05",  "0"],
                                    ["NOP",     "",     ""],
                                    ["GOTO",   "0x05",  ""],
                                    ["ADDLW",   "0xFF", ""],
                                    ["RETURN",  "",     ""]         ]


        # tkinter Widgets

        # create window pop up
        # create the new window to load/save/edit/compile code
        self.code_window = tk.Toplevel()
        self.code_window.title("Code Editor")
        self.code_window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_xpos, window_ypos))
        # bind functions
        self.code_window.wm_protocol('WM_DELETE_WINDOW', self.on_close_window) # clean up after window close

        # style
        self.code_window["background"] = COLOUR_INNER2_BACKGROUND
        self.code_window.rowconfigure(0, weight=1)
        self.code_window.columnconfigure((0), weight=1)

        # create a CodeDisplayFrame - put in new CodeWindow
        self.code_frame = CodeDisplayFrame(self.code_window, self.current_file_name, self.current_file_path)
        self.code_frame.grid(column=0, row=0, columnspan=2, sticky="NSEW")

        # create buttons
        # container Frame
        self.button_frame = ttk.Frame(self.code_window, style='CodeWindow.TFrame')
        self.button_frame.grid(column=0, row=1, columnspan=2, sticky="SW")
        self.button_frame.columnconfigure((0,1,2), weight=1)

        #open code file
        self.open_code_button = ttk.Button(self.button_frame, text="open", command=self.open_text_file)
        self.open_code_button.grid(column=0, row=0, sticky="EW")
        
        #save code file
        self.save_code_button = ttk.Button(self.button_frame, text="save", command=self.save_text_file)
        self.save_code_button.grid(column=1, row=0, sticky="EW")

        #'save as' code file
        self.save_as_code_button = ttk.Button(self.button_frame, text="save as", command=self.save_as_text_file)
        self.save_as_code_button.grid(column=2, row=0, sticky="EW")

        # compile program
        self.compile_button = ttk.Button(self.button_frame, text="compile code", command=self.compile_code)
        self.compile_button.grid(column=0, row=1, columnspan=2, sticky="EW")

        #load_program_into_MCU
        self.load_into_MCU_button = ttk.Button(self.button_frame, text="load program into MCU", command=self.load_program_into_MCU)
        self.load_into_MCU_button.grid(column=2, row=1, columnspan=1, sticky="EW")

        # apply main button style to all buttons
        for child in self.button_frame.winfo_children():
            child.configure(padding=5, style="CodeWindow.TButton")
            child.grid(padx=5, pady=5)
        self.load_into_MCU_button.configure(style="MainWindow3.TButton")
        self.compile_button.configure(style="MainWindow4.TButton")

        # checkbox to keep window at the top
        keep_at_top_checkbox = ttk.Checkbutton( self.code_window,
                                                text="Keep window on top",
                                                variable=self.always_on_top,
                                                onvalue=True,
                                                offvalue=False,
                                                style="MCUTickbox3.TCheckbutton",
                                                padding=5,
                                                takefocus=False,
                                                command=self._toggle_keep_on_top      )
        keep_at_top_checkbox.grid(column=0, row=2, pady=(0,0), padx=(0,0), sticky="W")
        
        # checkbox toggle light/dark code theme
        toggle_colour_theme = ttk.Checkbutton(     self.code_window,
                                                    text="Toggle dark / light theme",
                                                    variable=self.dark_theme,
                                                    onvalue=True,
                                                    offvalue=False,
                                                    style="MCUTickbox3.TCheckbutton",
                                                    padding=5,
                                                    takefocus=False,
                                                    command=self._toggle_dark_theme      )
        toggle_colour_theme.grid(column=1, row=2, pady=(0,0), padx=(0,0), sticky="EW")


    ## CodeWindow methods

    # display options
    def _toggle_keep_on_top(self):
        if self.always_on_top.get() == True:
            self.code_window.attributes('-topmost', True)
        else:
            self.code_window.attributes('-topmost', False)

    def _toggle_dark_theme(self):
        self.code_frame.toggle_dark_theme(self.dark_theme.get())


    # open a text file and generate fill code editor with text
    def open_text_file(self):
        open_file_name = tk.filedialog.askopenfilename(initialdir="./", title="Open Text File", filetypes=(("Assembly Files", "*.asm"), ("Text Files", "*.txt"), ))
        if open_file_name:
            self.current_file_path.set(open_file_name)                      # save current file path
            self.current_file_name.set(os.path.basename(open_file_name))    # save current filename
            assembly_text = open(open_file_name, 'r')
            # populate text box
            self.code_frame.update_code_editor_display(assembly_text.read())
            assembly_text.close()
            self.parent.system_message(f"File '{open_file_name}' loaded into code editor.")

        else:
            self.parent.system_message("No file name chosen - Open File aborted.")

            self.code_frame.update_code_editor_display()

        # keep window at top
        self.code_window.lift()

    # save as - name/rename code editor text
    def save_as_text_file(self):
        
        # generate save filename
        save_file_name = tk.filedialog.asksaveasfilename(initialdir="./", initialfile="new_file.asm", title="Save Text File", filetypes=(("Assembly Files", "*.asm"), ("Text Files", "*.txt"), ))
        # if new filename given
        if save_file_name:
            self.current_file_path.set(save_file_name)                      # save current file path
            self.current_file_name.set(os.path.basename(save_file_name))    # save current filename
            # create new file
            new_file = open(save_file_name, 'w')
            # save contents of code editor textbox to file
            new_file.write(self.code_frame.code_text.get(1.0, tk.END))
             # close file
            new_file.close()
            # update code in code_editor textbox
            self.code_frame.update_code_editor_display()
            # log action
            self.parent.system_message(f"File saved as: '{save_file_name}'.")
    
        else:
            self.parent.system_message("No file name chosen - Save aborted.")

        # keep window at top
        self.code_window.lift()
    
    # save - save code editor text
    def save_text_file(self):
        # check if an existing file path valid (anything but starting string)
        if self.current_file_path.get() != self.empty_file_text:
            # update code in code_editor textbox
            self.code_frame.update_code_editor_display()
            # open file
            current_file = open(self.current_file_path.get(), 'w')
            # save
            current_file.write(self.code_frame.code_text.get(1.0, tk.END))
            # close file
            current_file.close()
            # log action
            self.parent.system_message(f"File saved as: '{self.current_file_path.get()}'.")

        # if no file path then call save as method
        else:
            self.save_as_text_file()

    # send compiled program to MCU_frame - list of 3 element lists (that make up the instruction)
    def load_program_into_MCU(self):
        self.parent.system_message("Loading program into Program Memory...")
        try:
            self.parent.MCU_frame.upload_program(self.compiled_program)
            self.parent.system_message(f"{len(self.compiled_program)} line program successfully loaded into MCU.")

        except Exception as e:
            self.parent.system_message(f"Failed to load program to MCU; Exception arguments:{e.args}")


    # compile the users code in the window
    def compile_code(self):
        self.parent.system_message("Compiling code...")
        
        # get the text from the text box in the code_frame object
        whole_text = self.code_frame.code_text.get(1.0, tk.END)

        # split the lines into words
        word_list_per_line = []

        for line in whole_text.split("\n"):
            word_list = []
            # for each word in line
            for word in line.split():
                # check for ';' comment character to ignore whole/rest of line
                if word[0] == ";":
                    break
                else:
                    word_list.append(word)
            # add word list to line list if any words
            if len(word_list) != 0:
                word_list_per_line.append(word_list)

        print(word_list_per_line)

        # create empty list for upload to MCU
        compiled_program = []
        for empty_instruction in range(256):
            compiled_program.append(["ADDWF", "0xFF", "-"]) # list of 3 empty strings (MCU format)
        
        # dict to store vars
        var_dict = {}

        subroutine_dict = {}

        # keep track of instruction address
        PC = 0

        # iterate through code lines
        for text_line, instruction in enumerate(word_list_per_line):
            instruction_line = []
            print(instruction)

            # INSTRUCTION from SET
            # if first part a recognised MNUMONIC then append next one or two parts into instruction code
            if instruction[0] in self.instruction_set:
                for i, part_instruction in enumerate(instruction):
                    # MNUMONIC
                    if i == 0:
                        instruction_line.append(part_instruction)
                    # 1st operand
                    elif i == 1: # can be literal value or address
                        if re.search('^0x[a-fA-F0-9]+$', part_instruction): # is already in hex format?
                            instruction_line.append(f"0x{int(int(part_instruction), 16):04X}")
                        elif re.search('^[0-9]*$', part_instruction):  # else if decimal turn into hex
                            instruction_line.append(f"0x{int(part_instruction, 10):04X}")
                        else:
                            instruction_line.append("") # operand 1 left empty if above criteria not met
                    # 2nd operand
                    elif i == 2: # one charcter only (defines destination or bit)
                        if re.search('^[0-9]{1}|[WwFf]{1}$', part_instruction): 
                            instruction_line.append(part_instruction)
                        else:
                            instruction_line.append("") # operand 2 left empty if above criteria not met

                    # stop instruction line; the rest can be ignored
                    elif i > 2:
                        break # if more parts ignore (no more than 3 parts needed)
                    else:
                        print(f"error compiling part {i} of instruction '{part_instruction}' on code editor line {code_line}; not recognised")

                # insert in the correct program address
                compiled_program[PC] = instruction_line
                # move to next line
                PC += 1

            # PROGRAM SECTIONS and SUBROUTINES
            # else, check 1st part ENDS with a ':' i.e. main: or loop:
            elif re.search('^[^0-9]+\w+:$', instruction[0]):
                # if only only part PC remains unchanged
                if len(instruction) == 1:
                    subroutine_dict.update({instruction[0] : f"0x{PC:04X}"})
                # if 3 parts and 2nd part is CODE and 3rd valid address then use prodecing address as location
                elif len(instruction) == 3 and re.search('^0x[a-fA-F0-9]+$', instruction[2]) :
                    if instruction[1] == "CODE":
                        # store location in subroutine dict - format hex
                        subroutine_dict.update({instruction[0] : f"{int(instruction[2]):04X}"})
                else:
                    print(f"Error creating subroutine/program section '{instruction}")

                # move to next line
                PC += 1

            # VARIABLES
            # else, if three parts (needed to define a variable address location), add variable to dictionary
            elif len(instruction) == 3 and re.search('^[^0-9]+\w+$', instruction[0]):
                if instruction[1] == "EQU":
                    var_dict.update({instruction[0] : instruction[2]})
                else:
                    print(f"Error creating variable '{instruction[0]}")
                # move to next line
                PC += 1


        print(compiled_program[:5])
        print(var_dict)
        print(subroutine_dict)




    def on_close_window(self):
        # destroy the toplevel window
        self.code_window.destroy()
        # clear code_window var in MainWindow
        self.parent.clear_code_window()
        # add note to log
        self.parent.system_message("Code Window closed.")

    def lift_window(self):
        self.code_window.lift()


    
