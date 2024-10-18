import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read updated data from the sales_data table into a DataFrame
df = pd.read_sql_query('SELECT * FROM sales_data', conn)

# Display basic statistics
print('Basic Statistics:')
print(df.describe())

# Plot total sales by product
total_sales_by_product = df.groupby('product_name')['quantity'].sum()
total_sales_by_product.plot(kind='bar', title='Total Sales by Product')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Sold')

# Save the plot as an image file within the project folder
plt.savefig('total_sales_by_product_updated.png')

# Close the database connection
conn.close()

print('Updated plot saved as total_sales_by_product_updated.png in the project folder.')

