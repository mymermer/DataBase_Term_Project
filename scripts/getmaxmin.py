import pandas as pd

def get_max_min(csv_file, column_name):
    try:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(csv_file)
        
        # Check if the column exists
        if column_name not in data.columns:
            return f"Error: Column '{column_name}' not found in the CSV file."

        # Get the maximum and minimum values of the column
        max_value = data[column_name].max()
        min_value = data[column_name].min()
        
        return f"Max value in column '{column_name}': {max_value}\nMin value in column '{column_name}': {min_value}"
    
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
csv_file = "LIG_POINTS.csv"  # Replace with your CSV file name
column_name = "coord_y"  # Replace with your target column name
print(get_max_min(csv_file, column_name))
