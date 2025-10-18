# xtdamo

xtdamo is a wrapper library based on the DaMo plugin (Dm), designed for automation tasks including window management, mouse control, keyboard simulation, image recognition, text searching, and more. It is suitable for scenarios such as game scripts and automated testing.

## Introduction

xtdamo provides a high-level encapsulation of the DaMo plugin, simplifying operations related to windows, mouse, keyboard, and image recognition. Key features include:

- Window binding and management
- Mouse movement and clicking
- Keyboard key simulation
- Image recognition and searching
- Text recognition and searching
- File and registry operations

## Installation

Ensure that Python 3.x is installed, and you can install xtdamo via pip:

```bash
pip install xtdamo
```

In addition, you need to place the DaMo plugin (dm.dll) in your project directory or specify its path.

## Usage Examples

### Initialize the DaMo Plugin

```python
from xtdamo import DmExcute

dm = DmExcute(dm_dirpath="path_to_dm_dll")
```

### Bind a Window

```python
from xtdamo.apiproxy import ApiProxy

api_proxy = ApiProxy(dm)
hwnd = 123456  # Window handle
api_proxy.BindWindow(hwnd)
```

### Find and Click an Image

```python
api_proxy.FindImageClick(0, 0, 800, 600, "image.png")
```

### Find and Click Text

```python
api_proxy.FindTextClick(0, 0, 800, 600, "Start", "FFFFFF")
```

### Mouse Operations

```python
from xtdamo.mouse import Mouse

mouse = Mouse(dm)
mouse.move_to(100, 200)  # Move mouse to specified coordinates
mouse.click_left(100, 200)  # Left-click
```

### Keyboard Operations

```python
from xtdamo.key import Key

key = Key(dm)
key.press("A")  # Press the A key
key.down("Enter")  # Press down the Enter key
key.up("Enter")  # Release the Enter key
```

## Contributing

Contributions of code or suggestions are welcome! Please refer to the [Contribution Guide](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE).