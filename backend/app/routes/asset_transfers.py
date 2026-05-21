"""
Asset Transfers API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..core.database import get_db
from ..models.asset_transfer import AssetTransfer
from ..models.asset import Asset
from ..schemas.asset_transfer import AssetTransfer as AssetTransferSchema, AssetTransferCreate, AssetTransferUpdate

router = APIRouter(prefix="/asset-transfers", tags=["asset-transfers"])

@router.get("/", response_model=List[AssetTransferSchema])
def get_asset_transfers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all asset transfers"""
    transfers = db.query(AssetTransfer).offset(skip).limit(limit).all()
    return transfers

@router.get("/asset/{asset_id}", response_model=List[AssetTransferSchema])
def get_transfers_by_asset(asset_id: int, db: Session = Depends(get_db)):
    """Get transfer history for an asset"""
    transfers = db.query(AssetTransfer).filter(AssetTransfer.assetid == asset_id).order_by(AssetTransfer.transferdate.desc()).all()
    return transfers

@router.get("/pending", response_model=List[AssetTransferSchema])
def get_pending_transfers(db: Session = Depends(get_db)):
    """Get all pending transfer requests"""
    transfers = db.query(AssetTransfer).filter(AssetTransfer.status == 'pending').all()
    return transfers

@router.get("/{transfer_id}", response_model=AssetTransferSchema)
def get_asset_transfer(transfer_id: int, db: Session = Depends(get_db)):
    """Get asset transfer by ID"""
    transfer = db.query(AssetTransfer).filter(AssetTransfer.transferid == transfer_id).first()
    if not transfer:
        raise HTTPException(status_code=404, detail="Asset transfer not found")
    return transfer

@router.post("/", response_model=AssetTransferSchema)
def create_asset_transfer(transfer: AssetTransferCreate, db: Session = Depends(get_db)):
    """Create new asset transfer request"""
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.assetid == transfer.assetid).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_transfer = AssetTransfer(**transfer.dict())
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

@router.put("/{transfer_id}", response_model=AssetTransferSchema)
def update_asset_transfer(transfer_id: int, transfer: AssetTransferUpdate, db: Session = Depends(get_db)):
    """Update asset transfer (approve/reject/complete)"""
    db_transfer = db.query(AssetTransfer).filter(AssetTransfer.transferid == transfer_id).first()
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Asset transfer not found")
    
    for key, value in transfer.dict(exclude_unset=True).items():
        setattr(db_transfer, key, value)
    
    # If approved, update asset location/user
    if transfer.status == 'completed':
        asset = db.query(Asset).filter(Asset.assetid == db_transfer.assetid).first()
        if asset:
            if db_transfer.tolocationid:
                asset.locationid = db_transfer.tolocationid
            if db_transfer.touserid:
                asset.assignedto = db_transfer.touserid
                asset.assigneddate = datetime.utcnow()
    
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

@router.post("/{transfer_id}/approve")
def approve_transfer(transfer_id: int, approver_id: int, db: Session = Depends(get_db)):
    """Approve a transfer request"""
    db_transfer = db.query(AssetTransfer).filter(AssetTransfer.transferid == transfer_id).first()
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Asset transfer not found")
    
    if db_transfer.status != 'pending':
        raise HTTPException(status_code=400, detail="Transfer is not pending")
    
    db_transfer.status = 'approved'
    db_transfer.approvedby = approver_id
    db_transfer.approvaldate = datetime.utcnow()
    
    db.commit()
    return {"message": "Transfer approved successfully"}

@router.post("/{transfer_id}/reject")
def reject_transfer(transfer_id: int, approver_id: int, reason: str, db: Session = Depends(get_db)):
    """Reject a transfer request"""
    db_transfer = db.query(AssetTransfer).filter(AssetTransfer.transferid == transfer_id).first()
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Asset transfer not found")
    
    if db_transfer.status != 'pending':
        raise HTTPException(status_code=400, detail="Transfer is not pending")
    
    db_transfer.status = 'rejected'
    db_transfer.approvedby = approver_id
    db_transfer.approvaldate = datetime.utcnow()
    db_transfer.notes = f"{db_transfer.notes}\nRejection reason: {reason}" if db_transfer.notes else f"Rejection reason: {reason}"
    
    db.commit()
    return {"message": "Transfer rejected successfully"}

@router.post("/{transfer_id}/complete")
def complete_transfer(transfer_id: int, db: Session = Depends(get_db)):
    """Mark transfer as completed and update asset"""
    db_transfer = db.query(AssetTransfer).filter(AssetTransfer.transferid == transfer_id).first()
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Asset transfer not found")
    
    if db_transfer.status != 'approved':
        raise HTTPException(status_code=400, detail="Transfer must be approved first")
    
    # Update asset
    asset = db.query(Asset).filter(Asset.assetid == db_transfer.assetid).first()
    if asset:
        if db_transfer.tolocationid:
            asset.locationid = db_transfer.tolocationid
        if db_transfer.touserid:
            asset.assignedto = db_transfer.touserid
            asset.assigneddate = datetime.utcnow()
    
    db_transfer.status = 'completed'
    db.commit()
    
    return {"message": "Transfer completed successfully"}
