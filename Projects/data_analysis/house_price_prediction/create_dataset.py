import pandas as pd
import numpy as np

# Create a sample dataset
np.random.seed(42)
num_samples = 100
data = {
    'feature1': np.random.rand(num_samples),
    'feature2': np.random.rand(num_samples),
    'feature3': np.random.rand(num_samples),
    'categorical_column': np.random.choice(['A', 'B', 'C'], num_samples),
    'target_column': np.random.rand(num_samples)
}

df = pd.DataFrame(data)
df.to_ ('dataset. ', index=False)
print("Dataset created successfully.")
