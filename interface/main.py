# -*- coding: utf-8 -*-

# Tkinter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font
from PIL import Image, ImageTk, Image
from functools import partial
import os
import numpy as np
import webbrowser

from processing.operators import basic_operator, sobel_operator, prewitt_operator, roberts_operator
from processing.filters import mean_filter, median_filter, gaussian_filter
from interface.opt import OptType
from interface.version import Version
from interface.box import GaussianDialog, CustomizeDialog


class MainINTF:
    def __init__(self):
        self.init_config()
        self.init_sytle()
        self.init_window()
        self.init_widgets()
        self.init_state()

    def __call__(self):
        self.window.mainloop()

    def init_config(self):
        os.chdir('img')
        self.initialdir = os.getcwd()
        os.chdir('..')
        self.filetypes = (('image files', ('*.bmp', '*.jpg', '*.jpeg', '*.png',
                                           '*.gif', '*.tiff', '*.webp')),
                          ('all files', '*'))
        self.parm = None

    def init_sytle(self):
        self.menu_font = ('Comic Sans MS', 10)

    def init_window(self):
        self.window = tk.Tk()
        self.window.title('Simple Raster Graphics Editor')
        self.window.geometry('800x400')
        self.window.minsize(400, 200)
        self.window.resizable(0, 0)
        self.window.iconbitmap('./img/title.ico')

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

        self.operation_menu.add_command(label='mean filter',
                                        command=partial(
                                            self.edit_img,
                                            OptType.MEAN_FILTER))
        self.operation_menu.add_command(label='median filter',
                                        command=partial(
                                            self.edit_img,
                                            OptType.MEDIAN_FILTER))
        self.operation_menu.add_command(label='gaussian filter',
                                        command=partial(
                                            self.edit_img,
                                            OptType.GAUSSIAN_FILTER))
        self.operation_menu.add_command(label='sobel operator',
                                        command=partial(
                                            self.edit_img,
                                            OptType.SOBEL_OPERATOR))
        self.operation_menu.add_command(label='prewitt operator',
                                        command=partial(
                                            self.edit_img,
                                            OptType.PREWITT_OPERATOR))
        self.operation_menu.add_command(label='roberts operator',
                                        command=partial(
                                            self.edit_img,
                                            OptType.ROBERTS_OPERATOR))
        self.operation_menu.add_command(label='customize operator',
                                        command=partial(
                                            self.edit_img,
                                            OptType.CUSTOMIZE_OPERATOR))

        self.menu.add_cascade(label='operation', menu=self.operation_menu)

        # feedback menu
        self.feedback_menu = tk.Menu(self.menu, tearoff=False)

        self.feedback_menu.add_command(label='github repo',
                                       command=self.display_repo)

        self.menu.add_cascade(label='feedback', menu=self.feedback_menu)

        # image panel
        self.panel = tk.Label(self.window)
        self.panel.pack(side="bottom", fill="both", expand="yes")

        self.config_font(self.file_menu, self.menu_font)
        self.config_font(self.edit_menu, self.menu_font)
        self.config_font(self.operation_menu, self.menu_font)
        self.config_font(self.feedback_menu, self.menu_font)

    def init_state(self):
        self.img = None
        self.version = None

    # handle function
    def config_font(self, widgt, style_tuple):
        style = Font(family=style_tuple[0], size=style_tuple[1])
        widgt.configure(font=style)

    def open_file(self, event=None):
        try:
            filepath = filedialog.askopenfilename(title='Select Image File',
                                                  initialdir=self.initialdir,
                                                  filetypes=self.filetypes)
            img = Image.open(filepath)
            version = Version(img)
        except:
            return
        else:
            self.filepath = filepath
            self.img = img
            self.version = version
            self.load_file()

    def load_file(self):
        if not self.img:
            return

        show_img = ImageTk.PhotoImage(self.version.current_version())
        self.panel.configure(image=show_img)
        self.panel.image = show_img

    def edit_img(self, opt_type):
        if not self.img:
            return

        switcher = {
            OptType.MEAN_FILTER: mean_filter,
            OptType.MEDIAN_FILTER: median_filter,
            OptType.SOBEL_OPERATOR: sobel_operator,
            OptType.PREWITT_OPERATOR: prewitt_operator,
            OptType.ROBERTS_OPERATOR: roberts_operator,
            OptType.CUSTOMIZE_OPERATOR: basic_operator
        }

        try:
            if (opt_type == OptType.GAUSSIAN_FILTER):
                self.parm = (0, 0)
                self.window.wait_window(GaussianDialog(self))
                img_after = gaussian_filter(self.version.current_version(),
                                            self.parm[0], self.parm[1])
            elif (opt_type == OptType.CUSTOMIZE_OPERATOR):
                self.parm = (np.zeros(0), np.zeros(0))
                CustomizeDialog(self)
                img_after = basic_operator(self.version.current_version(),
                                           self.parm[0], self.parm[1])
            else:
                func = switcher.get(opt_type)
                img_after = func(self.version.current_version())
        except:
            return
        else:
            self.version.add(img_after)
            self.load_file()

    def save_file(self, event=None):
        try:
            self.version.current_version().save(self.filepath)
        except:
            return

    def save_file_as(self, event=None):
        try:
            dirname, filename = os.path.split(self.filepath)
            filepath_save_as = filedialog.asksaveasfilename(
                title='save as',
                initialdir=dirname,
                initialfile=filename,
                filetypes=self.filetypes)
            self.version.current_version().save(filepath_save_as)
        except:
            return

    def quit_editor(self, event=None):
        self.window.quit()

    def undo_op(self, event=None):
        try:
            self.version.undo()
        except:
            return
        else:
            self.load_file()

    def redo_op(self, event=None):
        try:
            self.version.redo()
        except:
            return
        else:
            self.load_file()

    def display_repo(self, event=None):
        webbrowser.open("https://github.com/Yuan-Zhuo/Simple-Image-Processor",
                        new=0)
