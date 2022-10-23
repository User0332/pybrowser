import os
import json
import tkinter as tk
from types import MethodType
from light_objbrowser import browse
from domapi.webapi_classes import WebAPIClassBase
from js2py.base import JsObjectWrapper
from typing import Union

_clear = "cls" if os.name == "nt" else "clear"

def _table_dict(obj: dict[str]) -> str:
	obj = dict(obj) # copy the dict

	table = ""
	greatest_key_len = 0
	for key in tuple(obj.keys()):
		if key.startswith('_'): obj.pop(key)
		
	keys, values = tuple(obj.keys()), tuple(obj.values())

	for key in keys:
		if len(key) > greatest_key_len: greatest_key_len = len(key)

	for key, value in zip(keys, values):
		table+=f"{key+' '*(greatest_key_len-len(key))} | {value!r}\n"

	return table.removesuffix('\n')

class Console(WebAPIClassBase):
	def __init__(self, console_frame: tk.Frame):
		self._frame = console_frame

	def log(self, *args):
		text = ' '.join(str(arg) for arg in args)
		output = tk.Label(
			self._frame, text=text, 
			height=len(text.splitlines())+1, width=self._frame.winfo_width()
		)
		
		output.pack()

	def dir(self, obj: Union[dict, list, object, tuple, JsObjectWrapper, WebAPIClassBase]):
			title = "PyBrowser Object Browser"

			if obj is None:
				browse({}, "None | undefined | null", name=title)
				return

			if isinstance(obj, WebAPIClassBase):
				browse(obj._dict(), "WebAPIClass object", name=title)
				return
 
			if isinstance(obj, JsObjectWrapper):
				browse(obj.to_dict(), "Object object (JavaScript)", name=title)
				return

			if isinstance(obj, dict):
				browse(obj, "dict object", name=title)
				return
			
			if isinstance(obj, (list, tuple)):
				browse(
					{ str(i): item for i, item in enumerate(obj) },
					"list object",
					name=title
				)
				
				return
				

			browse(obj.__dict__, "object object (Python)", name=title)

	def clear(self):
		os.system(_clear)

	def table(self, obj: Union[dict, list, object, tuple, JsObjectWrapper, WebAPIClassBase]):
		if type(obj) in (list, tuple):
			for i, item in enumerate(obj): print(f"{i} | {item!r}")
			return

		if type(obj) is dict:
			print(_table_dict(obj))
			return

		if type(obj) is JsObjectWrapper:
			print(_table_dict(obj.to_dict()))
			return

		if isinstance(obj, WebAPIClassBase):
			print(_table_dict(json.loads(str(obj))))

		print(_table_dict(obj.__dict__))

	def _dict(self) -> dict:
		return {
			func: f"Built-in Python Function {func}"
			for func in self.__class__.__dict__
			if (not func.startswith('_')) and (type(getattr(self, func)) is MethodType)
		}

	def __str__(self):
		return json.dumps(
			self._dict(),
			indent='\t'
		)
		
