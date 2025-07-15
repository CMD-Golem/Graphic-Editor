import tkinter as tk
from abc import ABC, abstractmethod
from shapes import Group

# Observer Superklasse von: Controller, Drawing, Tree
class Observer(ABC):
	@abstractmethod
	def update(self, selected_id:int):
		pass

# Subjekt Superklasse von: Model
class Subject(ABC):
	def __init__(self):
		# Liste um die Beobachter zu Speichern
		self._observers = []

	# Beobachter anmelden
	def attach(self, observer:Observer):
		self._observers.append(observer)

	# Beobachter abmelden
	def detach(self, observer:Observer):
		self._observers.remove(observer)

	# Beobachter benachrichtigen
	def notify_observers(self, selected_id:int):
		for observer in self._observers:
			observer.update(selected_id)


class Model(Subject):
	def __init__(self):
		super().__init__()
		self.root = Group(0, 0) # Anfang der Gruppenhierarchie
		self.id = 0
		self.selected_figure = None

	def setSelection(self, selected_id:int):
		if selected_id != None:
			self.selected_figure = self.root.findFigure(selected_id)
			self.selected_figure.selected = True
		else: # Wenn nichts ausgewählt, selected_figure auf None gesetzt
			self.selected_figure = None

		self.notify_observers(selected_id)


# Klasse um alle Fenster gleichzeitig zu schliessen
class Closer:
	def __init__(self):
		self.views = [] # Liste mit allen Fenstern

	def attach(self, view):
		self.views.append(view) # Fenster in der Liste hinzufügen

	# Alle Fenster schliessen
	def destroy(self):
		for view in self.views:
			view.window.destroy()