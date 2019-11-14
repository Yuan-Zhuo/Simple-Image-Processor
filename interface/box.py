import tkinter as tk
from tkinter.font import Font
import numpy as np


# gaussian_filter
class GaussianDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('parameter configuration')
        self.parent = parent
        self.grab_set()

        row1 = tk.Frame(self)
        row1.pack(fill="x")
        label1 = tk.Label(row1, text='size: ', width=10)
        label1.configure(font=Font(family="Times", size=12))
        label1.pack(side=tk.LEFT)
        self.size_var = tk.StringVar()
        tk.Entry(row1, textvariable=self.size_var, width=20).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        label2 = tk.Label(row2, text='sigma: ', width=10)
        label2.configure(font=Font(family="Times", size=12))
        label2.pack(side=tk.LEFT)
        self.sigma_var = tk.IntVar()
        tk.Entry(row2, textvariable=self.sigma_var,
                 width=20).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill="x")

        tk.Button(row3, text="cancel", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="ok", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        try:
            parm = (int(self.size_var.get()), float(self.sigma_var.get()))
        except:
            pass
        else:
            self.parent.parm = parm
        finally:
            self.destroy()

    def cancel(self):
        self.destroy()


# customize_operator
class CustomizeDialog:
    def __init__(self, parent):
        self.parent = parent
        self.size = 0
        self.m1 = []
        self.m2 = []
        self.mm1 = []
        self.mm2 = []

        self.parent.window.wait_window(self.SizeDialog(self))
        self.parent.window.wait_window(self.KernelDialog(self))

        try:
            self.parent.parm = (np.array(self.mm1), np.array(self.mm2))
        except:
            return

    class SizeDialog(tk.Toplevel):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.grab_set()
            self.title('Kernel Size')

            self.sizetext = tk.StringVar()
            lb = tk.Label(self, text='Enter the n:')
            lb.grid(row=0, column=0, padx=5, pady=5)
            ent = tk.Entry(self, width=15, textvariable=self.sizetext)
            ent.grid(row=0, column=1, padx=5, pady=5)
            bnt = tk.Button(self, text='Enter', command=self.get_size)
            bnt.grid(row=1, column=0, columnspan=2, pady=10)

        def get_size(self):
            try:
                size = int(eval(self.sizetext.get()))
            except:
                pass
            else:
                self.parent.size = size
            finally:
                self.destroy()

    class KernelDialog(tk.Toplevel):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            try:
                self.size = self.parent.size
                assert (self.size > 0)
            except:
                self.destroy()

            self.grab_set()
            self.title('Kernel Input')

            for i in range(self.size):
                line = []
                for j in range(self.size):
                    temporarytext1 = tk.StringVar()
                    ent = tk.Entry(self, width=3, textvariable=temporarytext1)
                    ent.grid(row=i, column=j, padx=5, pady=5)
                    line.append(temporarytext1)
                self.parent.m1.append(line)

            lb = tk.Label(self, text='x--y')
            lb.grid(row=self.size // 2, column=self.size, padx=10)

            for i in range(self.size):
                line = []
                for j in range(self.size):
                    temporarytext2 = tk.StringVar()
                    ent = tk.Entry(self, width=3, textvariable=temporarytext2)
                    ent.grid(row=i, column=1 + self.size + j, padx=5, pady=5)
                    line.append(temporarytext2)
                self.parent.m2.append(line)

            btn = tk.Button(self, text='Enter', command=self.get_kernel)
            btn.grid(row=self.size, column=self.size, padx=10)

        def get_kernel(self):
            try:
                mm1 = [[int(j.get()) for j in i] for i in self.parent.m1]
                mm2 = [[int(j.get()) for j in i] for i in self.parent.m2]
            except:
                pass
            else:
                self.parent.mm1 = mm1
                self.parent.mm2 = mm2
            finally:
                self.destroy()
