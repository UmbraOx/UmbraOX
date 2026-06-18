import pandas as pd

# Sample data creation
data = {
    'Name': ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown'],
    'Years_of_Experience': [10, 5, 7, None],
    'Specialty': ['Engine Repair', 'Transmission', 'Brakes', 'General Maintenance'],
    'Email': ['john.doe@example.com', 'jane.smith@example.com', '', 'bob.brown@example.com']
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Handling missing data
# Fill missing values in 'Years_of_Experience' with the median value
median_experience = df['Years_of_Experience'].median()
df['Years_of_Experience'].fillna(median_experience, inplace=True)

# Fill missing values in 'Email' with a placeholder
df['Email'].fillna('no-email@example.com', inplace=True)

# Column type detection and conversion if necessary
print("Data types before conversion:")
print(df.dtypes)
# Convert 'Years_of_Experience' to integer
df['Years_of_Experience'] = df['Years_of_Experience'].astype(int)
print("\nData types after conversion:")
print(df.dtypes)

# Statistical analysis
summary_stats = df.describe(include='all')
print("\nSummary statistics of the DataFrame:")
print(summary_stats)

# Printing formatted output
print("\nFormatted Output:\n")
for index, row in df.iterrows():
    print(f"Name: {row['Name']}")
    print(f"Years of Experience: {row['Years_of_Experience']}")
    print(f"Specialty: {row['Specialty']}")
    print(f"Email: {row['Email']}\n")

# Implementation Notes:
# 1. Missing data in 'Years_of_experience' was handled by filling with the median value to avoid skewing average.
# 2. Missing email addresses were filled with a placeholder to ensure all records have an email field.
# 3. The data types of columns were checked and converted where necessary (e.g., 'Years_of_Experience' from float to int).
# 4. A summary of the dataset was provided using describe() to understand the distribution of data.
# 5. Data was printed in a structured format for easy readability.
