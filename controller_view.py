import tkinter as tk
from tkinter import ttk
from shapes import *
from observer import *


class Controller(Observer):
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

		settings = tk.LabelFrame(self.window, text="Update and add figures")
		self.label = tk.Label(settings, text="")
		self.label.pack(fill="x", expand=True)

		frame = tk.Frame(settings)
		frame.columnconfigure(1, weight=1)
		self.x = self.labeledEntry(frame, "X", 0)
		self.y = self.labeledEntry(frame, "Y", 1)
		self.w = self.labeledEntry(frame, "W/R", 2)
		self.h = self.labeledEntry(frame, "H", 3)
		self.color = self.labeledEntry(frame, "Color", 4)
		frame.pack(fill="x", expand=True, padx=8)
		
		b1 = tk.Button(settings, text="Update Selected Figure", command=self.modify)
		b2 = tk.Button(settings, text="Create Rectangle", command=self.addRectangle)
		b3 = tk.Button(settings, text="Create Circle", command=self.addCircle)
		b4 = tk.Button(settings, text="Create Composite", command=self.addComposite)
		b1.pack(fill="x", expand=True, padx=8, pady=5)
		b2.pack(fill="x", expand=True, padx=8, pady=5)
		b3.pack(fill="x", expand=True, padx=8, pady=5)
		b4.pack(fill="x", expand=True, padx=8, pady=5)

		settings.grid(row=0, column=1, sticky="NESW")

	def run(self):
		self.window.mainloop()

	def update(self):
		pass

	def labeledEntry(self, parent:tk.Frame, label_text:str, i:int):
		label = tk.Label(parent, text=label_text)
		entry = tk.Entry(parent)
		label.grid(row=i, column=0, pady=5)
		entry.grid(row=i, column=1, sticky="NESW", pady=5)
		return entry
	
	def modify(self):
		pass
	
	def updateComposite(self, component:Component):
		selected = self.treeview.item(self.treeview.focus())
		composite = self.model.get(selected.get("values")[3])

		if not(type(composite, Composite)):
			composite = composite.parent
		
		composite.add_component(component)
		self.model.notify_observers()
	
	def addRectangle(self):
		id = self.model.getNewId()
		x = self.x.get()
		y = self.y.get()
		w = self.w.get()
		h = self.h.get()
		c= self.color.get()
		
		self.updateComposite(Rectangle(x, y, w, h, c, id))
	
	def addCircle(self):
		id = self.model.getNewId()
		x = self.x.get()
		y = self.y.get()
		r = self.w.get()
		c= self.color.get()
		
		self.updateComposite(Circle(x, y, r, c, id))

	def addComposite(self):
		id = self.model.getNewId()
		x = self.x.get()
		y = self.y.get()
		
		self.updateComposite(Composite(x, y, id))