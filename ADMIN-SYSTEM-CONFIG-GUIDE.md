# Admin System Configuration Guide

## 🎯 Overview

The **System Configuration** section provides administrators with a comprehensive interface to manage all location hierarchy data and understand asset ID generation.

## 📍 Access

**URL**: http://localhost:3000/admin/config  
**Navigation**: Click "⚙️ Admin" in the top navigation bar

## 🎨 Features

### 1. Asset ID Generator Tab

Interactive tool to understand and preview asset ID format.

**Features:**
- Visual format breakdown
- Interactive selection
- Real-time preview
- Component explanation

**How to Use:**
1. Select Category (e.g., Monitor)
2. Select Country (e.g., Lao PDR)
3. Select Province (e.g., Luang Prabang)
4. Select Company (e.g., AVIS)
5. See generated ID: `MLALPBAVIS25015`

### 2. Countries Management Tab

Manage countries for location hierarchy.

**Features:**
- View all countries
- Add new country
- Edit existing country
- Delete country (soft delete)
- Activate/deactivate

**Fields:**
- Country Name (e.g., "Lao PDR")
- Country Code (2 chars, e.g., "LA")
- Active status

**Actions:**
- ✏️ Edit - Modify country details
- 🗑️ Delete - Soft delete (sets inactive)

### 3. Provinces Management Tab

Manage provinces/states within countries.

**Features:**
- View all provinces
- Filter by country
- Add new province
- Edit existing province
- Delete province

**Fields:**
- Province Name (e.g., "Vientiane Capital")
- Province Code (3 chars, e.g., "VTE")
- Country (dropdown)
- Active status

**Relationship:**
- Each province belongs to one country
- Provinces are used in asset ID generation

### 4. Companies Management Tab

Manage companies/organizations.

**Features:**
- View all companies
- Add new company
- Edit existing company
- Delete company
- Full contact information

**Fields:**
- Company Name (e.g., "AVIS Rent A Car")
- Company Code (4 chars, e.g., "AVIS")
- Province (optional)
- Address
- Phone
- Email
- Active status

**Relationship:**
- Companies can be linked to provinces
- Company code is used in asset ID

### 5. Categories Management Tab

Manage main asset categories.

**Features:**
- View all categories
- Add new category
- Edit existing category
- Delete category
- Single-letter codes

**Fields:**
- Category Name (e.g., "Monitor")
- Category Code (1 char, e.g., "M")
- Description
- Active status

**Pre-seeded Categories:**
- C = Computer
- L = Laptop
- M = Monitor
- P = Printer
- N = Network
- S = Server
- W = Workstation
- T = Tablet
- H = Phone
- A = Accessory
- D = Desktop
- U = UPS
- O = Other

## 🎨 UI Components

### Tab Navigation

```
[🔢 Asset ID Generator] [🌍 Countries] [🏛️ Provinces] [🏢 Companies] [📦 Categories]
```

### Data Table

Each management tab shows a table with:
- ID column
- Name/Description columns
- Code column (with badge)
- Status badge (Active/Inactive)
- Action buttons (Edit/Delete)

### Add/Edit Modal

Modal form with:
- Form fields
- Validation
- Cancel/Save buttons
- Error messages
- Success notifications

## 📊 Data Relationships

```
Country (LA)
  └── Province (VTE)
      └── Company (AVIS)
          └── Assets
```

## 🔢 Asset ID Format

```
Format: [Category][Country][Province][Company][Year][Sequence]
Length: 15 characters total

Example: MLALPBAVIS25015

Breakdown:
M     = Monitor (1 char)
LA    = Lao (2 chars)
LPB   = Luang Prabang (3 chars)
AVIS  = Company (4 chars)
25    = Year 2025 (2 chars)
015   = Sequence #15 (3 chars)
```

## 🚀 Common Tasks

### Add a New Country

1. Go to **Countries** tab
2. Click "+ Add Country"
3. Enter:
   - Country Name: "Thailand"
   - Country Code: "TH"
   - Check "Active"
4. Click "Create"

### Add a New Province

1. Go to **Provinces** tab
2. Click "+ Add Province"
3. Enter:
   - Province Name: "Bangkok"
   - Province Code: "BKK"
   - Country: Select "Thailand (TH)"
   - Check "Active"
4. Click "Create"

### Add a New Company

1. Go to **Companies** tab
2. Click "+ Add Company"
3. Enter:
   - Company Name: "AVIS Rent A Car"
   - Company Code: "AVIS"
   - Province: Select "Bangkok (BKK)"
   - Address, Phone, Email (optional)
   - Check "Active"
4. Click "Create"

### Add a New Category

