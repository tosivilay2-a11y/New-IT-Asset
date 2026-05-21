# System Config UI - Set Default Workflow

## User Interaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER OPENS SYSTEM CONFIG                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              SystemConfig.jsx Component Loads                   │
│  - Renders tab navigation                                       │
│  - Includes StockLocationConfig component                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         USER CLICKS "📍 Stock Location" TAB                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      StockLocationConfig.jsx Component Mounts                   │
│  - useEffect hook triggers                                      │
│  - Calls loadData()                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         API CALL: GET /stock-locations/                         │
│  - Headers: Authorization: Bearer {token}                       │
│  - Response: Array of stock locations                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              UI RENDERS STOCK LOCATIONS LIST                    │
│                                                                 │
│  ⭐ DEFAULT  RMAL IT Stock                                      │
│             Stock ID: 3 | Company: RMAL                         │
│                                                                 │
│             Ford office                                         │
│             Stock ID: 4 | Company: Ford                         │
│             [✓ Set Default]  ← Button visible                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│    USER CLICKS "✓ Set Default" BUTTON ON "Ford office"         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      handleSetDefault(4) Function Called                        │
│  - Sets loading state to true                                   │
│  - Disables buttons                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│    API CALL: POST /stock-locations/set-default/4               │
│  - Headers: Authorization: Bearer {token}                       │
│  - Backend processes:                                           │
│    1. Validates stock location exists                           │
│    2. Sets all others to stockdefault = false                   │
│    3. Sets location 4 to stockdefault = true                    │
│    4. Commits transaction                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         API RESPONSE: 200 OK                                    │
│  {                                                              │
│    "message": "Stock location 'Ford office' set as default",   │
│    "stock_location": {                                          │
│      "stockid": 4,                                              │
│      "stockname": "Ford office",                                │
│      "locationid": 1,                                           │
│      "stockdefault": true                                       │
│    }                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      SUCCESS MESSAGE DISPLAYED                                  │
│  "Stock location set as default successfully!"                  │
│  (Auto-hides after 3 seconds)                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         loadData() CALLED TO REFRESH UI                         │
│  - Fetches updated stock locations from API                     │
│  - Updates component state                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         API CALL: GET /stock-locations/                         │
│  - Returns updated list with new default                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              UI UPDATES WITH NEW STATE                          │
│                                                                 │
│             RMAL IT Stock                                       │
│             Stock ID: 3 | Company: RMAL                         │
│             [✓ Set Default]  ← Button now visible               │
│                                                                 │
│  ⭐ DEFAULT  Ford office                                        │
│             Stock ID: 4 | Company: Ford                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              WORKFLOW COMPLETE ✅                               │
│  - New default is set                                           │
│  - UI reflects changes                                          │
│  - User can set another default if needed                       │
└─────────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
App
├── SystemConfig (frontend/src/pages/SystemConfig.jsx)
│   ├── Tabs Navigation
│   │   ├── Asset ID Generator
│   │   ├── File Storage
│   │   ├── Stock Location ← User clicks here
│   │   ├── Staff Management
│   │   ├── Countries
│   │   ├── Provinces
│   │   ├── Companies
│   │   └── Categories
│   │
│   └── Tab Content
│       └── StockLocationConfig (frontend/src/components/admin/StockLocationConfig.jsx)
│           ├── Stock Locations List
│           │   ├── Location Item 1
│           │   │   ├── Location Name
│           │   │   ├── Default Badge (if default)
│           │   │   └── Set Default Button (if not default)
│           │   │
│           │   └── Location Item 2
│           │       ├── Location Name
│           │       ├── Default Badge (if default)
│           │       └── Set Default Button (if not default)
│           │
│           ├── Create New Stock Location Form
│           └── Info Cards
```

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND STATE                            │
├──────────────────────────────────────────────────────────────┤
│ stockLocations: [                                            │
│   {                                                          │
│     stockid: 3,                                              │
│     stockname: "RMAL IT Stock",                              │
│     locationid: 1,                                           │
│     stockdefault: false  ← Updated after set-default         │
│   },                                                         │
│   {                                                          │
│     stockid: 4,                                              │
│     stockname: "Ford office",                                │
│     locationid: 2,                                           │
│     stockdefault: true   ← Updated after set-default         │
│   }                                                          │
│ ]                                                            │
└──────────────────────────────────────────────────────────────┘
                          ↕ (API calls)
┌──────────────────────────────────────────────────────────────┐
│                    BACKEND DATABASE                          │
├──────────────────────────────────────────────────────────────┤
│ stocklocation table:                                         │
│                                                              │
│ stockid | stockname        | locationid | stockdefault      │
│---------|------------------|------------|------------------│
│    3    | RMAL IT Stock    |     1      |     false         │
│    4    | Ford office      |     2      |     true          │
│                                                              │
│ (Exactly one row has stockdefault = true)                   │
└──────────────────────────────────────────────────────────────┘
```

## API Endpoints Used

### 1. GET /stock-locations/
**Purpose**: Fetch all stock locations
**Called**: On page load and after set-default

```
Request:
  GET /stock-locations/
  Headers: Authorization: Bearer {token}

Response (200 OK):
  [
    {
      "stockid": 3,
      "stockname": "RMAL IT Stock",
      "locationid": 1,
      "stockdefault": false
    },
    {
      "stockid": 4,
      "stockname": "Ford office",
      "locationid": 2,
      "stockdefault": true
    }
  ]
```

### 2. POST /stock-locations/set-default/{stock_id}
**Purpose**: Set a stock location as default
**Called**: When user clicks "Set Default" button

```
Request:
  POST /stock-locations/set-default/4
  Headers: Authorization: Bearer {token}

Response (200 OK):
  {
    "message": "Stock location 'Ford office' set as default",
    "stock_location": {
      "stockid": 4,
      "stockname": "Ford office",
      "locationid": 2,
      "stockdefault": true
    }
  }

Error Response (404):
  {
    "detail": "Stock location not found"
  }

Error Response (401):
  {
    "detail": "Not authenticated"
  }
```

## State Management

### Component State
```javascript
const [stockLocations, setStockLocations] = useState([]);
const [selectedStockLocation, setSelectedStockLocation] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState('');
const [success, setSuccess] = useState('');
```

### State Transitions

```
Initial State:
  loading: true
  stockLocations: []
  error: ''
  success: ''

After loadData():
  loading: false
  stockLocations: [...]
  error: ''
  success: ''

After clicking Set Default:
  loading: true
  (button disabled)

After API response:
  loading: false
  success: 'Stock location set as default successfully!'
  (auto-hide after 3 seconds)

After refresh:
  stockLocations: [...] (updated with new default)
  success: ''
```

## Error Handling

```
┌─────────────────────────────────────────┐
│         USER ACTION                     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│         API CALL                        │
└─────────────────────────────────────────┘
              ↓
        ┌─────┴─────┐
        ↓           ↓
    SUCCESS      ERROR
        ↓           ↓
    ┌───┴───┐   ┌───┴───┐
    ↓       ↓   ↓       ↓
  200     Other 404    401
  OK      2xx  Not    Not
          OK   Found  Auth
    ↓       ↓   ↓       ↓
  Show    Show Show    Show
  Success Error Error  Error
  Message Message Message Message
```

## Performance Optimization

### Lazy Loading
- Stock locations loaded only when tab is clicked
- Not loaded on page load

### Bulk Update
- All non-default locations updated in single query
- Efficient database operation

### Caching
- Stock locations cached in component state
- Refreshed after set-default action

### Debouncing
- Success message auto-hides after 3 seconds
- Prevents message clutter

## Security Measures

1. **Authentication**: JWT token required
2. **Authorization**: Only authenticated users can set default
3. **Input Validation**: Stock ID validated on backend
4. **SQL Injection Prevention**: Parameterized queries
5. **CORS**: Properly configured headers
6. **Error Messages**: No sensitive data leaked

## Testing Checklist

- [x] Login works
- [x] Stock locations load
- [x] Default badge displays correctly
- [x] Set Default button visible on non-default
- [x] Set Default button hidden on default
- [x] Button click triggers API call
- [x] API call succeeds
- [x] Success message displays
- [x] UI refreshes
- [x] New default shows badge
- [x] Previous default loses badge
- [x] Only one default exists
- [x] Database state consistent
- [x] Error handling works
- [x] Performance acceptable

---

**Status**: ✅ COMPLETE AND VERIFIED
