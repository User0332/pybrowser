import json
import domapi
import tkinter as tk
import get_site
import js2py
import ctypes
from api.console import Console
from api.location import Location
from api.window import Window


user32 = ctypes.windll.user32
screen_x, screen_y = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

try:
	text, _location = get_site.get(
		input("URL: ")
	)
except KeyboardInterrupt:
	print("\nCTRL-C -- Exit")
	exit(0)

try: document = domapi.make_document_from_str(text)
except domapi.xml.ParseError: document = domapi.make_document_from_str(f"<html>{text}</html>")

class _Object(domapi.webapi_classes.WebAPIClassBase):
	def _dict(self) -> dict:
		return {
			**{
				key: value
				for key, value in self.__dict__.items()
				if type(value) is not js2py.base.JsObjectWrapper 
			},
			**{
				key: value.to_dict()
				for key, value in self.__dict__.items()
				if type(value) is js2py.base.JsObjectWrapper
			}
		}

	def __str__(self):
		return json.dumps(
			self._dict(),
			indent='\t'
		)

def make_new_console_input():
	console_input = tk.Entry(console_window)
	console_input.bind("<Return>", exec_js)
	
	console_input.pack()

	return console_input

def exec_js(event: tk.Event):
	js: str = event.widget.get()

	try: js2py.parse_js(js) # check for syntax errors
	except js2py.PyJsException as e:
		console.log(e)
		make_new_console_input()
		return

	js = \
		f"function(window, document, location, console, refs, InternalPython) {{ return {js} }}"
	
	try:	
		main_func = js2py.eval_js(js)
		console.log(main_func(window, document, location, console, refs, globals()))
	except js2py.PyJsException as e:
		console.log(f"Error: {e}") # change to console.error once implemented
		make_new_console_input()
		return

	make_new_console_input()

browser_window = tk.Tk()
browser_window.title("PyBrowser")
browser_window.geometry(f"{screen_x}x{screen_y}")
browser_window.resizable(True, True)

console_window = tk.Tk()
console_window.title("PyBrowser JavaScript Console")
console_window.geometry("500x800")
console_window.resizable(True, True)

refs = _Object()
console = Console(console_window)
location = Location(_location, "<protocol>")
window = Window(document, location, browser_window)

make_new_console_input()

browser_window.after(0, console_window.mainloop)
browser_window.mainloop()