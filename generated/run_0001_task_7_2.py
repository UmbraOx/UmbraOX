# test_gui_main.py
import pytest
from unittest.mock import patch, mock_open
from gui_main import display_message, main

@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

def test_display_message(capsys):
    message = "Test message"
    display_message(message)
    captured = capsys.readouterr()
    assert captured.out == f"{message}\n", "Display message should match the input"

@patch('gui_main.display_message')
def test_main_valid_input(mock_display_message, mock_input):
    mock_input.return_value = "123.45"
    main()
    mock_display_message.assert_called_once_with("Valid input: 123.45")

@patch('gui_main.display_message')
def test_main_invalid_input(mock_display_message, mock_input):
    mock_input.return_value = "abc"
    main()
    mock_display_message.assert_called_once_with("Invalid input")
