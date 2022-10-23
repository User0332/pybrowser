import exceptions
import os
import httpx

def get(url_or_uri: str, headers: dict=None):
	if os.path.isfile(url_or_uri):
		return open(url_or_uri, 'r').read(), httpx.URL("index.html")

	resp = httpx.get(
		url_or_uri,
		headers=headers
	)

	if not resp.headers["Content-Type"].startswith("text/html"):
		raise (
			exceptions.UnSupportedContentType(
				f"The content type {resp.headers['Content-Type']} is unknown to pybrowser."
			)
		)

	return resp.content.decode(), resp.url