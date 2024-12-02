# Navigate to the project directory
cd ~/projects/sales_data_analysis_tool

# Create a Python script for data analysis and visualization
echo "import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read data from the sales_data table into a DataFrame
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
plt.savefig('total_sales_by_product.png')

# Close the database connection
conn.close()

print('Plot saved as total_sales_by_product.png in the project folder.')
" > data_analysis.py

# Run the Python script for data analysis and visualization
python3 data_analysis.py
