from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes import auth, users, assets, inventory, audits
from .routes import assets_enhanced, admin  # Enhanced routes
from .routes import countries, provinces, companies, main_categories, asset_utils, locations  # Location hierarchy & utilities
from .routes import departments, asset_statuses, asset_transfers  # Asset control features
from .routes import config, staff, asset_checkinout_history, stock_location, data_import, asset_requests, cost_centers  # Configuration management & staff & history & stock location & data import & asset requests & cost centers
from .core.database import engine, Base

from .models import (
    User, Category, Location, Asset, 
    InventoryItem, InventoryTransaction,
    AuditSession, AuditRecord,
    Country, Province, Company, MainCategory, AssetSequence,
    Department, AssetStatus, AssetTransfer, SystemConfig, Staff,
    AssetCheckInOutHistory, StockLocation, AssetConditionReport, AssetRequest, CostCenter
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Asset Management System",
    version="2.0.0",
    description="Comprehensive IT Asset Management with QR codes, auto-generated IDs, and lifecycle tracking"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication & Users
app.include_router(auth.router)
app.include_router(users.router)

# Location Hierarchy
app.include_router(countries.router)
app.include_router(provinces.router)
app.include_router(companies.router)
app.include_router(locations.router)
app.include_router(main_categories.router)

# Asset Control Features
app.include_router(departments.router)
app.include_router(asset_statuses.router)
app.include_router(asset_transfers.router)

# Asset Management (Enhanced)
app.include_router(assets_enhanced.router)  # New comprehensive asset routes
app.include_router(assets.router)  # Keep legacy routes for compatibility
app.include_router(asset_utils.router)  # Asset ID & QR code utilities

# Inventory & Audits
app.include_router(inventory.router)
app.include_router(audits.router)

# Admin & Configuration
app.include_router(admin.router)  # Admin routes
app.include_router(config.router)  # Configuration management
app.include_router(staff.router)  # Staff management
app.include_router(asset_checkinout_history.router)  # Check-in/check-out history
app.include_router(stock_location.router)  # Stock location management
app.include_router(data_import.router)  # Batch import/export (Excel)
app.include_router(asset_requests.router)  # HR asset request tickets
app.include_router(cost_centers.router)  # Cost center management

@app.get("/")
def root():
    return {
        "message": "IT Asset Management System API",
        "version": "2.0.0",
        "features": [
            "Auto-generated Asset IDs",
            "QR Code Generation",
            "Asset Lifecycle Management",
            "System Configuration",
            "Comprehensive Tracking"
        ],
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0"
    }

# Serve local uploaded files
uploads_dir = Path(__file__).parent.parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
