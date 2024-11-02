import pandas as pd

# List of file names to process
file_names = [
    'eurocup_box_score.csv',
    'eurocup_players.csv',
    'eurocup_teams.csv',
    'euroleague_box_score.csv',
    'euroleague_players.csv',
    'euroleague_teams.csv'
]

# Base folder path
folder_path = 'C:/Users/DELL/Desktop/Dataset - Copy/'

# Loop through each file
for file_name in file_names:
    # Load the dataset
    file_path = folder_path + file_name
    df = pd.read_csv(file_path)

    # Update the 'valuation' column with the new calculated values based on the formula
    df['valuation'] = (
        df['points'] +
        df['total_rebounds'] +
        df['assists'] +
        df['steals'] +
        df['fouls_received']
    ) - (
        df['turnovers'] +
        df['fouls_committed']
    )

    # Rename the 'valuation' column to 'evaluation'
    df.rename(columns={'valuation': 'evaluation'}, inplace=True)

    # Additional step for specific player files
    if file_name in ['eurocup_players.csv', 'euroleague_players.csv']:
        # Calculate evaluation_per_game
        df['valuation_per_game'] = df['evaluation'] / df['games_played']
        
        # Rename the 'valuation_per_game' column to 'evaluation_per_game'
        df.rename(columns={'valuation_per_game': 'evaluation_per_game'}, inplace=True)

    # Save the modified DataFrame to a new file with "_with_evaluation" suffix
    output_path = folder_path + file_name.replace('.csv', '_with_evaluation.csv')
    df.to_csv(output_path, index=False)

    print(f"Modified file saved to {output_path} with the updated 'evaluation' and 'evaluation_per_game' columns where applicable.")
