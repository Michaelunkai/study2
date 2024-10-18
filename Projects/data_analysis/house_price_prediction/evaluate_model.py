import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the model and test data
model = joblib.load('model.pkl')
X_test = joblib.load('X_test.pkl')
y_test = joblib.load('y_test.pkl')

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
print(f"MSE: {mean_squared_error(y_test, y_pred)}")
print(f"R²: {r2_score(y_test, y_pred)}")
