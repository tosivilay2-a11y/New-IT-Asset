const { Pool } = require('pg');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../.env') });

// Validate required environment variables
if (!process.env.DB_HOST) {
  console.error('✗ ERROR: DB_HOST is not set in .env file');
  console.error('✗ Please create .env file from .env.example and configure database settings');
  process.exit(1);
}

const config = {
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_DATABASE,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  min: 2,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
};

// Log configuration (without password)
console.log('Database Configuration:');
console.log(`  Host: ${config.host}`);
console.log(`  Port: ${config.port}`);
console.log(`  Database: ${config.database}`);
console.log(`  User: ${config.user}`);

let pool = null;

async function getConnection() {
  try {
    if (pool) {
      return pool;
    }
    pool = new Pool(config);
    
    // Test connection
    const client = await pool.connect();
    console.log('✓ Database connected successfully');
    client.release();
    
    return pool;
  } catch (error) {
    console.error('✗ Database connection failed:', error.message);
    throw error;
  }
}

async function closeConnection() {
  try {
    if (pool) {
      await pool.end();
      pool = null;
      console.log('✓ Database connection closed');
    }
  } catch (error) {
    console.error('✗ Error closing database connection:', error.message);
  }
}

// Handle process termination
process.on('SIGINT', async () => {
  await closeConnection();
  process.exit(0);
});

module.exports = {
  getConnection,
  closeConnection,
  config,
};
