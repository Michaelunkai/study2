import sqlite3
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

