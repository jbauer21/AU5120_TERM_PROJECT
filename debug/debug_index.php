<?php
// Database connection configuration
$servername = "localhost";
$username = getenv('DB_USER') ?: 'your_username'; // Replace with actual username for testing
$password = getenv('DB_PASSWORD') ?: 'your_password'; // Replace with actual password for testing
$dbname = "bookstore_db"; // Directly use the database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {
    echo "Database connection successful.<br>";
}

// Test 1: Check if database is selected
if ($conn->select_db($dbname)) {
    echo "Database selected successfully: $dbname<br>";
} else {
    echo "Failed to select database: " . $conn->error . "<br>";
}

// Test 2: Check if tables exist
$tables = ['Subjects', 'Suppliers', 'Books', 'Customers', 'Carriers', 'Orders', 'OrderDetails', 'Employees'];
foreach ($tables as $table) {
    $result = $conn->query("SHOW TABLES LIKE '$table';");
    if ($result && $result->num_rows > 0) {
        echo "Table '$table' exists.<br>";
    } else {
        echo "Table '$table' does NOT exist or query failed: " . $conn->error . "<br>";
    }
}

// Test 3: Run a basic SELECT query
$query = "SELECT Title, UnitPrice FROM Books WHERE Quantity > 10;";
echo "Running query: $query<br>";
$result = $conn->query($query);

if ($result) {
    if ($result->num_rows > 0) {
        echo "Query executed successfully. Displaying results:<br><br>";
        // Display results in a table
        echo "<table border='1'><tr>";
        // Print table headers
        while ($field = $result->fetch_field()) {
            echo "<th>" . htmlspecialchars($field->name) . "</th>";
        }
        echo "</tr>";

        // Print table rows
        while ($row = $result->fetch_assoc()) {
            echo "<tr>";
            foreach ($row as $value) {
                echo "<td>" . htmlspecialchars($value) . "</td>";
            }
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "Query executed successfully but returned no results.<br>";
    }
} else {
    echo "Error executing query: " . $conn->error . "<br>";
}

$conn->close();
?>
