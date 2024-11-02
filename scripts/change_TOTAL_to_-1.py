import pandas as pd

# List of box score files to process
box_score_files = [
    'eurocup_box_score.csv',
    'euroleague_box_score.csv'
]

# Set the folder path to go up one level
folder_path = '../Dataset - Copy/'

# Loop through each file
for file_name in box_score_files:
    # Load the dataset
    file_path = folder_path + file_name
    df = pd.read_csv(file_path)

    # Replace "TOTAL" in the "dorsal" column with -1
    df['dorsal'] = df['dorsal'].replace("TOTAL", -1)

    # Save the modified DataFrame to a new file with "_filtered" suffix
    filtered_file_path = folder_path + file_name.replace('.csv', '_filtered.csv')
    df.to_csv(filtered_file_path, index=False)

    print(f"Modified file saved to {filtered_file_path} with 'TOTAL' replaced by -1 in the 'dorsal' column.")
