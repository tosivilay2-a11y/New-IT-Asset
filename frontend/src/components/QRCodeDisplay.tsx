import React, { useState, useEffect } from 'react';
import { Button, Card, Row, Col, Spinner } from 'react-bootstrap';
import api from '../services/api';
import './QRCodeDisplay.css';

interface QRCodeDisplayProps {
  assetId: string;
}

interface Asset {
  asset_id: string;
  name: string;
  brand?: string;
  model?: string;
  serial_number?: string;
  purchase_date?: string;
  status?: string;
}

const QRCodeDisplay: React.FC<QRCodeDisplayProps> = ({ assetId }) => {
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const [asset, setAsset] = useState<Asset | null>(null);
  const [loading, setLoading] = useState(true);
  const qrRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchAssetDetails();
    fetchQRCode();
  }, [assetId]);

  const fetchAssetDetails = async () => {
    try {
      const response = await api.get(`/api/assets/${assetId}`);
      setAsset(response.data);
    } catch (error) {
      console.error('Error fetching asset details:', error);
    }
  };

  const fetchQRCode = async () => {
    try {
      const response = await api.get(`/api/assets/${assetId}/qr-code`);
      if (response.data && response.data.qr_code) {
        setQrCodeUrl(response.data.qr_code);
      }
    } catch (error) {
      console.error('Error fetching QR code:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (printWindow && qrRef.current) {
      const content = qrRef.current.innerHTML;
      printWindow.document.write(`
        <html>
          <head>
            <title>Asset Label - ${assetId}</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
              }
              .asset-label-card {
                border: 2px solid #000;
                padding: 15px;
                max-width: 400px;
                margin: 0 auto;
              }
              .asset-label-header {
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 10px;
                border-bottom: 2px solid #000;
                padding-bottom: 5px;
              }
              .asset-details {
                font-size: 12px;
                line-height: 1.6;
              }
              .asset-details div {
                margin-bottom: 5px;
              }
              .qr-code-container {
                text-align: center;
              }
              .qr-code-image {
                width: 150px;
                height: 150px;
                border: 1px solid #ddd;
              }
              .qr-code-label {
                font-size: 10px;
                font-weight: bold;
                margin-top: 5px;
              }
              .asset-label-footer {
                text-align: center;
                font-size: 10px;
                margin-top: 10px;
                padding-top: 5px;
                border-top: 1px solid #ccc;
              }
              @media print {
                body { margin: 0; padding: 10px; }
              }
            </style>
          </head>
          <body>
            ${content}
          </body>
        </html>
      `);
      printWindow.document.close();
      setTimeout(() => {
        printWindow.print();
      }, 250);
    }
  };

  const downloadQRCode = () => {
    if (qrCodeUrl) {
      const link = document.createElement('a');
      link.download = `Asset_QR_${assetId}.png`;
      link.href = qrCodeUrl;
      link.click();
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return new Date().toLocaleDateString();
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="text-center p-4">
        <Spinner animation="border" />
        <p className="mt-2">Generating QR code...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Asset Label for Printing */}
      <div ref={qrRef} className="asset-label">
        <Card className="asset-label-card">
          <Card.Body className="p-3">
            {/* Header */}
            <div className="text-center asset-label-header">
              <strong>IT ASSET LABEL</strong>
            </div>
            
            <Row className="g-2">
              {/* Left Column - Asset Details */}
              <Col xs={7}>
                <div className="asset-details">
                  <div>
                    <strong>Asset ID:</strong> {asset?.asset_id || assetId}
                  </div>
                  <div>
                    <strong>Name:</strong> {asset?.name || 'N/A'}
                  </div>
                  <div>
                    <strong>Model:</strong> {asset?.brand && asset?.model ? 
                      `${asset.brand} ${asset.model}` : 
                      asset?.model || asset?.brand || 'N/A'}
                  </div>
                  <div>
                    <strong>Serial:</strong> {asset?.serial_number || 'N/A'}
                  </div>
                  <div>
                    <strong>Date:</strong> {formatDate(asset?.purchase_date)}
                  </div>
                  <div>
                    <strong>Status:</strong> {asset?.status || 'N/A'}
                  </div>
                </div>
              </Col>
              
              {/* Right Column - QR Code */}
              <Col xs={5} className="qr-code-container">
                {qrCodeUrl ? (
                  <div>
                    <img 
                      src={qrCodeUrl} 
                      alt="QR Code" 
                      className="qr-code-image"
                    />
                    <div className="qr-code-label">
                      <strong>SCAN ME</strong>
                    </div>
                  </div>
                ) : (
                  <div className="text-muted">No QR Code</div>
                )}
              </Col>
            </Row>
            
            {/* Footer */}
            <div className="asset-label-footer">
              Generated: {new Date().toLocaleDateString()} | IT Asset Management System
            </div>
          </Card.Body>
        </Card>
      </div>
      
      {/* Action Buttons - Hidden in Print */}
      <div className="d-flex justify-content-center gap-2 mt-3 no-print">
        <Button variant="primary" onClick={handlePrint}>
          <i className="bi bi-printer me-2"></i>
          Print Label
        </Button>
        <Button variant="success" onClick={downloadQRCode} disabled={!qrCodeUrl}>
          <i className="bi bi-download me-2"></i>
          Download QR
        </Button>
      </div>
      
      {/* Preview Note - Hidden in Print */}
      <div className="text-center mt-2 no-print">
        <small className="text-muted">
          Label size: 4" × 2" | Optimized for standard asset labels
        </small>
      </div>
    </div>
  );
};

export default QRCodeDisplay;
