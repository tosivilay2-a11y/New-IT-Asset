"""
Company Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    companyid = Column(Integer, primary_key=True, index=True)
    companyname = Column(String(200), nullable=False)
    companycode = Column(String(10), unique=True, nullable=False)  # 4-char code (e.g., AVIS, FORD)
    provinceid = Column(Integer, ForeignKey("provinces.provinceid"))
    address = Column(String(500))
    phone = Column(String(20))
    email = Column(String(100))
    isactive = Column(Boolean, default=True)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    province = relationship("Province", back_populates="companies")
    locations = relationship("Location", back_populates="company")
    departments = relationship("Department", back_populates="company")
