from httpx import URL
from domapi.webapi_classes import WebAPIClassBase

class Location(WebAPIClassBase):
	def __init__(self, urlobj: URL, protocol: str): # add other args in the future
		self._url = URL
		self._protocol = protocol

	@property
	def host(self) -> str:
		return f"{self.hostName}:{self.port}"

	@property
	def port(self) -> str:
		return str(self._url.port) if self._url.port else ""
	@property
	def hostName(self) -> str:
		return self._url.host

	@property
	def protocol(self) -> str:
		return self._protocol

	@property
	def pathname(self) -> str:
		return self._url.path

	@property
	def search(self) -> str:
		return f"?{self._url.query.decode()}"

	@property
	def hash(self) -> str:
		return f"#{self._url.fragment}"

	@property
	def origin(self) -> str:
		return f"{self.protocol}//{self.host}"

	@property
	def href(self) -> str:
		return f"{self.origin}{self.pathname}{self.search}{self.hash}"

	@property
	def ancestorOrigins(self) -> list[str]:
		pass # figure this out

	@href.setter
	def href(self, new_href: str):
		pass # do something here to reload, maybe through use of a a browser main func

	def reload(self):
		self.href = self.href # initiate reload