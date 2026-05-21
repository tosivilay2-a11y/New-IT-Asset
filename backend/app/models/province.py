"""
Province Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class Province(Base):
    __tablename__ = "provinces"
    
    provinceid = Column(Integer, primary_key=True, index=True)
    provincename = Column(String(100), nullable=False)
    provincecode = Column(String(3), nullable=False)  # 3-char code (e.g., VTE, LPB, BKK)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=False)
    isactive = Column(Boolean, default=True)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    country = relationship("Country", back_populates="provinces")
    companies = relationship("Company", back_populates="province")
