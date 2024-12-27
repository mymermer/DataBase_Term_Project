import pandas as pd

# List of file names to process
file_names = [
    'CUP_HEADER.csv',
    'LIG_HEADER.csv'
]

# Base folder path
folder_path = 'C:/Users/DELL/Desktop/'

# Columns to process
columns_to_process = [
    'score_extra_time_1_a',
    'score_extra_time_2_a',
    'score_extra_time_3_a',
    'score_extra_time_4_a',
    'score_extra_time_1_b',
    'score_extra_time_2_b',
    'score_extra_time_3_b',
    'score_extra_time_4_b'
]

# Loop through each file
for file_name in file_names:
    # Load the dataset
    file_path = folder_path + file_name
    df = pd.read_csv(file_path)

    # Replace empty cells in the specified columns with 0
    for column in columns_to_process:
        df[column] = df[column].fillna(0)

    # Compare and update values for specific conditions
    # Compare score_extra_time_1_a with score_quarter_4_a
    df['score_extra_time_1_a'] = df.apply(
        lambda row: 0 if row['score_extra_time_1_a'] == row['score_quarter_4_a'] else row['score_extra_time_1_a'], axis=1
    )

    # Compare score_extra_time_1_b with score_quarter_4_b
    df['score_extra_time_1_b'] = df.apply(
        lambda row: 0 if row['score_extra_time_1_b'] == row['score_quarter_4_b'] else row['score_extra_time_1_b'], axis=1
    )

    # Save the modified DataFrame to a new file with "_updated" suffix
    output_path = folder_path + file_name.replace('.csv', '_updated.csv')
    df.to_csv(output_path, index=False)

    print(f"Modified file saved to {output_path} with the updated values in the specified columns.")
