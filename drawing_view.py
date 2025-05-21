import tkinter as tk

from observer import *

class Drawing:
	def __init__(self, model:Model, destroy:Closer):
		self.model = model
		self.destroy = destroy
		model.attach(self)
		destroy.attach(self)

		self.window = tk.Tk()
		self.window.protocol("WM_DELETE_WINDOW", self.destroy.destroy)

		button = tk.Button(self.window, text="Refresh", command=self.refresh)
		button.pack()

		self.canvas = tk.Canvas(self.window, width=800, height=800)
		self.canvas.pack(fill="both", expand=True)
		# hbar = Scrollbar(self.window, orient=HORIZONTAL)
		# hbar.pack(side=BOTTOM,fill=X)
		# hbar.config(command=self.canvas.xview)
		# vbar=Scrollbar(self.window,orient=VERTICAL)
		# vbar.pack(side=RIGHT,fill=Y)
		# vbar.config(command=self.canvas.yview)
		# self.window.config(width=300,height=300)
		# self.window.config(Xscrollcommand=hbar.set, Yscrollcommand=vbar.set)
		# self.window.pack(side=LEFT,expand=True,fill=BOTH)

	def run(self):
		self.window.mainloop()

	def refresh(self):
		self.model.draw(self.canvas)