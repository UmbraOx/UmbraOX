import pytest
from unittest.mock import patch
from your_module import Sidebar  # Import the module being tested

# Fixture to create a sidebar instance
@pytest.fixture
def sidebar():
    return Sidebar()

def test_sidebar_initialization(sidebar):
    """Test that the sidebar is initialized correctly."""
    assert sidebar.is_visible, "Sidebar should be visible by default."
    assert len(sidebar.items) == 0, "Sidebar should start with no items."

def test_add_item_to_sidebar(sidebar):
    """Test adding an item to the sidebar."""
    sidebar.add_item("Home")
    assert len(sidebar.items) == 1, "Sidebar should have one item after adding."
    assert sidebar.items[0] == "Home", "The added item should be 'Home'."

def test_add_multiple_items_to_sidebar(sidebar):
    """Test adding multiple items to the sidebar."""
    sidebar.add_item("Home")
    sidebar.add_item("Profile")
    assert len(sidebar.items) == 2, "Sidebar should have two items after adding."
    assert sidebar.items[0] == "Home", "The first item should be 'Home'."
    assert sidebar.items[1] == "Profile", "The second item should be 'Profile'."

def test_remove_item_from_sidebar(sidebar):
    """Test removing an item from the sidebar."""
    sidebar.add_item("Home")
    sidebar.remove_item("Home")
    assert len(sidebar.items) == 0, "Sidebar should have no items after removal."
    with pytest.raises(ValueError, match="Item 'Home' not found in sidebar"):
        sidebar.remove_item("Home")

def test_sidebar_rendering(sidebar):
    """Test the rendering of the sidebar."""
    sidebar.add_item("Home")
    sidebar.add_item("Profile")
    rendered = sidebar.render()
    assert "Home" in rendered, "Rendered output should include 'Home'."
    assert "Profile" in rendered, "Rendered output should include 'Profile'."

def test_sidebar_rendering_with_no_items(sidebar):
    """Test the rendering of the sidebar with no items."""
    rendered = sidebar.render()
    assert rendered == "", "Rendered output should be an empty string if no items are present."

@patch("your_module.ExternalService.get_data")
def test_load_external_data(mock_get_data, sidebar):
    """Test loading external data into the sidebar."""
    mock_get_data.return_value = ["Item1", "Item2"]
    sidebar.load_external_data()
    assert len(sidebar.items) == 2, "Sidebar should have two items after loading external data."
    assert sidebar.items[0] == "Item1", "The first item should be 'Item1'."
    assert sidebar.items[1] == "Item2", "The second item should be 'Item2'."

@patch("your_module.ExternalService.get_data")
def test_load_external_data_with_error(mock_get_data, sidebar):
    """Test loading external data with an error."""
    mock_get_data.side_effect = Exception("Failed to fetch data")
    with pytest.raises(Exception, match="Failed to fetch data"):
        sidebar.load_external_data()
