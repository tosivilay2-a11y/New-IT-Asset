from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class Staff(Base):
    __tablename__ = "staff"
    
    staffid = Column(Integer, primary_key=True, index=True)
    employeeid = Column(String, unique=True, index=True, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=True, index=True)
    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    employmentstatus = Column(String, default="Active")  # Active, Inactive, On Leave, Terminated
    
    # Company and Location Links
    companyid = Column(Integer, ForeignKey("companies.companyid"), nullable=True, index=True)
    locationid = Column(Integer, ForeignKey("locations.id"), nullable=True, index=True)
    costcenterid = Column(Integer, ForeignKey("cost_centers.costcenterid"), nullable=True, index=True)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=True, index=True)
    provinceid = Column(Integer, ForeignKey("provinces.provinceid"), nullable=True, index=True)
    departmentid = Column(Integer, ForeignKey("departments.departmentid"), nullable=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cost_center = relationship("CostCenter")
    country = relationship("Country")
    province = relationship("Province")
    company = relationship("Company")
    location = relationship("Location")
    department_rel = relationship("Department")

