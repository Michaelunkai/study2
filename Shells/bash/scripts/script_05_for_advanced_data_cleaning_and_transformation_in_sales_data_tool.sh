# Navigate to the project directory
cd ~/projects/sales_data_analysis_tool

# Create a Python script for data cleaning and transformation
echo "import sqlite3
import pandas as pd
import numpy as np

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read data from the sales_data table into a DataFrame
df = pd.read_sql_query('SELECT * FROM sales_data', conn)

# Data Cleaning and Transformation

# Handle missing data by filling with the median for numerical columns and mode for categorical columns
df['quantity'] = df['quantity'].fillna(df['quantity'].median())
df['price'] = df['price'].fillna(df['price'].median())
df['product_name'] = df['product_name'].fillna(df['product_name'].mode()[0])

# Detect and handle outliers using the Z-score method
z_scores = np.abs((df[['quantity', 'price']] - df[['quantity', 'price']].mean()) / df[['quantity', 'price']].std())
df = df[(z_scores < 3).all(axis=1)]

# Create a new column for total sales
df['total_sales'] = df['quantity'] * df['price']

# Save the cleaned and transformed data back to the database
df.to_sql('sales_data_cleaned', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print('Data cleaned, transformed, and saved in the sales_data_cleaned table.')
" > data_cleaning_and_transformation.py

# Update the data analysis script to use the cleaned and transformed data
echo "import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read cleaned data from the sales_data_cleaned table into a DataFrame
df = pd.read_sql_query('SELECT * FROM sales_data_cleaned', conn)

# Display basic statistics
print('Basic Statistics after Cleaning and Transformation:')
print(df.describe())

# Plot total sales by product using cleaned data
total_sales_by_product = df.groupby('product_name')['total_sales'].sum()
total_sales_by_product.plot(kind='bar', title='Total Sales by Product (Cleaned Data)')
plt.xlabel('Product Name')
plt.ylabel('Total Sales')

# Save the plot as an image file within the project folder
plt.savefig('total_sales_by_product_cleaned.png')

# Close the database connection
conn.close()

print('Updated plot saved as total_sales_by_product_cleaned.png in the project folder.')
" > data_analysis_cleaned.py

# Run the Python script for data cleaning and transformation
python3 data_cleaning_and_transformation.py

# Run the updated data analysis script using cleaned data
python3 data_analysis_cleaned.py
