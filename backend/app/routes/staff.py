from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from ..core.database import get_db
from ..core.security import require_admin
from ..models.user import User
from ..models.staff import Staff
from ..models.company import Company
from ..models.location import Location
from ..models.cost_center import CostCenter
from ..models.country import Country
from ..models.province import Province
from ..models.department import Department
from ..schemas.staff import StaffCreate, StaffResponse, StaffImportResponse

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/", response_model=List[StaffResponse])
def list_staff(db: Session = Depends(get_db)):
    """List all staff members with company and location details"""
    return db.query(Staff).order_by(Staff.created_at.desc()).all()

@router.post("/", response_model=StaffResponse)
def create_staff(
    staff: StaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new staff member"""
    # Check if employee ID already exists
    existing_staff = db.query(Staff).filter(Staff.employeeid == staff.employeeid).first()
    if existing_staff:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    # Check if email already exists (if provided)
    if staff.email:
        existing_email = db.query(Staff).filter(Staff.email == staff.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Validate country exists (if provided)
    if staff.countryid:
        country = db.query(Country).filter(Country.countryid == staff.countryid).first()
        if not country:
            raise HTTPException(status_code=400, detail="Country not found")

    # Validate province exists and matches country (if provided)
    if staff.provinceid:
        province = db.query(Province).filter(Province.provinceid == staff.provinceid).first()
        if not province:
            raise HTTPException(status_code=400, detail="Province not found")
        if staff.countryid and province.countryid != staff.countryid:
            raise HTTPException(status_code=400, detail="Province does not belong to the selected Country")

    # Validate company exists and matches province (if provided)
    if staff.companyid:
        company = db.query(Company).filter(Company.companyid == staff.companyid).first()
        if not company:
            raise HTTPException(status_code=400, detail="Company not found")
        if staff.provinceid and company.provinceid != staff.provinceid:
            raise HTTPException(status_code=400, detail="Company does not belong to the selected Province")
    
    # Validate department exists and matches company (if provided)
    if staff.departmentid:
        dept = db.query(Department).filter(Department.departmentid == staff.departmentid).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department not found")
        if staff.companyid and dept.companyid != staff.companyid:
            raise HTTPException(status_code=400, detail="Department does not belong to the selected Company")
    
    # Validate location exists (if provided)
    if staff.locationid:
        location = db.query(Location).filter(Location.id == staff.locationid).first()
        if not location:
            raise HTTPException(status_code=400, detail="Location not found")
        if staff.companyid and location.companyid and location.companyid != staff.companyid:
            raise HTTPException(status_code=400, detail="Location does not belong to the selected Company")

    # Validate cost center exists (if provided)
    effective_costcenterid = staff.costcenterid
    
    # Auto-fill default cost center from department if not manually specified
    if not effective_costcenterid and staff.departmentid:
        dept = db.query(Department).filter(Department.departmentid == staff.departmentid).first()
        if dept and dept.costcenterid:
            effective_costcenterid = dept.costcenterid

    if effective_costcenterid:
        costcenter = db.query(CostCenter).filter(CostCenter.costcenterid == effective_costcenterid).first()
        if not costcenter:
            raise HTTPException(status_code=400, detail="Cost Center not found")
        if staff.companyid and costcenter.companyid and costcenter.companyid != staff.companyid:
            raise HTTPException(status_code=400, detail="Cost Center does not belong to the selected Company")
    
    db_staff = Staff(
        employeeid=staff.employeeid,
        fullname=staff.fullname,
        email=staff.email,
        department=staff.department,
        position=staff.position,
        employmentstatus=staff.employmentstatus,
        companyid=staff.companyid,
        locationid=staff.locationid,
        costcenterid=effective_costcenterid,
        countryid=staff.countryid,
        provinceid=staff.provinceid,
        departmentid=staff.departmentid
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    """Get a specific staff member"""
    staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@router.get("/company/{company_id}", response_model=List[StaffResponse])
def get_staff_by_company(company_id: int, db: Session = Depends(get_db)):
    """Get all staff members in a company"""
    staff = db.query(Staff).filter(Staff.companyid == company_id).order_by(Staff.fullname).all()
    return staff

@router.get("/location/{location_id}", response_model=List[StaffResponse])
def get_staff_by_location(location_id: int, db: Session = Depends(get_db)):
    """Get all staff members at a location"""
    staff = db.query(Staff).filter(Staff.locationid == location_id).order_by(Staff.fullname).all()
    return staff

@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: int,
    staff_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a staff member"""
    db_staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Check if email is being changed to an existing email
    if "email" in staff_update and staff_update["email"] and staff_update["email"] != db_staff.email:
        existing_email = db.query(Staff).filter(Staff.email == staff_update["email"]).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Validate country exists (if provided)
    if staff_update.get("countryid"):
        country = db.query(Country).filter(Country.countryid == staff_update["countryid"]).first()
        if not country:
            raise HTTPException(status_code=400, detail="Country not found")

    # Validate province exists (if provided)
    if staff_update.get("provinceid"):
        province = db.query(Province).filter(Province.provinceid == staff_update["provinceid"]).first()
        if not province:
            raise HTTPException(status_code=400, detail="Province not found")
        ctry_id = staff_update.get("countryid", db_staff.countryid)
        if ctry_id and province.countryid != ctry_id:
            raise HTTPException(status_code=400, detail="Province does not belong to the selected Country")

    # Validate company exists (if provided)
    if staff_update.get("companyid"):
        company = db.query(Company).filter(Company.companyid == staff_update["companyid"]).first()
        if not company:
            raise HTTPException(status_code=400, detail="Company not found")
        prov_id = staff_update.get("provinceid", db_staff.provinceid)
        if prov_id and company.provinceid != prov_id:
            raise HTTPException(status_code=400, detail="Company does not belong to the selected Province")

    # Validate department exists (if provided)
    if staff_update.get("departmentid"):
        dept = db.query(Department).filter(Department.departmentid == staff_update["departmentid"]).first()
        if not dept:
            raise HTTPException(status_code=400, detail="Department not found")
        comp_id = staff_update.get("companyid", db_staff.companyid)
        if comp_id and dept.companyid != comp_id:
            raise HTTPException(status_code=400, detail="Department does not belong to the selected Company")
    
    # Validate location exists (if provided)
    if staff_update.get("locationid"):
        location = db.query(Location).filter(Location.id == staff_update["locationid"]).first()
        if not location:
            raise HTTPException(status_code=400, detail="Location not found")
        comp_id = staff_update.get("companyid", db_staff.companyid)
        if comp_id and location.companyid and location.companyid != comp_id:
            raise HTTPException(status_code=400, detail="Location does not belong to the selected Company")

    # Auto-fill default cost center from department if department is being updated and cost center is not provided
    if "departmentid" in staff_update and "costcenterid" not in staff_update:
        dept_id = staff_update["departmentid"]
        if dept_id:
            dept = db.query(Department).filter(Department.departmentid == dept_id).first()
            if dept and dept.costcenterid:
                staff_update["costcenterid"] = dept.costcenterid

    # Validate cost center exists (if provided)
    if staff_update.get("costcenterid"):
        costcenter = db.query(CostCenter).filter(CostCenter.costcenterid == staff_update["costcenterid"]).first()
        if not costcenter:
            raise HTTPException(status_code=400, detail="Cost Center not found")
        comp_id = staff_update.get("companyid", db_staff.companyid)
        if comp_id and costcenter.companyid and costcenter.companyid != comp_id:
            raise HTTPException(status_code=400, detail="Cost Center does not belong to the selected Company")
    
    # Update fields
    for key, value in staff_update.items():
        if key != "staffid" and key != "employeeid" and hasattr(db_staff, key):
            setattr(db_staff, key, value)
    
    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.delete("/{staff_id}")
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a staff member"""
    staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    db.delete(staff)
    db.commit()
    return {"message": "Staff member deleted successfully"}

@router.post("/import", response_model=StaffImportResponse)
async def import_staff(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Import staff members from Excel/CSV file"""
    try:
        # Read file content
        content = await file.read()
        
        # Determine file type and parse accordingly
        if file.filename.endswith('.csv'):
            # Parse CSV
            text_stream = io.StringIO(content.decode('utf-8'))
            reader = csv.DictReader(text_stream)
            rows = list(reader)
        elif file.filename.endswith(('.xlsx', '.xls')):
            # Parse Excel using openpyxl
            try:
                import openpyxl
            except ImportError:
                raise HTTPException(
                    status_code=400,
                    detail="Excel support not installed. Please use CSV format or install openpyxl."
                )
            
            excel_stream = io.BytesIO(content)
            workbook = openpyxl.load_workbook(excel_stream)
            worksheet = workbook.active
            
            # Get headers from first row
            headers = [cell.value for cell in worksheet[1]]
            rows = []
            
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                row_dict = {}
                for i, header in enumerate(headers):
                    if header:
                        row_dict[header.lower().replace(' ', '')] = row[i]
                rows.append(row_dict)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please use .csv, .xlsx, or .xls"
            )
        
        # Process rows
        imported_staff = []
        errors = []
        
        for idx, row in enumerate(rows, start=2):
            try:
                # Normalize column names
                row_normalized = {k.lower().replace(' ', ''): v for k, v in row.items()}
                
                # Extract required fields
                employeeid = row_normalized.get('employeeid') or row_normalized.get('employee_id')
                fullname = row_normalized.get('fullname') or row_normalized.get('full_name')
                
                if not employeeid or not fullname:
                    errors.append(f"Row {idx}: Missing Employee ID or Full Name")
                    continue
                
                # Check if employee ID already exists
                existing = db.query(Staff).filter(Staff.employeeid == str(employeeid)).first()
                if existing:
                    errors.append(f"Row {idx}: Employee ID '{employeeid}' already exists")
                    continue
                
                # Extract optional fields
                email = row_normalized.get('email')
                department = row_normalized.get('department')
                position = row_normalized.get('position')
                employmentstatus = row_normalized.get('employmentstatus') or row_normalized.get('employment_status') or 'Active'
                
                # Extract geographic and corporate fields
                country_name = row_normalized.get('country') or row_normalized.get('countryname')
                province_name = row_normalized.get('province') or row_normalized.get('provincename')
                company_name = row_normalized.get('company') or row_normalized.get('companyname')
                department_name = row_normalized.get('department') or row_normalized.get('departmentname') or row_normalized.get('departmentcode')
                location_name = row_normalized.get('location') or row_normalized.get('locationname')
                costcenter_name = row_normalized.get('costcenter') or row_normalized.get('cost_center') or row_normalized.get('costcentercode')
                
                countryid = None
                provinceid = None
                companyid = None
                departmentid = None
                locationid = None
                costcenterid = None
                
                # Look up country by name or code
                if country_name:
                    country = db.query(Country).filter(
                        (Country.countryname == str(country_name)) | (Country.countrycode == str(country_name))
                    ).first()
                    if country:
                        countryid = country.countryid
                    else:
                        errors.append(f"Row {idx}: Country '{country_name}' not found")
                        continue

                # Look up province by name or code
                if province_name:
                    province = db.query(Province).filter(
                        (Province.provincename == str(province_name)) | (Province.provincecode == str(province_name))
                    ).first()
                    if province:
                        if countryid and province.countryid != countryid:
                            errors.append(f"Row {idx}: Province '{province_name}' does not belong to selected Country")
                            continue
                        provinceid = province.provinceid
                    else:
                        errors.append(f"Row {idx}: Province '{province_name}' not found")
                        continue

                # Look up company by name or code
                if company_name:
                    company = db.query(Company).filter(
                        (Company.companyname == str(company_name)) | (Company.companycode == str(company_name))
                    ).first()
                    if company:
                        if provinceid and company.provinceid != provinceid:
                            errors.append(f"Row {idx}: Company '{company_name}' does not belong to selected Province")
                            continue
                        companyid = company.companyid
                    else:
                        errors.append(f"Row {idx}: Company '{company_name}' not found")
                        continue
                
                # Look up department by name or code
                if department_name:
                    dept = db.query(Department).filter(
                        (Department.departmentname == str(department_name)) | (Department.departmentcode == str(department_name))
                    ).first()
                    if dept:
                        if companyid and dept.companyid != companyid:
                            errors.append(f"Row {idx}: Department '{department_name}' does not belong to selected Company")
                            continue
                        departmentid = dept.departmentid
                        # If a department text isn't in rows, store resolved name in the text field
                        department = dept.departmentname
                    else:
                        # Fallback: keep string department as is
                        pass

                # Look up location by name or code
                if location_name:
                    location = db.query(Location).filter(
                        (Location.name == str(location_name))
                    ).first()
                    if location:
                        if companyid and location.companyid and location.companyid != companyid:
                            errors.append(f"Row {idx}: Location '{location_name}' does not belong to selected Company")
                            continue
                        locationid = location.id
                    else:
                        errors.append(f"Row {idx}: Location '{location_name}' not found")
                        continue

                # Look up cost center by name or code
                if costcenter_name:
                    costcenter = db.query(CostCenter).filter(
                        (CostCenter.costcentername == str(costcenter_name)) | (CostCenter.costcentercode == str(costcenter_name))
                    ).first()
                    if costcenter:
                        if companyid and costcenter.companyid and costcenter.companyid != companyid:
                            errors.append(f"Row {idx}: Cost Center '{costcenter_name}' does not belong to selected Company")
                            continue
                        costcenterid = costcenter.costcenterid
                    else:
                        errors.append(f"Row {idx}: Cost Center '{costcenter_name}' not found")
                        continue
                elif departmentid:
                    # Fallback to default cost center of the department
                    dept_obj = db.query(Department).filter(Department.departmentid == departmentid).first()
                    if dept_obj and dept_obj.costcenterid:
                        costcenterid = dept_obj.costcenterid
                
                # Check if email already exists (if provided)
                if email:
                    existing_email = db.query(Staff).filter(Staff.email == email).first()
                    if existing_email:
                        errors.append(f"Row {idx}: Email '{email}' already exists")
                        continue
                
                # Create staff member
                db_staff = Staff(
                    employeeid=str(employeeid),
                    fullname=str(fullname),
                    email=email,
                    department=department,
                    position=position,
                    employmentstatus=str(employmentstatus),
                    companyid=companyid,
                    locationid=locationid,
                    costcenterid=costcenterid,
                    countryid=countryid,
                    provinceid=provinceid,
                    departmentid=departmentid
                )
                db.add(db_staff)
                db.flush()  # Flush to get the ID
                imported_staff.append(db_staff)
                
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")
        
        # Commit all changes
        db.commit()
        
        # Refresh all imported staff to get updated data
        for staff in imported_staff:
            db.refresh(staff)
        
        # If there were errors, still return success but include error info
        if errors:
            print(f"Import warnings: {errors}")
        
        return StaffImportResponse(
            imported_count=len(imported_staff),
            staff=imported_staff
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to import staff: {str(e)}")
