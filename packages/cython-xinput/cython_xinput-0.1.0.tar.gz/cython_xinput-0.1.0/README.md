# cython_xinput

[![PyPI - Version](https://img.shields.io/pypi/v/cython_xinput.svg)](https://pypi.org/project/cython_xinput)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cython_xinput.svg)](https://pypi.org/project/cython_xinput)
[![CI](https://github.com/zariiii9003/cython_xinput/actions/workflows/wheels.yml/badge.svg)](https://github.com/zariiii9003/cython_xinput/actions/workflows/wheels.yml)

## Installation

```console
pip install cython-xinput
```

## Example

```python3
from cython_xinput import XinputButtons, XinputGamepad

xg = XinputGamepad(0)

xg.configure_deadzone(
    left_thumb=0.01,
    right_thumb=0.01,
    trigger=0.01,
)
xg.set_vibration(left=0.00, right=0.2)

while True:
    if not xg.update():
        continue

    print(xg.left_thumbstick())
    print(xg.right_trigger())
        
    buttons = xg.buttons()
    if XinputButtons.A in buttons:
        print("A")
    if XinputButtons.DPAD_UP in buttons:
        print("DPAD_UP")
```