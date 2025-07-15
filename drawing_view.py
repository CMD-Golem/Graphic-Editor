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

	def run(self):
		self.window.mainloop()

	def getSelection(self, event):
		click_margin = 5
		selected = self.canvas.find_overlapping(event.x - click_margin, event.y - click_margin,event.x + click_margin, event.y + click_margin)
		self.deselect()

		if len(selected) >= 1:
			selected_id = self.canvas.gettags(selected[0])[1]
			self.model.setSelection(int(selected_id))
		else:
			self.model.setSelection(None)

	def deselect(self):
		self.model.root.deselect()

		for item in self.canvas.find_all():
			self.canvas.itemconfig(item, width=self.model.root.border)

	def update(self, selected_id:int):
		# zeichnet daten auf den canvas und berechnet grösse neu
		self.canvas.delete("all")
		self.model.root.draw(self.canvas)
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

		# wählt ID aus
		if selected_id != None:
			item = self.canvas.find_withtag((f"figure_{selected_id}"))
			self.canvas.itemconfig(item, width=6)
		

