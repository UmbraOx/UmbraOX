import pytest
from unittest.mock import patch
from game import play_game, end_game

# Test the main happy path
def test_play_game_happy_path():
    assert play_game(1) == "Playing on level 1", "Should return correct message for level 1"
    assert play_game(5) == "Playing on level 5", "Should return correct message for level 5"

# Test at least one error/edge case
def test_play_game_invalid_level():
    with pytest.raises(ValueError, match="Level must be at least 1"):
        play_game(0)

# Test the end_game function
def test_end_game():
    assert end_game() == "Game ended", "Should return correct message when ending game"

# Example of mocking an external dependency
@patch('game.some_external_function')
def test_play_game_with_mock(mock_func):
    mock_func.return_value = "Mocked response"
    result = play_game(3)
    assert result == "Playing on level 3", "Should return correct message for level 3 even with mocked function"
