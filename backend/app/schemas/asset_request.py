from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssetRequestCreate(BaseModel):
    staff_id: Optional[int] = None
    staff_name: str
    staff_email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    province_id: Optional[int] = None
    location_id: Optional[int] = None
    asset_type: str = "Computer"
    priority: str = "Medium"
    reason: Optional[str] = None
    notes: Optional[str] = None

class AssetRequestUpdate(BaseModel):
    status: Optional[str] = None  # Pending, Approved, Rejected
    notes: Optional[str] = None
    assigned_assetcode: Optional[str] = None

class AssetRequestResponse(BaseModel):
    requestid: int
    staff_id: Optional[int] = None
    staff_name: str
    staff_email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    province_id: Optional[int] = None
    location_id: Optional[int] = None
    province_name: Optional[str] = None
    location_name: Optional[str] = None
    asset_type: str
    priority: str
    reason: Optional[str] = None
    status: str
    notes: Optional[str] = None
    requested_by: Optional[str] = None
    assigned_assetcode: Optional[str] = None
    assigned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