1. Go to **Categories** tab
2. Click "+ Add Category"
3. Enter:
   - Category Name: "Tablet"
   - Category Code: "T"
   - Description: "Tablet devices"
   - Check "Active"
4. Click "Create"

### Test Asset ID Generation

1. Go to **Asset ID Generator** tab
2. Select:
   - Category: [M] Monitor
   - Country: Lao PDR (LA)
   - Province: Luang Prabang (LPB)
   - Company: AVIS
3. See preview: `MLALPBAVIS25015`
4. View breakdown of each component

## 📝 Validation Rules

### Country Code
- Must be exactly 2 characters
- Uppercase letters only
- Must be unique

### Province Code
- Must be exactly 3 characters
- Uppercase letters only
- Can be duplicated across countries

### Company Code
- Must be exactly 4 characters
- Uppercase letters only
- Must be unique

### Category Code
- Must be exactly 1 character
- Uppercase letter only
- Must be unique

## 🎯 Best Practices

### Naming Conventions

**Countries:**
- Use official country names
- Use ISO 3166-1 alpha-2 codes

**Provinces:**
- Use official province/state names
- Use common abbreviations

**Companies:**
- Use full legal names
- Use recognizable abbreviations

**Categories:**
- Use clear, descriptive names
- Choose intuitive single letters

### Code Selection

**Good Examples:**
- LA = Lao PDR
- VTE = Vientiane
- AVIS = AVIS Rent A Car
- M = Monitor

**Bad Examples:**
- XX = Unknown country
- ABC = Random province
- COMP = Too generic

## 🔒 Security

**Access Control:**
- Only admin users should access this section
- All changes are logged
- Soft deletes preserve data integrity

**Data Integrity:**
- Cannot delete items in use
- Codes must be unique
- Relationships are enforced

## 🐛 Troubleshooting

### "Country code already exists"
- Each country code must be unique
- Check existing countries first
- Use standard ISO codes

### "Cannot delete country"
- Country has provinces
- Delete provinces first
- Or use soft delete (deactivate)

### "Province not showing in dropdown"
- Check if province is active
- Check if country is selected
- Refresh the page

### "Asset ID preview not updating"
- Ensure all fields are selected
- Check browser console for errors
- Verify backend is running

## 📱 Mobile Support

All admin pages are mobile-responsive:
- Tables scroll horizontally
- Forms stack vertically
- Touch-friendly buttons
- Optimized layouts

## 🔗 Integration

### With Asset Creation

When creating an asset:
1. Select category from Categories
2. Select location from Countries/Provinces/Companies
3. Asset ID is auto-generated using these codes
4. Sequence increments per company per year

### With Location Selector

The LocationSelector component uses:
- Countries from Countries table
- Provinces from Provinces table
- Companies from Companies table

### With Asset ID Preview

The AssetIDPreview component uses:
- Category codes from Categories
- Location codes from hierarchy
- Current year
- Next sequence number

## 📊 Statistics

After seeding, you'll have:
- **5 Countries** (LA, TH, VN, KH, MM)
- **8 Provinces** (VTE, LPB, CPS, SVK, APU, BKK, CNX, HKT)
- **7 Companies** (AVIS, FORD, EFGL, LARV, RMAG, COMN)
- **13 Categories** (C, L, M, P, N, S, W, T, H, A, O, D, U)

## 🎓 Training Tips

### For Administrators

1. **Start with Asset ID Generator**
   - Understand the format first
   - See how codes combine
   - Test different combinations

2. **Set Up Location Hierarchy**
   - Add countries first
   - Then provinces
   - Then companies
   - Test in asset creation

3. **Configure Categories**
   - Review existing categories
   - Add custom categories if needed
   - Use meaningful codes

### For Users

1. **Understanding Asset IDs**
   - Show them the generator
   - Explain each component
   - Demonstrate with examples

2. **Location Selection**
   - Explain the hierarchy
   - Show cascading dropdowns
   - Practice with test data

## 📚 Related Documentation

- **Phase 1**: `INTEGRATION-PHASE1-COMPLETE.md`
- **Phase 2**: `INTEGRATION-PHASE2-COMPLETE.md`
- **Location Hierarchy**: `LOCATION-HIERARCHY-GUIDE.md`
- **Quick Reference**: `QUICK-REFERENCE.md`

## ✅ Checklist

Before going live:
- [ ] All countries added
- [ ] All provinces added
- [ ] All companies added
- [ ] All categories configured
- [ ] Asset ID generator tested
- [ ] Location hierarchy verified
- [ ] Test asset created successfully
- [ ] QR codes generated
- [ ] Admin access restricted

---

**Access**: http://localhost:3000/admin/config  
**Status**: ✅ Production Ready  
**Last Updated**: May 5, 2026
