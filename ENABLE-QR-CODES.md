# Enable QR Code Functionality

## Current Status
✅ Asset Detail View is working with QR code placeholders
⚠️ Real QR codes require the 'qrcode' package

## To Enable Real QR Codes

### Step 1: Install Package
```bash
cd frontend
npm install qrcode
```

### Step 2: Update AssetDetailView.jsx
Replace the placeholder imports and components with the real QR code functionality:

**At the top of the file, change:**
```javascript
// Current (placeholder version):
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { assetsAPI } from '../services/api';
import './AssetDetailView.css';

// To (real QR version):
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { assetsAPI } from '../services/api';
import QRCode from 'qrcode';
import './AssetDetailView.css';
```

**Replace SimpleQRPreview component:**
```javascript
// Replace the placeholder version with:
const SimpleQRPreview = ({ assetId, onClick }) => {
  const [qrCodeUrl, setQrCodeUrl] = useState('');

  useEffect(() => {
    const generateQR = async () => {
      try {
        const url = await QRCode.toDataURL(`AssetID:${assetId}`, {
          width: 120,
          margin: 1,
          color: {
            dark: '#000000',
            light: '#FFFFFF'
          }
        });
        setQrCodeUrl(url);
      } catch (error) {
        console.error('Error generating QR code:', error);
      }
    };
    generateQR();
  }, [assetId]);

  return (
    <div className="qr-code-simple-preview" onClick={onClick}>
      {qrCodeUrl ? (
        <img src={qrCodeUrl} alt="QR Code" className="qr-code-image" />
      ) : (
        <div className="qr-loading">Loading QR...</div>
      )}
    </div>
  );
};
```

**Replace QRCodeDisplay component:**
```javascript
// Replace the placeholder version with:
const QRCodeDisplay = ({ assetId, assetName }) => {
  const [qrCodeUrl, setQrCodeUrl] = useState('');

  useEffect(() => {
    const generateQR = async () => {
      try {
        const url = await QRCode.toDataURL(`AssetID:${assetId}`, {
          width: 300,
          margin: 2,
          color: {
            dark: '#000000',
            light: '#FFFFFF'
          }
        });
        setQrCodeUrl(url);
      } catch (error) {
        console.error('Error generating QR code:', error);
      }
    };
    generateQR();
  }, [assetId]);

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>Asset Label - ${assetId}</title>
          <style>
            body { 
              font-family: Arial, sans-serif; 
              text-align: center; 
              padding: 20px;
            }
            .label { 
              border: 2px solid #000; 
              padding: 20px; 
              display: inline-block;
              margin: 20px;
            }
            .asset-id { 
              font-size: 24px; 
              font-weight: bold; 
              margin: 10px 0;
              font-family: 'Courier New', monospace;
            }
            .asset-name { 
              font-size: 16px; 
              margin: 10px 0;
            }
            img { 
              margin: 10px 0;
            }
          </style>
        </head>
        <body>
          <div class="label">
            <img src="${qrCodeUrl}" alt="QR Code" />
            <div class="asset-id">${assetId}</div>
            <div class="asset-name">${assetName || ''}</div>
          </div>
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  const handleDownload = () => {
    const link = document.createElement('a');
    link.download = `Asset_QR_${assetId}.png`;
    link.href = qrCodeUrl;
    link.click();
  };

  return (
    <div className="qr-code-display">
      {qrCodeUrl && (
        <>
          <img src={qrCodeUrl} alt="Asset QR Code" className="qr-code-large" />
          <div className="qr-actions">
            <button className="btn btn-success" onClick={handlePrint}>
              <span>🖨️</span> Print Label
            </button>
            <button className="btn btn-primary" onClick={handleDownload}>
              <span>⬇️</span> Download QR
            </button>
          </div>
        </>
      )}
    </div>
  );
};
```

### Step 3: Restart Frontend
After making changes:
1. Stop frontend server (Ctrl+C)
2. Run `npm start`

## Quick Install Script
I've created `install-qrcode.bat` - just double-click it to install automatically.

## What You Get

### With Placeholders (Current)
- ✅ Asset detail view works
- ✅ All information displays
- ✅ Print functionality (with placeholder)
- ⚠️ QR shows placeholder box

### With Real QR Codes (After Install)
- ✅ Everything above, plus:
- ✅ Real QR codes generated
- ✅ Scannable QR codes
- ✅ Download QR as PNG
- ✅ Professional print labels

## No Rush!
The asset detail view is fully functional now. Add QR codes when convenient - it's just a nice-to-have feature!