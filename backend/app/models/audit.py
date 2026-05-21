from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class AuditSession(Base):
    __tablename__ = "audit_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="in_progress")  # in_progress, completed
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    created_by_user = relationship("User", back_populates="audit_sessions")
    records = relationship("AuditRecord", back_populates="audit_session")

class AuditRecord(Base):
    __tablename__ = "audit_records"
    
    id = Column(Integer, primary_key=True, index=True)
    audit_session_id = Column(Integer, ForeignKey("audit_sessions.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    expected_quantity = Column(Integer, nullable=False)
    actual_quantity = Column(Integer, nullable=False)
    discrepancy_type = Column(String)  # missing, damaged, extra, none
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    audit_session = relationship("AuditSession", back_populates="records")
    inventory_item = relationship("InventoryItem")
