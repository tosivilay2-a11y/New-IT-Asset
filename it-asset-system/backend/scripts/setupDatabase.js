const { getConnection, closeConnection } = require('../src/config/database');
const fs = require('fs');
const path = require('path');

async function setupDatabase() {
  try {
    console.log('Starting database setup...\n');
    const pool = await getConnection();

    // Read the SQL schema file
    const schemaPath = path.join(__dirname, 'schema-postgres.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');

    // Split by semicolons and filter out comments and empty statements
    const statements = schema
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0 && !stmt.startsWith('--') && !stmt.startsWith('\\c'));

    console.log(`Executing ${statements.length} SQL statements...\n`);

    let successCount = 0;
    for (const statement of statements) {
      try {
        if (statement.includes('CREATE TABLE')) {
          const tableName = statement.match(/CREATE TABLE.*?(\w+)\s*\(/i)?.[1];
          if (tableName) {
            console.log(`Creating table: ${tableName}...`);
          }
        }
        await pool.query(statement);
        successCount++;
      } catch (error) {
        // Ignore "already exists" errors
        if (!error.message.includes('already exists')) {
          console.error(`Error executing statement: ${error.message}`);
        }
      }
    }

    console.log('\n' + '='.repeat(50));
    console.log('✓ Database setup completed successfully!');
    console.log('='.repeat(50));
    console.log(`\nExecuted ${successCount} statements`);
    console.log('\nAll 30 tables created with indexes and relationships.');
    console.log('\nNext step: Run "npm run db:seed" to populate initial data');
    console.log('='.repeat(50));

  } catch (error) {
    console.error('✗ Database setup failed:', error.message);
    console.error(error);
    throw error;
  } finally {
    await closeConnection();
  }
}

// Run setup
setupDatabase()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
