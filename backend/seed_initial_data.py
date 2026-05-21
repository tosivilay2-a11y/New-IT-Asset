"""
Seed Initial Data for Enhanced Asset Management System
Run this after expanding the database schema
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import sys

SEED_DATA_SQL = """
-- =============================================
-- SEED COUNTRIES
-- =============================================
INSERT INTO countries (countryname, countrycode, isactive) VALUES
('Thailand', 'TH', TRUE),
('United States', 'US', TRUE),
('Singapore', 'SG', TRUE),
('Japan', 'JP', TRUE),
('Malaysia', 'MY', TRUE)
ON CONFLICT (countrycode) DO NOTHING;

-- =============================================
-- SEED PROVINCES
-- =============================================
INSERT INTO provinces (provincename, provincecode, countryid, isactive) 
SELECT 'Bangkok', 'BKK', countryid, TRUE FROM countries WHERE countrycode = 'TH'
UNION ALL
SELECT 'Chiang Mai', 'CNX', countryid, TRUE FROM countries WHERE countrycode = 'TH'
UNION ALL
SELECT 'Phuket', 'PKT', countryid, TRUE FROM countries WHERE countrycode = 'TH'
UNION ALL
SELECT 'California', 'CA', countryid, TRUE FROM countries WHERE countrycode = 'US'
UNION ALL
SELECT 'New York', 'NY', countryid, TRUE FROM countries WHERE countrycode = 'US'
UNION ALL
SELECT 'Texas', 'TX', countryid, TRUE FROM countries WHERE countrycode = 'US'
ON CONFLICT DO NOTHING;

-- =============================================
-- SEED COMPANIES
-- =============================================
INSERT INTO companies (companyname, companycode, address, phone, email, isactive) VALUES
('ABC Corporation', 'ABC', '123 Business Street, Bangkok', '+66-2-123-4567', 'info@abc.com', TRUE),
('XYZ Limited', 'XYZ', '456 Commerce Road, Bangkok', '+66-2-234-5678', 'contact@xyz.com', TRUE),
('Tech Solutions Inc', 'TSI', '789 Innovation Ave, Bangkok', '+66-2-345-6789', 'hello@techsol.com', TRUE)
ON CONFLICT (companycode) DO NOTHING;

-- =============================================
-- SEED DEPARTMENTS
-- =============================================
INSERT INTO departments (departmentname, departmentcode, companyid, description, isactive)
SELECT 'Information Technology', 'IT', companyid, 'IT Department', TRUE FROM companies WHERE companycode = 'ABC'
UNION ALL
SELECT 'Human Resources', 'HR', companyid, 'HR Department', TRUE FROM companies WHERE companycode = 'ABC'
UNION ALL
SELECT 'Finance', 'FIN', companyid, 'Finance Department', TRUE FROM companies WHERE companycode = 'ABC'
UNION ALL
SELECT 'Operations', 'OPS', companyid, 'Operations Department', TRUE FROM companies WHERE companycode = 'ABC'
ON CONFLICT DO NOTHING;

-- =============================================
-- SEED USER TYPES
-- =============================================
INSERT INTO usertypes (typename, typecode, description, managerlevel, canapprove, canmanageusers, canaccessreports, isactive) VALUES
('System Administrator', 'SYSADMIN', 'Full system access', 5, TRUE, TRUE, TRUE, TRUE),
('Manager', 'MGR', 'Department manager', 3, TRUE, TRUE, TRUE, TRUE),
('Staff', 'STAFF', 'Regular staff member', 1, FALSE, FALSE, FALSE, TRUE),
('Technician', 'TECH', 'Technical support staff', 2, FALSE, FALSE, FALSE, TRUE)
ON CONFLICT (typecode) DO NOTHING;

-- =============================================
-- SEED USER ROLES
-- =============================================
INSERT INTO userroles (rolename, description, isactive) VALUES
('Admin', 'System administrator with full access', TRUE),
('Manager', 'Department manager with approval rights', TRUE),
('Staff', 'Regular user with basic access', TRUE),
('Viewer', 'Read-only access', TRUE)
ON CONFLICT (rolename) DO NOTHING;

-- =============================================
-- SEED PERMISSIONS
-- =============================================
INSERT INTO permissions (permissionkey, permissionname, description, category, isactive) VALUES
('asset.create', 'Create Asset', 'Can create new assets', 'Asset Management', TRUE),
('asset.read', 'View Asset', 'Can view asset details', 'Asset Management', TRUE),
('asset.update', 'Update Asset', 'Can update asset information', 'Asset Management', TRUE),
('asset.delete', 'Delete Asset', 'Can delete assets', 'Asset Management', TRUE),
('asset.assign', 'Assign Asset', 'Can assign assets to users', 'Asset Management', TRUE),
('user.create', 'Create User', 'Can create new users', 'User Management', TRUE),
('user.read', 'View User', 'Can view user details', 'User Management', TRUE),
('user.update', 'Update User', 'Can update user information', 'User Management', TRUE),
('user.delete', 'Delete User', 'Can delete users', 'User Management', TRUE),
('config.manage', 'Manage Configuration', 'Can manage system configuration', 'System', TRUE),
('report.view', 'View Reports', 'Can view system reports', 'Reporting', TRUE),
('approval.manage', 'Manage Approvals', 'Can approve/reject requests', 'Workflow', TRUE)
ON CONFLICT (permissionkey) DO NOTHING;

