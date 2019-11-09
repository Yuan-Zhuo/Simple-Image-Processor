# -*- coding: utf-8 -*-

# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image


class MainINTF:
    def __init__(self):
        self.init_config()
        self.init_window()
        self.init_widgets()

    def __call__(self):
        self.window.mainloop()

    def init_config(self):
        self.initialdir = "/"
        self.filetypes = (('image files', ('*.bmp', '*.jpg', '*.jpeg', '*.png',
                                           '*.gif', '*.tiff', '*.webp')),
                          ('all files', '*'))

    def init_window(self):
        self.window = tk.Tk()
        self.window.title('Simple Raster Graphics Editor')
        self.window.geometry('800x400')
        self.window.minsize(400, 200)

    def init_widgets(self):
        # main menu
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)

        # file menu
        self.file_menu = tk.Menu(self.menu, tearoff=False)

        self.file_menu.add_command(label='open',
                                   command=self.open_file,
                                   accelerator='Ctrl+O')
        self.window.bind('<Control-o>', self.open_file)
        self.file_menu.add_command(label='save',
                                   command=self.save_file,
                                   accelerator='Ctrl+S')
        self.window.bind('<Control-s>', self.save_file)
        self.file_menu.add_command(label='save as', command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='exit',
                                   command=self.quit_editor,
                                   accelerator='Alt+F4')

        self.menu.add_cascade(label='file', menu=self.file_menu)

        # edit menu
        self.edit_menu = tk.Menu(self.menu, tearoff=False)

        self.edit_menu.add_command(label='undo',
                                   command=self.undo_op,
                                   accelerator='Ctrl+Z')
        self.window.bind('<Control-z>', self.undo_op)
        self.edit_menu.add_command(label='redo',
                                   command=self.redo_op,
                                   accelerator='Ctrl+Y')
        self.window.bind('<Control-y>', self.redo_op)

        self.menu.add_cascade(label='edit', menu=self.edit_menu)

        # operation menu
        self.operation_menu = tk.Menu(self.menu, tearoff=False)

        self.menu.add_cascade(label='operation', menu=self.operation_menu)

        # feedback menu
        self.feedback_menu = tk.Menu(self.menu, tearoff=False)

        self.feedback_menu.add_command(label='github repo',
                                       command=self.display_repo)

        self.menu.add_cascade(label='feedback', menu=self.feedback_menu)

    # handle function
    def open_file(self, event=None):
        filepath = filedialog.askopenfilename(title='Select Image File',
                                              initialdir=self.initialdir,
                                              filetypes=self.filetypes)

    def save_file(self):
        pass

    def save_file_as(self):
        pass

    def quit_editor(self):
        pass

    def undo_op(self):
        pass

    def redo_op(self):
        pass

    def display_repo(self):
        pass


if __name__ == '__main__':
    edt = MainINTF()
    edt()
