import pytest
from unittest.mock import patch
from flask import Flask
from myapp import app  # Import your Flask app

# Fixture to set up the test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the main happy path: accessing a valid static file
def test_serve_static_file_happy_path(client):
    response = client.get('/static/sample.txt')
    assert response.status_code == 200, "Should return status code 200 for successful access"
    assert b"Sample Content" in response.data, "Response should contain the content of sample.txt"

# Test an error/edge case: accessing a non-existent static file
def test_serve_static_file_not_found(client):
    response = client.get('/static/nonexistent.txt')
    assert response.status_code == 404, "Should return status code 404 for non-existent files"

# Mocking external dependencies (if any)
# For example, if you need to mock a database call or an API request
@patch('myapp.some_module.SomeExternalDependency')
def test_serve_static_file_with_mock(mock_dependency, client):
    response = client.get('/static/sample.txt')
    assert response.status_code == 200, "Should return status code 200 for successful access"
    mock_dependency.assert_not_called(), "External dependency should not be called for static file serving"
