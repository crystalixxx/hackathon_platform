import pytest

from backend.app import main

def test_file():
    assert main.my_function(1) == 0.5
