import pandas as pd
from sys import getsizeof

def analyze_memory_usage(df):
    """
    Analyzes the memory usage of each column in a DataFrame.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to analyze.
    
    Returns:
    None: Prints formatted output with memory usage statistics.
    """
    # Check if the input is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    # Display basic information about the DataFrame
    print("DataFrame Info:")
    df.info()
    print("\n")
    
    # Calculate memory usage of each column
    mem_usage = df.memory_usage(deep=True)
    
    # Detect and handle missing data
    missing_data = df.isnull().sum()
    print("Missing Data Count for Each Column:")
    print(missing_data[missing_data > 0])
    print("\n")
    
    # Display memory usage statistics in a formatted table
    mem_usage_df = pd.DataFrame({
        'Column': mem_usage.index,
        'Memory Usage (Bytes)': mem_usage.values,
        'Data Type': df.dtypes.values
    })
    
    print("Memory Usage Statistics:")
    print(mem_usage_df.to_string(index=False))
    print("\n")
    
    # Calculate total memory usage of the DataFrame
    total_memory = mem_usage.sum()
    print(f"Total Memory Usage: {total_memory} bytes")
    print("\n")
    
    # Suggest data type optimization (optional)
    suggest_optimization(df)

def suggest_optimization(df):
    """
    Provides suggestions for optimizing DataFrame memory usage by suggesting 
    more efficient data types for each column.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to analyze.
    
    Returns:
    None: Prints formatted output with optimization suggestions.
    """
    print("Memory Optimization Suggestions:")
    for col in df.columns:
        dtype = df[col].dtype
        if 'int' in str(dtype):
            min_val, max_val = df[col].min(), df[col].max()
            # Suggest smaller int types where possible
            if pd.api.types.is_signed_integer_dtype(dtype) and min_val >= -128 and max_val <= 127:
                print(f"Consider changing column '{col}' to 'int8'")
            elif pd.api.types.is_unsigned_integer_dtype(dtype) and max_val <= 255:
                print(f"Consider changing column '{col}' to 'uint8'")
            elif min_val >= -32768 and max_val <= 32767:
                print(f"Consider changing column '{col}' to 'int16'")
            elif pd.api.types.is_unsigned_integer_dtype(dtype) and max_val <= 65535:
                print(f"Consider changing column '{col}' to 'uint16'")
        elif 'float' in str(dtype):
            # Suggest float32 instead of float64 when possible
            if df[col].dtype == 'float64':
                print(f"Consider changing column '{col}' to 'float32'")
    print("\n")

# Example usage:
# df = pd.DataFrame({
#     'a': range(1000),
#     'b': [None] * 1000,
#     'c': [True, False] * 500
# })
# analyze_memory_usage(df)
