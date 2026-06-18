# test_calculator.py
import pytest
from unittest.mock import patch
from calculator import add, subtract, multiply, divide

# Test addition - happy path
def test_add():
    assert add(2, 3) == 5, "2 + 3 should equal 5"

# Test subtraction - happy path
def test_subtract():
    assert subtract(5, 3) == 2, "5 - 3 should equal 2"

# Test multiplication - happy path
def test_multiply():
    assert multiply(4, 3) == 12, "4 * 3 should equal 12"

# Test division - happy path
def test_divide():
    assert divide(8, 2) == 4, "8 / 2 should equal 4"

# Test division by zero - error/edge case
def test_divide_by_zero():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert str(excinfo.value) == "Cannot divide by zero", "Expected ValueError for division by zero"

# Mock external dependency example (assuming there's an external function call in the calculator module)
@patch('calculator.some_external_function')
def test_with_mock(mock_ext_func):
    mock_ext_func.return_value = 10
    result = add(5, mock_ext_func())
    assert result == 15, "5 + 10 should equal 15"
