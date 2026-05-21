from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AssetBase(BaseModel):
    assetname: str
    assetcode: Optional[str] = None
    serialnumber: Optional[str] = None
    modelnumber: Optional[str] = None
    manufacturer: Optional[str] = None
    
    # Categorization
    maincategoryid: int
    categoryid: Optional[int] = None
    
    # Location Hierarchy
    countryid: int
    provinceid: int
    companyid: int
    locationid: int
    departmentid: Optional[int] = None
    stockid: Optional[list[int]] = None
    
    # Assignment
    assignedto: Optional[int] = None
    assigneddate: Optional[datetime] = None
    
    # Financial
    purchasedate: Optional[datetime] = None
    purchaseprice: Optional[float] = None
    currentvalue: Optional[float] = None
    depreciationrate: Optional[float] = None
    warrantyexpiry: Optional[datetime] = None
    
    # Purchase Order
    po_number: Optional[str] = None
    po_attachment_path: Optional[str] = None
    
    # Cost Center
    cost_center: Optional[str] = None
    
    # Status
    statusid: int
    condition: Optional[str] = None
    
    # Technical Specs
    specifications: Optional[str] = None
    
    # Notes
    notes: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    assetname: Optional[str] = None
    serialnumber: Optional[str] = None
    modelnumber: Optional[str] = None
    manufacturer: Optional[str] = None
    categoryid: Optional[int] = None
    locationid: Optional[int] = None
    departmentid: Optional[int] = None
    assignedto: Optional[int] = None
    assigneddate: Optional[datetime] = None
    purchasedate: Optional[datetime] = None
    purchaseprice: Optional[float] = None
    currentvalue: Optional[float] = None
    depreciationrate: Optional[float] = None
    warrantyexpiry: Optional[datetime] = None
    po_number: Optional[str] = None
    po_attachment_path: Optional[str] = None
    cost_center: Optional[str] = None
    statusid: Optional[int] = None
    condition: Optional[str] = None
    specifications: Optional[str] = None
    notes: Optional[str] = None

class AssetResponse(AssetBase):
    assetid: int
    qrcode: Optional[str] = None
    isactive: bool
    createdat: datetime
    updatedat: datetime
    createdby: Optional[int] = None
    
    # Related data for frontend display
    main_category_name: Optional[str] = None
    category_name: Optional[str] = None
    country_name: Optional[str] = None
    province_name: Optional[str] = None
    company_name: Optional[str] = None
    location_name: Optional[str] = None
    department_name: Optional[str] = None
    status_name: Optional[str] = None
    assigned_user_name: Optional[str] = None
    stock_location_name: Optional[str] = None
    
    class Config:
        from_attributes = True
