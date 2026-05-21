-- =============================================
-- Create IT Asset Management Database
-- Run this in PostgreSQL if database doesn't exist
-- =============================================

-- Create database
CREATE DATABASE it_asset_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Connect to the new database
\c it_asset_db;

-- Verify connection
SELECT current_database();

-- Show message
SELECT 'Database it_asset_db created successfully!' AS message;
