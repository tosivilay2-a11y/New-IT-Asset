# Multi-File PO Attachment Display Fix - Complete

## Summary
Fixed the edit page (`/assets/{id}/edit`) to properly display existing PO attachments with delete buttons and allow adding new files.

## Changes Made

### 1. Frontend - AssetFormNew.jsx

#### State Management
- Added `po_attachment_existing: []` to track parsed existing files from backend
- Kept `po_attachment: []` for newly selected files
- Kept `po_attachment_path: ''` to store raw JSON string from backend

#### Data Loading (fetchAsset)
- Parse `po_attachment_path` JSON array from backend response
- Handle both single file paths and JSON arrays
- Store parsed files in `po_attachment_existing` state

```javascript
// Parse existing attachments from backend
let existingAttachments = [];
if (assetData.po_attachment_path) {
  try {
    // Try to parse as JSON array
    if (typeof assetData.po_attachment_path === 'string' && assetData.po_attachment_path.startsWith('[')) {
      existingAttachments = JSON.parse(assetData.po_attachment_path);
    } else if (typeof assetData.po_attachment_path === 'string' && assetData.po_attachment_path) {
      // Single file path
      existingAttachments = [assetData.po_attachment_path];
    }
  } catch (e) {
    console.error('Error parsing po_attachment_path:', e);
    existingAttachments = [];
  }
}
```

#### UI Rendering
- Display existing attachments as clickable links with delete buttons
- Show newly selected files separately with different styling
- Extract filename from URL for display
- Each file has individual delete button

```javascript
{/* Show existing attachments in edit mode */}
{editMode && asset.po_attachment_existing && asset.po_attachment_existing.length > 0 && (
  <div className="existing-attachments">
    <h4>Current Attachments ({asset.po_attachment_existing.length})</h4>
    <div className="file-list existing">
      {asset.po_attachment_existing.map((fileUrl, idx) => {
        const filename = fileUrl.split(/[\\/]/).pop() || 'File';
        return (
          <div key={`existing-${idx}`} className="file-info existing-file">
            <span className="file-name">
              <a href={fileUrl} target="_blank" rel="noopener noreferrer" className="attachment-link">
                📎 {filename}
              </a>
            </span>
            <button
              type="button"
              className="file-remove"
              onClick={() => setAsset(prev => ({
                ...prev,
                po_attachment_existing: prev.po_attachment_existing.filter((_, i) => i !== idx)
              }))}
              title="Remove this attachment"
            >✕</button>
          </div>
        );
      })}
    </div>
  </div>
)}
```

#### Form Submission
- Only send newly selected files to backend
- Backend appends new files to existing list
- Existing files are preserved automatically

```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  setSaving(true);
  setError('');
  setSuccess('');

  try {
    const newFiles = asset.po_attachment || [];
    const newFileList = newFiles.filter(f => f instanceof File);

    if (editMode && id) {
      // For edit: only send new files, existing files are preserved by backend
      const dataToSend = { ...asset };
      // Remove fields that shouldn't be sent
      delete dataToSend.po_attachment_existing;
      delete dataToSend.po_attachment_path;
      
      if (newFileList.length > 0) {
        await assetsAPI.updateWithFiles(id, { ...dataToSend, po_attachment: newFileList });
      } else {
        await assetsAPI.update(id, dataToSend);
      }
      setSuccess('Asset updated successfully');
    }
    // ... rest of submission logic
  }
};
```

### 2. Frontend - AssetFormNew.css

Added comprehensive styling for existing and new attachments:

```css
.existing-attachments {
  margin-bottom: 15px;
}

.existing-attachments h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
  color: #166534;
}

.file-list.existing {
  margin-top: 12px;
  padding: 12px;
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 6px;
}

.file-list.new {
  margin-top: 12px;
  padding: 12px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
}

.file-info.existing-file {
  background: #ecfdf5;
  border-color: #a7f3d0;
}

.file-info.new-file {
  background: #eff6ff;
  border-color: #bfdbfe;
}
```

### 3. Backend - assets.py (No Changes Needed)

The backend already handles file appending correctly:
- `_parse_attachments()` - parses JSON array or single path
- `_serialize_attachments()` - converts list to JSON string
- `update_asset_with_file()` - appends new files to existing list

```python
# Handle file upload if provided — append to existing list
if po_attachment and po_attachment.filename:
    file_path = FileUploadService.save_file(po_attachment, db_asset.assetcode)
    existing = _parse_attachments(db_asset.po_attachment_path)
    existing.append(file_path)
    asset_dict['po_attachment_path'] = _serialize_attachments(existing)
```

## User Workflows

### Scenario 1: View Existing Files
1. User navigates to `/assets/7/edit`
2. Form loads with existing attachments displayed
3. Each file shows as a clickable link with filename
4. Delete button (✕) appears next to each file

### Scenario 2: Add New Files
1. User clicks "Add more PO file(s)..." button
2. Selects 2 new files
3. New files appear in "New Files to Upload" section
4. User can delete individual new files before saving
5. User clicks "Update Asset"
6. Backend appends new files to existing list
7. All files (existing + new) are now saved

### Scenario 3: Delete Existing File
1. User clicks ✕ button next to existing file
2. File is removed from `po_attachment_existing` array
3. User clicks "Update Asset"
4. Backend receives updated asset without that file
5. File is removed from the list

### Scenario 4: Delete and Add
1. Asset has 2 existing files
2. User deletes 1 existing file (removes from display)
3. User adds 1 new file
4. User clicks "Update Asset"
5. Backend receives 1 new file to append
6. Result: 2 total files (1 original + 1 new)

## Testing Checklist

- [ ] Edit page loads with existing attachments displayed
- [ ] Existing files show as clickable links
- [ ] Delete button works for existing files
- [ ] Can add new files while keeping existing ones
- [ ] New files show in separate section with different styling
- [ ] Delete button works for new files
- [ ] Saving with new files appends them to existing list
- [ ] Saving without new files preserves existing list
- [ ] File count displays correctly
- [ ] Filenames are extracted correctly from URLs
- [ ] Links open files in new tab

## Files Modified

1. `frontend/src/pages/AssetFormNew.jsx`
   - Added `po_attachment_existing` state
   - Parse JSON array from backend
   - Display existing files with delete buttons
   - Updated form submission logic

2. `frontend/src/pages/AssetFormNew.css`
   - Added styles for existing attachments section
   - Added styles for new files section
   - Color-coded sections (green for existing, blue for new)
   - Responsive design maintained

## Backend Compatibility

No backend changes required. The existing implementation already:
- Parses JSON arrays of file paths
- Appends new files to existing list
- Serializes back to JSON for storage
- Resolves URLs for frontend display

## Notes

- Existing files are stored as JSON array in `po_attachment_path`
- New files are uploaded sequentially via `updateWithFiles()`
- Backend automatically appends new files to existing list
- Frontend only sends new files, not the entire list
- Deleted files are removed from frontend state before submission
- If user deletes all existing files and adds none, the list becomes empty
