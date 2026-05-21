"""
Cost Center Model
Linked to Country/Province/Company only — no department FK
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class CostCenter(Base):
    __tablename__ = "cost_centers"
    
    costcenterid = Column(Integer, primary_key=True, index=True)
    costcentername = Column(String(150), nullable=False)
    costcentercode = Column(String(50), unique=True, nullable=False)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=False)
    provinceid = Column(Integer, ForeignKey("provinces.provinceid"), nullable=True)
    companyid = Column(Integer, ForeignKey("companies.companyid"), nullable=True)
    description = Column(String(500), nullable=True)
    isactive = Column(Boolean, default=True)
    createdat = Column(DateTime, default=datetime.utcnow)
    updatedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    country = relationship("Country")
    province = relationship("Province")
    company = relationship("Company")
