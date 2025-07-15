from __future__ import annotations # macht rekursive Typen tipps möglich
from abc import ABC, abstractmethod

import tkinter as tk

# Component
class Figure(ABC):
	id_counter = 0 # Klassenatribut, gilt global für ganzes Programm

	@classmethod
	def generateId(cls):
		cls.id_counter += 1
		return cls.id_counter

	def __init__(self, x:int, y:int, col:str):
		self.rel_x = x
		self.rel_y = y
		self.color = col
		self.id = Figure.generateId()
		self.parent = None
		self.border = 2
		self.selected = False

	def __str__(self):
		return f"(x {self.getX()}, y {self.getY()}, w {self.getBoundingBoxWidth()}, h {self.getBoundingBoxHeight()}), (abs: x {self.getAbsX()}, y {self.getAbsY()}), col:{self.color}"

	def set_parent(self, parent:Figure):
		self.parent = parent

	def delete(self):
		if self.parent:
			self.parent.figures.remove(self)

	def getX(self):
		return self.rel_x
	
	def getY(self):
		return self.rel_y

	def getAbsX(self):
		if self.parent:
			return self.parent.getAbsX() + self.getX()
		else:
			return self.getX()

	def getAbsY(self):
		if self.parent:
			return self.parent.getAbsY() + self.getY()
		else:
			return self.getY()
	
	@abstractmethod
	def getBoundingBoxWidth(self):
		pass

	@abstractmethod
	def getBoundingBoxHeight(self):
		pass
		
	def strRecursive(self, level:int):
		print(level * "    ", self)

	def treeRecursive(self, parent, treeview):
		text = self.__str__()
		return treeview.insert(parent, tk.END, text=text, values=self.id)

	def findFigure(self, selected_id:int):
		if selected_id == self.id:
			return self
		else:
			return False
		
	def deselect(self):
		self.selected = False
		
	@abstractmethod
	def draw(self):
		pass

# Composite
class Group(Figure):
	def __init__(self, x:int=0, y:int=0):
		super().__init__(x, y, "magenta")
		self.figures: list[Figure] = []

	def __str__(self):
		return f"Group: {super().__str__()}"
	
	def add(self, figure:Figure):
		figure.set_parent(self)
		self.figures.append(figure)

	def getBoundingBoxX(self):
		# Sucht Komponente am weitesten links
		x = 0
		for figure in self.figures:
			figure_x = figure.getX()
			if (figure_x < x):
				x = figure_x

		return self.getAbsX() + x

	def getBoundingBoxY(self):
		# Sucht Komponente am weitesten oben
		y = 0
		for figure in self.figures:
			figure_y = figure.getY()
			if (figure_y < y):
				y = figure_y

		return self.getAbsY() + y

	def getBoundingBoxWidth(self):
		# Sucht weiteste linke und weiteste rechte Komponente
		leftmost = 0
		rightmost = 0
		for figure in self.figures:
			figure_left = figure.getX()
			figure_right = figure_left + figure.getBoundingBoxWidth()

			if (figure_left < leftmost):
				leftmost = figure_left
			if (figure_right > rightmost):
				rightmost = figure_right

		return rightmost - leftmost

	def getBoundingBoxHeight(self):
		# Sucht tiefste und höchste Komponente
		highest = 0
		lowest = 0
		for figure in self.figures:
			figure_top = figure.getY()
			figure_bottom = figure_top + figure.getBoundingBoxHeight()

			if (figure_top < highest):
				highest = figure_top
			if (figure_bottom > lowest):
				lowest = figure_bottom

		return lowest - highest
	
	def strRecursive(self, level:int=0):
		super().strRecursive(level)
		level += 1
		for figure in self.figures:
			figure.strRecursive(level)

	def treeRecursive(self, parent, treeview):
		new_parent = super().treeRecursive(parent, treeview)

		for figure in self.figures:
			figure.treeRecursive(new_parent, treeview)

	def findFigure(self, selected_id:int):
		if selected_id == self.id:
			return self
		
		for figure in self.figures:
			found_figure = figure.findFigure(selected_id)
			if not(found_figure == False):
				return found_figure
		
		# Gibt False zurück wenn nichts gefunden wird
		return False
	
	def deselect(self):
		super().deselect()

		for figure in self.figures:
			figure.deselect()
	
	def draw(self, canvas:tk.Canvas):
		x = self.getBoundingBoxX() 
		y = self.getBoundingBoxY() 
		w = self.getBoundingBoxWidth()
		h = self.getBoundingBoxHeight()
		canvas.create_rectangle(x, y, x+w, y+h, outline=self.color, dash=(50), fill='', width=self.border, tags=(f"figure_{self.id}", self.id)) # tag als Tupel mit zwei Werten, erster für ID Suche, zweiter um ID auszulesen

		for figure in self.figures:
			figure.draw(canvas)

class Rectangle(Figure):
	def __init__(self, x:int=0, y:int=0, width:int=1, height:int=1, color:str="black"):
		super().__init__(x, y, color)
		self.width = width
		self.height = height

	def __str__(self):
		return f"Rectangle: {super().__str__()}, (w: {self.width}, h: {self.height})"
	
	def getBoundingBoxWidth(self):
		return self.width
		
	def getBoundingBoxHeight(self):
		return self.height
	
	def draw(self, canvas:tk.Canvas):
		x = self.getAbsX()
		y = self.getAbsY()
		w = self.getBoundingBoxWidth()
		h = self.getBoundingBoxHeight()
		canvas.create_rectangle(x, y, x+w, y+h, outline=self.color, width=self.border, fill='', tags=(f"figure_{self.id}", self.id)) # tag als Tupel mit zwei Werten, erster für ID Suche, zweiter um ID auszulesen

class Circle(Figure):
	def __init__(self, x:int=0, y:int=0, radius:int=1, color:str="black"):
		super().__init__(x, y, color)
		self.radius = radius

	def __str__(self):
		return f"Circle: {super().__str__()}, r: {self.radius}"
	
	def getBoundingBoxWidth(self):
		return 2* self.radius
		
	def getBoundingBoxHeight(self):
		return 2* self.radius
	
	def draw(self, canvas:tk.Canvas):
		x = self.getAbsX()
		y = self.getAbsY()
		w = self.getBoundingBoxWidth()
		h = self.getBoundingBoxHeight()
		canvas.create_oval(x, y, x+w, y+h, outline=self.color, width=self.border, fill='', tags=(f"figure_{self.id}", self.id)) # tag als Tupel mit zwei Werten, erster für ID Suche, zweiter um ID auszulesen