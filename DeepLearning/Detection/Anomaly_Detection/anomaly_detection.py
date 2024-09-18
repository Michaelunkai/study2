import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Generate random data for the example
np.random.seed(42)
data = pd.DataFrame({
    'feature1': np.random.normal(0, 1, 1000),
    'feature2': np.random.normal(0, 1, 1000)
})

# Introduce some outliers
data.iloc[::10] = data.iloc[::10] + np.random.normal(5, 1, 2)

# Plot the data
plt.scatter(data['feature1'], data['feature2'], s=5)
plt.title("Data with Outliers")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

# Initialize the Isolation Forest model
model = IsolationForest(contamination=0.1)

# Fit the model
model.fit(data)

# Predict anomalies
data['anomaly'] = model.predict(data)

# Plot the anomalies
fig, ax = plt.subplots()
colors = {1: 'blue', -1: 'red'}
ax.scatter(data['feature1'], data['feature2'], c=data['anomaly'].apply(lambda x: colors[x]), s=5)
plt.title("Anomaly Detection")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
