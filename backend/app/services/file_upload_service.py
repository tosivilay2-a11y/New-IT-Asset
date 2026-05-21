import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import shutil
from .cloud_storage_service import storage_service

class FileUploadService:
    """Service for handling file uploads - now uses CloudStorageService"""
    
    @classmethod
    def validate_file(cls, file: UploadFile) -> bool:
        """Validate file type and size"""
        return storage_service.validate_file(file)
    
    @classmethod
    def save_file(cls, file: UploadFile, asset_code: str) -> str:
        """Save uploaded file and return the file path/URL"""
        return storage_service.save_file(file, asset_code)
    
    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """Delete file from storage"""
        return storage_service.delete_file(file_path)
    
    @classmethod
    def get_file_info(cls, file_path: str) -> Optional[dict]:
        """Get file information"""
        return storage_service.get_file_info(file_path)