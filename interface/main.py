# -*- coding: utf-8 -*-

# Tkinter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font
from PIL import Image, ImageTk
from functools import partial
import os
import numpy as np
import webbrowser
import base64

from processing.operators import basic_operator, sobel_operator, prewitt_operator, roberts_operator
from processing.filters import mean_filter, median_filter, gaussian_filter
from interface.opt_type import *
from interface.version import Version
from interface.box import GaussianDialog, CustomizeDialog
from interface.icon import icon_img


class MainINTF:
    def __init__(self):
        self.init_config()
        self.init_sytle()
        self.init_window()
        self.init_icon()
        self.init_widgets()
        self.init_state()

    def __call__(self):
        self.window.mainloop()

    def init_config(self):
        try:
            os.chdir('img')
            initialdir = os.getcwd()
            os.chdir('..')
        except:
            initialdir = os.getcwd()
        finally:
            self.initialdir = initialdir

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

    def init_icon(self):
        tmp = open("temp.ico", "wb+")
        tmp.write(base64.b64decode(icon_img))
        tmp.close()
        self.window.iconbitmap("temp.ico")
        os.remove("temp.ico")

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
                                            self.edit_img_convolution,
                                            ConvolutionOptType.MEAN_FILTER))
        self.operation_menu.add_command(label='median filter',
                                        command=partial(
                                            self.edit_img_convolution,
                                            ConvolutionOptType.MEDIAN_FILTER))
        self.operation_menu.add_command(
            label='gaussian filter',
            command=partial(self.edit_img_convolution,
                            ConvolutionOptType.GAUSSIAN_FILTER))
        self.operation_menu.add_command(label='sobel operator',
                                        command=partial(
                                            self.edit_img_convolution,
                                            ConvolutionOptType.SOBEL_OPERATOR))
        self.operation_menu.add_command(
            label='prewitt operator',
            command=partial(self.edit_img_convolution,
                            ConvolutionOptType.PREWITT_OPERATOR))
        self.operation_menu.add_command(
            label='roberts operator',
            command=partial(self.edit_img_convolution,
                            ConvolutionOptType.ROBERTS_OPERATOR))
        self.operation_menu.add_command(
            label='customize operator',
            command=partial(self.edit_img_convolution,
                            ConvolutionOptType.CUSTOMIZE_OPERATOR))

        # binary morph operation menu
        self.morph_binary_menu = tk.Menu(self.operation_menu, tearoff=False)

        # edge detection
        self.edge_detection_submenu = tk.Menu(self.morph_binary_menu,
                                              tearoff=False)

        self.edge_detection_submenu.add_command(label='standard', command=None)
        self.edge_detection_submenu.add_command(label='internal', command=None)
        self.edge_detection_submenu.add_command(label='external', command=None)

        self.morph_binary_menu.add_cascade(label='Edge Detection',
                                           menu=self.edge_detection_submenu)

        # reconstruction(binary)
        self.reconstruction_binary_submenu = tk.Menu(self.morph_binary_menu,
                                                     tearoff=False)

        self.reconstruction_binary_submenu.add_command(
            label='conditional dilation', command=None)
        self.reconstruction_binary_submenu.add_command(
            label='conditional erosion', command=None)

        self.morph_binary_menu.add_cascade(
            label='Reconstruction', menu=self.reconstruction_binary_submenu)

        self.operation_menu.add_cascade(label='Binary Morphological',
                                        menu=self.morph_binary_menu)

        # grayscale morph operation menu
        self.morph_grayscale_menu = tk.Menu(self.operation_menu, tearoff=False)

        # reconstruction(grayscale)
        self.reconstruction_grayscale_submenu = tk.Menu(
            self.morph_grayscale_menu, tearoff=False)

        self.reconstruction_grayscale_submenu.add_command(
            label='geodesic dilation', command=None)
        self.reconstruction_grayscale_submenu.add_command(
            label='geodesic erosion', command=None)
        self.reconstruction_grayscale_submenu.add_command(
            label='open operation', command=None)
        self.reconstruction_grayscale_submenu.add_command(
            label='close operation', command=None)

        self.morph_grayscale_menu.add_cascade(
            label='Reconstruction', menu=self.reconstruction_grayscale_submenu)

        # gradient
        self.gradient_submenu = tk.Menu(self.morph_grayscale_menu,
                                        tearoff=False)

        self.gradient_submenu.add_command(label='standard', command=None)
        self.gradient_submenu.add_command(label='external', command=None)
        self.gradient_submenu.add_command(label='internal', command=None)

        self.morph_grayscale_menu.add_cascade(label='Gradient',
                                              menu=self.gradient_submenu)

        self.operation_menu.add_cascade(label='Grayscale Morphological',
                                        menu=self.morph_grayscale_menu)

        self.menu.add_cascade(label='operation', menu=self.operation_menu)

        # feedback menu
        self.feedback_menu = tk.Menu(self.menu, tearoff=False)

        self.feedback_menu.add_command(label='github repo',
                                       command=self.display_repo)

        self.menu.add_cascade(label='feedback', menu=self.feedback_menu)

        # image panel
        self.panel = tk.Label(self.window)
        self.panel.pack(fill=tk.BOTH, expand=1)
        self.panel.bind('<Configure>', self.load_file)

        # status bar
        self.status_bar = tk.Label(self.window,
                                   text='ready',
                                   bd=1,
                                   relief=tk.SUNKEN,
                                   anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.config_font(self.file_menu, self.menu_font)
        self.config_font(self.edit_menu, self.menu_font)
        self.config_font(self.operation_menu, self.menu_font)
        self.config_font(self.feedback_menu, self.menu_font)

    def init_state(self):
        self.img = None
        self.version = None

    # handle function
    def resize_img(self, w_box, h_box, pil_image):
        w, h = pil_image.size
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def update_status_bar(self):
        try:
            width, height = self.img.size
            flag = False
            for i in range(width):
                for j in range(height):
                    r, g, b = self.img.getpixel((i, j))
                    if r != g != b:
                        flag = True
                        break
        except:
            self.status_bar.config(text='ready')
        else:
            self.status_bar.config(
                text='ready\tsize:({}, {})\tmode: {}'.format(
                    width, height, 'RGB' if flag else 'GRAY'))

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
            self.update_status_bar()

    def load_file(self, event=None):
        if not self.img:
            return
        try:
            show_img = self.version.current_version()
            max_width = self.window.winfo_width() * 0.8
            max_height = self.window.winfo_height() * 0.8

            show_img_resized = ImageTk.PhotoImage(
                self.resize_img(max_width, max_height, show_img))
        except:
            return
        else:
            self.panel.configure(image=show_img_resized)
            self.panel.image = show_img_resized

    def edit_img_convolution(self, opt_type):
        if not self.img:
            return

        switcher = {
            ConvolutionOptType.MEAN_FILTER: mean_filter,
            ConvolutionOptType.MEDIAN_FILTER: median_filter,
            ConvolutionOptType.SOBEL_OPERATOR: sobel_operator,
            ConvolutionOptType.PREWITT_OPERATOR: prewitt_operator,
            ConvolutionOptType.ROBERTS_OPERATOR: roberts_operator,
            ConvolutionOptType.CUSTOMIZE_OPERATOR: basic_operator
        }

        try:
            if (opt_type == ConvolutionOptType.GAUSSIAN_FILTER):
                self.parm = (0, 0)
                self.window.wait_window(GaussianDialog(self))
                img_after = gaussian_filter(self.version.current_version(),
                                            self.parm[0], self.parm[1])
            elif (opt_type == ConvolutionOptType.CUSTOMIZE_OPERATOR):
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
