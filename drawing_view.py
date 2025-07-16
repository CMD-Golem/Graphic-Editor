import tkinter as tk
from observer import *
from shapes import *

class Drawing(Observer):
	def __init__(self, model:Model, destroy:Closer):
		self.model = model
		self.destroy = destroy

		model.attach(self) # Wird im Observer Pattern an das Subjekt "model" angehängt
		destroy.attach(self)

		self.window = tk.Tk()
		self.window.title("Drawing View")
		self.window.geometry("800x400")
		self.window.resizable(True, True)
		self.window.protocol("WM_DELETE_WINDOW", self.destroy.destroy)

		self.window.columnconfigure(0, weight=1)
		self.window.rowconfigure(1, weight=1)

		button = tk.Button(self.window, text="Refresh", command=lambda: self.update(self.model.selected_figure.id))
		button.grid(column=0, row=0, pady=5)

		self.canvas = tk.Canvas(self.window, bg="white")
		self.canvas.grid(column=0, row=1, sticky=tk.NSEW)

		self.canvas.bind("<Button-1>", self.getSelection) # Einfacher Mausklick ruft getSelection auf

		# Scrollbars
		hbar = tk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.canvas.xview)
		vbar = tk.Scrollbar(self.window,orient=tk.VERTICAL, command=self.canvas.yview)
		self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		hbar.grid(column=0, row=2, sticky=tk.EW)
		vbar.grid(column=1, row=0, sticky=tk.NS, rowspan=2)

	def run(self):
		self.window.mainloop()

	def getSelection(self, event):
		# Korrigiert Scrollbar koordinaten
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)

		# Findet angeklickte Figur
		click_margin = 5 # Maus-hitbox quadratische seitenlänge 10
		selected = self.canvas.find_overlapping(x - click_margin, y - click_margin, x + click_margin, y + click_margin)
		
		self.model.root.deselect()

		if len(selected) >= 1:
			selected_id = self.canvas.gettags(selected[0])[1] # Tupel wird entpackt -> nur Zahlen ID
			self.model.setSelection(int(selected_id))
		else:
			self.model.setSelection(None)

	def update(self, selected_id:int):
		# Zeichnet daten auf den canvas und berechnet grösse neu
		self.canvas.delete("all")
		self.model.root.draw(self.canvas)
		self.canvas.configure(scrollregion=self.canvas.bbox("all")) # scrollbereich neu berechnen

		# Wählt ID aus
		if selected_id != None:
			item = self.canvas.find_withtag((f"figure_{selected_id}"))
			self.canvas.itemconfig(item, width=6)
		

