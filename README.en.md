# xtdamo

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/sandorn/xtdamo)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

xtdamo is a modern wrapper library based on the DaMo plugin (Dm), designed for automation tasks including window management, mouse control, keyboard simulation, image recognition, text searching, and more. It is suitable for scenarios such as game scripts, automated testing, and RPA.

## ✨ Key Features

### 🏗️ Modern Architecture Design

-   **Layered Architecture**: Clear 3-tier design `DmExcute -> ApiProxy -> CoreEngine`
-   **Smart Routing**: Automatically selects the best method implementation
-   **Modular**: Separate `Key` and `Mouse` modules with clear responsibilities
-   **Backward Compatible**: Seamless migration for legacy code

### 🛡️ Robust Error Handling

-   **Parameter Validation**: Complete parameter range checking and type validation
-   **Friendly Errors**: Detailed error messages and diagnostic suggestions
-   **Exception Safety**: Comprehensive exception handling mechanism

### 📚 Complete Documentation Support

-   **Google Style**: Detailed docstrings for all methods
-   **Type Annotations**: Full type hints for IDE-friendly intellisense
-   **Rich Examples**: Practical code examples for every feature

### 🚀 Enhanced Functionality

-   **Safe Click**: `safe_click` with random delays for anti-detection
-   **Convenient Properties**: `position` property for quick mouse position get/set
-   **Advanced Operations**: Support for duration-based clicks, drag operations, etc.

## Introduction

xtdamo provides a high-level encapsulation of the DaMo plugin, simplifying operations related to windows, mouse, keyboard, and image recognition. Key features include:

-   **Window Management**: Window finding, binding, property retrieval
-   **Mouse Operations**: Movement, clicking, dragging, scrolling
-   **Keyboard Simulation**: Key presses, combinations, text input
-   **Image Recognition**: Image finding, color recognition
-   **Text Recognition**: Text finding, OCR
-   **Advanced Features**: File operations, registry operations

## Installation

### System Requirements

-   **Python 3.8+ (32-bit version)** - DaMo plugin only supports 32-bit Python
-   Windows Operating System
-   DaMo plugin (dm.dll)

> **Important**: DaMo plugin can only run in 32-bit Python environment. Please ensure you use 32-bit Python.

### Installation Steps

1. **Create 32-bit Python Virtual Environment**:

```bash
# Ensure using 32-bit Python to create virtual environment
python -m venv .venv --python=python3.12-32  # or specify 32-bit Python path
.venv\Scripts\activate  # Windows
```

2. **Install from Source**:

```bash
git clone https://github.com/sandorn/xtdamo.git
cd xtdamo
pip install -e .
```

3. **Install from PyPI** (Planned):

```bash
pip install xtdamo
```

> **Note**: Please ensure installation and execution in 32-bit Python environment.

### DaMo Plugin Configuration

Place the DaMo plugin (dm.dll) in your project directory, or specify the path via environment variables:

```bash
# Set DaMo plugin authentication info (optional)
set DM_REG_CODE=your_registration_code
set DM_VER_INFO=your_version_info
```

## Architecture Design

xtdamo adopts a clear layered architecture design to ensure maintainability and extensibility:

```
┌─────────────────────────────────────┐
│      DmExcute (Main Entry)          │
│  - Unified calling interface        │
│  - Automatic method routing         │
└──────────────┬──────────────────────┘
               │
               ├──────────────────────┐
               │                      │
       ┌───────▼────────┐    ┌───────▼────────┐
       │   ApiProxy     │    │  CoreEngine    │
       │ (High-level)   │───>│ (Core Engine)  │
       │                │    │                │
       │ - Friendly API │    │ - Core methods │
       │ - Smart errors │    │ - Direct DM    │
       │ - Auto logging │    │ - Base features│
       └────────────────┘    └────────────────┘
```

### Core Features

-   **Layered Architecture**: Clear hierarchy with distinct responsibilities
-   **Smart Routing**: Automatically selects the most appropriate implementation
-   **Backward Compatible**: Maintains compatibility with old code
-   **Easy to Extend**: Modular design for convenient feature expansion

For more architecture details, see [Architecture Update](docs/architecture_update.md).

## 📖 Usage Examples

### Quick Start

```python
from xtdamo import DmExcute

# Initialize (auto-registers DaMo plugin)
dm = DmExcute()

# Check version info
print(f"Version: {dm.ver()}")
print(f"Library Version: {dm.__version__}")  # Output: 0.2.0
```

### Window Operations

```python
# Find window
hwnd = dm.FindWindow("", "Notepad")
if hwnd == 0:
    print("Window not found")
    exit(1)

# Bind window (high-level interface with parameter validation)
try:
    dm.绑定窗口(
        hwnd,
        display='gdi',      # Display mode
        mouse='windows3',   # Mouse mode
        keypad='windows',   # Keyboard mode
        mode=101            # Binding mode
    )
    print("Binding successful!")
except ValueError as e:
    print(f"Parameter error: {e}")
except AssertionError as e:
    print(f"Binding failed: {e}")

# Use default configuration (recommended)
dm.绑定窗口(hwnd)  # Use default parameters
```

### Mouse Operations (Multiple Ways)

