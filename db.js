const mysql = require('mysql2');

// Create a connection pool
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '', // Your MySQL password
  database: 'your_database_name'
});

// Export a promise-based query interface
const promisePool = pool.promise();

module.exports = {
  createUser: async (userData) => {
    const [result] = await promisePool.query('INSERT INTO users SET ?', userData);
    return result;
  },
  getUserByEmail: async (email) => {
    const [rows] = await promisePool.query('SELECT * FROM users WHERE email = ?', [email]);
    return rows[0];
  },
  createProduct: async (productData) => {
    const [result] = await promisePool.query('INSERT INTO products SET ?', productData);
    return result;
  },
  getAllProducts: async () => {
    const [rows] = await promisePool.query('SELECT * FROM products');
    return rows;
  },
  createOrder: async (orderData) => {
    const [result] = await promisePool.query('INSERT INTO orders SET ?', orderData);
    return result;
  },
  getAllOrders: async () => {
    const [rows] = await promisePool.query('SELECT * FROM orders');
    return rows;
  }
};
