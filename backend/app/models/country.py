"""
Country Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class Country(Base):
    __tablename__ = "countries"
    
    countryid = Column(Integer, primary_key=True, index=True)
    countryname = Column(String(100), nullable=False)
    countrycode = Column(String(2), unique=True, nullable=False)  # 2-char code (e.g., LA, TH, US)
    isactive = Column(Boolean, default=True)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provinces = relationship("Province", back_populates="country")
