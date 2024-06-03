import cython_xinput

import pytest


def test_module():
    assert hasattr(cython_xinput, "XinputButtons")
    assert hasattr(cython_xinput, "XinputGamepad")


def test_instantiation():
    with pytest.raises(RuntimeError):
        cython_xinput.XinputGamepad(0)
