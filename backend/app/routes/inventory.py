from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.inventory import InventoryItem, InventoryTransaction
from ..models.user import User
from ..schemas.inventory import (
    InventoryItemCreate, InventoryItemResponse,
    InventoryTransactionCreate, InventoryTransactionResponse
)

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/", response_model=List[InventoryItemResponse])
def list_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(InventoryItem).offset(skip).limit(limit).all()

@router.post("/", response_model=InventoryItemResponse)
def create_inventory_item(
    item: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_item = db.query(InventoryItem).filter(InventoryItem.sku == item.sku).first()
    if db_item:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    db_item = InventoryItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.post("/transaction", response_model=InventoryTransactionResponse)
def create_transaction(
    transaction: InventoryTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(InventoryItem).filter(InventoryItem.id == transaction.inventory_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    if transaction.transaction_type == "stock_in":
        item.quantity += transaction.quantity
    elif transaction.transaction_type == "stock_out":
        if item.quantity < transaction.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        item.quantity -= transaction.quantity
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    
    db_transaction = InventoryTransaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/alerts", response_model=List[InventoryItemResponse])
def get_low_stock_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(InventoryItem).filter(InventoryItem.quantity <= InventoryItem.min_quantity).all()
