import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from my_constants import *
from styling import MainStyle


class CodeDisplayFrame(ttk.Frame):
    def __init__(self, parent, file_name, file_path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(padding=10, style="CodeWindow.TFrame")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.file_path = file_path
        self.file_name = file_name
        _code_text_size = 10


        # tkinter widgets

        # label for code box
        self.file_name_title = ttk.Label(self, text="File Name: ", style="CodeWindow.TLabel")
        self.file_name_title.grid(column=0, row=0, sticky="W")
        self.file_name_label = ttk.Label(self, textvariable=self.file_name, style="CodeWindow.TLabel")
        self.file_name_label.grid(column=1, row=0, sticky="EW")

        # frame to contain code text boxes (lines and code + canvas for scrolling)
        self.code_box_frame = ttk.Frame(self, style="CodeWindow.TFrame")
        self.code_box_frame.grid(column=0, row=1, columnspan=2, sticky="NSEW")
        self.code_box_frame.columnconfigure(0, weight=1)
        self.code_box_frame.rowconfigure(0, weight=1)

        # canvas
        self.scroll_canvas = tk.Canvas(self.code_box_frame)
        self.scroll_canvas.grid(column=0, row=0, sticky="NSEW")
        self.scroll_canvas.columnconfigure(0, weight=1)

        # scrollbars
        self.code_scroll = tk.Scrollbar(self.code_box_frame, orient='vertical', command=self.scroll_canvas.yview)
        self.code_scroll.grid(column=2, row=0, sticky="NS")

        self.code_scroll_h = tk.Scrollbar(self.code_box_frame, orient='horizontal', command=self.scroll_canvas.xview)
        self.code_scroll_h.grid(column=0, row=1, sticky="EW")

        # configure canvas
        self.scroll_canvas.configure(yscrollcommand=self.code_scroll.set)
        self.scroll_canvas.configure(xscrollcommand=self.code_scroll_h.set)
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.scroll_canvas.bind('<Leave>', self._unbound_to_mousewheel)

        # create ANOTHER inner frame inside canvas
        self.inner_frame = tk.Frame(self.scroll_canvas)

        # add INNER FRAME to a window in the canvas
        self.scroll_canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

        # contents of code_box_frame frame (contains line numbers and code lines)
        # code line numbers textbox
        self.code_text_lines = tk.Text(self.inner_frame, width=CODE_LINE_TEXT_WIDTH, height=MAX_CODE_LINES, bg="gray60", fg="white", font=("Courier", _code_text_size), wrap="none")
        self.code_text_lines['yscrollcommand'] = self.code_scroll.set
        self.code_text_lines.grid(column=0, row=0, padx=(0, 5))
        # fill line numbers textbox
        self.populate_line_numbers(MAX_CODE_LINES)
        # lock line text
        self.code_text_lines.configure(state="disabled")

        # code text box
        self.code_text = tk.Text(self.inner_frame, width=CODE_WINDOW_WIDTH, height=MAX_CODE_LINES, font=("Courier", _code_text_size), wrap="none")
        self.code_text['yscrollcommand'] = self.code_scroll.set
        self.code_text.grid(column=1, row=0)

        # code file path label
        self.file_path_title = ttk.Label(self, text="File Path: ", style="CodeWindow.TLabel")
        self.file_path_title.grid(column=0, row=2, sticky="W")
        self.file_path_label = ttk.Label(self, textvariable=self.file_path, style="CodeWindow.TLabel")
        self.file_path_label.grid(column=1, row=2, sticky="EW")
        

        # display code in textbox
        self.update_code_editor_display()


    # CodeDisplayFrame methods

    # display code in textbox
    def update_code_editor_display(self, new_code_text=None):
        # initialise text
        text_to_clip = ""

        # if new code text given
        if new_code_text != None:
            text_to_clip = new_code_text

        # if no new code text given
        else:
            # get existing text from code editor
            text_to_clip = self._clipped_code_text(self.code_text.get(1.0, tk.END))

        # clip code
        clipped_code_text = self._clipped_code_text(text_to_clip)
        # clear text box
        self.code_text.delete(1.0, tk.END)
        # add clipped text back to code editor textbox
        self.code_text.insert(1.0, clipped_code_text)

    # keep code to within the MAX_CODE_LINES size
    def _clipped_code_text(self, text):
        delimeter = '\n'
        line_list = text.splitlines()
        return delimeter.join(line_list[0:MAX_CODE_LINES])

    # create the line numbers for the code editor display
    def populate_line_numbers(self, max_code_lines):
        for line in range(max_code_lines):
            if line < 9:
                self.code_text_lines.insert(tk.END, f"  {line + 1}\n")
            elif line < 99:
                self.code_text_lines.insert(tk.END, f" {line + 1}\n")
            elif line < 999:
                self.code_text_lines.insert(tk.END, f"{line + 1}\n")

    
    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bound_to_mousewheel(self, event):
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.scroll_canvas.unbind_all("<MouseWheel>")
