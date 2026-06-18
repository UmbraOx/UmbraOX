import pytest
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Import the module being tested
from dashboard import app  # Adjust the import according to your project structure

# Fixture for setting up and tearing down the web driver
@pytest.fixture(params=['chrome', 'firefox'])
def browser(request):
    if request.param == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        driver = webdriver.Chrome(options=options)
    elif request.param == 'firefox':
        options = FirefoxOptions()
        options.headless = True
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Firefox(options=options)
    
    yield driver
    driver.quit()

# Fixture for setting up the test server
@pytest.fixture
def app_client():
    with app.test_client() as client:
        yield client

# Test happy path: Dashboard loads correctly on desktop
def test_dashboard_loads_correctly_desktop(browser, app_client):
    browser.get('http://127.0.0.1:5000/dashboard')
    assert "Dashboard" in browser.title, "Dashboard title should be 'Dashboard'"
    assert browser.find_element(By.ID, 'dashboard-container').is_displayed(), "Dashboard container should be displayed"

# Test edge case: Dashboard loads correctly on mobile
def test_dashboard_loads_correctly_mobile(browser, app_client):
    # Set browser size to mobile dimensions
    browser.set_window_size(412, 800)  # Example mobile resolution
    browser.get('http://127.0.0.1:5000/dashboard')
    assert "Dashboard" in browser.title, "Dashboard title should be 'Dashboard'"
    assert browser.find_element(By.ID, 'dashboard-container').is_displayed(), "Dashboard container should be displayed"

# Test performance: Dashboard loads within a reasonable time
def test_dashboard_loads_within_performance_threshold(browser, app_client):
    import time
    start_time = time.time()
    browser.get('http://127.0.0.1:5000/dashboard')
    end_time = time.time()
    load_time = end_time - start_time
    assert load_time < 5, f"Dashboard should load within 5 seconds, but took {load_time} seconds"

# Test error case: Dashboard handles missing data gracefully
@patch('dashboard.get_data')
def test_dashboard_handles_missing_data(mock_get_data, browser, app_client):
    mock_get_data.return_value = None
    browser.get('http://127.0.0.1:5000/dashboard')
    assert "No data available" in browser.find_element(By.ID, 'error-message').text, "Error message should be displayed"

# Test responsiveness: Dashboard elements are correctly positioned on resize
def test_dashboard_responsive(browser, app_client):
    # Set initial size to desktop
    browser.set_window_size(1920, 1080)
    browser.get('http://127.0.0.1:5000/dashboard')
    
    # Resize to mobile
    browser.set_window_size(412, 800)
    assert browser.find_element(By.ID, 'dashboard-container').location['x'] == 0, "Dashboard container should be aligned to the left on resize"
