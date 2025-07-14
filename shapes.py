from __future__ import annotations # make recursive type hint possible
from abc import ABC, abstractmethod

import tkinter as tk

# Component
class Figure(ABC):
	def __init__(self, x:int, y:int, col:str):
		self.rel_x = x
		self.rel_y = y
		self.color = col
		self.id = None
		self.parent = None
		self.border = 2
		self.selected = False

	def __str__(self):
		return f"(x {self.getX()}, y {self.getY()}, w {self.getBoundingBoxWidth()}, h {self.getBoundingBoxHeight()}), (abs: x {self.getAbsX()}, y {self.getAbsY()}), col:{self.color}"

	def set_parent(self, parent:Figure):
		self.parent = parent

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
		return treeview.insert(parent, tk.END, text=text, values=(self.id))

	def findId(self, id:int):
		if id == self.id:
			return self
		else:
			return False
		
	def findSelected(self):
		if self.selected:
			return self
		else:
			return False
		
	def deselect(self, canvas):
		canvas.itemconfig(self.id, width=self.border)
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
		# get lowest (most left) x of figure in group
		x = 0
		for figure in self.figures:
			figure_x = figure.getX()
			if (figure_x < x):
				x = figure_x

		# add lowest x to own abs x
		return self.getAbsX() + x

	def getBoundingBoxY(self):
		# get lowest (heighest) y of figure in group
		y = 0
		for figure in self.figures:
			figure_y = figure.getY()
			if (figure_y < y):
				y = figure_y

		# add lowest y to own abs y
		return self.getAbsY() + y

	def getBoundingBoxWidth(self):
		# find leftmost and rightmost x'es
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
		# find highest and lowest y'es
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

	def findId(self, id:int):
		# check if own id matches
		if id == self.id:
			return self
		
		# go trough all own Figures and return id if matches
		for figure in self.figures:
			if not(figure.findId(id) == False):
				return figure
		
		# return false if id couldnt be found
		return False
	
	def findSelected(self):
		# check if own id matches
		if self.selected:
			return self
		
		# go trough all own Figures and return id if matches
		for figure in self.figures:
			if not(figure.findSelected() == False):
				return figure.findSelected()
		
		# return false if id couldnt be found
		return False
	
	def deselect(self, canvas):
		super().deselect(canvas)

		for figure in self.figures:
			figure.deselect(canvas)
	
	def draw(self, canvas:tk.Canvas):
		x = self.getBoundingBoxX() + self.border*2
		y = self.getBoundingBoxY() + self.border*2
		w = self.getBoundingBoxWidth() + self.border*2
		h = self.getBoundingBoxHeight() + self.border*2
		self.id = canvas.create_rectangle(x, y, x+w, y+h, outline=self.color, dash=(50), fill='', width=self.border)

		for figure in self.figures:
			figure.draw(canvas)

class Rectangle(Figure):
	def __init__(self, x:int, y:int, width:int, height:int, color:str):
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
		x = self.getAbsX() + self.border*2
		y = self.getAbsY() + self.border*2
		w = self.getBoundingBoxWidth() + self.border*2
		h = self.getBoundingBoxHeight() + self.border*2
		self.id = canvas.create_rectangle(x, y, x+w, y+h, outline=self.color, width=self.border, fill='')

class Circle(Figure):
	def __init__(self, x:int, y:int, radius:int, color:str):
		super().__init__(x, y, color)
		self.radius = radius

	def __str__(self):
		return f"Circle: {super().__str__()}, r: {self.radius}"
	
	def getBoundingBoxWidth(self):
		return 2* self.radius
		
	def getBoundingBoxHeight(self):
		return 2* self.radius
	
	def draw(self, canvas:tk.Canvas):
		x = self.getAbsX() + self.border*2
		y = self.getAbsY() + self.border*2
		w = self.getBoundingBoxWidth() + self.border*2
		h = self.getBoundingBoxHeight() + self.border*2
		self.id = canvas.create_oval(x, y, x+w, y+h, outline=self.color, width=self.border, fill='')