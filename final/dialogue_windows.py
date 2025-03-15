from tkinter import *
import tkinter as tk
from tkinter import ttk, font

class ConfigureText(tk.Toplevel):
    def __init__(self, parent):
        self.available_fonts = sorted(font.families())
        super().__init__(parent)
        self.title("Insert text")
        self.geometry("400x200")
        self.styles = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
        self.values = None
        self.initial_font = tk.StringVar(value='Arial')

        styles_frame = Frame(self, height=100, width=100, relief=SUNKEN, borderwidth=3)
        italic_check = tk.Checkbutton(styles_frame, text="Italic", variable=self.styles[0])
        italic_check.grid(row=0, column=0, sticky="w", padx=15)
        bold_check = tk.Checkbutton(styles_frame, text="Bold", variable=self.styles[1])
        bold_check.grid(row=1, column=0, sticky="w", padx=15)
        underline_check = tk.Checkbutton(styles_frame, text="Underline", variable=self.styles[2])
        underline_check.grid(row=2, column=0, sticky="w", padx=15)
        strikethrough_check = tk.Checkbutton(styles_frame, text="Strikethrough", variable=self.styles[3])
        strikethrough_check.grid(row=3, column=0, sticky="w", padx=15)
        styles_frame.grid(row=0, column=0, pady=5)

        font_frame = Frame(self, height=30, width=100)
        font_label = Label(font_frame, text="Font")
        font_label.grid(row=0, column=0)
        font_family_dropdown = ttk.Combobox(font_frame, width=25, textvariable=self.initial_font, values=self.available_fonts, state="readonly")
        font_family_dropdown.grid(row=1, column=0)
        font_frame.grid(row=0, column=1)

        insert_text_label = Label(self, text="Text")
        insert_text_label.grid(row=1, column=0, columnspan=2)
        insert_text_field = Entry(self, font=("Arial", 12), width=40)
        insert_text_field.grid(row=2, column=0, columnspan=2, padx=15)

        apply_button = Button(self, text="Apply", width=10, command=lambda: _apply())
        apply_button.grid(row=3, column=0, columnspan=2, pady=10)

        def _apply():
            self.values = [insert_text_field.get(), font_family_dropdown.get(), map(lambda e: BooleanVar.get(e), self.styles)]
            self.destroy()

class ToolSize(tk.Toplevel):
    def __init__(self, parent, init_value):
        super().__init__(parent)
        self.title("Select Tool Size")
        self.geometry("400x100")
        self.value = init_value

        brush_size_label = Label(self, text="Tool Size")
        brush_size_label.pack()

        brush_size_slider = Scale(self, length=250, from_=1, to=25, orient=HORIZONTAL)
        brush_size_slider.set(self.value)
        brush_size_slider.pack()

        apply_button = Button(self, text="Apply", width=10, command=lambda: _apply())
        apply_button.pack()

        def _apply():
            self.value = brush_size_slider.get()
            self.destroy()
    