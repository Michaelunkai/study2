import sqlite3
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

