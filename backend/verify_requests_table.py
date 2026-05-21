import sys
from sqlalchemy import create_engine, inspect, text
from app.core.config import settings

def main():
    print(f"Connecting to database: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables found:", tables)
    
    if "asset_requests" not in tables:
        print("asset_requests table does not exist. It will be created by SQLAlchemy on backend startup.")
        return
        
    columns = [col['name'] for col in inspector.get_columns("asset_requests")]
    print("Existing columns in asset_requests:", columns)
    
    required_cols = {
        "staff_id": "INTEGER REFERENCES staff(staffid)",
        "company_id": "INTEGER REFERENCES companies(companyid)",
        "province_id": "INTEGER REFERENCES provinces(provinceid)",
        "location_id": "INTEGER REFERENCES locations(id)"
    }
    
    with engine.begin() as conn:
        for col_name, col_type in required_cols.items():
            if col_name not in columns:
                print(f"Adding column '{col_name}' ({col_type}) to 'asset_requests'...")
                try:
                    conn.execute(text(f"ALTER TABLE asset_requests ADD COLUMN {col_name} {col_type}"))
                    print(f"Successfully added column '{col_name}'!")
                except Exception as e:
                    print(f"Error adding column '{col_name}': {e}")
            else:
                print(f"Column '{col_name}' already exists.")

if __name__ == "__main__":
    main()
