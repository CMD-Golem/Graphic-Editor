import tkinter as tk
from tkinter import ttk
from shapes import *
from observer import *
from tree_view import *


class Controller(Observer):
	def __init__(self, model:Model, destroy:Closer):
		super().__init__()
		self.destroy = destroy
		self.model: Model = model
		model.attach(self)
		destroy.attach(self)

		self.window = tk.Tk()
		self.window.configure(width=400, height=400)
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
		b4 = tk.Button(settings, text="Create Group", command=self.addGroup)
		b1.pack(fill="x", expand=True, padx=8, pady=5)
		b2.pack(fill="x", expand=True, padx=8, pady=5)
		b3.pack(fill="x", expand=True, padx=8, pady=5)
		b4.pack(fill="x", expand=True, padx=8, pady=5)

		settings.grid(row=0, column=1, sticky="NESW")

	#Hilfsfunktion um Entries zu kreieren
	def labeledEntry(self, parent:tk.Frame, label_text:str, i:int):
		label = tk.Label(parent, text=label_text)
		entry = tk.Entry(parent)
		label.grid(row=i, column=0, pady=5)
		entry.grid(row=i, column=1, sticky="NESW", pady=5)
		return entry

	def run(self):
		self.window.mainloop()

	def update(self, selected_id):
		if selected_id == None:
			return
		
		selected = self.model.selected_figure

		self.x.delete(0, tk.END)
		self.y.delete(0, tk.END)
		self.w.delete(0, tk.END)
		self.h.delete(0, tk.END)
		self.color.delete(0, tk.END)

		self.x.insert(0, selected.getX())
		self.y.insert(0, selected.getY())

		#print(type(selected), selected)

		if isinstance(selected, Rectangle):
			self.w.insert(0, selected.width)
			self.h.insert(0, selected.height)
			self.color.insert(0, selected.color)

		elif isinstance(selected, Circle):
			self.w.insert(0, selected.radius)
			self.color.insert(0, selected.color)

	#Hilfsfunktion um Figuren der jeweiligen Gruppe hinzu zufügen
	def addFigure(self, figure):
		selected = self.model.selected_figure

		if not isinstance(selected, Group):
			selected = selected.parent

		selected.add(figure)

		self.model.notify_observers(None)

	#für Button: "modify"
	def modify(self):
		selected = self.model.selected_figure
		selected.x = self.x
		selected.y = self.y

		if isinstance(selected, Rectangle):
			selected.width = self.w
			selected.height = self.h
			selected.color = self.color

		elif isinstance(selected, Circle):
			selected.radius = self.w
			selected.color = self.color

		self.model.notify_observers(None)
	
	#für Button: "Add Rectangle"
	def addRectangle(self):
		x = self.x.get()
		y = self.y.get()
		w = self.w.get()
		h = self.h.get()
		c= self.color.get()
		
		self.addFigure(Rectangle(x, y, w, h, c))
	
	#für Button: "Add Circle"
	def addCircle(self):
		x = self.x.get()
		y = self.y.get()
		r = self.w.get()
		c= self.color.get()
		
		self.addFigure(Circle(x, y, r, c))

	#für Button: "Add Group"
	def addGroup(self):
		x = self.x.get()
		y = self.y.get()
		
		self.addFigure(Group(x, y))