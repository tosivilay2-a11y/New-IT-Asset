from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class Asset(Base):
    __tablename__ = "assets"
    
    assetid = Column(Integer, primary_key=True, index=True)
    
    # Asset Identification
    assetcode = Column(String(50), unique=True, nullable=False, index=True)  # Generated ID
    assetname = Column(String(200), nullable=False)
    serialnumber = Column(String(100))
    modelnumber = Column(String(100))
    manufacturer = Column(String(100))
    
    # Categorization
    maincategoryid = Column(Integer, ForeignKey("maincategories.maincategoryid"), nullable=False)
    categoryid = Column(Integer, ForeignKey("categories.id"))
    
    # Location Hierarchy
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=False)
    provinceid = Column(Integer, ForeignKey("provinces.provinceid"), nullable=False)
    companyid = Column(Integer, ForeignKey("companies.companyid"), nullable=False)
    locationid = Column(Integer, ForeignKey("locations.id"), nullable=False)
    departmentid = Column(Integer, ForeignKey("departments.departmentid"))
    
    # Stock Location
    # PostgreSQL schema uses integer[] for stock IDs
    stockid = Column(ARRAY(Integer), nullable=True)
    
    # Assignment
    assignedto = Column(Integer, nullable=True)  # Staff member ID (no FK constraint - can be staff or user)
    assigneddate = Column(DateTime, nullable=True)
    
    # Financial
    purchasedate = Column(DateTime, nullable=True)
    purchaseprice = Column(Float)
    currentvalue = Column(Float)
    depreciationrate = Column(Float)  # Annual depreciation %
    warrantyexpiry = Column(DateTime, nullable=True)
    
    # Purchase Order
    po_number = Column(String(100))  # Purchase Order Number
    po_attachment_path = Column(String(500))  # File path for PO attachment
    
    # Cost Center
    cost_center = Column(String(100))  # Cost center for accounting
    
    # Status
    statusid = Column(Integer, ForeignKey("assetstatuses.statusid"), nullable=False)
    condition = Column(String(50))  # Excellent, Good, Fair, Poor
    
    # Technical Specs
    specifications = Column(Text)  # JSON or text field for flexible specs
    
    # QR Code
    qrcode = Column(Text)  # Base64 encoded QR code image
    
    # Tracking
    isactive = Column(Integer, default=1)  # Use Integer (1=true, 0=false) for PostgreSQL compatibility
    createdat = Column(DateTime, nullable=True)  # Will be set explicitly in routes
    updatedat = Column(DateTime, nullable=True)  # Will be set explicitly in routes
    createdby = Column(Integer, ForeignKey("users.userid"))
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    main_category = relationship("MainCategory", back_populates="assets")
    category = relationship("Category", back_populates="assets")
    country = relationship("Country")
    province = relationship("Province")
    company = relationship("Company")
    location = relationship("Location", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    status = relationship("AssetStatus", back_populates="assets")
    creator = relationship("User", foreign_keys=[createdby])
    transfers = relationship("AssetTransfer", back_populates="asset")
