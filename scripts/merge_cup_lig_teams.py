import pandas as pd

# Load the two CSV files
file1 = pd.read_csv('unique_teams.csv')  
file2 = pd.read_csv('unique_teams1.csv') 

# Combine the two files
combined = pd.concat([file1, file2])

# Drop duplicates based on abbreviations and full names
unique_teams = combined.drop_duplicates(subset=['abbreviation', 'full_name']).reset_index(drop=True)

# Save the cleaned data to a new CSV file
unique_teams.to_csv('unique_teams_cleaned.csv', index=False)
