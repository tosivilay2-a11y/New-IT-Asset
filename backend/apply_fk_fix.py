#!/usr/bin/env python3
"""
Apply the foreign key constraint removal migration
Run this after updating the model
"""
import subprocess
import sys

def run_migration():
    """Run the Alembic migration"""
    try:
        print("Applying migration to remove assignedto foreign key constraint...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=".",
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migration applied successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Migration failed!")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
