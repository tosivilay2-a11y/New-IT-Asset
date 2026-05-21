"""
Department Model — now includes costcenterid FK
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Department(Base):
    __tablename__ = "departments"
    
    departmentid = Column(Integer, primary_key=True, index=True)
    departmentname = Column(String(100), nullable=False)
    departmentcode = Column(String(20), unique=True, nullable=False)
    companyid = Column(Integer, ForeignKey("companies.companyid"), nullable=False)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=True)
    provinceid = Column(Integer, ForeignKey("provinces.provinceid"), nullable=True)
    costcenterid = Column(Integer, ForeignKey("cost_centers.costcenterid"), nullable=True)
    description = Column(String(500))
    isactive = Column(Boolean, default=True)
    
    # Relationships
    company = relationship("Company", back_populates="departments")
    country = relationship("Country")
    province = relationship("Province")
    cost_center = relationship("CostCenter")
    assets = relationship("Asset", back_populates="department")
