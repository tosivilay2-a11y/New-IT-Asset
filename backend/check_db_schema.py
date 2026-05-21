#!/usr/bin/env python
"""
Check PostgreSQL database schema for assets table
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env")
    exit(1)

try:
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    # Get columns for assets table
    columns = inspector.get_columns('assets')
    
    print("Assets table columns:")
    print("-" * 80)
    for col in columns:
        print(f"Name: {col['name']:<20} Type: {str(col['type']):<20} Nullable: {col['nullable']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
