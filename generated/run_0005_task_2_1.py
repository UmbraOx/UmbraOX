# test_calculator.py
import pytest
from unittest.mock import patch
from calculator import add

# Test the main happy path
def test_add_happy_path():
    assert add(2, 3) == 5, "Should be 5"

def test_add_with_zero():
    assert add(0, 5) == 5, "Adding zero should return the other number"
    assert add(5, 0) == 5, "Adding zero should return the other number"

# Test an error/edge case
def test_add_negative_numbers():
    assert add(-1, -1) == -2, "Should be -2"

# Mock external dependencies with unittest.mock (not applicable here as there are no external dependencies)
# But let's assume we have a function that calls an external API

def fetch_data_from_api():
    # Simulate fetching data from an external API
    return 42

def add_with_external_dependency(a, b):
    external_value = fetch_data_from_api()
    return a + b + external_value

@patch('test_calculator.fetch_data_from_api')
def test_add_with_external_dependency(mock_fetch):
    mock_fetch.return_value = 10
    assert add_with_external_dependency(2, 3) == 15, "Should be 15 with mocked external value"

# Each test function tests ONE thing
