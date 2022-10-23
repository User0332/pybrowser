import exceptions
import os
import httpx

def get(url_or_uri: str, headers: dict=None):
	if url_or_uri.startswith("file://"):
		file = url_or_uri.removeprefix("file://")

		if os.path.isfile(file):
			return open(file, 'r').read(), httpx.URL("index.html")

		raise (
			FileNotFoundError(
				f"Could not find the file {file}"
			)
		)

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