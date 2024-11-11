-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS OrderDetails;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Carriers;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Subjects;

-- Create the database if it doesn't exist and use it
CREATE DATABASE IF NOT EXISTS bookstore_db;
USE bookstore_db;

-- Create Subjects Table
CREATE TABLE Subjects (
    SubjectID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100) NOT NULL
);

-- Create Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    CompanyName VARCHAR(100) NOT NULL,
    ContactLastName VARCHAR(50),
    ContactFirstName VARCHAR(50),
    Phone VARCHAR(20)
);

-- Create Employees Table
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    LastName VARCHAR(50) NOT NULL,
    FirstName VARCHAR(50) NOT NULL
);

-- Create Books Table
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(150) NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL,
    Author VARCHAR(100),
    Quantity INT NOT NULL,
    SupplierID INT,
    SubjectID INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
    FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
);

-- Create Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    LastName VARCHAR(50) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    Phone VARCHAR(20)
);

-- Create Carriers Table
CREATE TABLE Carriers (
    ShipperID INT PRIMARY KEY AUTO_INCREMENT,
    ShpperName VARCHAR(100) NOT NULL  -- Ensure column name matches CSV format if necessary
);

-- Create Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    EmployeeID INT,
    OrderDate DATE NOT NULL,
    ShippedDate DATE,
    ShipperID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (ShipperID) REFERENCES Carriers(ShipperID)
);

-- Create OrderDetails Table
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    BookID INT,
    Quantity INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);
