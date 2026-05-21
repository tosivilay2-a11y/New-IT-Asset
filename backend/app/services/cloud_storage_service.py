import os
import uuid
import boto3
from pathlib import Path
from typing import Optional, Union
from fastapi import UploadFile, HTTPException
from botocore.exceptions import ClientError, NoCredentialsError
import shutil
from ..core.config import settings


def _build_r2_client(access_key: str, secret_key: str, endpoint: str):
    return boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='auto',
    )


class CloudStorageService:
    """Service for handling file uploads to local storage or Cloudflare R2"""

    LOCAL_UPLOAD_DIR = Path("uploads/po_attachments")

    ALLOWED_EXTENSIONS = {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif',
        '.doc', '.docx', '.xls', '.xlsx'
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE.lower()
        if self.storage_type == "r2":
            self._init_r2_client()
        else:
            self._init_local_storage()

    def _init_local_storage(self):
        self.LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        print("[OK] Local storage initialized")

    def _init_r2_client(self):
        try:
            if not all([
                settings.R2_ACCESS_KEY_ID,
                settings.R2_SECRET_ACCESS_KEY,
                settings.R2_BUCKET_NAME,
                settings.R2_ENDPOINT_URL,
            ]):
                raise ValueError("Missing required R2 configuration.")

            self.r2_client = _build_r2_client(
                settings.R2_ACCESS_KEY_ID,
                settings.R2_SECRET_ACCESS_KEY,
                settings.R2_ENDPOINT_URL,
            )
            self.bucket_name = settings.R2_BUCKET_NAME
            self.public_url = settings.R2_PUBLIC_URL if settings.R2_PUBLIC_URL else settings.R2_ENDPOINT_URL
            print(f"[OK] Cloudflare R2 storage configured (bucket: {self.bucket_name})")

        except Exception as e:
            print(f"[ERROR] Failed to initialize R2 storage: {e}")
            print("Falling back to local storage...")
            self.storage_type = "local"
            self._init_local_storage()

    def reload_from_db(self):
        """Reload R2 credentials from the database (called after config save)."""
        try:
            from ..core.database import SessionLocal
            from ..models.system_config import SystemConfig

            db = SessionLocal()
            try:
                configs = {
                    c.config_key: c.config_value
                    for c in db.query(SystemConfig).filter(SystemConfig.is_active == True).all()
                }
            finally:
                db.close()

            new_type = configs.get("storage_type", "local").lower()
            self.storage_type = new_type

            if new_type == "r2":
                access_key = configs.get("r2_access_key_id", "")
                secret_key = configs.get("r2_secret_access_key", "")
                endpoint = configs.get("r2_endpoint_url", "")
                bucket = configs.get("r2_bucket_name", "")
                public_url = configs.get("r2_public_url", "")

                if all([access_key, secret_key, endpoint, bucket]):
                    self.r2_client = _build_r2_client(access_key, secret_key, endpoint)
                    self.bucket_name = bucket
                    self.public_url = public_url if public_url else endpoint
                    print(f"[OK] R2 reloaded — bucket: {bucket}, public_url: {self.public_url}")
                    return True
                else:
                    print("[ERROR] Incomplete R2 config in DB, staying on local")
                    self.storage_type = "local"
                    self._init_local_storage()
                    return False
            else:
                self._init_local_storage()
                return True

        except Exception as e:
            print(f"[ERROR] reload_from_db error: {e}")
            return False

    def validate_file(self, file: UploadFile) -> bool:
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        if hasattr(file, 'size') and file.size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max: {self.MAX_FILE_SIZE / 1024 / 1024:.0f}MB"
            )
        return True

    def save_file(self, file: UploadFile, asset_code: str) -> str:
        try:
            self.validate_file(file)
            file_ext = Path(file.filename).suffix.lower()
            unique_filename = f"{asset_code}_{uuid.uuid4().hex[:8]}{file_ext}"

            if self.storage_type == "r2":
                return self._save_to_r2(file, unique_filename)
            else:
                return self._save_to_local(file, unique_filename)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    def _save_to_local(self, file: UploadFile, filename: str) -> str:
        file_path = self.LOCAL_UPLOAD_DIR / filename
        upload_dir_abs = self.LOCAL_UPLOAD_DIR.resolve()
        file_path_abs = file_path.resolve()

        try:
            file_path_abs.relative_to(upload_dir_abs)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid file path")

        with open(file_path_abs, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        backend_dir = Path(__file__).parent.parent.parent
        try:
            return str(file_path_abs.relative_to(backend_dir.resolve()))
        except ValueError:
            return str(file_path)

    def _save_to_r2(self, file: UploadFile, filename: str) -> str:
        try:
            key = f"po_attachments/{filename}"
            file.file.seek(0)

            self.r2_client.upload_fileobj(
                file.file,
                self.bucket_name,
                key,
                ExtraArgs={
                    'ContentType': file.content_type or 'application/octet-stream',
                    'Metadata': {
                        'original_filename': file.filename,
                        'uploaded_by': 'asset_management_system',
                    }
                }
            )

            base = self.public_url.rstrip('/') if self.public_url else settings.R2_ENDPOINT_URL.rstrip('/')
            # Always use public URL for stored paths — private endpoint is not publicly accessible
            # If public_url is the private endpoint (fallback), warn and use it anyway
            return f"{base}/{key}"
        except ClientError as e:
            code = e.response['Error']['Code']
            if code == 'NoSuchBucket':
                raise HTTPException(status_code=500, detail=f"R2 bucket '{self.bucket_name}' not found")
            elif code in ('AccessDenied', '403'):
                raise HTTPException(
                    status_code=500,
                    detail="R2 Access Denied. Go to Cloudflare Dashboard → R2 → Manage R2 API Tokens and ensure the token has Object Read & Write on this bucket."
                )
            raise HTTPException(status_code=500, detail=f"R2 upload failed: {code}")
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="R2 credentials not configured")

    def delete_file(self, file_path: str) -> bool:
        try:
            if self.storage_type == "r2" and file_path.startswith(('http://', 'https://')):
                return self._delete_from_r2(file_path)
            return self._delete_from_local(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False

    def _delete_from_local(self, file_path: str) -> bool:
        try:
            p = Path(file_path)
            if p.exists():
                p.unlink()
                return True
            return False
        except Exception:
            return False

    def _delete_from_r2(self, file_url: str) -> bool:
        try:
            if self.public_url and file_url.startswith(self.public_url):
                key = file_url.replace(f"{self.public_url.rstrip('/')}/", "")
            else:
                base = f"{settings.R2_ENDPOINT_URL.rstrip('/')}/{self.bucket_name}/"
                if file_url.startswith(base):
                    key = file_url.replace(base, "")
                else:
                    return False
            self.r2_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def get_file_info(self, file_path: str) -> Optional[dict]:
        try:
            if self.storage_type == "r2" and file_path.startswith(('http://', 'https://')):
                return self._get_r2_file_info(file_path)
            return self._get_local_file_info(file_path)
        except Exception:
            return None

    def _get_local_file_info(self, file_path: str) -> Optional[dict]:
        try:
            p = Path(file_path)
            if p.exists():
                s = p.stat()
                return {'filename': p.name, 'size': s.st_size, 'storage_type': 'local'}
            return None
        except Exception:
            return None

    def _get_r2_file_info(self, file_url: str) -> Optional[dict]:
        try:
            if self.public_url and file_url.startswith(self.public_url):
                key = file_url.replace(f"{self.public_url.rstrip('/')}/", "")
            else:
                base = f"{settings.R2_ENDPOINT_URL.rstrip('/')}/{self.bucket_name}/"
                key = file_url.replace(base, "") if file_url.startswith(base) else None
            if not key:
                return None
            resp = self.r2_client.head_object(Bucket=self.bucket_name, Key=key)
            return {
                'filename': key.split('/')[-1],
                'size': resp.get('ContentLength', 0),
                'modified': resp.get('LastModified'),
                'content_type': resp.get('ContentType'),
                'storage_type': 'r2',
            }
        except ClientError:
            return None


# Singleton
storage_service = CloudStorageService()

class CloudStorageService:
    """Service for handling file uploads to local storage or Cloudflare R2"""
    
    # Define upload directory for local storage
    LOCAL_UPLOAD_DIR = Path("uploads/po_attachments")
    
    # Allowed file types
    ALLOWED_EXTENSIONS = {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', 
        '.doc', '.docx', '.xls', '.xlsx'
    }
    
    # Max file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    def __init__(self):
        """Initialize the storage service based on configuration"""
        self.storage_type = settings.STORAGE_TYPE.lower()
        
        if self.storage_type == "r2":
            self._init_r2_client()
        else:
            self._init_local_storage()
    
    def _init_local_storage(self):
        """Initialize local storage"""
        self.LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        print("[OK] Local storage initialized")
    
    def _init_r2_client(self):
        """Initialize Cloudflare R2 client"""
        try:
            if not all([
                settings.R2_ACCOUNT_ID,
                settings.R2_ACCESS_KEY_ID,
                settings.R2_SECRET_ACCESS_KEY,
                settings.R2_BUCKET_NAME,
                settings.R2_ENDPOINT_URL
            ]):
                raise ValueError("Missing required R2 configuration. Please check your .env file.")
            
            self.r2_client = boto3.client(
                's3',
                endpoint_url=settings.R2_ENDPOINT_URL,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                region_name='auto'  # R2 uses 'auto' as region
            )
            
            self.bucket_name = settings.R2_BUCKET_NAME
            self.public_url = settings.R2_PUBLIC_URL or settings.R2_ENDPOINT_URL
            
            # Don't test connection on init — just mark as configured.
            # Connection errors will surface on first upload attempt.
            print(f"[OK] Cloudflare R2 storage configured (bucket: {self.bucket_name})")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize R2 storage: {e}")
            print("Falling back to local storage...")
            self.storage_type = "local"
            self._init_local_storage()
    
    def validate_file(self, file: UploadFile) -> bool:
        """Validate file type and size"""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size (if available)
        if hasattr(file, 'size') and file.size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size too large. Maximum size: {self.MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
            )
        
        return True
    
    def save_file(self, file: UploadFile, asset_code: str) -> str:
        """Save uploaded file and return the file URL/path"""
        try:
            # Validate file
            self.validate_file(file)
            
            # Generate unique filename
            file_ext = Path(file.filename).suffix.lower()
            unique_filename = f"{asset_code}_{uuid.uuid4().hex[:8]}{file_ext}"
            
            if self.storage_type == "r2":
                return self._save_to_r2(file, unique_filename)
            else:
                return self._save_to_local(file, unique_filename)
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    def _save_to_local(self, file: UploadFile, filename: str) -> str:
        """Save file to local storage"""
        file_path = self.LOCAL_UPLOAD_DIR / filename
        
        # Ensure the file path is within the upload directory
        upload_dir_abs = self.LOCAL_UPLOAD_DIR.resolve()
        file_path_abs = file_path.resolve()
        
        # Check if file path is within upload directory
        try:
            file_path_abs.relative_to(upload_dir_abs)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        # Save file
        with open(file_path_abs, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return relative path from backend directory
        backend_dir = Path(__file__).parent.parent.parent
        try:
            relative_path = file_path_abs.relative_to(backend_dir.resolve())
            return str(relative_path)
        except ValueError:
            return str(file_path)
    
    def _save_to_r2(self, file: UploadFile, filename: str) -> str:
        """Save file to Cloudflare R2"""
        try:
            # Upload to R2
            key = f"po_attachments/{filename}"
            
            # Reset file pointer to beginning
            file.file.seek(0)
            
            self.r2_client.upload_fileobj(
                file.file,
                self.bucket_name,
                key,
                ExtraArgs={
                    'ContentType': file.content_type or 'application/octet-stream',
                    'Metadata': {
                        'original_filename': file.filename,
                        'uploaded_by': 'asset_management_system'
                    }
                }
            )
            
            # Return public URL
            if self.public_url:
                return f"{self.public_url.rstrip('/')}/{key}"
            else:
                return f"{settings.R2_ENDPOINT_URL.rstrip('/')}/{self.bucket_name}/{key}"
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise HTTPException(status_code=500, detail="R2 bucket not found")
            elif error_code == 'AccessDenied':
                raise HTTPException(status_code=500, detail="R2 access denied")
            else:
                raise HTTPException(status_code=500, detail=f"R2 upload failed: {error_code}")
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="R2 credentials not configured")
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            if self.storage_type == "r2" and file_path.startswith(('http://', 'https://')):
                return self._delete_from_r2(file_path)
            else:
                return self._delete_from_local(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False
    
    def _delete_from_local(self, file_path: str) -> bool:
        """Delete file from local storage"""
        try:
            full_path = Path(file_path)
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def _delete_from_r2(self, file_url: str) -> bool:
        """Delete file from Cloudflare R2"""
        try:
            # Extract key from URL
            if self.public_url and file_url.startswith(self.public_url):
                key = file_url.replace(f"{self.public_url.rstrip('/')}/", "")
            else:
                # Extract from R2 endpoint URL
                base_url = f"{settings.R2_ENDPOINT_URL.rstrip('/')}/{self.bucket_name}/"
                if file_url.startswith(base_url):
                    key = file_url.replace(base_url, "")
                else:
                    return False
            
            self.r2_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
            
        except ClientError:
            return False
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get file information"""
        try:
            if self.storage_type == "r2" and file_path.startswith(('http://', 'https://')):
                return self._get_r2_file_info(file_path)
            else:
                return self._get_local_file_info(file_path)
        except Exception:
            return None
    
    def _get_local_file_info(self, file_path: str) -> Optional[dict]:
        """Get local file information"""
        try:
            full_path = Path(file_path)
            if full_path.exists():
                stat = full_path.stat()
                return {
                    'filename': full_path.name,
                    'size': stat.st_size,
                    'created': stat.st_ctime,
                    'modified': stat.st_mtime,
                    'storage_type': 'local'
                }
            return None
        except Exception:
            return None
    
    def _get_r2_file_info(self, file_url: str) -> Optional[dict]:
        """Get R2 file information"""
        try:
            # Extract key from URL
            if self.public_url and file_url.startswith(self.public_url):
                key = file_url.replace(f"{self.public_url.rstrip('/')}/", "")
            else:
                base_url = f"{settings.R2_ENDPOINT_URL.rstrip('/')}/{self.bucket_name}/"
                if file_url.startswith(base_url):
                    key = file_url.replace(base_url, "")
                else:
                    return None
            
            response = self.r2_client.head_object(Bucket=self.bucket_name, Key=key)
            
            return {
                'filename': key.split('/')[-1],
                'size': response.get('ContentLength', 0),
                'created': response.get('LastModified'),
                'modified': response.get('LastModified'),
                'content_type': response.get('ContentType'),
                'storage_type': 'r2'
            }
            
        except ClientError:
            return None

# Create a singleton instance
storage_service = CloudStorageService()