import pandas as pd
import numpy as np
from sklearn.datasets import make_blobs

# Generate sample data
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# Create a DataFrame
df = pd.DataFrame(X, columns=['feature_1', 'feature_2'])
df['label'] = y

# Save the DataFrame to a CSV file
df.to_csv('kmeans_data.csv', index=False)

print("Dataset created and saved as kmeans_data.csv")
