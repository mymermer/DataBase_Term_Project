import os
import pandas as pd

# Load the cleaned CSV file
unique_teams = pd.read_csv('unique_teams_cleaned.csv')

# Directory containing the folders
directory_path = 'sports-logos-main/sports-logos-main/basketball/euroleague/img' 

# Add a new column for logo URLs
unique_teams['logo_url'] = ''

# Get all folder names in the directory
folders = os.listdir(directory_path)

# Function to find the best matching folder (case-insensitive)
def find_best_folder(full_name, folders):
    full_name_words = set(full_name.lower().split())  # Split full_name into words and convert to lowercase
    best_match = None
    max_matches = 0

    for folder in folders:
        folder_words = set(folder.lower().split('_'))  # Split folder name into words and convert to lowercase
        matches = len(full_name_words.intersection(folder_words))
        if matches > max_matches:
            max_matches = matches
            best_match = folder

    return best_match

# Populate the logo_url column
for index, row in unique_teams.iterrows():
    full_name = row['full_name']
    best_folder = find_best_folder(full_name, folders)
    if best_folder:
        unique_teams.at[index, 'logo_url'] = f"/{best_folder}/{best_folder}_small.png"

# Save the updated DataFrame to a new CSV
unique_teams.to_csv('unique_teams_with_logos.csv', index=False)