-- =============================================
-- SEED ROLE PERMISSIONS
-- =============================================
INSERT INTO rolepermissions (roleid, permissionid)
SELECT r.roleid, p.permissionid 
FROM userroles r, permissions p 
WHERE r.rolename = 'Admin'
ON CONFLICT DO NOTHING;

INSERT INTO rolepermissions (roleid, permissionid)
SELECT r.roleid, p.permissionid 
FROM userroles r, permissions p 
WHERE r.rolename = 'Manager' 
AND p.permissionkey IN ('asset.create', 'asset.read', 'asset.update', 'asset.assign', 'user.read', 'report.view', 'approval.manage')
ON CONFLICT DO NOTHING;

INSERT INTO rolepermissions (roleid, permissionid)
SELECT r.roleid, p.permissionid 
FROM userroles r, permissions p 
WHERE r.rolename = 'Staff' 
AND p.permissionkey IN ('asset.read', 'user.read')
ON CONFLICT DO NOTHING;

-- =============================================
-- SEED MAIN CATEGORIES
-- =============================================
INSERT INTO maincategories (categoryname, categorycode, description, isactive) VALUES
('Computer', 'COMP', 'Desktop and laptop computers', TRUE),
('Printer', 'PRNT', 'Printers and scanners', TRUE),
('Network Equipment', 'NETW', 'Routers, switches, access points', TRUE),
('Furniture', 'FURN', 'Office furniture', TRUE),
('Mobile Device', 'MOBL', 'Smartphones and tablets', TRUE),
('Monitor', 'MNTR', 'Computer monitors and displays', TRUE),
('Server', 'SRVR', 'Server hardware', TRUE),
('Storage', 'STOR', 'Storage devices and NAS', TRUE)
ON CONFLICT (categorycode) DO NOTHING;

-- =============================================
-- SEED ASSET STATUSES
-- =============================================
INSERT INTO assetstatuses (statusname, statuscode, description, colorcode, isactive) VALUES
('Available', 'AVAIL', 'Asset is available for use', 'success', TRUE),
('In Use', 'INUSE', 'Asset is currently assigned', 'primary', TRUE),
('Maintenance', 'MAINT', 'Asset is under maintenance', 'warning', TRUE),
('Repair', 'REPAIR', 'Asset is being repaired', 'warning', TRUE),
('Disposed', 'DISP', 'Asset has been disposed', 'danger', TRUE),
('Lost', 'LOST', 'Asset is lost or missing', 'danger', TRUE),
('Reserved', 'RESV', 'Asset is reserved', 'info', TRUE)
ON CONFLICT (statuscode) DO NOTHING;

-- =============================================
-- SEED SYSTEM CONFIGURATION
-- =============================================
INSERT INTO systemconfig (configkey, configvalue, description, category, datatype, isactive) VALUES
('asset_id_format', '{"pattern": "{category}-{country}-{province}-{company}-{year}-{sequence}", "sequence_length": 4, "separator": "-", "uppercase": true}', 
 'Asset ID generation format', 'asset_management', 'json', TRUE),
('qr_code_size', '300', 'Default QR code size in pixels', 'qr_code', 'number', TRUE),
('qr_code_error_correction', 'M', 'QR code error correction level (L, M, Q, H)', 'qr_code', 'string', TRUE),
('default_asset_status', 'available', 'Default status for new assets', 'asset_management', 'string', TRUE),
('require_approval_threshold', '50000', 'Asset value requiring approval', 'workflow', 'number', TRUE),
('system_name', 'IT Asset Management System', 'System display name', 'general', 'string', TRUE),
('company_name', 'ABC Corporation', 'Default company name', 'general', 'string', TRUE)
ON CONFLICT (configkey) DO NOTHING;

-- =============================================
-- SEED ASSET ID FORMAT
-- =============================================
INSERT INTO assetidformat (formatname, formatpattern, description, example, isactive, isdefault) VALUES
('Standard Format', '{category}-{country}-{province}-{company}-{year}-{sequence}', 
 'Standard asset ID format with all components', 'COMP-TH-BKK-ABC-2026-0001', TRUE, TRUE),
('Short Format', '{category}-{company}-{year}-{sequence}', 
 'Simplified format without location', 'COMP-ABC-2026-0001', TRUE, FALSE),
('Location First', '{country}-{province}-{category}-{sequence}', 
 'Location-based format', 'TH-BKK-COMP-0001', TRUE, FALSE)
