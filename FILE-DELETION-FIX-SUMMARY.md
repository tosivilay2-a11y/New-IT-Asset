# File Deletion Fix - Summary

## Problem
Files deleted in the edit form were not being removed when saved. They would reappear after page reload.

## Root Cause
Frontend deleted files from UI state but didn't send the updated file list to backend. Backend had no way to know which files should be deleted.

## Solution

### Frontend (AssetFormNew.jsx)
Send the remaining files that should be kept:
```javascript
const filesToKeep = [...(asset.po_attachment_existing || [])];
dataToSend.po_attachment_path = JSON.stringify(filesToKeep);
```

### Backend (assets.py)
Respect the file list sent from frontend:
```python
if 'po_attachment_path' in asset_dict and asset_dict['po_attachment_path']:
    existing_files = _parse_attachments(asset_dict['po_attachment_path'])
else:
    existing_files = _parse_attachments(db_asset.po_attachment_path)
```

## What Changed

| Scenario | Before | After |
|----------|--------|-------|
| Delete 1 file | File reappears | File stays deleted ✅ |
| Delete all files | Files reappear | All files deleted ✅ |
| Delete + Add | Only add works | Both work ✅ |
| No changes | Works | Works ✅ |

## Files Modified

1. `frontend/src/pages/AssetFormNew.jsx` - handleSubmit()
2. `backend/app/routes/assets.py` - update_asset_with_file()

## Testing

Quick test:
1. Edit asset with files
2. Delete a file
3. Save
4. Reload page
5. ✅ File should be gone

## Status: COMPLETE ✅

File deletion now works correctly and persists after save.

---

**Implementation Date:** May 8, 2026
