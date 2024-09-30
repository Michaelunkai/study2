import pandas as pd
import  ite3

# Path to your Excel file
excel_file = "/mnt/c/Users/micha/Downloads/game_list.xlsx"

# Desired name of your SQLite database file
 ite_db = "/mnt/c/Users/micha/Downloads/game_list.db"

# Load Excel file
excel_data = pd.read_excel(excel_file, sheet_name=None)  # Load all sheets

# Create a connection to SQLite database
conn =  ite3.connect( ite_db)
cursor = conn.cursor()

# Loop through each sheet in the Excel file
for sheet_name, data in excel_data.items():
    # Convert sheet to SQL table
    data.to_sql(sheet_name, conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Conversion completed successfully.")
