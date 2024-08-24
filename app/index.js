// db.js - MySQL database connection setup

const mysql = require('mysql');
require('dotenv').config(); // Load environment variables

// Create a connection pool to handle multiple connections (recommended for production)
const pool = mysql.createPool({
  connectionLimit: 10, // adjust as needed
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

// Attempt to connect to the database
pool.getConnection((err, connection) => {
  if (err) {
    console.error('Database connection error:', err.stack);
    return;
  }
  console.log('MySQL connected as id ' + connection.threadId);
  connection.release(); // Release the connection
});

module.exports = pool;

// // Import necessary modules
// const express = require('express');
// const cors = require('cors');
// const mongoose = require('mongoose'); // Import Mongoose if using MongoDB
// require('dotenv').config(); // To load environment variables from a .env file

// // Create an Express application
// const app = express();
// const PORT = process.env.PORT || 3000;

// // CORS configuration
// const corsOptions = {
//   origin: 'http://localhost:3000/', // Replace with your frontend URL
//   methods: ['GET', 'POST', 'PUT', 'DELETE'],
//   allowedHeaders: ['Content-Type', 'Authorization']
// };

// app.use(cors(corsOptions));

// // Middleware to parse JSON request body
// app.use(express.json());

// // Database connection (example using MongoDB with Mongoose)
// const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/mydatabase';
// mongoose.connect(MONGODB_URI, {
//   useNewUrlParser: true,
//   useUnifiedTopology: true
// })
// .then(() => console.log('MongoDB connected'))
// .catch(err => console.error('MongoDB connection error:', err));

// // Example route handler
// app.get('/api/users', (req, res) => {
//   // Replace with your actual route handler logic
//   res.json({ message: 'Hello from your API!' });
// });

// // Start the server
// app.listen(PORT, () => {
//   console.log(`Server listening on http://localhost:${PORT}`);
// });

