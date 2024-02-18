import sqlite3

# Connect to the database
connection = sqlite3.connect("safety_database.db")
cursor = connection.cursor()

# Execute a query to retrieve data from the ingredients table
cursor.execute("SELECT * FROM ingredients")
rows = cursor.fetchall()

# Print the retrieved data
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()
