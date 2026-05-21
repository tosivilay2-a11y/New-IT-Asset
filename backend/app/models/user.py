from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    userid = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, unique=True)  # Keep for backward compatibility
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    full_name = Column(String, nullable=True)  # Keep for backward compatibility
    role = Column(String, default="user")  # admin or user
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    audit_sessions = relationship("AuditSession", back_populates="created_by_user")
