#!/usr/bin/env python3
"""Sync .env R2 credentials into the system_configs database table"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.core.database import SessionLocal
from app.models.system_config import SystemConfig

def sync():
    db = SessionLocal()
    try:
        updates = {
            "storage_type":       os.getenv("STORAGE_TYPE", "r2"),
            "r2_account_id":      os.getenv("R2_ACCOUNT_ID", ""),
            "r2_access_key_id":   os.getenv("R2_ACCESS_KEY_ID", ""),
            "r2_secret_access_key": os.getenv("R2_SECRET_ACCESS_KEY", ""),
            "r2_bucket_name":     os.getenv("R2_BUCKET_NAME", ""),
            "r2_endpoint_url":    os.getenv("R2_ENDPOINT_URL", ""),
            "r2_public_url":      os.getenv("R2_PUBLIC_URL", ""),
        }
        for key, value in updates.items():
            row = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
            if row:
                row.config_value = value
            else:
                db.add(SystemConfig(config_key=key, config_value=value,
                                    config_type="string", category="storage"))
            print(f"  {'***' if 'secret' in key else value}  → {key}")
        db.commit()
        print("✅ DB synced with .env")
    except Exception as e:
        db.rollback()
        print(f"❌ {e}")
    finally:
        db.close()

if __name__ == "__main__":
    sync()
