from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AuditSessionCreate(BaseModel):
    name: str

class AuditSessionResponse(BaseModel):
    id: int
    name: str
    status: str
    created_by: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AuditRecordCreate(BaseModel):
    inventory_item_id: int
    expected_quantity: int
    actual_quantity: int
    discrepancy_type: Optional[str] = None
    notes: Optional[str] = None

class AuditRecordResponse(BaseModel):
    id: int
    audit_session_id: int
    inventory_item_id: int
    expected_quantity: int
    actual_quantity: int
    discrepancy_type: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
