#!/usr/bin/env python
"""Test if backend can start"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("Testing backend imports...")
    from app.main import app
    print("✓ Successfully imported app")
    
    from app.core.database import engine
    print("✓ Successfully imported database engine")
    
    # Test database connection
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Database connection successful")
    
    print("\n✓ All checks passed! Backend should work.")
    print("\nYou can now start the server with:")
    print("python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
