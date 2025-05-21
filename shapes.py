from __future__ import annotations # make recursive type hint possible

import tkinter as tk

class Component():
	def __init__(self, x:int, y:int, c:str, id:int):
		self.pos_x = x
		self.pos_y = y
		self.color = c
		self.id = id
		self.parent = None

	def __str__(self):
		(min_x, max_x) = self.get_bounding_box_x()
		(min_y, max_y) = self.get_bounding_box_y()

		return f"pos: {self.pos_x}, {self.pos_y}; pos_abs: {self.get_absolute_x()}, {self.get_absolute_y()}; bounding_box: {max_x - min_x}, {max_y - min_y}"
	
	def set_parent(self, parent:Composite):
		self.parent = parent

	def get_absolute_x(self):
		if self.parent:
			return self.parent.get_absolute_x() + self.pos_x
		else:
			return self.pos_x

	def get_absolute_y(self):
		if self.parent:
			return self.parent.get_absolute_y() + self.pos_y
		else:
			return self.pos_y
		
	def print_descriptor(self, i:int):
		print(i * "    ", self)

	def findId(self, id:int):
		if id == self.id:
			return self
		else:
			return False

class Composite(Component):
	def __init__(self, x:int, y:int, id:int):
		super().__init__(x, y, "purple", id)
		self.components: list[Component] = []

	def __str__(self):
		return f"Composite: ({super().__str__()})"
	
	def add_component(self, component:Composite):
		component.set_parent(self)
		self.components.append(component)

	def get_bounding_box_x(self):
		min_x = None
		max_x = 0

		for el in self.components:
			(min, max) = el.get_bounding_box_x()
			
			if (max > max_x):
				max_x = max
			if (min_x == None or min < min_x):
				min_x = min

		if (min_x == None):
			min_x = 0
		
		return min_x, max_x

	def get_bounding_box_y(self):
		min_y = None
		max_y = 0

		for el in self.components:
			(min, max) = el.get_bounding_box_y()

			if (max > max_y):
				max_y = max
			if (min_y == None or min < min_y):
				min_y = min

		if (min_y == None):
			min_y = 0

		return min_y, max_y
	
	def print_descriptor(self, i:int=0):
		print(i * "    ", self)
		i += 1
		for el in self.components:
			el.print_descriptor(i)

	def findId(self, id:int):
		# check if own id matches
		if id == self.id:
			return self
		
		# go trough all own components and return id if matches
		for el in self.components:
			if not(el.findId(id) == False):
				return el.findId(id)
		
		# return false if id couldnt be found
		return False
	
	def draw(self, canvas:tk.Canvas):
		x,w = self.get_bounding_box_x()
		y,h = self.get_bounding_box_y()
		canvas.create_polygon(x, y, x+w, y, x+w, y+h, x, y+h, outline=self.color, fill='')

		for el in self.components:
			el.draw(canvas)

class Rectangle(Component):
	def __init__(self, x:int, y:int, width:int, height:int, color:str, id:int):
		super().__init__(x, y, color, id)
		self.width = width
		self.height = height

	def __str__(self):
		return f"Rectangle: (size: {self.width}, {self.height}; {super().__str__()})"
	
	def get_bounding_box_x(self):
		return (self.get_absolute_x(), self.get_absolute_x() + self.width)
		
	def get_bounding_box_y(self):
		return (self.get_absolute_y(), self.get_absolute_y() + self.height)
	
	def draw(self, canvas:tk.Canvas):
		x,w = self.get_bounding_box_x()
		y,h = self.get_bounding_box_y()
		canvas.create_polygon(x, y, x+w, y, x+w, y+h, x, y+h, outline=self.color, fill='')

class Circle(Component):
	def __init__(self, x:int, y:int, radius:int, color:str, id:int):
		super().__init__(x, y, color, id)
		self.radius = radius

	def __str__(self):
		return f"Circle: (radius: {self.radius}; {super().__str__()})"
	
	def get_bounding_box_x(self):
		return (self.get_absolute_x() - self.radius, self.get_absolute_x() + self.radius)
		
	def get_bounding_box_y(self):
		return (self.get_absolute_y() - self.radius, self.get_absolute_y() + self.radius)
	
	def draw(self, canvas:tk.Canvas):
		x,w = self.get_bounding_box_x()
		y,h = self.get_bounding_box_y()
		canvas.create_oval(x, y, x+w, y+h, outline=self.color, fill='')