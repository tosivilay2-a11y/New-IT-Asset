#!/usr/bin/env python3
"""
Add stockid column to assets table
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env file")
    exit(1)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        # Check if column already exists
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='assets' AND column_name='stockid'
        """))
        
        if result.fetchone():
            print("✅ stockid column already exists")
        else:
            print("Adding stockid column to assets table...")
            
            # Add the column
            connection.execute(text("""
                ALTER TABLE assets 
                ADD COLUMN stockid INTEGER REFERENCES stocklocation(stockid)
            """))
            
            connection.commit()
            print("✅ stockid column added successfully")
            
            # Verify
            result = connection.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name='assets' AND column_name='stockid'
            """))
            
            row = result.fetchone()
            if row:
                print(f"✅ Verified: {row[0]} ({row[1]})")
            
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n✅ Migration complete!")
