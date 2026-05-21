"""
Seed Categories and Other Missing Data
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def seed_categories():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.begin() as conn:
        # Seed main categories
        conn.execute(text("""
            INSERT INTO maincategories (categoryname, categorycode, description, isactive) VALUES
            ('Computer', 'COMP', 'Desktop and laptop computers', TRUE),
            ('Printer', 'PRNT', 'Printers and scanners', TRUE),
            ('Network Equipment', 'NETW', 'Routers, switches, access points', TRUE),
            ('Furniture', 'FURN', 'Office furniture', TRUE),
            ('Mobile Device', 'MOBL', 'Smartphones and tablets', TRUE),
            ('Monitor', 'MNTR', 'Computer monitors and displays', TRUE),
            ('Server', 'SRVR', 'Server hardware', TRUE),
            ('Storage', 'STOR', 'Storage devices and NAS', TRUE)
            ON CONFLICT (categorycode) DO NOTHING
        """))
        
        # Seed asset statuses
        conn.execute(text("""
            INSERT INTO assetstatuses (statusname, statuscode, description, colorcode, isactive) VALUES
            ('Available', 'AVAIL', 'Asset is available for use', 'success', TRUE),
            ('In Use', 'INUSE', 'Asset is currently assigned', 'primary', TRUE),
            ('Maintenance', 'MAINT', 'Asset is under maintenance', 'warning', TRUE),
            ('Repair', 'REPAIR', 'Asset is being repaired', 'warning', TRUE),
            ('Disposed', 'DISP', 'Asset has been disposed', 'danger', TRUE),
            ('Lost', 'LOST', 'Asset is lost or missing', 'danger', TRUE),
            ('Reserved', 'RESV', 'Asset is reserved', 'info', TRUE)
            ON CONFLICT (statuscode) DO NOTHING
        """))
        
        # Seed user types
        conn.execute(text("""
            INSERT INTO usertypes (typename, typecode, description, managerlevel, canapprove, canmanageusers, canaccessreports, isactive) VALUES
            ('System Administrator', 'SYSADMIN', 'Full system access', 5, TRUE, TRUE, TRUE, TRUE),
            ('Manager', 'MGR', 'Department manager', 3, TRUE, TRUE, TRUE, TRUE),
            ('Staff', 'STAFF', 'Regular staff member', 1, FALSE, FALSE, FALSE, TRUE),
            ('Technician', 'TECH', 'Technical support staff', 2, FALSE, FALSE, FALSE, TRUE)
            ON CONFLICT (typecode) DO NOTHING
        """))
        
        # Seed user roles
        conn.execute(text("""
            INSERT INTO userroles (rolename, description, isactive) VALUES
            ('Admin', 'System administrator with full access', TRUE),
            ('Manager', 'Department manager with approval rights', TRUE),
            ('Staff', 'Regular user with basic access', TRUE),
            ('Viewer', 'Read-only access', TRUE)
            ON CONFLICT (rolename) DO NOTHING
        """))
        
        # Seed system config
        conn.execute(text("""
            INSERT INTO systemconfig (configkey, configvalue, description, category, datatype, isactive) VALUES
            ('asset_id_format', '{"pattern": "{category}-{country}-{province}-{company}-{year}-{sequence}", "sequence_length": 4}', 
             'Asset ID generation format', 'asset_management', 'json', TRUE),
            ('qr_code_size', '300', 'Default QR code size in pixels', 'qr_code', 'number', TRUE),
            ('default_asset_status', 'available', 'Default status for new assets', 'asset_management', 'string', TRUE)
            ON CONFLICT (configkey) DO NOTHING
        """))
        
        print("✓ Categories seeded successfully!")
        print("✓ Asset statuses seeded successfully!")
        print("✓ User types seeded successfully!")
        print("✓ User roles seeded successfully!")
        print("✓ System config seeded successfully!")

if __name__ == "__main__":
    seed_categories()
