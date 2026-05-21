# Phase 2 UI Guide

## 🎨 New UI Components

### 1. Asset ID Preview Card

```
┌─────────────────────────────────────────────────────────┐
│ Asset ID Preview                    ● Auto-generated    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│              MLALPBAVIS25015                            │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  M    LA    LPB   AVIS   25    015                     │
│ Cat  Ctry  Prov  Comp  Year   Seq                      │
├─────────────────────────────────────────────────────────┤
│ 💡 This ID will be automatically generated when you     │
│    save the asset                                        │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Purple gradient background
- Large, monospace font for ID
- Component breakdown
- Animated status dot
- Auto-updates on changes

### 2. Location Selector

```
┌──────────────────────────────────────────────────────────┐
│ Location *                                                │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────┐│
│  │ Country *       │  │ Province *      │  │ Company *││
│  ├─────────────────┤  ├─────────────────┤  ├──────────┤│
│  │ Lao PDR (LA)   ▼│  │ Luang Prabang  ▼│  │ AVIS    ▼││
│  └─────────────────┘  └─────────────────┘  └──────────┘│
│                                                           │
└──────────────────────────────────────────────────────────┘
```

**Behavior:**
1. Select Country → Provinces load
2. Select Province → Companies load
3. Select Company → Complete

### 3. Category Selector

```
┌──────────────────────────────────────────────────────────┐
│ Main Category *                                           │
├──────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐ │
│  │ [M] Monitor                                       ▼│ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  Options:                                                 │
│  • [C] Computer                                          │
│  • [L] Laptop                                            │
│  • [M] Monitor                                           │
│  • [P] Printer                                           │
│  • [N] Network                                           │
│  • [S] Server                                            │
│  • [W] Workstation                                       │
│  • [T] Tablet                                            │
│  • [H] Phone                                             │
│  • [A] Accessory                                         │
│  • [D] Desktop                                           │
│  • [U] UPS                                               │
│  • [O] Other                                             │
└──────────────────────────────────────────────────────────┘
```

### 4. QR Code Generator

```
┌──────────────────────────────────────────────────────────┐
│ QR Code                          [🔲 Generate QR Code]   │
├──────────────────────────────────────────────────────────┤
│                                                           │
│                    ████████████████                       │
│                    ██          ██                       │
│                    ██  ██████  ██                       │
│                    ██  ██████  ██                       │
│                    ██  ██████  ██                       │
│                    ██          ██                       │
│                    ████████████████                       │
│                                                           │
│                  MLALPBAVIS25015                         │
│                  Dell Monitor 24inch                     │
│                                                           │
│  [🖨️ Print]  [💾 Download]  [📋 Copy]  [🔄 Regenerate] │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## 📱 Enhanced Asset Form

### Tab Navigation

```
┌──────────────────────────────────────────────────────────┐
│  Add New Asset                                        [×] │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [1. Basic Info] [2. Technical] [3. Assignment]          │
│  [4. Purchase] [5. QR Code]                              │
│                                                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Tab Content Here]                                      │
│                                                           │
│                                                           │
│                                                           │
├──────────────────────────────────────────────────────────┤
│                          [Cancel]  [Save Asset]          │
└──────────────────────────────────────────────────────────┘
```

### Tab 1: Basic Information

```
┌──────────────────────────────────────────────────────────┐
│ Basic Information                                         │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Asset ID Preview: MLALPBAVIS25015                   ││
│  │ M  LA  LPB  AVIS  25  015                          ││
│  └─────────────────────────────────────────────────────┘│
│                                                           │
│  Main Category *                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ [M] Monitor                                       ▼│ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  Location *                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Lao PDR ▼│  │ LPB     ▼│  │ AVIS    ▼│              │
│  └──────────┘  └──────────┘  └──────────┘              │
│                                                           │
│  Purchase Date *                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 2025-01-15                                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  Status                    Brand                          │
│  ┌──────────┐             ┌──────────┐                  │
│  │Available▼│             │ Dell     │                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
│  Model                     Model Name                     │
│  ┌──────────┐             ┌──────────┐                  │
│  │ P2422H   │             │ Dell 24" │                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
│  Serial Number             SN Type                        │
│  ┌──────────┐             ┌──────────┐                  │
│  │ SN123456 │             │ Standard │                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
│  Description                                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Dell 24-inch FHD monitor                           │ │
│  │                                                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Tab 2: Technical Specifications

```
┌──────────────────────────────────────────────────────────┐
│ Technical Specifications                                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Processor                 RAM                            │
│  ┌──────────┐             ┌──────────┐                  │
│  │ N/A      │             │ N/A      │                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
│  Storage                   Graphics                       │
│  ┌──────────┐             ┌──────────┐                  │
│  │ N/A      │             │ N/A      │                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
│  Display                   Operating System               │
│  ┌──────────┐             ┌──────────┐                  │
│  │ 24" FHD  │             │ N/A      │                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Tab 3: Assignment Information

