from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class AssetConditionReport(Base):
    __tablename__ = "asset_condition_reports"

    reportid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid"), nullable=False, index=True)
    action = Column(String(20), nullable=False, index=True)  # CHECKIN / CHECKOUT

    # Who this report is about / who performed it
    staffid = Column(Integer, nullable=True)
    userid = Column(Integer, nullable=True)

    # High-level condition
    overall_condition = Column(String(50), nullable=True)

    # Detailed sections stored as JSON text
    physical_condition = Column(Text, nullable=True)
    functional_test = Column(Text, nullable=True)
    accessories = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    asset = relationship("Asset", foreign_keys=[assetid])

