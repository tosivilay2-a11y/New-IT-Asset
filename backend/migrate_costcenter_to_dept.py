"""
Migration:
1. Drop departmentid column from cost_centers (cost centers no longer own a dept)
2. Add costcenterid column to departments (depts now reference a cost center)

Run: python backend/migrate_costcenter_to_dept.py
"""
import psycopg2
import sys
from pathlib import Path

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
    print("MIGRATION: Flip Cost Center <-> Department Relationship")
    print("=" * 60)

    # ── Step 1: Drop departmentid from cost_centers ──────────────
    print("\n[Step 1] Removing departmentid from cost_centers...")
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'cost_centers' AND column_name = 'departmentid'
    """)
    if cur.fetchone():
        cur.execute("ALTER TABLE cost_centers DROP COLUMN IF EXISTS departmentid")
        print("[OK] departmentid column dropped from cost_centers.")
    else:
        print("[SKIP] departmentid not present in cost_centers.")

    # ── Step 2: Add costcenterid to departments ───────────────────
    print("\n[Step 2] Adding costcenterid to departments...")
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'departments' AND column_name = 'costcenterid'
    """)
    if not cur.fetchone():
        cur.execute("""
            ALTER TABLE departments
            ADD COLUMN costcenterid INTEGER REFERENCES cost_centers(costcenterid)
        """)
        print("[OK] costcenterid column added to departments.")
    else:
        print("[SKIP] costcenterid already present in departments.")

    conn.commit()
    print("\n" + "=" * 60)
    print("[SUCCESS] Migration completed!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] Migration failed: {e}")
    if 'conn' in locals():
        conn.rollback()
    sys.exit(1)
finally:
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()
