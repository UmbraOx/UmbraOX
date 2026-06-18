"""
This script performs a simple data processing task. It reads data from a CSV file,
processes it by filtering out rows based on a condition, and writes the processed
data to a new CSV file.
"""

import csv
from typing import List

def read_csv(file_path: str) -> List[dict]:
    """
    Read data from a CSV file and return as a list of dictionaries.
    
    :param file_path: Path to the input CSV file
    :return: List of dictionaries representing rows in the CSV
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def filter_data(data: List[dict], condition_key: str, condition_value: str) -> List[dict]:
    """
    Filter data based on a condition.
    
    :param data: List of dictionaries to filter
    :param condition_key: Key to check the condition against
    :param condition_value: Value that must match for rows to be included
    :return: Filtered list of dictionaries
    """
    return [row for row in data if row.get(condition_key) == condition_value]

def write_csv(file_path: str, data: List[dict], fieldnames: List[str]):
    """
    Write data to a CSV file.
    
    :param file_path: Path to the output CSV file
    :param data: List of dictionaries to write
    :param fieldnames: List of keys that correspond to the fields in the CSV
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    try:
        input_file = 'input.csv'
        output_file = 'output.csv'
        condition_key = 'status'
        condition_value = 'active'

        # Read data from CSV
        data = read_csv(input_file)

        # Filter data based on the condition
        filtered_data = filter_data(data, condition_key, condition_value)

        # Write processed data to a new CSV file
        fieldnames = data[0].keys() if data else []
        write_csv(output_file, filtered_data, fieldnames)

        print(f"Processed data has been written to {output_file}")

    except FileNotFoundError as e:
        print(f"Error: The file {e.filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
