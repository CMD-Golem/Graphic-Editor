import tkinter as tk
from observer import *
from shapes import *

class Drawing(Observer):
	def __init__(self, model:Model, destroy:Closer):
		self.model = model
		self.destroy = destroy
		model.attach(self)
		destroy.attach(self)

		self.window = tk.Tk()
		self.window.protocol("WM_DELETE_WINDOW", self.destroy.destroy)

		button = tk.Button(self.window, text="Refresh", command=lambda: self.update(None))
		button.pack()

		self.canvas = tk.Canvas(self.window, width=800, height=400)
		self.canvas.pack(fill="both", expand=True)

		self.canvas.bind("<Button-1>", self.getSelection)

		"""
		hbar = tk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.canvas.xview)
		hbar.pack(side=tk.BOTTOM,fill=tk.X)
		vbar=tk.Scrollbar(self.window,orient=tk.VERTICAL, command=self.canvas.yview)
		vbar.pack(side=tk.RIGHT,fill=tk.Y)
		self.window.config(Xscrollcommand=hbar.set, Yscrollcommand=vbar.set)
		"""

		#self.window.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

	def getSelection(self, event):
		click_margin = 5
		self.deselect()

		figures = self.canvas.find_overlapping(event.x - click_margin, event.y - click_margin,event.x + click_margin, event.y + click_margin)

		if len(figures) >= 1:
			self.model.setSelection(figures[0])

	def deselect(self):
		for id in self.canvas.find_all():
			self.canvas.itemconfig(id, width=self.model.root.border)
		self.model.root.deselect()

	def run(self):
		self.window.mainloop()

	def update(self, selected_id):
		if selected_id != None:
			self.canvas.itemconfig(selected_id, width=6)
		self.model.root.draw(self.canvas)
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		

