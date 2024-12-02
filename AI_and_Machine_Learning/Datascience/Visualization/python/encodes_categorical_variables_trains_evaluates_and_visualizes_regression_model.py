import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

# Step 1: Prepare the data
data = {
    'Hours Studied': [1, 2, 3, 4, 5],
    'Hours Slept': [5, 6, 7, 8, 9],
    'Gender': ['Male', 'Female', 'Female', 'Male', 'Male'],
    'Test Score': [50, 55, 60, 65, 70]
}

df = pd.DataFrame(data)

# Step 2: Encode Categorical Variables
encoder = OneHotEncoder(drop='first')
encoded_gender = encoder.fit_transform(df[['Gender']]).toarray()
encoded_gender_df = pd.DataFrame(encoded_gender, columns=encoder.get_feature_names_out(['Gender']))
df_encoded = pd.concat([df.drop('Gender', axis=1), encoded_gender_df], axis=1)

# Step 3: Split the data into training and testing sets
X = df_encoded.drop('Test Score', axis=1)
y = df_encoded['Test Score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Step 4: Create and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions on the test set
y_pred = model.predict(X_test)

# Step 6: Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R²):", r2)

# Step 7: Plot the coefficients
coefficients = model.coef_
features = X.columns

plt.figure(figsize=(10, 6))
plt.bar(features, coefficients)
plt.xlabel('Features')
plt.ylabel('Coefficient Value')
plt.title('Linear Regression Coefficients')
plt. ow()
