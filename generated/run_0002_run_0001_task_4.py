import pytest
from unittest.mock import patch, MagicMock
from your_module import initialize_environment  # Replace with the actual module name

# Fixture to mock external dependencies
@pytest.fixture
def mock_dependencies():
    with patch('your_module.SomeExternalClass') as MockClass:
        instance = MockClass.return_value
        yield instance

# Test for the main happy path
def test_initialize_environment_happy_path(mock_dependencies):
    # Arrange
    model_name = 'qwen2.5-coder:14b'
    
    # Act
    result = initialize_environment(model_name)
    
    # Assert
    mock_dependencies.initialize.assert_called_once_with(model_name)
    assert result == "Environment initialized successfully", "The environment should be initialized successfully"

# Test for an error/edge case (e.g., invalid model name)
def test_initialize_environment_invalid_model(mock_dependencies):
    # Arrange
    invalid_model_name = 'invalid-model'
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid model name"):
        initialize_environment(invalid_model_name)
    mock_dependencies.initialize.assert_not_called(), "The external dependency should not be initialized for an invalid model"

# Test for an error/edge case (e.g., external dependency failure)
def test_initialize_environment_dependency_failure(mock_dependencies):
    # Arrange
    model_name = 'qwen2.5-coder:14b'
    mock_dependencies.initialize.side_effect = Exception("Dependency failed to initialize")
    
    # Act & Assert
    with pytest.raises(Exception, match="Dependency failed to initialize"):
        initialize_environment(model_name)
    mock_dependencies.initialize.assert_called_once_with(model_name), "The external dependency should be initialized but fail"
