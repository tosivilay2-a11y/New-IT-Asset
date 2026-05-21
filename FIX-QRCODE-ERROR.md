# Fix QR Code Module Error

## Error Message
```
Module not found: Error: Can't resolve 'qrcode' in 'D:\New-Asset-management\frontend\src\pages'
```

## Solution

### Option 1: Use Batch File (Easiest)
1. **Run the install script**:
   ```
   install-qrcode.bat
   ```

2. **Restart frontend**:
   - Stop current server (Ctrl+C in terminal)
   - Run: `npm start`

### Option 2: Manual Installation
1. **Open Command Prompt or PowerShell**

2. **Navigate to frontend folder**:
   ```bash
   cd D:\New-Asset-management\frontend
   ```

3. **Install qrcode package**:
   ```bash
   npm install qrcode --save
   ```

4. **Restart frontend**:
   - Stop current server (Ctrl+C)
   - Run: `npm start`

### Option 3: Using npm in VS Code Terminal
1. **Open terminal in VS Code** (Ctrl + `)

2. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

3. **Install package**:
   ```bash
   npm install qrcode
   ```

4. **Restart frontend**:
   - Stop server (Ctrl+C)
   - Run: `npm start`

## Verify Installation

After installation, check `frontend/package.json`:
```json
"dependencies": {
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2",
  "react-scripts": "5.0.1",
  "qrcode": "^1.5.3"  ← Should be here
}
```

## Alternative: Temporarily Disable QR Code

If you want to test without QR code functionality, you can temporarily comment out the import:

**In `frontend/src/pages/AssetDetailView.jsx`:**
```javascript
// import QRCode from 'qrcode';  // Comment this line

// Then replace QR generation with placeholder:
const generateQR = async () => {
  // Temporarily disabled
  setQrCodeUrl('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==');
};
```

## Troubleshooting

### Issue: npm command not found
**Solution**: Install Node.js from https://nodejs.org/

### Issue: Permission denied
**Solution**: Run Command Prompt as Administrator

### Issue: Network error
**Solution**: 
1. Check internet connection
2. Try: `npm install qrcode --registry https://registry.npmjs.org/`

### Issue: Package still not found after install
**Solution**:
1. Delete `node_modules` folder
2. Delete `package-lock.json`
3. Run: `npm install`
4. Run: `npm install qrcode`

## After Installation

1. **Restart frontend server**
2. **Clear browser cache** (Ctrl+Shift+Delete)
3. **Refresh page** (Ctrl+F5)
4. **Test the feature**:
   - Go to http://localhost:3000/assets
   - Click eye icon on any asset
   - QR code should now display

## Expected Result

After successful installation:
- ✅ Frontend compiles without errors
- ✅ Asset detail page loads
- ✅ QR code displays in preview
- ✅ QR code modal works
- ✅ Print and download work

## Still Having Issues?

If the error persists:

1. **Check Node.js version**:
   ```bash
   node --version
   npm --version
   ```
   Should be Node.js 14+ and npm 6+

2. **Clear npm cache**:
   ```bash
   npm cache clean --force
   ```

3. **Reinstall all packages**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Check for typos** in package.json

5. **Restart VS Code** completely

## Quick Commands Summary

```bash
# Navigate to frontend
cd D:\New-Asset-management\frontend

# Install qrcode
npm install qrcode

# Restart server
# Press Ctrl+C to stop
npm start
```

---

**Need Help?** Check `QUICK-START-ASSET-DETAIL.md` for more information.
