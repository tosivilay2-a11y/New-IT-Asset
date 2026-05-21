from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InventoryItemBase(BaseModel):
    name: str
    sku: str
    quantity: int = 0
    min_quantity: int = 10
    unit_price: Optional[float] = None
    location_id: Optional[int] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InventoryTransactionCreate(BaseModel):
    inventory_item_id: int
    transaction_type: str
    quantity: int
    reference: Optional[str] = None
    notes: Optional[str] = None

class InventoryTransactionResponse(BaseModel):
    id: int
    inventory_item_id: int
    transaction_type: str
    quantity: int
    reference: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
