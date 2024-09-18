import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Step 1: Prepare the data
hours_studied = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
test_scores = np.array([50, 55, 60, 65, 70])

# Step 2: Create and train the model
model = LinearRegression()
model.fit(hours_studied, test_scores)

# Step 3: Make predictions on new data
test_hours = np.array([6, 7]).reshape(-1, 1)
predicted_scores = model.predict(test_hours)
print("Predicted Scores for [6, 7] hours:", predicted_scores)

# Step 4: Make predictions on training data for evaluation
predicted_scores_train = model.predict(hours_studied)

# Step 5: Calculate evaluation metrics
mae = mean_absolute_error(test_scores, predicted_scores_train)
mse = mean_squared_error(test_scores, predicted_scores_train)
rmse = np.sqrt(mse)
r2 = r2_score(test_scores, predicted_scores_train)

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R²):", r2)

# Step 6: Plot the data points and the regression line
plt.scatter(hours_studied, test_scores, color='blue', label='Actual Scores')
plt.plot(hours_studied, predicted_scores_train, color='red', label='Regression Line')
plt.xlabel('Hours Studied')
plt.ylabel('Test Score')
plt.title('Linear Regression: Hours Studied vs. Test Score')
plt.legend()
plt. ow()
