# 🔧 Quick Fix - Install QR Code Package

## The Problem
Frontend is showing error: `Module not found: Error: Can't resolve 'qrcode'`

## The Solution (Choose One)

### ⚡ FASTEST - Use Batch File
1. Double-click: **`install-qrcode.bat`**
2. Wait for installation to complete
3. Restart frontend server (Ctrl+C, then `npm start`)

### 💻 Manual - Command Line
Open Command Prompt or PowerShell and run:

```bash
cd D:\New-Asset-management\frontend
npm install qrcode
```

Then restart frontend server.

### 🎯 VS Code Terminal
1. Open terminal in VS Code (Ctrl + `)
2. Run these commands:
```bash
cd frontend
npm install qrcode
```
3. Restart frontend (Ctrl+C, then `npm start`)

## That's It!

After installation:
- Frontend will compile successfully
- Asset detail page will work
- QR codes will display

## Test It
1. Go to http://localhost:3000/assets
2. Click the eye icon (👁️) on any asset
3. You should see the detail page with QR code

---

**Still having issues?** Check `FIX-QRCODE-ERROR.md` for detailed troubleshooting.
