from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StaffCreate(BaseModel):
    employeeid: str
    fullname: str
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    employmentstatus: str = "Active"
    companyid: Optional[int] = None
    locationid: Optional[int] = None
    costcenterid: Optional[int] = None
    countryid: Optional[int] = None
    provinceid: Optional[int] = None
    departmentid: Optional[int] = None

class StaffUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    employmentstatus: Optional[str] = None
    companyid: Optional[int] = None
    locationid: Optional[int] = None
    costcenterid: Optional[int] = None
    countryid: Optional[int] = None
    provinceid: Optional[int] = None
    departmentid: Optional[int] = None

class StaffResponse(BaseModel):
    staffid: int
    employeeid: str
    fullname: str
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    employmentstatus: str
    companyid: Optional[int] = None
    locationid: Optional[int] = None
    costcenterid: Optional[int] = None
    countryid: Optional[int] = None
    provinceid: Optional[int] = None
    departmentid: Optional[int] = None
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True

class StaffImportResponse(BaseModel):
    imported_count: int
    staff: list[StaffResponse]
