# Testing Multi-File PO Attachment Feature

## Prerequisites
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`
- Logged in as admin user
- At least one asset exists with PO attachments

## Test Case 1: View Existing Attachments

### Steps
1. Navigate to Assets page
2. Click on an asset that has PO attachments (e.g., Asset ID 7)
3. Click "Edit" button
4. Scroll to "Purchasing Information" tab
5. Look for "Attach PO Document" section

### Expected Results
- ✅ "Current Attachments" section displays
- ✅ Shows count of existing files (e.g., "Current Attachments (2)")
- ✅ Each file displays as a clickable link with filename
- ✅ Files have 📎 icon
- ✅ Section has green background
- ✅ Each file has ✕ delete button

### Example Output
```
Current Attachments (2)
📎 COMPLAVTERMAL26036_2fd34292.pdf  ✕
📎 MLAVTERMAL26037_500cca15.jpg     ✕
```

---

## Test Case 2: Click Existing File Link

### Steps
1. From Test Case 1, click on one of the file links
2. Verify file opens in new tab

### Expected Results
- ✅ File opens in new browser tab
- ✅ File displays correctly (PDF viewer or image viewer)
- ✅ Original edit page remains open

---

## Test Case 3: Delete Existing File

### Steps
1. From Test Case 1, click ✕ button next to first file
2. Verify file is removed from display
3. Click ✕ button next to second file
4. Verify both files are removed

### Expected Results
- ✅ File immediately removed from display
- ✅ "Current Attachments" section disappears when all files deleted
- ✅ No console errors

---

## Test Case 4: Add New Files

### Steps
1. From Test Case 1, click "Add more PO file(s)..." button
2. Select 2 files from your computer (PDF, image, or Office doc)
3. Verify files appear in form

### Expected Results
- ✅ File picker dialog opens
- ✅ Can select multiple files
- ✅ "New Files to Upload (2)" section appears
- ✅ Section has blue background
- ✅ Each file shows:
  - 📄 filename
  - File size (e.g., "0.45 MB")
  - ✕ delete button

### Example Output
```
Current Attachments (2)
📎 COMPLAVTERMAL26036_2fd34292.pdf  ✕
📎 MLAVTERMAL26037_500cca15.jpg     ✕

Add more PO file(s)...

