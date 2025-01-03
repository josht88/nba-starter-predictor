import sqlite3
import pandas as pd
import os

# File path for SQLite database
rookie_db = 'rookies.db'

# Define required columns for processing
columns_needed = ['Player', 'FG%', '3P%', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK']

# Create SQLite database
conn_rookie = sqlite3.connect(rookie_db)

# Process all rookie CSV files in the current directory
for file in os.listdir():
    if file.startswith('rookies_') and file.endswith('.csv'):
        year = file.split('_')[1].split('.')[0]  # Extract year from filename

        # Load data from CSV, skipping bad lines if necessary
        rookies = pd.read_csv(file, skiprows=1)

        # Display columns for debugging
        print(f"Processing {file}")
        print("Columns in file:", rookies.columns.tolist())

        # Strip spaces from columns
        rookies.columns = rookies.columns.str.strip()

        # Map required columns explicitly
        col_mapping = {
            'Player': 'Player',
            'FG%': 'FG%',
            '3P%': '3P%',
            'MP': 'MP.1',
            'PTS': 'PTS.1',
            'TRB': 'TRB.1',
            'AST': 'AST.1',
            'STL': 'STL.1',
            'BLK': 'BLK.1'
        }

        # Verify all required columns are found
        missing_columns = [col for col in col_mapping.values() if col not in rookies.columns]
        if missing_columns:
            print(f"Skipping {file} due to missing columns: {missing_columns}")
            continue

        # Filter and rename columns
        rookies = rookies[list(col_mapping.values())]
        rookies.columns = columns_needed

        # Replace invalid or missing values with 0
        rookies = rookies.replace(['', ' ', None, '-'], 0)

        # Ensure numeric columns are properly converted
        numeric_columns = ['FG%', '3P%', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK']
        for col in numeric_columns:
            rookies[col] = pd.to_numeric(rookies[col], errors='coerce').fillna(0)

        # Write to database with year-specific table
        rookies.to_sql(f'rookies_{year}', conn_rookie, if_exists='replace', index=False)
        print(f"Table rookies_{year} created successfully.")

# Close database connection
conn_rookie.close()

print('Rookie database processing complete.')
