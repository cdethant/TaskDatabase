const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json()); // To parse JSON request body

// Configure MySQL connection
const db = mysql.createConnection({
  host: 'your_mysql_host', // Replace with your MySQL host
  user: 'your_mysql_user', // Replace with your MySQL username
  password: 'your_mysql_password', // Replace with your MySQL password
  database: 'task_data' // Replace with your MySQL database name
});

// Connect to MySQL
db.connect(err => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to the MySQL database.');
});

// Endpoint to handle incoming CSV-like data
app.post('/save-csv', (req, res) => {
  const { timestamp, results } = req.body;

  // Prepare the query for inserting data
  const insertQuery = `
    INSERT INTO task_results (balloonType, outcome, reactionTime, inflationTime, totalReward, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
  `;

  // Insert each row into the MySQL database
  results.forEach(row => {
    const { balloonType, outcome, reactionTime, inflationTime, totalReward } = row;

    db.query(insertQuery, [balloonType, outcome, reactionTime, inflationTime, totalReward, timestamp], (err) => {
      if (err) {
        console.error('Error inserting data into MySQL:', err);
        return res.status(500).json({ status: 'error', message: 'Failed to save data to the database.' });
      }
    });
  });

  res.status(200).json({ status: 'success', message: 'Data saved to the database successfully!' });
});

// Start the server
const PORT = 8000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
