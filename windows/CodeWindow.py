import tkinter as tk
import os
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
        
        self.empty_file_text = "** No file loaded **"
        self.current_file_path = tk.StringVar(value=self.empty_file_text)
        self.current_file_name = tk.StringVar(value=self.empty_file_text)

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
        self.compiled_program = [   ["GOTO",   "0x05",  ""],
                                    ["ADDLW",  "0xFF",  ""],
                                    ["ADDLW",  "0xFF",  ""],
                                    ["ADDLW",  "0xFF",  ""],
                                    ["ADDLW",  "0xFF",  ""],
                                    ["CLRW",   "",  ""],
                                    ["MOVWF",  "0x85",  ""],
                                    ["MOVLW",  "0x02",  ""],
                                    ["MOVWF",  "0x05",  "0"],
                                    ["NOP",   "",  ""],
                                    ["CLRF",  "0x86",  ""],
                                    ["MOVLW",  "0x01",  ""],
                                    ["ADDWF",  "0x06",  "1"],
                                    ["GOTO",  "0x0C",  ""],
                                    ["ADDLW",  "0xFF",  ""],    ]


        # tkinter Widgets

        # create window pop up
        # create the new window to load/save/edit/compile code
        self.code_window = tk.Toplevel()
        self.code_window.title("Code Editor")
        self.code_window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_xpos, window_ypos))
        # bind functions
        self.code_window.wm_protocol('WM_DELETE_WINDOW', self.on_close_window) # clean up after window close

        # style
        self.code_window["background"] = COLOUR_MAIN_BACKGROUND
        self.code_window.rowconfigure(0, weight=1)
        self.code_window.columnconfigure(0, weight=1)

        # create a CodeDisplayFrame - put in new CodeWindow
        self.code_frame = CodeDisplayFrame(self.code_window, self.current_file_name, self.current_file_path)
        self.code_frame.grid(column=0, row=0, sticky="NSEW")

        # create buttons
        # container Frame
        self.button_frame = ttk.Frame(self.code_window, style='CodeWindow.TFrame', padding=10)
        self.button_frame.grid(column=0, row=1, sticky="SEW")
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
        self.load_into_MCU_button.configure(style="CodeWindow2.TButton")


    # CodeWindow methods

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

    def on_close_window(self):
        # destroy the toplevel window
        self.code_window.destroy()
        # clear code_window var in MainWindow
        self.parent.clear_code_window()
        # add note to log
        self.parent.system_message("Code Window closed.")

    def lift_window(self):
        self.code_window.lift()


    
