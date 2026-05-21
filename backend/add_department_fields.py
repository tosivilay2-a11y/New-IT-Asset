import sys
from sqlalchemy import create_engine, inspect, text
from app.core.config import settings

def main():
    print(f"Connecting to database: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables found:", tables)
    
    if "departments" not in tables:
        print("departments table does not exist. Something is wrong.")
        return
        
    columns = [col['name'] for col in inspector.get_columns("departments")]
    print("Existing columns in departments:", columns)
    
    required_cols = {
        "countryid": "INTEGER REFERENCES countries(countryid)",
        "provinceid": "INTEGER REFERENCES provinces(provinceid)",
        "costcenter": "VARCHAR(100)"
    }
    
    with engine.begin() as conn:
        for col_name, col_type in required_cols.items():
            if col_name not in columns:
                print(f"Adding column '{col_name}' ({col_type}) to 'departments'...")
                try:
                    conn.execute(text(f"ALTER TABLE departments ADD COLUMN {col_name} {col_type}"))
                    print(f"Successfully added column '{col_name}'!")
                except Exception as e:
                    print(f"Error adding column '{col_name}': {e}")
            else:
                print(f"Column '{col_name}' already exists.")

if __name__ == "__main__":
    main()
