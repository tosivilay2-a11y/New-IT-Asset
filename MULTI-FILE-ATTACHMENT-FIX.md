# Multi-File Attachment Fix - Complete Solution

## Problem
When uploading 2 or more PO attachment files, the error occurred:
```
400: 'str' object has no attribute '_sa_instance_state'
```

This happened because the frontend was passing the `po_attachment` array to the backend in the JSON data, even though it was also sending individual files. The backend tried to serialize this array as if it were a SQLAlchemy model object, causing the error.

## Root Cause Analysis

### Frontend Issue
The `updateWithFile` and `createWithFile` methods were including the entire `po_attachment` array in the JSON data:
```javascript
// WRONG - includes po_attachment array
const { po_attachment: file, ...assetData } = data;
formData.append('asset_data', JSON.stringify(assetData)); // assetData still has po_attachment
```

### Backend Issue
The backend's `update_asset` function received invalid data types and tried to set them on the SQLAlchemy model, causing the `_sa_instance_state` error.

## Solution

### 1. Fixed Frontend API Service (`frontend/src/services/api.js`)

**Before:**
```javascript
updateWithFile: (id, data) => {
  const formData = new FormData();
  const { po_attachment: file, ...assetData } = data;
  formData.append('asset_data', JSON.stringify(assetData)); // BUG: assetData still contains po_attachment
  if (file) formData.append('po_attachment', file);
  return api.put(`/assets/${id}/with-file`, formData, ...);
}
```

**After:**
```javascript
updateWithFile: (id, data) => {
  const formData = new FormData();
  const { po_attachment: file, ...assetData } = data;
  delete assetData.po_attachment; // FIXED: Explicitly remove the array
  formData.append('asset_data', JSON.stringify(assetData));
  if (file) formData.append('po_attachment', file);
  return api.put(`/assets/${id}/with-file`, formData, ...);
}
```

Same fix applied to `createWithFile`.

### 2. Enhanced Backend Error Handling (`backend/app/routes/assets.py`)

Added better error reporting to help debug issues:
```python
except Exception as e:
    db.rollback()
    print(f"Error updating asset with file: {e}")
    import traceback
    traceback.print_exc()  # Print full stack trace
    raise HTTPException(status_code=400, detail=str(e))
```

## How Multi-File Upload Works

### Creating Asset with Multiple Files
1. User selects 2 files in the form
2. Form shows "2 file(s) selected"
3. On save:
   - Asset is created first (without files) → returns `assetId`
   - File 1 is uploaded via `/assets/{id}/with-file` → appended to `po_attachment_path`
   - File 2 is uploaded via `/assets/{id}/with-file` → appended to `po_attachment_path`
   - Both files are stored as a JSON array in the database

### Sequential Upload Pattern
```javascript
fileArray.reduce((promise, file) => {
  return promise.then(() => {
    if (file instanceof File) {
      return assetsAPI.updateWithFile(id, { ...assetData, po_attachment: file });
    }
    return Promise.resolve();
  });
}, Promise.resolve());
```

This ensures:
- Files upload one at a time (sequential, not parallel)
- Each file is properly appended before the next one starts
- No race conditions or data corruption

## Backend File Handling

The backend already had the infrastructure:
- `_parse_attachments(raw: str)` - Parses JSON array of file paths
- `_serialize_attachments(paths: list)` - Serializes files back to JSON
- Both `/with-file` endpoints append files to the existing list

Example:
```python
existing = _parse_attachments(db_asset.po_attachment_path)  # ["file1.pdf"]
existing.append(file_path)  # ["file1.pdf", "file2.pdf"]
asset_dict['po_attachment_path'] = _serialize_attachments(existing)
```

## Testing

### Manual Testing
1. Create a new asset
2. Select 2 PO attachment files
3. Click "Create Asset"
4. Check the asset detail - both files should be listed
5. Edit the asset and add another file
6. All 3 files should now be attached

### Automated Testing
Run the test script:
```bash
python backend/test_multi_file_upload.py
```

This script:
- Logs in with test credentials
- Creates an asset with the first file
- Updates the asset with the second file
- Verifies both files are attached

## Files Modified

1. **`frontend/src/services/api.js`**
   - Fixed `createWithFile()` to remove `po_attachment` array
   - Fixed `updateWithFile()` to remove `po_attachment` array
   - Added `createWithFiles()` for sequential multi-file creation
   - Added `updateWithFiles()` for sequential multi-file updates

2. **`backend/app/routes/assets.py`**
   - Enhanced error handling in `update_asset_with_file()`
   - Added traceback printing for debugging

3. **`backend/test_multi_file_upload.py`** (NEW)
   - Test script for multi-file upload functionality

## Key Takeaways

- Always clean up data before sending to backend
- Use sequential uploads for file operations to avoid race conditions
- Backend should validate and sanitize incoming data
- Clear error messages help with debugging
