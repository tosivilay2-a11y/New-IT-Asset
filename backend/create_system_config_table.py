#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.system_config import SystemConfig

def create_system_config_table():
    """Create the system_configs table"""
    try:
        print("Creating system_configs table...")
        
        # Create the table
        Base.metadata.create_all(bind=engine, tables=[SystemConfig.__table__])
        
        print("✅ system_configs table created successfully!")
        
        # Add some default configurations
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Check if any configs already exist
            existing_count = db.query(SystemConfig).count()
            
            if existing_count == 0:
                print("Adding default configurations...")
                
                default_configs = [
                    SystemConfig(
                        config_key="storage_type",
                        config_value="local",
                        config_type="string",
                        description="File storage type (local or r2)",
                        category="storage"
                    ),
                    SystemConfig(
                        config_key="max_file_size",
                        config_value="10485760",  # 10MB in bytes
                        config_type="number",
                        description="Maximum file upload size in bytes",
                        category="storage"
                    ),
                    SystemConfig(
                        config_key="allowed_file_types",
                        config_value=".pdf,.jpg,.jpeg,.png,.gif,.doc,.docx,.xls,.xlsx",
                        config_type="string",
                        description="Allowed file extensions for uploads",
                        category="storage"
                    )
                ]
                
                for config in default_configs:
                    db.add(config)
                
                db.commit()
                print(f"✅ Added {len(default_configs)} default configurations")
            else:
                print(f"Found {existing_count} existing configurations, skipping defaults")
                
        except Exception as e:
            print(f"Error adding default configurations: {e}")
            db.rollback()
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating system_configs table: {e}")
        return False

if __name__ == "__main__":
    success = create_system_config_table()
    sys.exit(0 if success else 1)