#!/usr/bin/env python
"""Create staff table in the database"""

from app.core.database import engine, Base
from app.models.staff import Staff

# Create the staff table
Base.metadata.create_all(bind=engine)
print("✓ Staff table created successfully")
