import os
import pandas as pd
import sqlite3

# Connect to both rookie and starter databases
rookie_conn = sqlite3.connect('rookies.db')
starter_conn = sqlite3.connect('start_check.db')
output_conn = sqlite3.connect('merged_data.db')

# Merge rookie stats with starter status
def merge_data():
    # Get list of tables in rookies.db
    cursor = rookie_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rookie_tables = [row[0] for row in cursor.fetchall()]

    # Load starter data from single 'players' table
    starter_df = pd.read_sql('SELECT * FROM players', starter_conn)
    starter_players = set(starter_df['Player'])

    all_data = []

    for table in rookie_tables:
        # Load rookie data
        rookie_df = pd.read_sql(f'SELECT * FROM {table}', rookie_conn)

        # Add binary column to indicate if player became a starter
        rookie_df['is_starter'] = rookie_df['Player'].apply(lambda x: 1 if x in starter_players else 0)
        all_data.append(rookie_df)

    # Concatenate all years into a single DataFrame if data exists
    if all_data:
        merged_df = pd.concat(all_data)

        # Save to new database
        merged_df.to_sql('merged_data', output_conn, if_exists='replace', index=False)

# Merge the data
merge_data()

# Close connections
rookie_conn.close()
starter_conn.close()
output_conn.close()
