# Navigate to the project directory
cd ~/projects/sales_data_analysis_tool

# Create a sample CSV file for data ingestion within the project folder
echo "date,product_name,quantity,price
2024-01-05,Product D,30,14.99
2024-01-06,Product E,25,24.99
2024-01-07,Product F,40,5.99
2024-01-08,Product A,20,9.99
" > new_sales_data.csv

# Enhance the Python script for data ingestion
echo "import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read data from the CSV file into a DataFrame
new_data = pd.read_csv('new_sales_data.csv')

# Insert the new data into the sales_data table
new_data.to_sql('sales_data', conn, if_exists='append', index=False)

# Confirm the data was added and display the updated sales data
df = pd.read_sql_query('SELECT * FROM sales_data', conn)
print('Updated Sales Data:')
print(df)

# Close the database connection
conn.close()
" > ingest_data.py

# Update the data analysis script to include the new data
echo "import sqlite3
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
" > data_analysis.py

# Run the Python script to ingest data from the CSV file
python3 ingest_data.py

# Run the updated data analysis script
python3 data_analysis.py
