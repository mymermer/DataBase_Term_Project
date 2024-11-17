import pandas as pd
import os

# Define the tables and columns with the specific problem
tables = {
    "CUP_POINTS.csv": "game_play_id",
    "LIG_POINTS.csv": "game_play_id",
    "CUP_PLAY_BY_PLAY.csv": "game_point_id",
    "LIG_PLAY_BY_PLAY.csv": "game_point_id"
}

def format_last_section(value):
    """Format the last section of a string to ensure 3 digits."""
    try:
        parts = value.split('_')
        if len(parts) > 2:  # Ensure it's the expected format
            parts[-1] = parts[-1].zfill(3)  # Pad last part with zeros
            return '_'.join(parts)
        return value
    except Exception as e:
        print(f"Error formatting value {value}: {e}")
        return value

def process_csv(file_name, column_name):
    """Process a CSV file to format the specific column."""
    try:
        # Check if the file exists
        if not os.path.exists(file_name):
            print(f"File not found: {file_name}")
            return
        
        # Read the CSV file
        df = pd.read_csv(file_name)

        # Check if the column exists
        if column_name not in df.columns:
            print(f"Column '{column_name}' not found in {file_name}")
            return

        # Update the column
        df[column_name] = df[column_name].apply(format_last_section)

        # Save the updated CSV back to the same file
        df.to_csv(file_name, index=False)
        print(f"Processed file: {file_name}")
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")

# Process each table
for file_name, column_name in tables.items():
    process_csv(file_name, column_name)
