from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.audit import AuditSession, AuditRecord
from ..models.inventory import InventoryItem
from ..models.user import User
from ..schemas.audit import (
    AuditSessionCreate, AuditSessionResponse,
    AuditRecordCreate, AuditRecordResponse
)

router = APIRouter(prefix="/audits", tags=["audits"])

@router.get("/", response_model=List[AuditSessionResponse])
def list_audit_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(AuditSession).offset(skip).limit(limit).all()

@router.post("/", response_model=AuditSessionResponse)
def create_audit_session(
    audit: AuditSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_audit = AuditSession(name=audit.name, created_by=current_user.id)
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit

@router.post("/{audit_id}/records", response_model=AuditRecordResponse)
def add_audit_record(
    audit_id: int,
    record: AuditRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audit = db.query(AuditSession).filter(AuditSession.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit session not found")
    
    item = db.query(InventoryItem).filter(InventoryItem.id == record.inventory_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    discrepancy = record.actual_quantity - record.expected_quantity
    if discrepancy < 0:
        discrepancy_type = "missing"
    elif discrepancy > 0:
        discrepancy_type = "extra"
    else:
        discrepancy_type = "none"
    
    db_record = AuditRecord(
        audit_session_id=audit_id,
        inventory_item_id=record.inventory_item_id,
        expected_quantity=record.expected_quantity,
        actual_quantity=record.actual_quantity,
        discrepancy_type=record.discrepancy_type or discrepancy_type,
        notes=record.notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/{audit_id}/report")
def get_audit_report(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audit = db.query(AuditSession).filter(AuditSession.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit session not found")
    
    records = db.query(AuditRecord).filter(AuditRecord.audit_session_id == audit_id).all()
    
    total_items = len(records)
    discrepancies = [r for r in records if r.discrepancy_type != "none"]
    
    return {
        "audit_session": audit,
        "total_items_audited": total_items,
        "total_discrepancies": len(discrepancies),
        "records": records
    }

@router.put("/{audit_id}/complete")
def complete_audit(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audit = db.query(AuditSession).filter(AuditSession.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit session not found")
    
    audit.status = "completed"
    audit.completed_at = datetime.utcnow()
    db.commit()
    return {"message": "Audit session completed"}
