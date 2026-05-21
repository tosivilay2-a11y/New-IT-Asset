"""
Asset Status Model
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class AssetStatus(Base):
    __tablename__ = "assetstatuses"
    
    statusid = Column(Integer, primary_key=True, index=True)
    statusname = Column(String(50), nullable=False, unique=True)
    statuscode = Column(String(20), unique=True, nullable=False)
    description = Column(String(500))
    color = Column(String(20), default="#6c757d")  # Bootstrap color classes
    isactive = Column(Boolean, default=True)
    
    # Relationships
    assets = relationship("Asset", back_populates="status")
