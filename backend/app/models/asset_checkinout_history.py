from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class AssetCheckInOutHistory(Base):
    __tablename__ = "asset_checkinout_history"
    
    historyid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid"), nullable=False, index=True)
    action = Column(String, nullable=False)  # CHECKOUT or CHECKIN
    userid = Column(Integer, nullable=True)  # User who performed the action
    staffid = Column(Integer, nullable=True)  # Staff member assigned to (for checkout)
    reason = Column(String, nullable=True)
    condition_before = Column(String, nullable=True)  # Asset condition before action
    condition_after = Column(String, nullable=True)  # Asset condition after action
    location_before = Column(Integer, nullable=True)  # Location before action
    location_after = Column(Integer, nullable=True)  # Location after action
    notes = Column(Text, nullable=True)  # Additional notes
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    asset = relationship("Asset", foreign_keys=[assetid])
