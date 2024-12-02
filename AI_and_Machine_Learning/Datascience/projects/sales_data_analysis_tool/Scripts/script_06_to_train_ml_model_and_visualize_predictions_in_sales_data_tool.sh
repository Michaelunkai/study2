# Navigate to the project directory
cd ~/projects/sales_data_analysis_tool

# Install additional packages required for machine learning
pip3 install scikit-learn

# Create a Python script for training a machine learning model and making predictions
echo "import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read cleaned data from the sales_data_cleaned table into a DataFrame
df = pd.read_sql_query('SELECT * FROM sales_data_cleaned', conn)

# Prepare the data for machine learning
X = df[['quantity', 'price']]
y = df['total_sales']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the model predictions to a new table in the database
predictions_df = pd.DataFrame({'quantity': X_test['quantity'], 'price': X_test['price'], 'predicted_sales': y_pred})
predictions_df.to_sql('sales_predictions', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print('Model trained and predictions saved in the sales_predictions table.')
" > train_predictive_model.py

# Create a Python script to visualize the predictions
echo "import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read the predictions from the sales_predictions table into a DataFrame
df = pd.read_sql_query('SELECT * FROM sales_predictions', conn)

# Plot the predicted sales
plt.scatter(df['quantity'], df['predicted_sales'], color='blue', label='Predicted Sales')
plt.xlabel('Quantity')
plt.ylabel('Predicted Sales')
plt.title('Predicted Sales vs Quantity')
plt.legend()

# Save the plot as an image file within the project folder
plt.savefig('predicted_sales_vs_quantity.png')

# Close the database connection
conn.close()

print('Prediction plot saved as predicted_sales_vs_quantity.png in the project folder.')
" > visualize_predictions.py

# Run the Python script to train the model and make predictions
python3 train_predictive_model.py

# Run the Python script to visualize the predictions
python3 visualize_predictions.py
