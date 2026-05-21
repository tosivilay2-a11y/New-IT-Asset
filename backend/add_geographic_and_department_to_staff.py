import os
import sys
from pathlib import Path
import psycopg2

backend_dir = Path(__file__).resolve().parent
env_file = backend_dir / ".env"
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
    print(f"Connecting to database to check staff table schema...")
    user, password, host, port, dbname = parse_db_url(db_url)
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check existing columns
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'staff'
    """)
    existing_cols = {row[0] for row in cur.fetchall()}
    print(f"Existing staff columns: {existing_cols}")
    
    # Columns to add
    cols_to_add = {
        "countryid": "ALTER TABLE staff ADD COLUMN countryid INTEGER REFERENCES countries(countryid)",
        "provinceid": "ALTER TABLE staff ADD COLUMN provinceid INTEGER REFERENCES provinces(provinceid)",
        "departmentid": "ALTER TABLE staff ADD COLUMN departmentid INTEGER REFERENCES departments(departmentid)"
    }
    
    for col_name, sql in cols_to_add.items():
        if col_name not in existing_cols:
            print(f"Adding column '{col_name}'...")
            cur.execute(sql)
            print(f"[OK] Added '{col_name}' successfully.")
        else:
            print(f"Column '{col_name}' already exists in staff table.")
            
    cur.close()
    conn.close()
    print("Migration completed successfully.")
except Exception as e:
    print(f"[ERROR] Migration failed: {e}")
    sys.exit(1)
