"""
Asset Status Schemas
"""
from pydantic import BaseModel
from typing import Optional

class AssetStatusBase(BaseModel):
    statusname: str
    statuscode: str
    description: Optional[str] = None
    color: str = "#6c757d"
    isactive: bool = True

class AssetStatusCreate(AssetStatusBase):
    pass

class AssetStatusUpdate(BaseModel):
    statusname: Optional[str] = None
    statuscode: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    isactive: Optional[bool] = None

class AssetStatus(AssetStatusBase):
    statusid: int
    
    class Config:
        from_attributes = True
