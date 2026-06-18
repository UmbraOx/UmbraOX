import requests
import pandas as pd
from datetime import datetime

# Function to fetch real-time data from the backend service
def fetch_real_time_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to process the fetched data
def process_data(data):
    if not data:
        print("No data received.")
        return None

    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame(data['data'])

    # Handle missing data by filling it with the mean of the column
    mean_value = df['value'].mean()
    df['value'].fillna(mean_value, inplace=True)

    # Detect column types
    print("Column Types:")
    for col in df.columns:
        print(f"{col}: {df[col].dtype}")

    # Perform basic statistical analysis
    summary_stats = df.describe()
    print("\nSummary Statistics:\n", summary_stats)

    return df

# Main function to integrate dashboard with backend services
def main():
    url = "http://backend-service/data"
    data = fetch_real_time_data(url)
    processed_df = process_data(data)

    if processed_df is not None:
        # Display the processed data
        print("\nProcessed Data:\n", processed_df)

# Execute the main function
if __name__ == "__main__":
    main()
