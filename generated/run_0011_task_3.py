import pytest
from unittest.mock import patch, MagicMock
from your_module import run_endpoint  # Import the module being tested

# Fixture to mock dependencies
@pytest.fixture
def mock_external_dependency():
    with patch('your_module.ExternalDependency') as MockClass:
        instance = MockClass.return_value
        yield instance

# Test happy path
def test_run_endpoint_happy_path(mock_external_dependency):
    """
    Tests the /api/run endpoint for the main happy path.
    """
    # Arrange
    expected_result = "Action completed successfully"
    mock_external_dependency.perform_action.return_value = expected_result
    
    # Act
    result = run_endpoint()
    
    # Assert
    assert result == expected_result, "The action should have been performed successfully."
    mock_external_dependency.perform_action.assert_called_once(), "perform_action should be called once."

# Test error/edge case
def test_run_endpoint_error(mock_external_dependency):
    """
    Tests the /api/run endpoint for an error scenario.
    """
    # Arrange
    expected_exception_message = "Failed to perform action"
    mock_external_dependency.perform_action.side_effect = Exception(expected_exception_message)
    
    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        run_endpoint()
    
    assert str(excinfo.value) == expected_exception_message, "The exception message should match the expected error."
