import pytest
from unittest.mock import patch, MagicMock
from gui_server import start_server, process_request  # Assuming these are the main functions in gui_server.py

# Fixtures for setup and teardown if needed
@pytest.fixture
def mock_config():
    return {
        'host': '127.0.0.1',
        'port': 8080,
        'debug': True
    }

# Test happy path
def test_start_server_happy_path(mock_config):
    with patch('gui_server.create_app') as mock_create_app, \
         patch('gui_server.app.run') as mock_run:
        
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        
        start_server(config=mock_config)
        
        mock_create_app.assert_called_once_with(mock_config)
        mock_app.run.assert_called_once_with(host='127.0.0.1', port=8080, debug=True)

def test_process_request_happy_path():
    with patch('gui_server.handle_request') as mock_handle_request:
        request = {'action': 'fetch_data'}
        response = process_request(request)
        
        mock_handle_request.assert_called_once_with(request)
        assert response == mock_handle_request.return_value, "The response should match the return value of handle_request"

# Test error/edge case
def test_process_request_invalid_request():
    with patch('gui_server.handle_request') as mock_handle_request:
        request = {'action': 'unknown'}
        response = process_request(request)
        
        mock_handle_request.assert_not_called()
        assert response == {"error": "Invalid action"}, "The response should indicate an invalid action"

# Additional tests can be added for other functions and edge cases
