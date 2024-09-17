# MODULE INSTALL REQUIRED: mysql-connector-python, pandas
import mysql.connector
import pandas as pd
from pathlib import Path

# Define connection details
host = ""  # e.g., '192.168.1.10' or 'db.example.com'
port = "3306"  # MySQL default port
database = "prototype"  # Name of the MySQL database
user = "ethan"  # MySQL user username
password = "Ttestdb123@"  # MySQL password


# Establish connection to the remote MySQL server
myconnection = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# The cursor is what enters queries into the host sytem.
cursor = myconnection.cursor()

# Be careful! If the name is not unique, data will be added to an existing table
table_name = "BART_data_1"


csv_file = Path('C:/Users/<device_username>/Downloads/task_data_15_09_2024_23_15_23.csv')  # Path where task data is saved

# Read csv file into a dataframe
df = pd.read_csv(csv_file)


columns = df.columns
column_definitions = ", ".join([f"`{col}` VARCHAR(255)" for col in columns])


# Use fstring to construct a MySQL query (if it doesn't exist yet)
create_table_query = f"""
CREATE TABLE IF NOT EXISTS `{table_name}` (
    {column_definitions}
);
"""

cursor.execute(create_table_query)
print(f"Table `{table_name}` created (if not exists).")


# fstring to insert data into the tables
insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}) VALUES ({', '.join(['%s' for _ in columns])})"

# Insert each row into the table
for row in df.itertuples(index=False, name=None):
    cursor.execute(insert_query, row)

print(f"{cursor.rowcount} rows were inserted.")

# Commit
myconnection.commit()

# Close connection
cursor.close()
myconnection.close()
