import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('sales_data_analysis.db')
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

