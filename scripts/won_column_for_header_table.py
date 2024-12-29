import pandas as pd

# List of header files to process
header_files = [
    'eurocup_header.csv',
    'euroleague_header.csv'
]

# Set the folder path to go up one level
folder_path = '../Dataset - Copy/'

# Loop through each file
for file_name in header_files:
    # Load the dataset
    file_path = folder_path + file_name
    df = pd.read_csv(file_path)

    # Create the 'winner' column based on the conditions
    df['winner'] = df.apply(
        lambda row: 'team_a' if row['score_a'] > row['score_b'] else ('team_b' if row['score_a'] < row['score_b'] else 'draw'),
        axis=1
    )

    # Save the modified DataFrame to a new file with "_with_winner" suffix
    output_path = folder_path + file_name.replace('.csv', '_with_winner.csv')
    df.to_csv(output_path, index=False)

    print(f"Modified file saved to {output_path} with the new 'winner' column.")
