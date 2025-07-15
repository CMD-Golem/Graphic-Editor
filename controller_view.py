import tkinter as tk
from tkinter import messagebox
from shapes import *
from observer import *
from tree_view import *


class Controller(Observer):
	def __init__(self, model:Model, destroy:Closer):
		super().__init__()
		self.destroy = destroy
		self.model: Model = model

		model.attach(self) # Wird im Observer Pattern an das Subjekt "model" angehängt
		destroy.attach(self)

		self.window = tk.Tk()
		self.window.title("Controller View")
		self.window.geometry("450x380")
		self.window.resizable(True, False)
		self.window.protocol("WM_DELETE_WINDOW", self.destroy.destroy)
		self.window.columnconfigure(1, weight=1)
		self.window.rowconfigure(0, weight=1)

		settings = tk.LabelFrame(self.window, text="Update and add figures")
		self.label = tk.Label(settings, text="")
		self.label.pack(fill=tk.X, expand=True)

		frame = tk.Frame(settings)
		frame.columnconfigure(1, weight=1)
		self.x = self.labeledEntry(frame, "X", 0)
		self.y = self.labeledEntry(frame, "Y", 1)
		self.w = self.labeledEntry(frame, "W/R", 2)
		self.h = self.labeledEntry(frame, "H", 3)
		self.color = self.labeledEntry(frame, "Color", 4)
		frame.pack(fill=tk.X, expand=True, padx=8)
		
		b1 = tk.Button(settings, text="Update Selected Figure", command=self.modify)
		b2 = tk.Button(settings, text="Create Rectangle", command=self.addRectangle)
		b3 = tk.Button(settings, text="Create Circle", command=self.addCircle)
		b4 = tk.Button(settings, text="Create Group", command=self.addGroup)
		b5 = tk.Button(settings, text="Delete Selected Figure", command=self.delete)
		b1.pack(fill=tk.X, expand=True, padx=8, pady=5)
		b2.pack(fill=tk.X, expand=True, padx=8, pady=5)
		b3.pack(fill=tk.X, expand=True, padx=8, pady=5)
		b4.pack(fill=tk.X, expand=True, padx=8, pady=5)
		b5.pack(fill=tk.X, expand=True, padx=8, pady=5)

		settings.grid(row=0, column=1, sticky=tk.NSEW)

	# Hilfsfunktion um Entries zu kreieren
	def labeledEntry(self, parent:tk.Frame, label_text:str, i:int):
		label = tk.Label(parent, text=label_text)
		entry = tk.Entry(parent)
		label.grid(row=i, column=0, pady=5)
		entry.grid(row=i, column=1, sticky=tk.NSEW, pady=5)
		return entry

	def run(self):
		self.model.notify_observers(None) # Alle Views werden zum ersten mal geupdated
		self.window.mainloop()

	def update(self, selected_id:int):
		# Alles zuerst rauslöschen
		self.x.delete(0, tk.END)
		self.y.delete(0, tk.END)
		self.w.delete(0, tk.END)
		self.h.delete(0, tk.END)
		self.color.delete(0, tk.END)
		self.label["text"] = ""

		# Wenn nichts ausgewählt ist, Methode wird abgebrochen
		if selected_id == None:
			return
		
		selected = self.model.selected_figure # Model übergibt aktuell selektierte Figur
		self.label["text"] = selected
		self.x.insert(0, selected.getX())
		self.y.insert(0, selected.getY())

		if isinstance(selected, Rectangle):
			self.w.insert(0, selected.width)
			self.h.insert(0, selected.height)
			self.color.insert(0, selected.color)

		elif isinstance(selected, Circle):
			self.w.insert(0, selected.radius)
			self.color.insert(0, selected.color)

	# Hilfsfunktionen um Figuren der jeweiligen Gruppe hinzu zufügen
	def addFigure(self, figure:Figure):
		selected = self.model.selected_figure

		# Messagebox als Fehlermeldung an Nutzer, wenn nichts ausgewählt ist
		if selected == None:
			messagebox.showinfo(self.window, message="Please select a figure to insert a new figure")
			return
		if not isinstance(selected, Group):
			selected = selected.parent

		selected.add(figure)
		self.model.notify_observers(selected.id)

	def getFigure(self):
		x = int(self.x.get() or 0)
		y = int(self.y.get() or 0)
		return (x, y)
	
	def getRectangle(self):
		x, y = self.getFigure()
		w = int(self.w.get() or 1)
		h = int(self.h.get() or 1)
		c = self.color.get() or "black"
		return x, y, w, h, c
	
	def getCircle(self):
		x, y = self.getFigure()
		r = int(self.w.get() or 1)
		c = self.color.get() or "black"
		return x, y, r, c 

	# für Button: "modify"
	def modify(self):
		selected = self.model.selected_figure

		# Messagebox als Fehlermeldung an Nutzer, wenn nichts ausgewählt ist
		if selected == None:
			messagebox.showinfo(self.window, message="Please select the figure to modify")
			return
		if isinstance(selected, Rectangle):
			selected.rel_x, selected.rel_y, selected.width, selected.height, selected.color = self.getRectangle()
		elif isinstance(selected, Circle):
			selected.rel_x, selected.rel_y, selected.radius, selected.color = self.getCircle()
		else:
			selected.rel_x, selected.rel_y, = self.getFigure()

		self.model.notify_observers(selected.id)
	
	# für Button: "Add Rectangle"
	def addRectangle(self):
		x, y, w, h, c = self.getRectangle()
		self.addFigure(Rectangle(x, y, w, h, c))
	
	# für Button: "Add Circle"
	def addCircle(self):
		x, y, r, c = self.getCircle()
		self.addFigure(Circle(x, y, r, c))

	#für Button: "Add Group"
	def addGroup(self):
		x, y = self.getFigure()
		self.addFigure(Group(x, y))

	def delete(self):
		# Messagebox als Fehlermeldung an Nutzer, wenn nichts ausgewählt ist
		if self.model.selected_figure == None:
			messagebox.showinfo(self.window, message="Please select the figure to delete")
			return

		self.model.selected_figure.delete()
		self.model.notify_observers(None)