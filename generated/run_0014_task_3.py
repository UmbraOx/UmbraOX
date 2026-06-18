# Import necessary libraries
import pandas as pd
import numpy as np

# Sample data creation
data = {
    'A': np.random.rand(10),
    'B': np.random.rand(10)
}
df = pd.DataFrame(data)

# Handling missing data
df.fillna(df.mean(), inplace=True)

# Column type detection and basic statistical analysis
print("Data types:")
print(df.dtypes)
print("\nDescriptive statistics:")
print(df.describe())

# Example of a simple analysis: correlation between columns A and B
correlation = df['A'].corr(df['B'])
print(f"\nCorrelation between A and B: {correlation:.2f}")

# Convert DataFrame to JSON format for JavaScript use
data_json = df.to_json(orient='records')

# Print the JSON data
print("\nJSON Data for JavaScript:")
print(data_json)
