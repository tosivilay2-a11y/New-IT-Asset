"""
Sample data seeding script for Asset Management System
Run this after setting up the database to populate with sample data
"""
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models import (
    User, Category, Location, Asset, 
    InventoryItem, InventoryTransaction, 
    AuditSession, AuditRecord
)

def seed_database():
    db = SessionLocal()
    
    try:
        # Create users
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role="admin"
        )
        staff = User(
            email="staff@example.com",
            hashed_password=get_password_hash("staff123"),
            full_name="Staff User",
            role="staff"
        )
        db.add_all([admin, staff])
        db.commit()
        
        # Create categories
        categories = [
            Category(name="Electronics", description="Electronic devices and equipment"),
            Category(name="Furniture", description="Office furniture"),
            Category(name="Vehicles", description="Company vehicles"),
        ]
        db.add_all(categories)
        db.commit()
        
        # Create locations
        locations = [
            Location(name="Main Office", address="123 Main St"),
            Location(name="Warehouse", address="456 Storage Ave"),
            Location(name="Branch Office", address="789 Branch Rd"),
        ]
        db.add_all(locations)
        db.commit()
        
        # Create assets
        assets = [
            Asset(
                asset_id="LAPTOP001",
                name="Dell Latitude 5520",
                category_id=categories[0].id,
                purchase_date=datetime.now() - timedelta(days=365),
                value=1200.00,
                status="in_use",
                assigned_user_id=staff.id,
                location_id=locations[0].id
            ),
            Asset(
                asset_id="DESK001",
                name="Standing Desk",
                category_id=categories[1].id,
                purchase_date=datetime.now() - timedelta(days=180),
                value=800.00,
                status="available",
                location_id=locations[0].id
            ),
            Asset(
                asset_id="VAN001",
                name="Ford Transit Van",
                category_id=categories[2].id,
                purchase_date=datetime.now() - timedelta(days=730),
                value=35000.00,
                status="in_use",
                location_id=locations[1].id
            ),
        ]
        db.add_all(assets)
        db.commit()
        
        # Create inventory items
        inventory_items = [
            InventoryItem(
                name="USB Cable",
                sku="USB-C-001",
                quantity=50,
                min_quantity=20,
                unit_price=5.99,
                location_id=locations[1].id
            ),
            InventoryItem(
                name="Office Chair",
                sku="CHAIR-001",
                quantity=5,
                min_quantity=10,
                unit_price=150.00,
                location_id=locations[1].id
            ),
            InventoryItem(
                name="Printer Paper",
                sku="PAPER-A4",
                quantity=100,
                min_quantity=50,
                unit_price=8.99,
                location_id=locations[0].id
            ),
        ]
        db.add_all(inventory_items)
        db.commit()
        
        # Create inventory transactions
        transactions = [
            InventoryTransaction(
                inventory_item_id=inventory_items[0].id,
                transaction_type="stock_in",
                quantity=50,
                reference="PO-2024-001",
                notes="Initial stock"
            ),
            InventoryTransaction(
                inventory_item_id=inventory_items[1].id,
                transaction_type="stock_in",
                quantity=15,
                reference="PO-2024-002"
            ),
            InventoryTransaction(
                inventory_item_id=inventory_items[1].id,
                transaction_type="stock_out",
                quantity=10,
                reference="REQ-2024-001",
                notes="Distributed to offices"
            ),
        ]
        db.add_all(transactions)
        db.commit()
        
        # Create audit session
        audit = AuditSession(
            name="Q1 2024 Inventory Audit",
            status="completed",
            created_by=admin.id,
            completed_at=datetime.now()
        )
        db.add(audit)
        db.commit()
        
        # Create audit records
        audit_records = [
            AuditRecord(
                audit_session_id=audit.id,
                inventory_item_id=inventory_items[0].id,
                expected_quantity=50,
                actual_quantity=48,
                discrepancy_type="missing",
                notes="2 units unaccounted for"
            ),
            AuditRecord(
                audit_session_id=audit.id,
                inventory_item_id=inventory_items[2].id,
                expected_quantity=100,
                actual_quantity=100,
                discrepancy_type="none"
            ),
        ]
        db.add_all(audit_records)
        db.commit()
        
        print("✓ Database seeded successfully!")
        print("\nDefault credentials:")
        print("Admin: admin@example.com / admin123")
        print("Staff: staff@example.com / staff123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
