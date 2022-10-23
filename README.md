# PyBrowser

An attempt at a web browser written in Python.

<br/>

## Dependencies

- [Js2Py](https://pypi.org/project/Js2Py/) (Can be installed using `pip`)
- [domapi](https://github.com/User0332/domapi)
- [lightweight_objbrowser](https://github.com/User0332/lightweight-objbrowser)

## How it works

Currently, [`browser.py`](src/browser.py) will prompt the user to enter a URL or file path (in this case, you can use [`index.html`](test_files/index.html)). A window will then open with a text input box in the top right corner, which you can use like a console to evaluate JavaScript expressions (using `Js2Py`). You can use the `document` object (through `domapi`), as well as the `window`, `location`, and `console` objects (defined in [`api/`](src/api/)). Note that all of these objects are still not yet fully supported. Using `console.dir(obj)` will pop up a object browsing window using `lightweight_objbrowser`.
