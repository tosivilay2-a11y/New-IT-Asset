#!/usr/bin/env python
"""
Test asset creation to see if the isactive fix works
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from app.core.database import engine, SessionLocal
    from app.models.asset import Asset
    from datetime import datetime
    
    print("Testing asset creation...")
    
    # Create a test asset
    db = SessionLocal()
    
    test_asset = Asset(
        assetcode="TEST001",
        assetname="Test Asset",
        maincategoryid=1,
        countryid=1,
        provinceid=1,
        companyid=1,
        locationid=1,
        statusid=1,
        isactive=1,  # Use integer 1 instead of boolean True
        createdat=datetime.utcnow(),
        updatedat=datetime.utcnow(),
        createdby=1
    )
    
    db.add(test_asset)
    db.commit()
    
    print("✅ Asset created successfully!")
    print(f"Asset ID: {test_asset.assetid}")
    print(f"Asset Code: {test_asset.assetcode}")
    print(f"isactive: {test_asset.isactive}")
    
    db.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
