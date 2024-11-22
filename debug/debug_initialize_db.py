import os
import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': 'localhost',  # or your specific database host
    'database': 'bookstore_db'
}

try:
    # Connect to the database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Read and execute the SQL file
    with open('../sql/initialize_db.sql', 'r') as sql_file:
        sql_script = sql_file.read()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)

    # Check if tables exist
    tables = ['Subjects', 'Suppliers', 'Books', 'Customers', 'Carriers', 'Orders', 'OrderDetails', 'Employees']
    for table in tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}';")
        result = cursor.fetchone()
        if result:
            print(f"Table '{table}' created successfully.")
        else:
            print(f"Table '{table}' NOT found. There might be an issue.")

    cnx.commit()
    cursor.close()
    cnx.close()
    print("Database initialization completed.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)
except Exception as e:
    print(f"An error occurred: {e}")
