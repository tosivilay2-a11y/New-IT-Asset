"""
Asset Transfer Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssetTransferBase(BaseModel):
    assetid: int
    fromlocationid: Optional[int] = None
    fromuserid: Optional[int] = None
    tolocationid: Optional[int] = None
    touserid: Optional[int] = None
    transfertype: str  # 'location', 'user', 'both'
    reason: Optional[str] = None
    notes: Optional[str] = None

class AssetTransferCreate(AssetTransferBase):
    requestedby: int

class AssetTransferUpdate(BaseModel):
    status: Optional[str] = None  # pending, approved, rejected, completed
    approvedby: Optional[int] = None
    approvaldate: Optional[datetime] = None
    notes: Optional[str] = None

class AssetTransfer(AssetTransferBase):
    transferid: int
    transferdate: datetime
    requestedby: int
    approvedby: Optional[int] = None
    approvaldate: Optional[datetime] = None
    status: str
    
    class Config:
        from_attributes = True
