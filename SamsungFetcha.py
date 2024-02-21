import zipfile , os , sqlite3 , gzip , blackboxprotobuf , csv

filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = r"K:/TheProjectAIF/ITF/dbFolder"

openedZipfile = zipfile.ZipFile(filePath, mode="r")

for filename in openedZipfile.namelist():
    print("File: ", filename)


def extract_sqlite_data(db_path, query):
    """
    Extracts data from an SQLite database based on a provided SQL query.
    
    :param db_path: Path to the SQLite database file.
    :param query: SQL query to execute for data extraction.
    """
    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Execute the provided query
        cursor.execute(query)
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()
        
        # Print the rows
        for row in rows:
            print(row)
            
    finally:
        # Ensure the connection is closed even if an error occurs
        connection.close()

# Example usage
db_path = 'path/to/your/database_file.db'  # Update this path to the actual database file
query = 'SELECT * FROM your_table_name'  # Update the query based on what you're looking for
extract_sqlite_data(db_path, query)

        