New Files to Upload (2)
📄 invoice.pdf                       0.25 MB  ✕
📄 receipt.jpg                       0.15 MB  ✕
```

---

## Test Case 5: Delete New File Before Saving

### Steps
1. From Test Case 4, click ✕ button next to first new file
2. Verify file is removed
3. Click ✕ button next to second new file
4. Verify both new files are removed

### Expected Results
- ✅ File immediately removed from display
- ✅ "New Files to Upload" section disappears when all files deleted
- ✅ Existing files still visible
- ✅ No console errors

---

## Test Case 6: Save with New Files

### Steps
1. From Test Case 4 (with 2 new files selected):
2. Click "Update Asset" button
3. Wait for success message
4. Verify page redirects to assets list
5. Navigate back to edit page for same asset

### Expected Results
- ✅ "Asset updated successfully" message appears
- ✅ Page redirects to assets list after 1.5 seconds
- ✅ When editing again, all files are present:
  - 2 original existing files
  - 2 newly uploaded files
  - Total: 4 files in "Current Attachments"

---

## Test Case 7: Save Without New Files

### Steps
1. From Test Case 1, don't add any new files
2. Make a small change (e.g., edit Notes field)
3. Click "Update Asset" button
4. Wait for success message
5. Navigate back to edit page

### Expected Results
- ✅ "Asset updated successfully" message appears
- ✅ Existing files are unchanged
- ✅ Same number of files still present

---

## Test Case 8: Delete Existing and Add New

### Steps
1. From Test Case 1 (asset with 2 existing files):
2. Click ✕ to delete 1 existing file
3. Click "Add more PO file(s)..." and select 1 new file
4. Click "Update Asset"
5. Navigate back to edit page

### Expected Results
- ✅ "Asset updated successfully" message appears
- ✅ When editing again:
  - 1 original file remains (the one not deleted)
  - 1 new file is added
  - Total: 2 files in "Current Attachments"

---

## Test Case 9: Create New Asset with Files

### Steps
1. Navigate to Assets page
2. Click "Add New Asset" button
3. Fill in required fields (Basic Info tab)
4. Go to "Purchasing Information" tab
5. Click "Choose PO file(s)..." button
6. Select 2 files
7. Verify files appear in "New Files to Upload" section
8. Click "Create Asset" button
9. Wait for success message
10. Navigate to edit page for newly created asset

### Expected Results
- ✅ Files appear in "New Files to Upload" section (blue background)
- ✅ No "Current Attachments" section (new asset)
- ✅ "Asset created successfully" message appears
- ✅ When editing new asset:
  - Both files appear in "Current Attachments"
  - Files are accessible via links

---

## Test Case 10: File Type Validation

### Steps
1. From Test Case 4, try to select an unsupported file type (.exe, .zip, etc.)
2. Verify validation message

### Expected Results
- ✅ Alert appears: "[filename] is not a supported file type"
- ✅ File is not added to the list
- ✅ Supported types only: PDF, JPG, PNG, GIF, DOC, DOCX, XLS, XLSX

---

## Test Case 11: File Size Validation

### Steps
1. From Test Case 4, try to select a file larger than 10MB
2. Verify validation message

### Expected Results
- ✅ Alert appears: "[filename] exceeds 10MB limit"
- ✅ File is not added to the list
- ✅ Only files under 10MB are accepted

---

## Test Case 12: Responsive Design

### Steps
1. Open edit page on mobile device or use browser dev tools (F12)
2. Set viewport to mobile size (375px width)
3. Scroll to "Attach PO Document" section
4. Verify layout is readable

### Expected Results
- ✅ File list is readable on mobile
- ✅ Delete buttons are clickable
- ✅ File links are accessible
- ✅ No horizontal scrolling needed

---

## Test Case 13: Multiple Rapid Additions

### Steps
1. From Test Case 1:
2. Click "Add more PO file(s)..." and select 1 file
3. Immediately click "Add more PO file(s)..." again and select another file
4. Verify both files are in the list
5. Click "Update Asset"

### Expected Results
- ✅ Both files appear in "New Files to Upload" section
- ✅ Both files are uploaded successfully
- ✅ No race conditions or errors

---

## Test Case 14: Cancel Without Saving

### Steps
1. From Test Case 4 (with new files selected):
2. Click "Cancel" button
3. Verify page redirects to assets list
4. Navigate back to edit page

### Expected Results
- ✅ Page redirects to assets list
- ✅ New files are NOT saved
- ✅ Existing files remain unchanged
- ✅ No files were uploaded

---

## Test Case 15: Browser Console Check

### Steps
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Perform all above test cases
4. Check for errors

### Expected Results
- ✅ No red error messages
- ✅ No warnings about missing props
- ✅ No network errors (404, 500, etc.)
- ✅ Successful API calls logged

---

## Troubleshooting

### Issue: Files not displaying
- Check browser console for errors
- Verify backend is running
- Verify asset has `po_attachment_path` field populated
- Check if JSON parsing is working

### Issue: Delete button not working
- Check if button has correct onClick handler
- Verify state is updating
- Check browser console for errors

### Issue: Files not uploading
- Check file size (must be < 10MB)
- Check file type (must be supported)
- Verify backend is running
- Check network tab in dev tools

### Issue: Existing files not showing
- Verify asset was loaded correctly
- Check if `po_attachment_path` is JSON array
- Check browser console for parsing errors
- Verify backend is returning correct data

---

## Success Criteria

All test cases pass when:
- ✅ Existing files display correctly
- ✅ New files can be added
- ✅ Files can be deleted
- ✅ Changes are saved correctly
- ✅ No console errors
- ✅ Responsive design works
- ✅ File validation works
- ✅ No race conditions

## Sign-Off

- [ ] All test cases passed
- [ ] No console errors
- [ ] Responsive design verified
- [ ] File validation working
- [ ] Ready for production

---

**Date Tested:** _______________
**Tester Name:** _______________
**Notes:** _______________
