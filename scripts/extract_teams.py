import pandas as pd

# Read the CSV file
data = pd.read_csv('../backend/dataset/CUP_HEADER.csv')

# Extract team abbreviations from `season_team_id_a` and `season_team_id_b`
data['team_id_a'] = data['season_team_id_a'].str.split('_').str[1]
data['team_id_b'] = data['season_team_id_b'].str.split('_').str[1]

# Create a DataFrame for team_a and team_b
team_a = data[['team_id_a', 'team_a']].rename(columns={'team_id_a': 'abbreviation', 'team_a': 'full_name'})
team_b = data[['team_id_b', 'team_b']].rename(columns={'team_id_b': 'abbreviation', 'team_b': 'full_name'})

# Combine the two DataFrames and drop duplicates
unique_teams = pd.concat([team_a, team_b]).drop_duplicates().reset_index(drop=True)

# Save the result to a new CSV file
unique_teams.to_csv('unique_teams.csv', index=False)
