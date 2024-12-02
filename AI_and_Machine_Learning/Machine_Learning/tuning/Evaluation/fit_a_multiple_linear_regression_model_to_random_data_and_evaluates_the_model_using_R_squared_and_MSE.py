# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Example data
# Let's create a dataset with three features (x1, x2, x3) and one target variable (y)
np.random.seed(0)
x1 = np.random.rand(100)
x2 = np.random.rand(100)
x3 = np.random.rand(100)
y = 3 * x1 + 5 * x2 + 2 * x3 + np.random.rand(100)  # target variable with some noise

# Combine features into a single matrix
X = np.column_stack((x1, x2, x3))

# Step 1: Fit the Multiple Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# Print the coefficients
print(f"Intercept (b0): {model.intercept_}")
print(f"Coefficients (b1, b2, b3): {model.coef_}")

# Step 2: Make predictions
y_pred = model.predict(X)

# Step 3: Plotting the Actual vs Predicted values
plt.scatter(y, y_pred)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs Predicted Values")
plt. ow()

# Step 4: Evaluating the Model
from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y, y_pred)
r_squared = r2_score(y, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared: {r_squared}")
