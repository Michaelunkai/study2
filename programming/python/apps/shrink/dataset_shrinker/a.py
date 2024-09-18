import pandas as pd

# Load the dataset from your specified path
file_path = '/mnt/c/study/datascience/datasets/csv/game_info.csv'
game_info = pd.read_csv(file_path)

# Drop duplicate rows
game_info.drop_duplicates(inplace=True)

# Drop columns with a high percentage of missing values
threshold = 0.9  # Adjust the threshold as needed
game_info.dropna(thresh=int(threshold * len(game_info)), axis=1, inplace=True)

# Fill remaining missing values with appropriate values or drop remaining missing rows
game_info.fillna(method='ffill', inplace=True)

# Convert data types to more memory-efficient types
game_info = game_info.astype({
    col: 'float32' for col in game_info.select_dtypes(include=['float64']).columns
})
game_info = game_info.astype({
    col: 'int32' for col in game_info.select_dtypes(include=['int64']).columns
})

# Compress the CSV file while saving
output_path = '/mnt/c/study/datascience/datasets/csv/cleaned_game_info.csv'
game_info.to_csv(output_path, index=False, compression='zip')

print(f"Cleaned and compressed dataset saved to {output_path}")
