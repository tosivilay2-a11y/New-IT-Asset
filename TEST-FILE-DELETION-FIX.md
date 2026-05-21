# Test: File Deletion Fix

## Quick Test Steps

### Test 1: Delete Single File
1. Go to `/assets/{id}/edit` (asset with 2+ files)
2. Scroll to "Attach PO Document" section
3. Click ✕ next to first file
4. Verify file disappears from "Current Attachments"
5. Click "Update Asset"
6. Wait for success message
7. Reload page (F5)
8. ✅ File should still be deleted

### Test 2: Delete All Files
1. Go to `/assets/{id}/edit` (asset with 2 files)
2. Click ✕ next to first file
3. Click ✕ next to second file
4. Verify "Current Attachments" section disappears
5. Click "Update Asset"
6. Wait for success message
7. Reload page (F5)
8. ✅ No files should remain

### Test 3: Delete and Add
1. Go to `/assets/{id}/edit` (asset with 2 files)
2. Click ✕ next to one file (1 file remains)
3. Click "Add more PO file(s)..."
4. Select 1 new file
5. Verify:
   - 1 file in "Current Attachments"
   - 1 file in "New Files to Upload"
6. Click "Update Asset"
7. Wait for success message
8. Reload page (F5)
9. ✅ Should have 2 files total (1 original + 1 new)

### Test 4: No Changes
1. Go to `/assets/{id}/edit` (asset with 2 files)
2. Don't delete or add files
3. Click "Update Asset"
4. Wait for success message
5. Reload page (F5)
6. ✅ Should still have 2 files

## Browser Console Check

Open Developer Tools (F12) and check Console tab:

### Expected Debug Messages
```
DEBUG: Received asset_data keys: [...]
DEBUG: po_attachment_path: ["url1", "url2"]
DEBUG: Using provided file list: ["url1", "url2"]
DEBUG: Final file list: ["url1", "url2"]
```

### No Errors
- ✅ No red error messages
- ✅ No 400/500 status codes
- ✅ No network errors

## Network Tab Check

1. Open Developer Tools (F12)
2. Go to Network tab
3. Perform delete and save
4. Look for PUT request to `/assets/{id}/with-file` or `/assets/{id}`
5. Check Request payload:
   - Should include `po_attachment_path` with updated list
6. Check Response:
   - Should have 200 status
   - Should have updated `po_attachment_path`

## Success Criteria

All tests pass when:
- ✅ Deleted files don't reappear after reload
- ✅ All files can be deleted
- ✅ Can delete and add files together
- ✅ No changes preserves files
- ✅ No console errors
- ✅ Network requests successful

## Troubleshooting

### Issue: Files still appear after delete
**Check:**
1. Browser console for errors
2. Network tab for failed requests
3. Backend logs for errors
4. Verify backend is running

### Issue: Error when saving
**Check:**
1. File size (must be < 10MB)
2. File type (must be supported)
3. Backend is running
4. Network connection

### Issue: Console shows errors
**Check:**
1. Backend error logs
2. Network response status
3. JSON parsing errors
4. File path format

## Sign-Off

- [ ] Test 1 passed (delete single file)
- [ ] Test 2 passed (delete all files)
- [ ] Test 3 passed (delete and add)
- [ ] Test 4 passed (no changes)
- [ ] No console errors
- [ ] Network requests successful
- [ ] Ready for production

---

**Date Tested:** _______________
**Tester Name:** _______________
**Status:** _______________
