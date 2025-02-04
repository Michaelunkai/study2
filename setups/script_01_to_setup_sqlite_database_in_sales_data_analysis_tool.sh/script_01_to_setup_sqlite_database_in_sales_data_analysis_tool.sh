# Create and navigate to the project directory
mkdir -p ~/projects/sales_data_analysis_tool && cd ~/projects/sales_data_analysis_tool

# Install necessary packages
sudo apt-get update && sudo apt-get install -y python3 python3-pip sqlite3 && pip3 install pandas matplotlib sqlalchemy

# Create the Python script to set up the SQLite database
echo "import  ite3

# Connect to the database (or create it)
conn =  ite3.connect('sales_data_analysis.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product_name TEXT,
    quantity INTEGER,
    price REAL
)
''')

# Insert some sample data
cursor.executemany('''
INSERT INTO sales_data (date, product_name, quantity, price)
VALUES (?, ?, ?, ?)
''', [
    ('2024-01-01', 'Product A', 10, 9.99),
    ('2024-01-02', 'Product B', 5, 19.99),
    ('2024-01-03', 'Product C', 20, 4.99),
    ('2024-01-04', 'Product A', 15, 9.99)
])

conn.commit()
conn.close()

print('Database and table created with sample data.')
" > create_database.py

# Run the Python script to set up the SQLite database
 3 create_database.py
