import os

def save_summary_report(report_content):
    """
    Saves the given summary report content to a file named 'output_report.txt'.

    Parameters:
    report_content (str): The content of the summary report to be saved.

    Returns:
    None

    Raises:
    IOError: If there is an error writing to the file.
    """
    try:
        with open('output_report.txt', 'w', encoding='utf-8') as file:
            file.write(report_content)
        print("Report successfully saved to output_report.txt")
    except IOError as e:
        print(f"An error occurred while saving the report: {e}")

# Example usage:
if __name__ == "__main__":
    summary = "This is a sample summary report."
    save_summary_report(summary)
