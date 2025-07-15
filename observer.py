import tkinter as tk
from abc import ABC, abstractmethod
from shapes import Group

class Observer(ABC):
	@abstractmethod
	def update(self, selected_id):
		pass

class Subject(ABC):
	def __init__(self):
		# Liste um die Beobachter zu Speichern
		self._observers = []

	# Beobachter anmelden
	def attach(self, observer):
		self._observers.append(observer)

	# Beobachter abmelden
	def detach(self, observer):
		self._observers.remove(observer)

	# Beobachter benachrichtigen
	def notify_observers(self, id):
		for observer in self._observers:
			observer.update(id)

# model
class Model(Subject):
	def __init__(self):
		super().__init__()
		self.root = Group(0, 0)
		self.id = 0
		self.selected_figure = None

	def setSelection(self, selected_id):
		if selected_id != None:
			self.selected_figure = self.root.findFigure(selected_id)
			print(self.selected_figure)
			print(type(self.selected_figure))
			self.selected_figure.selected = True
		self.notify_observers(selected_id)
		


# Class to close all windows
class Closer:
	def __init__(self):
		self.views = [] # list of all windows

	def attach(self, view:Subject):
		self.views.append(view) # add new window to the list

	# close all windows in the list
	def destroy(self):
		for view in self.views:
			view.window.destroy()