from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class AssetRequest(Base):
    __tablename__ = "asset_requests"
    
    requestid = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.staffid"), nullable=True)
    staff_name = Column(String, nullable=False)
    staff_email = Column(String, nullable=True)
    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.companyid"), nullable=True)
    company_name = Column(String, nullable=True)
    province_id = Column(Integer, ForeignKey("provinces.provinceid"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    asset_type = Column(String, default="Computer")
    priority = Column(String, default="Medium")  # Low, Medium, High, Urgent
    reason = Column(String, nullable=True)
    status = Column(String, default="Pending")  # Pending, Approved, Rejected
    notes = Column(String, nullable=True)
    requested_by = Column(String, nullable=True)  # email of the HR user who requested
    assigned_assetcode = Column(String, nullable=True)  # code of the asset signed/assigned
    assigned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    staff = relationship("Staff")
    company = relationship("Company")
    province = relationship("Province")
    location = relationship("Location")

    @property
    def province_name(self):
        return self.province.provincename if self.province else None

    @property
    def location_name(self):
        return self.location.name if self.location else None
