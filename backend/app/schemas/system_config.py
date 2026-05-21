from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SystemConfigBase(BaseModel):
    config_key: str
    config_value: Optional[str] = None
    config_type: str = "string"
    description: Optional[str] = None
    category: str = "general"
    is_encrypted: bool = False
    is_active: bool = True

class SystemConfigCreate(SystemConfigBase):
    pass

class SystemConfigUpdate(BaseModel):
    config_value: Optional[str] = None
    config_type: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_encrypted: Optional[bool] = None
    is_active: Optional[bool] = None

class SystemConfigResponse(SystemConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CloudflareR2Config(BaseModel):
    storage_type: str = "local"  # "local" or "r2"
    r2_account_id: Optional[str] = None
    r2_access_key_id: Optional[str] = None
    r2_secret_access_key: Optional[str] = None
    r2_bucket_name: Optional[str] = None
    r2_endpoint_url: Optional[str] = None
    r2_public_url: Optional[str] = None

class CloudflareR2TestResponse(BaseModel):
    success: bool
    message: str
    details: Optional[dict] = None