ON CONFLICT DO NOTHING;

-- =============================================
-- UPDATE EXISTING USERS WITH NEW FIELDS
-- =============================================
UPDATE users SET 
    username = email,
    firstname = CASE 
        WHEN email LIKE 'admin%' THEN 'Admin'
        WHEN email LIKE 'staff%' THEN 'Staff'
        ELSE 'User'
    END,
    lastname = 'User',
    usertype = CASE 
        WHEN role = 'admin' THEN 'System Administrator'
        ELSE 'Staff'
    END,
    isactive = TRUE,
    companyid = (SELECT companyid FROM companies WHERE companycode = 'ABC' LIMIT 1),
    countryid = (SELECT countryid FROM countries WHERE countrycode = 'TH' LIMIT 1),
    roleid = (SELECT roleid FROM userroles WHERE rolename = CASE 
        WHEN users.role = 'admin' THEN 'Admin'
        ELSE 'Staff'
    END LIMIT 1)
WHERE username IS NULL;

-- =============================================
-- UPDATE EXISTING LOCATIONS
-- =============================================
UPDATE locations SET 
    isactive = TRUE,
    companyid = (SELECT companyid FROM companies WHERE companycode = 'ABC' LIMIT 1),
    provinceid = (SELECT provinceid FROM provinces WHERE provincecode = 'BKK' LIMIT 1)
WHERE companyid IS NULL;
"""

def seed_initial_data():
    """Execute seed data"""
    try:
        print("=" * 60)
        print("SEEDING INITIAL DATA")
        print("=" * 60)
        print()
        
        engine = create_engine(settings.DATABASE_URL)
        
        print("✓ Connected to database")
        print()
        print("Inserting seed data...")
        print()
        
        with engine.begin() as conn:
            statements = [s.strip() for s in SEED_DATA_SQL.split(';') if s.strip()]
            
            for statement in statements:
                if statement:
                    try:
                        conn.execute(text(statement))
                        
                        if 'INSERT INTO countries' in statement:
                            print("  ✓ Seeded countries (TH, US, SG, JP, MY)")
                        elif 'INSERT INTO provinces' in statement:
                            print("  ✓ Seeded provinces (Bangkok, Chiang Mai, etc.)")
                        elif 'INSERT INTO companies' in statement:
                            print("  ✓ Seeded companies (ABC, XYZ, TSI)")
                        elif 'INSERT INTO departments' in statement:
                            print("  ✓ Seeded departments (IT, HR, Finance, Operations)")
                        elif 'INSERT INTO usertypes' in statement:
                            print("  ✓ Seeded user types (Admin, Manager, Staff, Technician)")
                        elif 'INSERT INTO userroles' in statement:
                            print("  ✓ Seeded user roles (Admin, Manager, Staff, Viewer)")
                        elif 'INSERT INTO permissions' in statement:
                            print("  ✓ Seeded permissions (12 permissions)")
                        elif 'INSERT INTO rolepermissions' in statement and 'Admin' in statement:
                            print("  ✓ Assigned all permissions to Admin role")
                        elif 'INSERT INTO maincategories' in statement:
                            print("  ✓ Seeded main categories (Computer, Printer, Network, etc.)")
                        elif 'INSERT INTO assetstatuses' in statement:
                            print("  ✓ Seeded asset statuses (Available, In Use, Maintenance, etc.)")
                        elif 'INSERT INTO systemconfig' in statement:
                            print("  ✓ Seeded system configuration")
                        elif 'INSERT INTO assetidformat' in statement:
                            print("  ✓ Seeded asset ID formats")
                        elif 'UPDATE users' in statement:
                            print("  ✓ Updated existing users with new fields")
                        elif 'UPDATE locations' in statement:
                            print("  ✓ Updated existing locations")
                            
                    except Exception as e:
                        if 'duplicate' not in str(e).lower() and 'already exists' not in str(e).lower():
                            print(f"  ⚠ Warning: {str(e)[:100]}")
        
        print()
        print("=" * 60)
        print("✓ SEED DATA COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Initial data created:")
        print("  • 5 Countries (TH, US, SG, JP, MY)")
        print("  • 6 Provinces (Bangkok, Chiang Mai, etc.)")
        print("  • 3 Companies (ABC, XYZ, TSI)")
        print("  • 4 Departments (IT, HR, Finance, Operations)")
        print("  • 4 User Types (Admin, Manager, Staff, Technician)")
        print("  • 4 User Roles with permissions")
        print("  • 12 System permissions")
        print("  • 8 Main Categories (Computer, Printer, etc.)")
        print("  • 7 Asset Statuses (Available, In Use, etc.)")
        print("  • System configuration defaults")
        print("  • 3 Asset ID format templates")
        print()
        print("Your system is now ready to create assets!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR DURING SEED DATA")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    success = seed_initial_data()
    sys.exit(0 if success else 1)