```python
# Method 1: Through DmExcute main entry (auto-routing)
dm.MoveTo(100, 200)        # Move mouse
dm.LeftClick()             # Left click

# Method 2: Using convenient property
x, y = dm.Mouse.position   # Get current position
dm.Mouse.position = (500, 300)  # Set position

# Method 3: Using enhanced methods
dm.Mouse.safe_click(300, 400, auto_reset_pos=True)  # Safe click
dm.Mouse.click_left(100, 200, t=1.0)  # Long press for 1 second

# Method 4: Drag operation
dm.Mouse.MoveTo(100, 100)
dm.Mouse.LeftDown()
dm.Mouse.MoveTo(200, 200)
dm.Mouse.LeftUp()
```

### Keyboard Operations

```python
# Through DmExcute main entry
dm.KeyPressStr('Hello World')  # Input text
dm.KeyPress(13)                # Press Enter key (VK_RETURN)

# Using VirtualKeys constants
from xtdamo.time_utils import VirtualKeys
dm.Key.KeyPress(VirtualKeys.ENTER)
dm.Key.KeyPress(VirtualKeys.ESC)

# Combination keys
dm.Key.KeyDown(VirtualKeys.CTRL)   # Press Ctrl
dm.Key.KeyPress(ord('C'))          # Press C key
dm.Key.KeyUp(VirtualKeys.CTRL)     # Release Ctrl

# Wait for key press
if dm.Key.WaitKey(VirtualKeys.ESC, 5000):
    print("User pressed ESC key")
```

### Image Recognition and Operations

```python
# High-level interface - find and click image
success = dm.找图单击(0, 0, 1920, 1080, 'button.bmp', '000000', 0.9)
if success:
    print("Found and clicked successfully")

# Find and click until disappears
dm.找图单击至消失(0, 0, 800, 600, 'close.bmp', max_retries=10)

# Get coordinates
found, x, y = dm.找图返回坐标(0, 0, 1920, 1080, 'target.bmp')
if found:
    print(f"Image position: ({x}, {y})")
    dm.Mouse.safe_click(x, y)
```

### Text Recognition and Operations

```python
# Find and click text
success = dm.找字单击(0, 0, 800, 600, 'Start Game', 'FFFFFF', 0.9)

# Simple OCR
text = dm.简易识字(100, 100, 300, 200, 'FFFFFF', 0.9)
print(f"Recognized text: {text}")

# Find text and get coordinates
found, x, y = dm.找字返回坐标(0, 0, 800, 600, 'OK', 'FFFFFF', 0.9)
if found:
    dm.Mouse.MoveTo(x, y)
    dm.Mouse.LeftClick()
```

### Complete Example - Automation Script

```python
from xtdamo import DmExcute
from xtdamo.time_utils import sleep, VirtualKeys

def main():
    # Initialize
    dm = DmExcute()
    print(f"xtdamo version: {dm.__version__}")

    # Find and bind window
    hwnd = dm.FindWindow("", "Target Program")
    if hwnd == 0:
        print("Window not found")
        return

    # Bind window (use default config)
    dm.绑定窗口(hwnd)
    print("Window bound successfully")

    # Execute automation tasks
    try:
        # Click start button
        if dm.找图单击(0, 0, 800, 600, 'start_button.bmp'):
            print("Clicked start button successfully")
            sleep(1)

        # Input username
        dm.KeyPressStr('username')
        dm.KeyPress(VirtualKeys.TAB)

        # Input password
        dm.KeyPressStr('password')
        dm.KeyPress(VirtualKeys.ENTER)

        # Wait for login completion (find image confirmation)
        sleep(2)
        if dm.简易找图(0, 0, 800, 600, 'login_success.bmp'):
            print("Login successful!")

    finally:
        # Unbind window
        dm.解绑窗口()
        print("Window unbound")

if __name__ == '__main__':
    main()
```

## What's New in v0.2.0

### 🏗️ Architecture Improvements

-   **Layered Architecture Refactoring**: Established clear `DmExcute -> ApiProxy -> CoreEngine` 3-tier architecture
-   **Method Separation**: Separated keyboard and mouse methods from `CoreEngine` into independent `Key` and `Mouse` modules
-   **Smart Routing**: Optimized `DmExcute` method lookup mechanism
-   **Redundancy Removal**: Cleaned up duplicate helper methods, unified to standard API

### ✨ New Features

-   **Parameter Validation**: Complete parameter validation and range checking
-   **Enhanced Error Handling**: Detailed error information and diagnostic suggestions
-   **Advanced Mouse Methods**: `safe_click`, `click_left/click_right`, `position` property
-   **Version Metadata**: Added `__version__` and other metadata to `__init__.py`
-   **Complete Documentation**: Added Google Style docstrings to all modules and methods

### 🔧 Improvements

-   **Parameter Handling**: `None` parameters no longer override default config
-   **Type Annotations**: Completed type annotations for all methods
-   **Delay Configuration**: Unified keyboard and mouse delay parameter type to `float`
-   **Test Improvements**: Optimized test scripts to avoid repeated registration/unregistration loops

### 📦 Dependency Analysis

-   Confirmed `typing_extensions` is not required (Python 3.8+ has all used types built-in)
-   Maintained minimal dependency list with only necessary packages

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

## Contributing

Contributions of code or suggestions are welcome! Please refer to the [Contributing Guide](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE).

## Links

-   **Homepage**: [https://github.com/sandorn/xtdamo](https://github.com/sandorn/xtdamo)
-   **Issues**: [https://github.com/sandorn/xtdamo/issues](https://github.com/sandorn/xtdamo/issues)
-   **Documentation**: [docs/](docs/)
-   **Changelog**: [CHANGELOG.md](CHANGELOG.md)
