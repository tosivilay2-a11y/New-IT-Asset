#!/usr/bin/env python
"""Add cost center field to assets table"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_cost_center():
    """Add cost center field to assets table"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.begin() as conn:
            # Check if cost_center column exists
            result = conn.execute(text("PRAGMA table_info(assets)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'cost_center' not in columns:
                print("Adding cost_center column to assets table...")
                conn.execute(text("ALTER TABLE assets ADD COLUMN cost_center VARCHAR(100)"))
                print("✓ Added cost_center column successfully!")
            else:
                print("✓ cost_center column already exists")
        
        return True
        
    except Exception as e:
        print(f"✗ Error adding cost_center column: {e}")
        return False

if __name__ == "__main__":
    success = add_cost_center()
    sys.exit(0 if success else 1)