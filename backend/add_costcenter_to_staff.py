"""
Migration: Add costcenterid column to staff table.

Run: python backend/add_costcenter_to_staff.py
"""
import psycopg2
import sys
from pathlib import Path

# Load backend .env
env_file = Path(__file__).parent / ".env"
db_url = "postgresql://postgres:postgres@localhost:5432/assetdb"

if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("DATABASE_URL="):
                db_url = line.split("=", 1)[1].strip()
                break

db_url = db_url.replace("postgresql+psycopg2://", "postgresql://")

def parse_db_url(url):
    url = url.replace("postgresql://", "").replace("postgres://", "")
    user_pass, rest = url.split("@")
    user, password = user_pass.split(":", 1) if ":" in user_pass else (user_pass, "")
    host_port, dbname = rest.split("/", 1)
    host, port = host_port.split(":") if ":" in host_port else (host_port, "5432")
    return user, password, host, port, dbname

try:
    user, password, host, port, dbname = parse_db_url(db_url)
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = False
    cur = conn.cursor()

    print("=" * 60)
    print("MIGRATION: Add Cost Center Relationship to Staff")
    print("=" * 60)

    # ── Step 1: Add costcenterid to staff ────────────────────────
    print("\n[Step 1] Adding costcenterid column to staff...")
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'staff' AND column_name = 'costcenterid'
    """)
    if not cur.fetchone():
        cur.execute("""
            ALTER TABLE staff
            ADD COLUMN costcenterid INTEGER REFERENCES cost_centers(costcenterid)
        """)
        print("[OK] costcenterid column added to staff table.")
    else:
        print("[SKIP] costcenterid already present in staff table.")

    conn.commit()
    print("\n" + "=" * 60)
    print("[SUCCESS] Migration completed successfully!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] Migration failed: {e}")
    if 'conn' in locals():
        conn.rollback()
    sys.exit(1)
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
