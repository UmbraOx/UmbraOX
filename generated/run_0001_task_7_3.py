# test_gui_utils.py
import pytest
from gui_utils import validate_input

def test_validate_input_valid_number():
    assert validate_input("123.45") == True, "Valid number should return True"

def test_validate_input_invalid_number():
    assert validate_input("abc") == False, "Invalid number should return False"
