import pandas as pd
import os
import numpy as np
import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': 'localhost',
    'database': 'bookstore_db'
}

# Establish connection to MySQL
def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        print("Database connection successful.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
        return None

# Function to read CSV files and insert data into the database
def insert_data_from_csv(conn, table_name, csv_file_path, columns, auto_increment_columns=[]):
    cursor = conn.cursor()
    data = pd.read_csv(csv_file_path)
    columns_to_insert = [col for col in columns if col not in auto_increment_columns]

    for _, row in data.iterrows():
        placeholders = ", ".join(["%s"] * len(columns_to_insert))
        columns_str = ", ".join(columns_to_insert)
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, columns_str, placeholders)
        values = tuple(None if pd.isna(row[column]) else int(row[column]) if isinstance(row[column], (np.int64, np.int32)) else row[column] for column in columns_to_insert)

        try:
            cursor.execute(sql, values)
        except mysql.connector.Error as err:
            print("Error inserting data into {}: {}".format(table_name, err))

    conn.commit()  # Ensure each table data insertion is committed
    cursor.close()
    print("Data inserted into {} from {}.".format(table_name, csv_file_path))

# Main script to insert data from CSV files
def main():
    conn = connect_to_database()
    if not conn:
        return

    csv_files_info = {
        '../data/db_subject.csv': ('db_subject', ['SubjectID', 'CategoryName'], ['SubjectID']),
        '../data/db_supplier.csv': ('db_supplier', ['SupplierID', 'CompanyName', 'ContactLastName', 'ContactFirstName', 'Phone'], ['SupplierID']),
        '../data/db_employee.csv': ('db_employee', ['EmployeeID', 'LastName', 'FirstName'], ['EmployeeID']),
        '../data/db_book.csv': ('db_book', ['BookID', 'Title', 'UnitPrice', 'Author', 'Quantity', 'SupplierID', 'SubjectID'], ['BookID']),
        '../data/db_customer.csv': ('db_customer', ['CustomerID', 'LastName', 'FirstName', 'Phone'], ['CustomerID']),
        '../data/db_shipper.csv': ('db_shipper', ['ShipperID', 'ShpperName'], ['ShipperID']),  # Typo handled here
        '../data/db_order.csv': ('db_order', ['OrderID', 'CustomerID', 'EmployeeID', 'OrderDate', 'ShippedDate', 'ShipperID'], ['OrderID']),
        '../data/db_order_detail.csv': ('db_order_detail', ['OrderDetailID', 'OrderID', 'BookID', 'Quantity'], ['OrderDetailID'])
    }

    for file_path, (table_name, columns, auto_increment_cols) in csv_files_info.items():
        print("Inserting data from {} into {}...".format(file_path, table_name))
        insert_data_from_csv(conn, table_name, file_path, columns, auto_increment_columns=auto_increment_cols)

    conn.close()
    print("All data inserted successfully.")

if __name__ == "__main__":
    main()