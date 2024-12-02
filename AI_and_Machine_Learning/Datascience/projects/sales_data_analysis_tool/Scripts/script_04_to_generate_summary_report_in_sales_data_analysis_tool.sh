# Navigate to the project directory
cd ~/projects/sales_data_analysis_tool

# Create a Python script to generate a summary report
echo "import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('sales_data_analysis.db')

# Read data from the sales_data table into a DataFrame
df = pd.read_sql_query('SELECT * FROM sales_data', conn)

# Generate basic statistics
basic_stats = df.describe()

# Calculate total sales by product
total_sales_by_product = df.groupby('product_name')['quantity'].sum()

# Generate a summary report
with open('summary_report.txt', 'w') as f:
    f.write('Sales Data Summary Report\\n')
    f.write('==========================\\n\\n')
    
    f.write('Basic Statistics:\\n')
    f.write(basic_stats.to_string())
    f.write('\\n\\n')
    
    f.write('Total Sales by Product:\\n')
    f.write(total_sales_by_product.to_string())
    f.write('\\n\\n')
    
    f.write('Visualizations saved as total_sales_by_product.png and total_sales_by_product_updated.png\\n')

# Close the database connection
conn.close()

print('Summary report saved as summary_report.txt in the project folder.')
" > generate_summary_report.py

# Run the Python script to generate the summary report
python3 generate_summary_report.py
