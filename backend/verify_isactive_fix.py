#!/usr/bin/env python
"""
Verify that isactive column has been fixed
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env")
    exit(1)

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Check column type and default
        result = connection.execute(text("""
            SELECT 
                column_name,
                data_type,
                column_default,
                is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'assets' AND column_name = 'isactive'
        """))
        
        row = result.fetchone()
        if row:
            col_name, data_type, default_val, nullable = row
            print(f"Column: {col_name}")
            print(f"Type: {data_type}")
            print(f"Default: {default_val}")
            print(f"Nullable: {nullable}")
            
            if data_type in ['integer', 'boolean']:
                print("\n✅ Column type is correct!")
            else:
                print(f"\n⚠️ Column type is {data_type}, expected integer or boolean")
        else:
            print("❌ Column not found")
            
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
