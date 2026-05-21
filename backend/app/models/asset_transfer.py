"""
Asset Transfer Model - Track asset movements between locations/users
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class AssetTransfer(Base):
    __tablename__ = "assettransfers"
    
    transferid = Column(Integer, primary_key=True, index=True)
    assetid = Column(Integer, ForeignKey("assets.assetid"), nullable=False)
    
    # From location/user
    fromlocationid = Column(Integer, ForeignKey("locations.id"))
    fromuserid = Column(Integer, ForeignKey("users.userid"))
    
    # To location/user
    tolocationid = Column(Integer, ForeignKey("locations.id"))
    touserid = Column(Integer, ForeignKey("users.userid"))
    
    # Transfer details
    transferdate = Column(DateTime, default=datetime.utcnow)
    transfertype = Column(String(50))  # 'location', 'user', 'both'
    reason = Column(Text)
    notes = Column(Text)
    
    # Approval
    requestedby = Column(Integer, ForeignKey("users.userid"))
    approvedby = Column(Integer, ForeignKey("users.userid"))
    approvaldate = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, approved, rejected, completed
    
    # Relationships
    asset = relationship("Asset", back_populates="transfers")
    from_location = relationship("Location", foreign_keys=[fromlocationid])
    to_location = relationship("Location", foreign_keys=[tolocationid])
    from_user = relationship("User", foreign_keys=[fromuserid])
    to_user = relationship("User", foreign_keys=[touserid])
    requester = relationship("User", foreign_keys=[requestedby])
    approver = relationship("User", foreign_keys=[approvedby])
