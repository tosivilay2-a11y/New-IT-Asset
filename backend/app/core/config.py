from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Storage Settings
    STORAGE_TYPE: str = "local"  # "local" or "r2"
    
    # Cloudflare R2 Settings
    R2_ACCOUNT_ID: Optional[str] = None
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_BUCKET_NAME: Optional[str] = None
    R2_ENDPOINT_URL: Optional[str] = None  # e.g., https://your-account-id.r2.cloudflarestorage.com
    R2_PUBLIC_URL: Optional[str] = None    # e.g., https://your-domain.com or https://pub-xxx.r2.dev
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
