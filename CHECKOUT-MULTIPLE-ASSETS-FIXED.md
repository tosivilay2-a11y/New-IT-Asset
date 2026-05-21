# Checkout Multiple Assets - FIXED

## Issue
When checking out a second asset, the "Currently Assigned Assets" table only showed 1 item instead of 2.

## Root Cause
The `handleCheckout` function was trying to find assets in two ways:
1. First, search in `assignedAssets` (which only contains already-assigned assets)
2. Then, try to search via `/assets/?search=` endpoint (which doesn't exist)

When checking out a second asset:
- The asset wasn't in `assignedAssets` yet (it's not assigned)
- The search endpoint didn't exist, so the lookup failed
- The checkout failed silently or showed an error

## Solution
Updated the `handleCheckout` function to search all assets instead of just assigned ones:

### Before
```javascript
const asset = assignedAssets.find(a => a.assetcode === checkoutForm.assetId) || 
              (await api.get(`/assets/?search=${checkoutForm.assetId}`)).data[0];
```

### After
```javascript
let asset = null;
try {
  const allAssetsResponse = await api.get('/assets/?limit=1000');
  asset = allAssetsResponse.data.find(a => a.assetcode === checkoutForm.assetId);
} catch (err) {
  console.error('Error fetching all assets:', err);
}
```

## How It Works Now
1. Fetch all assets (up to 1000) from the API
2. Search for the asset by assetcode in the full list
3. If found, proceed with checkout
4. After checkout, refresh the assigned assets list

## Testing
1. Check out first asset to staff member
2. Verify it appears in "Currently Assigned Assets" table
3. Check out second asset to a different staff member
4. Verify BOTH assets appear in the table (not just 1)
5. Repeat for multiple assets

## Files Modified
- `frontend/src/pages/AssetCheckInOut.jsx` - Updated asset lookup logic in handleCheckout

## Status
✅ **FIXED** - Multiple assets can now be checked out and will all appear in the list
