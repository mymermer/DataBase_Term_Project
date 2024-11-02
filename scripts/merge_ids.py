import os
import pandas as pd

# Directory containing your CSV files
directory = './dataset/'

# Define column combinations to create new unique identifiers
column_combinations = {
    'game_player_id': ['game_id', 'player_id'],
    'game_play_id': ['game_id', 'number_of_play'],
    'season_player_id': ['season_code', 'player_id', 'team_id'],
    'game_point_id': ['game_id', 'number_of_play'],
    'season_team_id': ['season_code', 'team_id'],
    'season_team_id_a': ['season_code', 'team_id_a'],
    'season_team_id_b': ['season_code', 'team_id_b'],
}

# Columns to delete after combinations
columns_to_delete = [
    'season_code', 'team_id', 'number_of_play', 
    'team_id', 'number_of_play', 'player_id',
    'team_id_a', 'team_id_b'
]

# Process each .csv file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Load each CSV file
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)

        # Iterate over each combination, creating new columns as needed
        for new_column, cols in column_combinations.items():
            # Check if required columns exist and new column is not already present
            if all(col in df.columns for col in cols) and new_column not in df.columns:
                # Combine columns to create a unique identifier and insert it at the first column's position
                df[new_column] = df[cols].astype(str).agg('_'.join, axis=1)
                first_col_index = min(df.columns.get_loc(col) for col in cols)
                df.insert(first_col_index, new_column, df.pop(new_column))

        # Remove specified columns if they exist in the DataFrame
        df.drop(columns=[col for col in columns_to_delete if col in df.columns], inplace=True)

        # Save the updated DataFrame back to the same CSV file
        updated_filepath = os.path.join(directory, filename)
        df.to_csv(updated_filepath, index=False)

        # Display the updated DataFrame for verification
        print(f"Updated {filename}:\n", df.head())
