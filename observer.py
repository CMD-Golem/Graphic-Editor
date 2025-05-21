import tkinter as tk

from shapes import Composite


class Subject():
	def __init__(self):
		# Liste um die Beobachter zu Speichern
		self._observers = []

	# Beobachter anmelden
	def attach(self, observer:"Controller"):
		self._observers.append(observer)

	# Beobachter abmelden
	def detach(self, observer:"Controller"):
		self._observers.remove(observer)

	# Beobachter benachrichtigen
	def notify_observers(self):
		for observer in self._observers:
			observer.update(self)

# model
class Model(Subject):
	def __init__(self):
		super().__init__()
		self.root = Composite(0, 0, 0)
		self.id = 0

	def getNewId(self):
		self.id += 1
		return self.id
	
	def draw(self, canvas:tk.Canvas):
		self.root.draw(canvas)

	def get(self, id):
		return self.root.findId(id)
	
	def set(self, path):
		self.path = path

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