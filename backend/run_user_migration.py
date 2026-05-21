#!/usr/bin/env python
"""Run the user migration to add firstname and lastname columns"""

import subprocess
import sys

def run_migration():
    try:
        print("Running migration to add firstname and lastname columns to users table...")
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=".",
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Migration completed successfully!")
        else:
            print(f"\n❌ Migration failed with return code {result.returncode}")
            return False
        
        return True
    except Exception as e:
        print(f"Error running migration: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
