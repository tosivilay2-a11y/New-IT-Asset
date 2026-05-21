#!/usr/bin/env python
"""Create asset check-in/check-out history table in the database"""

from app.core.database import engine, Base
from app.models.asset_checkinout_history import AssetCheckInOutHistory

# Create the history table
Base.metadata.create_all(bind=engine)
print("✓ Asset check-in/check-out history table created successfully")
