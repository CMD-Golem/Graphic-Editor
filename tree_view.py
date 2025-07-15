from observer import *
import tkinter as tk
from tkinter import ttk
from shapes import *

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
        
        self.treeview = ttk.Treeview(self.window, columns=("id"))
        self.treeview.grid(row=0, column=0, sticky="NESW")

        self.treeview.bind("<Double-1>", self.getSelection)

    def run(self):
        self.window.mainloop()

    def getSelection(self, event):
        selected = self.treeview.selection()
        self.deselect()

        if len(selected) >= 1:
            id = self.treeview.item(selected[0], "values")[0]

            self.model.setSelection(int(id))

    def deselect(self):
        if len(self.treeview.selection()) > 0:
            self.treeview.selection_remove(self.treeview.selection()[0])
        self.model.root.deselect()

    def update(self, selected_id):
        self.model.root.treeRecursive("", self.treeview) #lädt daten ins treeview

        #klappt alles aus
        for item in self.treeview.get_children():
            self.treeview.item(item, open=True)

        #wählt ID aus
        if selected_id != None:
            for item in self.treeview.get_children(): 
                current_id = self.treeview.item(item, "values")[0]
                if selected_id == current_id:
                    self.treeview.selection_set(item)
        
        


