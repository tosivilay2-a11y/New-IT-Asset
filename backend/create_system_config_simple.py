#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set working directory to backend
os.chdir(backend_dir)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Now import the app modules
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
                        config_value="r2",  # Set to r2 by default since we have R2 configured
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
                    ),
                    # Add R2 configuration from environment
                    SystemConfig(
                        config_key="r2_account_id",
                        config_value=os.getenv("R2_ACCOUNT_ID", ""),
                        config_type="string",
                        description="Cloudflare R2 Account ID",
                        category="storage"
                    ),
                    SystemConfig(
                        config_key="r2_access_key_id",
                        config_value=os.getenv("R2_ACCESS_KEY_ID", ""),
                        config_type="string",
                        description="Cloudflare R2 Access Key ID",
                        category="storage"
                    ),
                    SystemConfig(
                        config_key="r2_secret_access_key",
                        config_value=os.getenv("R2_SECRET_ACCESS_KEY", ""),
                        config_type="string",
                        description="Cloudflare R2 Secret Access Key",
                        category="storage",
                        is_encrypted=True
                    ),
                    SystemConfig(
                        config_key="r2_bucket_name",
                        config_value=os.getenv("R2_BUCKET_NAME", ""),
                        config_type="string",
                        description="Cloudflare R2 Bucket Name",
                        category="storage"
                    ),
                    SystemConfig(
                        config_key="r2_endpoint_url",
                        config_value=os.getenv("R2_ENDPOINT_URL", ""),
                        config_type="string",
                        description="Cloudflare R2 Endpoint URL",
                        category="storage"
                    ),
                    SystemConfig(
                        config_key="r2_public_url",
                        config_value=os.getenv("R2_PUBLIC_URL", ""),
                        config_type="string",
                        description="Cloudflare R2 Public URL",
                        category="storage"
                    )
                ]
                
                for config in default_configs:
                    db.add(config)
                
                db.commit()
                print(f"✅ Added {len(default_configs)} default configurations")
                
                # Show what was added
                print("\nAdded configurations:")
                for config in default_configs:
                    value = config.config_value
                    if config.is_encrypted and value:
                        value = "***" + value[-4:] if len(value) > 4 else "***"
                    print(f"  - {config.config_key}: {value}")
                    
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
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_system_config_table()
    sys.exit(0 if success else 1)