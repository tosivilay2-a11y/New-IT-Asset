# Assets Management Page - User Guide

## Overview
The new Assets Management page provides a comprehensive interface for managing IT assets with advanced filtering, detailed asset information, and multi-tab asset creation.

## Features

### 1. **Asset List View**
- **Filters**: Year, Category, Location, Status
- **Table Columns**:
  - Asset ID (auto-generated)
  - Asset Name
  - Category (with badge)
  - Cost Center Location
  - Current Location
  - Status (color-coded badges)
  - Assigned To
  - Actions (View, Edit, Delete)

### 2. **Add New Asset Modal**
The asset creation form is organized into 5 tabs:

#### Tab 1: Basic Information
- **Asset ID Generation Fields** (Required):
  - Main Category (Laptop, Desktop, Monitor, etc.)
  - Country (Lao - LA)
  - Province (Vientiane, Luang Prabang, etc.)
  - Company (filtered by province)
  - Location
  - Purchase Date

- **Asset Details**:
  - Status (Available, In Use, Maintenance, Retired)
  - Category/Type
  - Brand
  - Model Name
  - Model Number
  - Serial Number
  - S/N Type
  - Description

#### Tab 2: Technical Specs
- Processor
- RAM
- Storage
- Graphics Card
- Display
- Operating System

#### Tab 3: Assignment
- Assigned To (Employee name)
- Department
- Assignment Date

#### Tab 4: Purchase Info
- Supplier
- Purchase Cost
- Invoice Number
- Warranty End Date

#### Tab 5: QR Code & Label
- QR Code preview (generated after creation)
- Label information

## Asset ID Format

The system auto-generates Asset IDs using the following format:

```
[Category][Country][Province][Company][Year][Sequence]
```

**Example**: `MLALPBAVIS25015`
- `M` = Monitor
- `LA` = Lao
- `LPB` = Luang Prabang
- `AVIS` = Company code
- `25` = Year 2025
- `015` = Sequence number

## Status Types

| Status | Color | Description |
|--------|-------|-------------|
| Available | Green | Asset is available for use |
| In Use | Blue | Asset is currently assigned |
| Maintenance | Orange | Asset is under maintenance |
| Retired | Purple | Asset is retired from service |
| Disposed | Red | Asset has been disposed |

## Filtering Assets

1. **Year Filter**: Filter by purchase year
2. **Category Filter**: Filter by asset type (Laptop, Desktop, etc.)
3. **Location Filter**: Filter by physical location
4. **Status Filter**: Filter by current status
5. **Clear Filters**: Reset all filters to show all assets

## Actions

### View Asset
- Click the eye icon (👁️) to view full asset details
- Shows all information across all tabs

### Edit Asset
- Click the pencil icon (✏️) to edit asset information
- Opens the same modal with pre-filled data

### Delete Asset
- Click the trash icon (🗑️) to delete an asset
- Requires confirmation before deletion

## Best Practices

1. **Always fill required fields** marked with asterisk (*)
2. **Use consistent naming** for brands and models
3. **Keep serial numbers accurate** for warranty tracking
4. **Update status regularly** to reflect current state
5. **Assign assets promptly** when deployed to users
6. **Document technical specs** for IT support reference

## API Endpoints Used

- `GET /assets` - Fetch all assets
- `POST /assets` - Create new asset
- `PUT /assets/{id}` - Update asset
- `DELETE /assets/{id}` - Delete asset
- `GET /assets/{id}/qr` - Generate QR code

## Keyboard Shortcuts

- `Esc` - Close modal
- `Ctrl + F` - Focus on search (when implemented)
- `Tab` - Navigate between form fields

## Mobile Responsive

The page is fully responsive and adapts to:
- Desktop (1400px+)
- Tablet (768px - 1399px)
- Mobile (< 768px)

## Troubleshooting

### Assets not loading
- Check backend connection
- Verify authentication token
- Check browser console for errors

### Cannot create asset
- Ensure all required fields are filled
- Check that Asset ID is unique
- Verify backend API is running

### Filters not working
- Clear browser cache
- Refresh the page
- Check filter values match asset data

## Future Enhancements

- [ ] Bulk import from Excel
- [ ] Export to PDF/Excel
- [ ] Advanced search
- [ ] Asset history timeline
- [ ] Maintenance scheduling
- [ ] Depreciation calculator
- [ ] Asset transfer workflow
- [ ] Email notifications

---

**Version**: 1.0.0  
**Last Updated**: May 5, 2026  
**Page Route**: `/assets`
