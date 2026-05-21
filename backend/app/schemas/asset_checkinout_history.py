from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssetCheckInOutHistoryCreate(BaseModel):
    assetid: int
    action: str  # CHECKOUT or CHECKIN
    userid: Optional[int] = None
    staffid: Optional[int] = None
    reason: Optional[str] = None
    condition_before: Optional[str] = None
    condition_after: Optional[str] = None
    location_before: Optional[int] = None
    location_after: Optional[int] = None
    notes: Optional[str] = None

class AssetCheckInOutHistoryResponse(BaseModel):
    historyid: int
    assetid: int
    action: str
    userid: Optional[int] = None
    staffid: Optional[int] = None
    reason: Optional[str] = None
    condition_before: Optional[str] = None
    condition_after: Optional[str] = None
    location_before: Optional[int] = None
    location_after: Optional[int] = None
    notes: Optional[str] = None
    staff_name: Optional[str] = None
    user_name: Optional[str] = None
    location_before_name: Optional[str] = None
    location_after_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
