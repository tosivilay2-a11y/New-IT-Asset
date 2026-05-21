#!/usr/bin/env python
"""
Recreate assets table with correct schema
This will drop and recreate the table to match the SQLAlchemy models
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
        print("Dropping existing assets table...")
        try:
            connection.execute(text("DROP TABLE IF EXISTS assets CASCADE"))
            connection.commit()
            print("✅ Table dropped")
        except Exception as e:
            print(f"⚠️ Could not drop table: {e}")
        
        print("\nRecreating assets table from SQLAlchemy models...")
        
        # Import models to create tables
        from app.models.asset import Asset
        from app.core.database import Base
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Assets table recreated successfully!")
        
        # Verify
        result = connection.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'assets'
            ORDER BY ordinal_position
        """))
        
        print("\nAssets table schema:")
        print("-" * 60)
        for row in result:
            print(f"{row[0]:<25} {row[1]}")
    
    print("\n✅ Done!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
