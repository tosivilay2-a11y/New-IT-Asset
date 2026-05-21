from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
import re
from ..core.database import get_db
from ..core.security import get_current_user
from ..core.config import settings
from ..models.system_config import SystemConfig
from ..models.user import User
from ..schemas.system_config import (
    SystemConfigCreate, SystemConfigUpdate, SystemConfigResponse,
    CloudflareR2Config, CloudflareR2TestResponse
)
from ..services.cloud_storage_service import CloudStorageService

router = APIRouter(prefix="/config", tags=["configuration"])


def _write_env_file(env_path: str, updates: dict):
    """Update specific keys in a .env file, preserving all other lines."""
    try:
        # Read existing content
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = []

        updated_keys = set()
        new_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') or '=' not in stripped:
                new_lines.append(line)
                continue
            key = stripped.split('=', 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
            else:
                new_lines.append(line)

        # Append any keys not already in the file
        for key, value in updates.items():
            if key not in updated_keys and value:
                new_lines.append(f"{key}={value}\n")

        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    except Exception as e:
        print(f"Warning: could not write .env file: {e}")

@router.get("/", response_model=List[SystemConfigResponse])
def get_all_configs(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all system configurations"""
    query = db.query(SystemConfig).filter(SystemConfig.is_active == True)
    if category:
        query = query.filter(SystemConfig.category == category)
    return query.all()

@router.get("/storage/status")
def get_storage_status(
    current_user: User = Depends(get_current_user)
):
    """Get live storage service status"""
    from ..services.cloud_storage_service import storage_service
    return {
        "active_storage_type": storage_service.storage_type,
        "bucket_name": getattr(storage_service, 'bucket_name', None),
        "public_url": getattr(storage_service, 'public_url', None),
        "r2_configured": hasattr(storage_service, 'r2_client'),
    }

@router.get("/file-url")
def get_public_file_url(
    path: str,
    current_user: User = Depends(get_current_user)
):
    """Convert a stored file path to a publicly accessible URL"""
    from ..services.cloud_storage_service import storage_service

    if not path:
        raise HTTPException(status_code=400, detail="path is required")

    # Already a full URL
    if path.startswith('http://') or path.startswith('https://'):
        # If it's the private R2 endpoint, swap to public URL
        private_endpoint = getattr(storage_service, 'r2_client', None) and settings.R2_ENDPOINT_URL
        public_url = getattr(storage_service, 'public_url', None)

        if private_endpoint and public_url and path.startswith(private_endpoint.rstrip('/')):
            # Replace private endpoint with public URL
            key = path.replace(f"{private_endpoint.rstrip('/')}/{storage_service.bucket_name}/", "")
            return {"url": f"{public_url.rstrip('/')}/{key}", "type": "r2_public"}

        return {"url": path, "type": "r2_url"}

    # Local file path — serve via /uploads static route
    clean = path.replace('\\', '/')
    if not clean.startswith('uploads/'):
        clean = f"uploads/{clean.lstrip('/')}"
    return {"url": f"http://localhost:8000/{clean}", "type": "local"}

@router.get("/storage", response_model=CloudflareR2Config)
def get_storage_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current storage configuration"""
    config_keys = [
        "storage_type", "r2_account_id", "r2_access_key_id", 
        "r2_secret_access_key", "r2_bucket_name", "r2_endpoint_url", "r2_public_url"
    ]
    
    configs = db.query(SystemConfig).filter(
        SystemConfig.config_key.in_(config_keys),
        SystemConfig.is_active == True
    ).all()
    
    config_dict = {config.config_key: config.config_value for config in configs}
    
    # Add defaults for missing values
    result = CloudflareR2Config(
        storage_type=config_dict.get("storage_type", "local"),
        r2_account_id=config_dict.get("r2_account_id"),
        r2_access_key_id=config_dict.get("r2_access_key_id"),
        r2_secret_access_key="***" if config_dict.get("r2_secret_access_key") else None,  # Mask secret
        r2_bucket_name=config_dict.get("r2_bucket_name"),
        r2_endpoint_url=config_dict.get("r2_endpoint_url"),
        r2_public_url=config_dict.get("r2_public_url")
    )
    
    return result

@router.post("/storage", response_model=dict)
def update_storage_config(
    config: CloudflareR2Config,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update storage configuration"""
    try:
        # Define configuration mappings
        config_mappings = [
            ("storage_type", config.storage_type, "string", "File storage type (local or r2)", "storage"),
            ("r2_account_id", config.r2_account_id, "string", "Cloudflare R2 Account ID", "storage"),
            ("r2_access_key_id", config.r2_access_key_id, "string", "Cloudflare R2 Access Key ID", "storage"),
            ("r2_secret_access_key", config.r2_secret_access_key, "string", "Cloudflare R2 Secret Access Key", "storage"),
            ("r2_bucket_name", config.r2_bucket_name, "string", "Cloudflare R2 Bucket Name", "storage"),
            ("r2_endpoint_url", config.r2_endpoint_url, "string", "Cloudflare R2 Endpoint URL", "storage"),
            ("r2_public_url", config.r2_public_url, "string", "Cloudflare R2 Public URL", "storage")
        ]
        
        updated_configs = []
        
        for key, value, config_type, description, category in config_mappings:
            # Skip if value is None or empty (except for storage_type)
            if value is None or (value == "" and key != "storage_type"):
                continue
                
            # Don't update secret if it's masked
            if key == "r2_secret_access_key" and value == "***":
                continue
            
            # Check if config exists
            existing_config = db.query(SystemConfig).filter(
                SystemConfig.config_key == key
            ).first()
            
            if existing_config:
                existing_config.config_value = value
                existing_config.config_type = config_type
                existing_config.description = description
                existing_config.category = category
                existing_config.is_encrypted = (key == "r2_secret_access_key")
            else:
                new_config = SystemConfig(
                    config_key=key,
                    config_value=value,
                    config_type=config_type,
                    description=description,
                    category=category,
                    is_encrypted=(key == "r2_secret_access_key")
                )
                db.add(new_config)
            
            updated_configs.append(key)
        
        db.commit()
        
        # Build the values to apply (resolve masked secret from DB)
        secret_value = config.r2_secret_access_key
        if secret_value == "***":
            secret_row = db.query(SystemConfig).filter(
                SystemConfig.config_key == "r2_secret_access_key"
            ).first()
            secret_value = secret_row.config_value if secret_row else None

        env_updates = {
            "STORAGE_TYPE": config.storage_type,
            "R2_ACCOUNT_ID": config.r2_account_id or "",
            "R2_ACCESS_KEY_ID": config.r2_access_key_id or "",
            "R2_SECRET_ACCESS_KEY": secret_value or "",
            "R2_BUCKET_NAME": config.r2_bucket_name or "",
            "R2_ENDPOINT_URL": config.r2_endpoint_url or "",
            "R2_PUBLIC_URL": config.r2_public_url or "",
        }

        # Update os.environ for current session
        for k, v in env_updates.items():
            if v:
                os.environ[k] = v

        # Write changes back to .env file so they persist across restarts
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
        env_path = os.path.normpath(env_path)
        _write_env_file(env_path, env_updates)

        # Reload storage service with new credentials immediately (no restart needed)
        from ..services.cloud_storage_service import storage_service
        if hasattr(storage_service, 'reload_from_db'):
            storage_service.reload_from_db()
        else:
            # Fallback: reinitialize directly
            storage_service.storage_type = config.storage_type.lower()
            if storage_service.storage_type == "r2":
                storage_service._init_r2_client()
            else:
                storage_service._init_local_storage()
        
        return {
            "success": True,
            "message": "Storage configuration saved and applied",
            "updated_configs": updated_configs,
            "storage_type": config.storage_type,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

@router.post("/storage/test", response_model=CloudflareR2TestResponse)
def test_storage_config(
    config: CloudflareR2Config,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Test storage configuration"""
    try:
        if config.storage_type == "local":
            return CloudflareR2TestResponse(
                success=True,
                message="Local storage is working",
                details={"storage_type": "local"}
            )
        
        # Test R2 configuration
        if not all([
            config.r2_account_id,
            config.r2_access_key_id,
            config.r2_secret_access_key,
            config.r2_bucket_name,
            config.r2_endpoint_url
        ]):
            return CloudflareR2TestResponse(
                success=False,
                message="Missing required R2 configuration fields",
                details={
                    "required_fields": [
                        "r2_account_id", "r2_access_key_id", "r2_secret_access_key",
                        "r2_bucket_name", "r2_endpoint_url"
                    ]
                }
            )
        
        # Get actual secret from database if masked
        if config.r2_secret_access_key == "***":
            secret_config = db.query(SystemConfig).filter(
                SystemConfig.config_key == "r2_secret_access_key"
            ).first()
            if secret_config:
                config.r2_secret_access_key = secret_config.config_value
            else:
                return CloudflareR2TestResponse(
                    success=False,
                    message="R2 secret access key not found in database"
                )
        
        # Create temporary storage service for testing
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        try:
            r2_client = boto3.client(
                's3',
                endpoint_url=config.r2_endpoint_url,
                aws_access_key_id=config.r2_access_key_id,
                aws_secret_access_key=config.r2_secret_access_key,
                region_name='auto'
            )
            
            # Test connection by trying to list objects (works even on empty buckets)
            # head_bucket requires bucket-level permissions; list_objects only needs object read
            try:
                r2_client.list_objects_v2(Bucket=config.r2_bucket_name, MaxKeys=1)
            except ClientError as bucket_err:
                # If we get NoSuchBucket it's a real error; other errors may just be permissions
                if bucket_err.response['Error']['Code'] == 'NoSuchBucket':
                    raise
                # Try a put to verify write access
                r2_client.put_object(
                    Bucket=config.r2_bucket_name,
                    Key='_connection_test.txt',
                    Body=b'test',
                    ContentType='text/plain'
                )
                r2_client.delete_object(Bucket=config.r2_bucket_name, Key='_connection_test.txt')
            
            return CloudflareR2TestResponse(
                success=True,
                message="Cloudflare R2 connection successful",
                details={
                    "storage_type": "r2",
                    "bucket_name": config.r2_bucket_name,
                    "endpoint_url": config.r2_endpoint_url
                }
            )
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                return CloudflareR2TestResponse(
                    success=False,
                    message=f"Bucket '{config.r2_bucket_name}' not found. Check the bucket name.",
                    details={"error_code": error_code}
                )
            elif error_code in ('AccessDenied', '403'):
                return CloudflareR2TestResponse(
                    success=False,
                    message="Access Denied. Your R2 API token needs 'Object Read & Write' permissions on this bucket. Go to Cloudflare Dashboard → R2 → Manage R2 API Tokens.",
                    details={"error_code": error_code}
                )
            else:
                return CloudflareR2TestResponse(
                    success=False,
                    message=f"R2 connection failed: {error_code}",
                    details={"error_code": error_code}
                )
        except NoCredentialsError:
            return CloudflareR2TestResponse(
                success=False,
                message="Invalid R2 credentials"
            )
        except Exception as e:
            return CloudflareR2TestResponse(
                success=False,
                message=f"Connection test failed: {str(e)}"
            )
            
    except Exception as e:
        return CloudflareR2TestResponse(
            success=False,
            message=f"Test failed: {str(e)}"
        )

@router.get("/{config_key}", response_model=SystemConfigResponse)
def get_config(
    config_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific configuration"""
    config = db.query(SystemConfig).filter(
        SystemConfig.config_key == config_key,
        SystemConfig.is_active == True
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return config

@router.post("/", response_model=SystemConfigResponse)
def create_config(
    config: SystemConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new configuration"""
    # Check if config already exists
    existing = db.query(SystemConfig).filter(
        SystemConfig.config_key == config.config_key
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Configuration key already exists")
    
    db_config = SystemConfig(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.put("/{config_key}", response_model=SystemConfigResponse)
def update_config(
    config_key: str,
    config: SystemConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update configuration"""
    db_config = db.query(SystemConfig).filter(
        SystemConfig.config_key == config_key
    ).first()
    
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    for key, value in config.dict(exclude_unset=True).items():
        setattr(db_config, key, value)
    
    db.commit()
    db.refresh(db_config)
    return db_config

@router.delete("/{config_key}")
def delete_config(
    config_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete configuration (soft delete)"""
    db_config = db.query(SystemConfig).filter(
        SystemConfig.config_key == config_key
    ).first()
    
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    db_config.is_active = False
    db.commit()
    return {"message": "Configuration deleted successfully"}