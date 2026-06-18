import pytest
from unittest.mock import patch, MagicMock
import urllib.error
import tkinter as tk

# Import the module being tested
from your_module import YourApplication  # Replace with actual module name

@pytest.fixture
def app():
    root = tk.Tk()
    app = YourApplication(root)
    yield app
    root.destroy()

@pytest.fixture
def mock_urlopen(mocker):
    return mocker.patch('urllib.request.urlopen')

def test_happy_path(app, mock_urlopen):
    # Mock the response from Ollama
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"success": true, "message": "Hello"}'
    mock_urlopen.return_value = mock_response

    # Call the method that interacts with Ollama
    result = app.interact_with_ollama()

    # Assert the response is as expected
    assert result == {"success": True, "message": "Hello"}, "Expected a successful response from Ollama"

def test_edge_case(app, mock_urlopen):
    # Mock an error scenario (e.g., HTTPError)
    mock_error = urllib.error.HTTPError('http://localhost:11434', 500, 'Internal Server Error', {}, None)
    mock_urlopen.side_effect = mock_error

    # Call the method that interacts with Ollama
    result = app.interact_with_ollama()

    # Assert the error is handled gracefully
    assert result == {"success": False, "message": "Failed to interact with Ollama"}, "Expected a failure response due to HTTPError"
