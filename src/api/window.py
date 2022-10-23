import tkinter as tk
from domapi.webapi_classes import Document
from .location import Location

class Window:
	def __init__(self, document: Document, location: Location, __window: tk.Tk) -> None:
		self._document = document
		self._location = location
		self._window = __window

	@property
	def document(self):
		return self._document

	@property
	def location(self):
		return self._location

	def alert(self, message: str):
		root = tk.Tk()
		root.title(f"{self.location.hostName if self.location.hostName else 'A file'} says...")
		root.geometry("400x50")
		root.resizable(False, False)

		tk.Label(root, text=message).pack()

		tk.Button(root, text="Ok", command=root.destroy).pack()

		root.mainloop()