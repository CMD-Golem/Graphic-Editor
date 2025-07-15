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
        
        self.treeview = ttk.Treeview(self.window, columns=("pos","size","color","id"))
        self.treeview.heading("#0", text="name")
        self.treeview.heading("pos", text="Position")
        self.treeview.heading("size", text="Size")
        self.treeview.heading("color", text="Color")
        self.treeview.heading("id", text="ID")
        self.treeview.grid(row=0, column=0, sticky="NESW")

    def run(self):
        self.window.mainloop()
        
    #hilfsfunktion
    def fill_tree(self, parent_node, figure):
        pos = f"({figure.getX()}, {figure.getY()})"
        #überprüfung des Typs
        if isinstance(figure, (Rectangle, Circle)):
            size = f"({figure.getBoundingBoxWidth()}, {figure.getBoundingBoxHeight()})"
        else:
            size = "---"

        #Einen Eintrag im Treeview erstellen
        node = self.treeview.insert(parent_node, 'end', text=figure.__class__.__name__, values=(pos, size, figure.color, figure.id))

        #Wenn die Figur eine Gruppe ist, ihre Kinder ebenfalls hinzufügen
        if isinstance(figure, Group):
            for child in figure.figures:
                self.fill_tree(node, child)

    def update(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        #Treeview füllen
        self.fill_tree('', self.model.root)
