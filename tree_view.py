from observer import *
import tkinter as tk
from tkinter import ttk
from shapes import *

class Tree(Observer):
	def __init__(self, model:Model, destroy:Closer):
		super().__init__()
		self.destroy = destroy
		self.model = model
		
		model.attach(self) # Wird im Observer Pattern an das Subjekt "model" angehängt
		destroy.attach(self)

		self.window = tk.Tk()
		self.window.title("Tree View")
		self.window.geometry("600x300")
		self.window.resizable(True, True)
		self.window.protocol("WM_DELETE_WINDOW", self.destroy.destroy)

		self.window.columnconfigure(0, weight=1)
		self.window.rowconfigure(0, weight=1)
		
		self.treeview = ttk.Treeview(self.window, columns=("id"), show="tree") # show tree zeigt nur tree an -> header row wird ausgeblendet
		self.treeview["displaycolumns"] = () # Blendet IDs im Treeview aus
		self.treeview.bind("<Button-1>", self.getSelection)
		self.treeview.grid(column=0, row=0, sticky=tk.NSEW)

        # Scrollbar
		vbar = tk.Scrollbar(self.window,orient=tk.VERTICAL, command=self.treeview.yview)
		self.treeview.configure(yscrollcommand=vbar.set)
		vbar.grid(column=1, row=0, sticky=tk.NS)

	def run(self):
		self.window.mainloop()

	def getSelection(self, event):
		# Findet angeklickte Zeile
		item = self.treeview.identify_row(event.y)
		
		self.model.root.deselect()

		if item:
			selected_id = self.treeview.item(item, "values")[0] # ID ist in der nullten Stelle von Values abgespeichert
			self.model.setSelection(int(selected_id))
		else:
			self.model.setSelection(None)

	def update(self, selected_id:int):
		# lädt daten ins treeview
		self.treeview.delete(*self.treeview.get_children())
		self.model.root.treeRecursive("", self.treeview)
		
		for item in self.getAllChildren():
			# klappt alles aus
			self.treeview.item(item, open=True)

			# wählt ID aus
			current_id = self.treeview.item(item, "values")[0]
			if selected_id == int(current_id):
				self.treeview.selection_set(item)

	def getAllChildren(self, parent=""):
		# Erstellt bei jedem Aufruf eine neue leere Liste
		children = []

		for child in self.treeview.get_children(parent):
			children.append(child)

			# Erweitert aktuelle Liste mit allen Kindern durch rekursives Aufrufen
			children.extend(self.getAllChildren(child))

		return children
		
		


