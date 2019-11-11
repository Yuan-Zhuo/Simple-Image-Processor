import tkinter as tk


class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('parameter configuration')

        self.parent = parent

        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='size: ', width=8).pack(side=tk.LEFT)
        self.size_var = tk.StringVar()
        tk.Entry(row1, textvariable=self.size_var, width=20).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='sigma: ', width=8).pack(side=tk.LEFT)
        self.sigma_var = tk.IntVar()
        tk.Entry(row2, textvariable=self.sigma_var,
                 width=20).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="cancel", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="ok", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        try:
            parm = (self.size_var.get(), self.sigma_var.get())
        except:
            pass
        else:
            self.parent.parm = parm
        finally:
            self.destroy()

    def cancel(self):
        self.destroy()
