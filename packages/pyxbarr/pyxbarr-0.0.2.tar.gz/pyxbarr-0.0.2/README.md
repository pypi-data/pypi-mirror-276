# pyxbarr

![PyPI](https://img.shields.io/pypi/v/pyxbarr?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyxbarr)

`pyxbarr` is a Python library for helping you create python plugins for [xbar](https://xbarapp.com) with ease!

The library wraps all the xbar menu creation logic with classes and objects
to let you create a plugin with a few lines of code and without dealing with
string formatting complications.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pyxbarr
```

## Usage

```python
import pyxbarr

# Create a new xbar plugin
plugin = pyxbarr.Plugin(
    # Set the title of the plugin
    title=pyxbarr.Item("My Plugin", font="Menlo", size=20),
    # Add items to the plugin
    items=[
        pyxbarr.Item("Hello", color="blue", href="https://github.com/gohadar/pyxbarr")
    ]
).add_items(
    # Add multiple items to the plugin
    [
        pyxbarr.Item("World", color="red", key="shift+k"),
        pyxbarr.Item("Foo", color="green", alternative=pyxbarr.Item("Bar", color="yellow")),
        # Add item with submenu
        pyxbarr.Item("Baz", color="purple", children=[
            pyxbarr.Item("Qux"),
            pyxbarr.Item("Quux"),
        ]),
    ]
)

print(plugin)
```

## Contributing

Please open an issue first to discuss what you would like to change.
I welcome any and all criticism, feedback, and suggestions even if I may not agree.
