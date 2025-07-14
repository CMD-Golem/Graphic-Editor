from observer import *
import tkinter as tk
from tkinter import ttk

class Tree(Observer):
    def __init__(self, model:Model, destroy:Closer):
        super().__init__()
        self.destroy = destroy
        self.model: Model = model
        model.attach(self)
        destroy.attach(self)
        
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.destroy.destroy)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        self.treeview = ttk.Treeview(self.window, columns=("pos","size","color","id"))
        self.treeview.heading("#0", text="name")
        self.treeview.heading("pos", text="Position")
        self.treeview.heading("size", text="Size")
        self.treeview.heading("color", text="Color")
        self.treeview.heading("id", text="ID")
        self.treeview.grid(row=0, column=0, sticky="NESW")

    def run(self):
        self.window.mainloop()
        
    def update(self):
        pass
