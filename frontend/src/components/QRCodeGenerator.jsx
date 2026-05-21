/**
 * QRCodeGenerator Component
 * Generate and display QR codes for assets
 */
import React, { useState } from 'react';
import axios from 'axios';
import './QRCodeGenerator.css';

const API_BASE_URL = 'http://localhost:8000';

function QRCodeGenerator({ assetId, assetName }) {
  const [qrCode, setQrCode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateQRCode = async () => {
    if (!assetId) {
      setError('Asset ID is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post(`${API_BASE_URL}/asset-utils/generate-qr-code`, {
        asset_id: assetId,
        asset_name: assetName || null
      });
      
      setQrCode(response.data.qr_code);
    } catch (err) {
      setError('Failed to generate QR code');
      console.error('Error generating QR code:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handleDownload = () => {
    if (!qrCode) return;

    // Create a temporary link to download the image
    const link = document.createElement('a');
    link.href = qrCode;
    link.download = `qr_${assetId}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCopy = async () => {
    if (!qrCode) return;

    try {
      // Convert base64 to blob
      const response = await fetch(qrCode);
      const blob = await response.blob();
      
      // Copy to clipboard
      await navigator.clipboard.write([
        new ClipboardItem({ 'image/png': blob })
      ]);
      
      alert('QR code copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy QR code:', err);
      alert('Failed to copy QR code');
    }
  };

  return (
    <div className="qr-code-generator">
      <div className="qr-header">
        <div className="qr-title">QR Code</div>
        {!qrCode && (
          <button 
            onClick={generateQRCode} 
            disabled={!assetId || loading}
            className="qr-generate-btn"
          >
            {loading ? 'Generating...' : '🔲 Generate QR Code'}
          </button>
        )}
      </div>

      {error && <div className="qr-error">{error}</div>}

      {loading && (
        <div className="qr-loading">
          <div>Generating QR code...</div>
        </div>
      )}

      {!loading && qrCode && (
        <div className="qr-display">
          <img src={qrCode} alt="Asset QR Code" className="qr-image" />
          
          <div className="qr-asset-info">
            <div className="qr-asset-id">{assetId}</div>
            {assetName && <div className="qr-asset-name">{assetName}</div>}
          </div>

          <div className="qr-actions">
            <button onClick={handlePrint} className="qr-action-btn primary">
              🖨️ Print
            </button>
            <button onClick={handleDownload} className="qr-action-btn">
              💾 Download
            </button>
            <button onClick={handleCopy} className="qr-action-btn">
              📋 Copy
            </button>
            <button onClick={() => setQrCode(null)} className="qr-action-btn">
              🔄 Regenerate
            </button>
          </div>
        </div>
      )}

      {!loading && !qrCode && !error && (
        <div className="qr-placeholder">
          <div className="qr-placeholder-icon">🔲</div>
          <div className="qr-placeholder-text">
            Click "Generate QR Code" to create a scannable code for this asset
          </div>
        </div>
      )}
    </div>
  );
}

export default QRCodeGenerator;
