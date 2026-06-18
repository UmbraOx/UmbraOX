import requests

def check_dashboard_accessibility(url):
    """
    Check if the dashboard is accessible at the given URL.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the dashboard is accessible, False otherwise.
    """
    try:
        response = requests.get(url)
        # Assuming a successful response code is 200
        if response.status_code == 200:
            print(f"Dashboard is accessible at {url}")
            return True
        else:
            print(f"Failed to access dashboard. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    url = "http://localhost:7860"
    check_dashboard_accessibility(url)
