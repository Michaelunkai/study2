import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# Example dataset
data = {
    'Size': [1500, 1700, 2000, 2200, 2500],
    'Bedrooms': [3, 3, 4, 4, 5],
    'Age': [10, 5, 20, 15, 5],
    'Price': [300000, 350000, 400000, 425000, 450000]
}
df = pd.DataFrame(data)

# Prepare data
X = df[['Size', 'Bedrooms', 'Age']]
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
