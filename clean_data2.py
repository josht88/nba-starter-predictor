import os
import pandas as pd
import sqlite3

# Create or connect to SQLite database
conn = sqlite3.connect('start_check.db')
cursor = conn.cursor()

# Create a new table in the database
cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                Player TEXT,
                G INTEGER,
                GS INTEGER)''')

# Function to process CSV files and filter data
def process_csv_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith("start_check_") and filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Read the CSV file
            df = pd.read_csv(file_path)

            # Filter the required columns
            df_filtered = df[['Player', 'G', 'GS']]

            # Apply the condition 0.75 * G <= GS
            df_filtered = df_filtered[df_filtered['GS'] >= 0.75 * df_filtered['G']]

            # Append data to the database
            df_filtered.to_sql('players', conn, if_exists='append', index=False)

# Folder containing CSV files
folder_path = './start_check_csv_files'
os.makedirs(folder_path, exist_ok=True)

# Process the CSV files
process_csv_files(folder_path)

# Commit and close the database connection
conn.commit()
conn.close()
