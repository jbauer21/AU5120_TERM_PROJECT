<?php
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

// Ensure database is selected
$conn->select_db($dbname);

// Initialize output
$output = "";

// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $query = $_POST['query'];

    // Prevent SQL DROP statements
    if (stripos($query, 'DROP') !== false) {
        $output = "DROP statements are not allowed.";
    } else {
        // Run the query and display results
        $result = $conn->query($query);
        
        if ($result) {
            if ($result->num_rows > 0) {
                // Start building table output
                $output .= "<table border='1'><tr>";
                // Print table headers
                while ($field = $result->fetch_field()) {
                    $output .= "<th>" . htmlspecialchars($field->name) . "</th>";
                }
                $output .= "</tr>";

                // Print table rows
                while ($row = $result->fetch_assoc()) {
                    $output .= "<tr>";
                    foreach ($row as $value) {
                        $output .= "<td>" . htmlspecialchars($value) . "</td>";
                    }
                    $output .= "</tr>";
                }
                $output .= "</table>";
            } else {
                $output = "No results found.";
            }
        } else {
            $output = "Error: " . $conn->error;
        }
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Term Project Demo</title>
</head>
<body>
    <h1>Term Project Demo</h1>
    <form method="post">
        <label for="query">Query Tables</label><br>
        <textarea id="query" name="query" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Submit">
        <input type="reset" value="Clear">
    </form>
    <br>
    <div>
        <h3>Results:</h3>
        <?php echo $output; ?>
    </div>
</body>
</html>
