# test_calculator.py

import pytest
from calculator import add, subtract, divide, multiply

# Fixture to mock external dependencies if needed
@pytest.fixture
def mock_dependency(mocker):
    # Example of mocking an external dependency
    mocked_function = mocker.patch('calculator.some_external_function')
    return mocked_function

# Test the main happy path
def test_add():
    assert add(2, 3) == 5, "Addition did not return the expected result"

def test_subtract():
    assert subtract(5, 3) == 2, "Subtraction did not return the expected result"

def test_divide():
    assert divide(10, 2) == 5, "Division did not return the expected result"

def test_multiply():
    assert multiply(4, 6) == 24, "Multiplication did not return the expected result"

# Test at least one error/edge case
def test_divide_by_zero():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert str(excinfo.value) == "Cannot divide by zero", "Expected ValueError for division by zero"

# Example of using a fixture to mock an external dependency
def test_with_mock_dependency(mock_dependency):
    # Assuming some_external_function is called within the functions we are testing
    result = add(2, 3)
    assert result == 5, "Addition did not return the expected result"
    mock_dependency.assert_not_called()  # Ensure the mocked function was not called

# Each test function tests ONE thing
def test_add_with_negative_numbers():
    assert add(-1, -1) == -2, "Addition with negative numbers did not return the expected result"

def test_subtract_with_negative_numbers():
    assert subtract(-5, 3) == -8, "Subtraction with negative numbers did not return the expected result"

def test_multiply_with_zero():
    assert multiply(0, 10) == 0, "Multiplication with zero did not return the expected result"
