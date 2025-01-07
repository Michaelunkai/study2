import sqlite3
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