```
┌──────────────────────────────────────────────────────────┐
│ Assignment Information                                    │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Assigned To                                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ John Doe                                           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  Department                                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │ IT Department                                      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  Assignment Date                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 2025-01-15                                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Tab 4: Purchase Information

```
┌──────────────────────────────────────────────────────────┐
│ Purchase Information                                      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Supplier                                                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Dell Laos                                          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  Purchase Cost             Invoice Number                 │
│  ┌──────────┐             ┌──────────┐                  │
│  │ 5000000  │             │INV-2025-1│                  │
│  └──────────┘             └──────────┘                  │
│                                                           │
│  Warranty End Date                                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 2028-01-15                                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Tab 5: QR Code & Label

```
┌──────────────────────────────────────────────────────────┐
│ QR Code & Label                                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  QR code will be generated automatically after the        │
│  asset is created. You can generate and print it from     │
│  the asset detail page.                                   │
│                                                           │
│                    ┌──────────┐                          │
│                    │          │                          │
│                    │    🔲    │                          │
│                    │          │                          │
│                    └──────────┘                          │
│                                                           │
│           QR Code will appear here after saving           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

### Asset ID Preview
- Background: Purple gradient (#667eea → #764ba2)
- Text: White
- Status dot: Green (#4ade80)

### Status Badges
- Available: Green (#10b981)
- In Use: Blue (#3b82f6)
- Maintenance: Orange (#f59e0b)
- Retired: Purple (#8b5cf6)
- Disposed: Red (#ef4444)

### Buttons
- Primary: Blue (#3498db)
- Secondary: Gray (#95a5a6)
- Delete: Red (#e74c3c)
- Success: Green (#27ae60)

## 📱 Responsive Breakpoints

### Desktop (> 768px)
- 3-column location selector
- 2-column form fields
- Full-width tables

### Tablet (768px)
- 2-column layouts
- Adjusted spacing
- Larger touch targets

### Mobile (< 768px)
- Single column
- Stacked elements
- Full-width buttons
- Simplified navigation

## 🎯 User Flow

```
1. Click "+ Add New Asset"
   ↓
2. Modal opens on "Basic Info" tab
   ↓
3. Select Category → Asset ID preview appears
   ↓
4. Select Location → Asset ID preview updates
   ↓
5. Fill remaining fields
   ↓
6. Navigate through tabs (optional)
   ↓
7. Click "Save Asset"
   ↓
8. Asset created with auto-generated ID
   ↓
9. Success message shown
   ↓
10. Modal closes, table refreshes
```

## 💡 Tips

### For Best Experience:
1. **Start with Category** - Select category first to see ID preview
2. **Complete Location** - Fill all three location fields
3. **Watch Preview** - Asset ID updates as you select
4. **Use Tabs** - Organize information logically
5. **Save Often** - Don't lose your work

### Keyboard Shortcuts:
- `Tab` - Navigate between fields
- `Enter` - Submit form (when focused on button)
- `Esc` - Close modal
- `Ctrl+P` - Print QR code (when viewing)

## 🔍 Visual Indicators

### Loading States
- Spinner icon
- "Loading..." text
- Disabled inputs

### Error States
- Red border
- Error message below field
- Icon indicator

### Success States
- Green checkmark
- Success message
- Auto-dismiss after 3s

### Required Fields
- Red asterisk (*)
- Bold label
- Validation on submit

---

**UI Design**: Modern, clean, professional  
**Framework**: React with CSS  
**Icons**: Emoji (universal support)  
**Responsive**: Mobile-first approach
