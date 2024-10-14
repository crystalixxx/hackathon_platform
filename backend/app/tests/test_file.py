import pytest

from backend.app import main

@pytest.mark.parametrize('test_input', [0])
def test_file(test_input):
    assert main.my_function(test_input) == 0
