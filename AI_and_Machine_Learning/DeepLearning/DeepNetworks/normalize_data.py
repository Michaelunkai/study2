import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Sample dataset
data = {
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': [100, 200, 300, 400, 500]
}

df = pd.DataFrame(data)
print("Original Data:")
print(df)

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Fit and transform the data
normalized_data = scaler.fit_transform(df)

# Convert the normalized data back to a DataFrame
normalized_df = pd.DataFrame(normalized_data, columns=df.columns)
print("Normalized Data:")
print(normalized_df)

# Save the normalized data to a CSV file
normalized_df.to_csv('normalized_data.csv', index=False)
print("Normalized data saved to 'normalized_data.csv'")
