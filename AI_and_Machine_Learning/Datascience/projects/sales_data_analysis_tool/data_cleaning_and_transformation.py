import sqlite3
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

