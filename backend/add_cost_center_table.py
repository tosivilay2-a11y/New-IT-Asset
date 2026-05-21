"""
Migration: Add cost_centers table and remove costcenter column from departments.

- Creates the cost_centers table
- Migrates any existing costcenter values from departments to cost_centers
- Drops the costcenter column from departments

Run with: python add_cost_center_table.py
"""
import psycopg2
import os
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

# Strip SQLAlchemy driver prefix to get plain psycopg2 URL
db_url = db_url.replace("postgresql+psycopg2://", "postgresql://")

def parse_db_url(url):
    url = url.replace("postgresql://", "").replace("postgres://", "")
    user_pass, rest = url.split("@")
    if ":" in user_pass:
        user, password = user_pass.split(":", 1)
    else:
        user, password = user_pass, ""
    host_port, dbname = rest.split("/", 1)
    if ":" in host_port:
        host, port = host_port.split(":")
    else:
        host, port = host_port, "5432"
    return user, password, host, port, dbname

try:
    user, password, host, port, dbname = parse_db_url(db_url)
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password,
        host=host, port=port
    )
    conn.autocommit = False
    cur = conn.cursor()
    print("=" * 60)
    print("MIGRATION: Cost Centers Table + Department Cleanup")
    print("=" * 60)

    # --- Step 1: Create cost_centers table ---
    print("\n[Step 1] Creating cost_centers table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cost_centers (
            costcenterid   SERIAL PRIMARY KEY,
            costcentername VARCHAR(150) NOT NULL,
            costcentercode VARCHAR(50) UNIQUE NOT NULL,
            countryid      INTEGER REFERENCES countries(countryid),
            provinceid     INTEGER REFERENCES provinces(provinceid),
            companyid      INTEGER REFERENCES companies(companyid),
            departmentid   INTEGER REFERENCES departments(departmentid),
            description    VARCHAR(500),
            isactive       BOOLEAN DEFAULT TRUE,
            createdat      TIMESTAMP DEFAULT NOW(),
            updatedat      TIMESTAMP DEFAULT NOW()
        )
    """)
    print("[OK] cost_centers table created (or already exists).")

    # --- Step 2: Migrate existing costcenter strings from departments ---
    print("\n[Step 2] Migrating existing costcenter data from departments...")

    # Check if costcenter column still exists in departments
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'departments' AND column_name = 'costcenter'
    """)
    has_col = cur.fetchone()

    if has_col:
        cur.execute("""
            SELECT departmentid, departmentname, departmentcode,
                   companyid, countryid, provinceid, costcenter
            FROM departments
            WHERE costcenter IS NOT NULL AND costcenter != ''
        """)
        rows = cur.fetchall()
        migrated = 0
        for row in rows:
            dept_id, dept_name, dept_code, company_id, country_id, province_id, cc_code = row
            # Generate a name from department name
            cc_name = f"{dept_name} Cost Center"
            # Check if code already exists in cost_centers
            cur.execute("SELECT costcenterid FROM cost_centers WHERE costcentercode = %s", (cc_code,))
            exists = cur.fetchone()
            if not exists and country_id:
                cur.execute("""
                    INSERT INTO cost_centers
                        (costcentername, costcentercode, countryid, provinceid, companyid, departmentid, isactive)
                    VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                """, (cc_name, cc_code, country_id, province_id, company_id, dept_id))
                migrated += 1
                print(f"   Migrated: {cc_code} -> {cc_name} (dept: {dept_name})")
        print(f"[OK] Migrated {migrated} cost center records.")

        # --- Step 3: Drop costcenter column from departments ---
        print("\n[Step 3] Dropping costcenter column from departments table...")
        cur.execute("ALTER TABLE departments DROP COLUMN costcenter")
        print("[OK] costcenter column removed from departments.")
    else:
        print("[SKIP] costcenter column does not exist in departments (already migrated).")

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
