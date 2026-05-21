"""
Seed Asset Control Data - Departments and Asset Statuses
"""
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Department, AssetStatus, Company

def seed_asset_statuses(db: Session):
    """Seed asset statuses"""
    print("Seeding asset statuses...")
    
    statuses = [
        {
            "statusname": "Available",
            "statuscode": "AVAIL",
            "description": "Asset is available for use",
            "color": "#28a745"  # Green
        },
        {
            "statusname": "In Use",
            "statuscode": "INUSE",
            "description": "Asset is currently assigned and in use",
            "color": "#007bff"  # Blue
        },
        {
            "statusname": "Maintenance",
            "statuscode": "MAINT",
            "description": "Asset is under maintenance or repair",
            "color": "#ffc107"  # Yellow
        },
        {
            "statusname": "Retired",
            "statuscode": "RETIR",
            "description": "Asset has been retired from service",
            "color": "#6c757d"  # Gray
        },
        {
            "statusname": "Disposed",
            "statuscode": "DISP",
            "description": "Asset has been disposed of",
            "color": "#dc3545"  # Red
        },
        {
            "statusname": "Lost",
            "statuscode": "LOST",
            "description": "Asset is lost or missing",
            "color": "#e83e8c"  # Pink
        },
        {
            "statusname": "Damaged",
            "statuscode": "DAMAG",
            "description": "Asset is damaged and needs repair",
            "color": "#fd7e14"  # Orange
        },
        {
            "statusname": "Reserved",
            "statuscode": "RESERV",
            "description": "Asset is reserved for future use",
            "color": "#17a2b8"  # Cyan
        }
    ]
    
    for status_data in statuses:
        existing = db.query(AssetStatus).filter(AssetStatus.statuscode == status_data["statuscode"]).first()
        if not existing:
            status = AssetStatus(**status_data)
            db.add(status)
            print(f"  ✓ Added status: {status_data['statusname']}")
        else:
            print(f"  - Status already exists: {status_data['statusname']}")
    
    db.commit()
    print("✓ Asset statuses seeded\n")

def seed_departments(db: Session):
    """Seed sample departments"""
    print("Seeding departments...")
    
    # Get first company for demo
    company = db.query(Company).first()
    if not company:
        print("  ! No companies found. Please seed companies first.")
        return
    
    departments = [
        {
            "departmentname": "Administration",
            "departmentcode": "ADMIN",
            "companyid": company.companyid,
            "description": "Administrative and management staff"
        },
        {
            "departmentname": "Customer Service",
            "departmentcode": "CS",
            "companyid": company.companyid,
            "description": "Customer service and support"
        },
        {
            "departmentname": "Finance",
            "departmentcode": "FIN",
            "companyid": company.companyid,
            "description": "Finance and accounting department"
        },
        {
            "departmentname": "Human Resources",
            "departmentcode": "HR",
            "companyid": company.companyid,
            "description": "Human resources and recruitment"
        },
        {
            "departmentname": "Information Technology",
            "departmentcode": "IT",
            "companyid": company.companyid,
            "description": "IT support and infrastructure"
        },
        {
            "departmentname": "Marketing",
            "departmentcode": "MKT",
            "companyid": company.companyid,
            "description": "Marketing and communications"
        },
        {
            "departmentname": "Operations",
            "departmentcode": "OPS",
            "companyid": company.companyid,
            "description": "Operations and logistics"
        },
        {
            "departmentname": "Sales",
            "departmentcode": "SALES",
            "companyid": company.companyid,
            "description": "Sales department"
        }
    ]
    
    for dept_data in departments:
        existing = db.query(Department).filter(Department.departmentcode == dept_data["departmentcode"]).first()
        if not existing:
            dept = Department(**dept_data)
            db.add(dept)
            print(f"  ✓ Added department: {dept_data['departmentname']}")
        else:
            print(f"  - Department already exists: {dept_data['departmentname']}")
    
    db.commit()
    print("✓ Departments seeded\n")

def main():
    print("=" * 70)
    print("SEEDING ASSET CONTROL DATA")
    print("=" * 70)
    print()
    
    db = SessionLocal()
    
    try:
        seed_asset_statuses(db)
        seed_departments(db)
        
        print("=" * 70)
        print("✓ ASSET CONTROL DATA SEEDED SUCCESSFULLY")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  - Asset Statuses: {db.query(AssetStatus).count()}")
        print(f"  - Departments: {db.query(Department).count()}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
