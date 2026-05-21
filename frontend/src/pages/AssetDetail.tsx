import React, { useState, useEffect } from 'react';
import { Card, Button, Row, Col, Badge, Modal, Table, Spinner, Alert } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import './AssetDetail.css';

interface Asset {
  id: number;
  asset_id: string;
  name: string;
  status: string;
  brand?: string;
  model?: string;
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;
  value?: number;
  location_id?: number;
  assigned_user_id?: number;
  qr_code?: string;
  created_at: string;
  updated_at: string;
  // Additional fields
  serial_number?: string;
  category?: string;
  condition?: string;
  description?: string;
}

interface QRCodeResponse {
  asset_id: string;
  qr_code: string;
}

// QR Code Display Component
const QRCodeDisplay: React.FC<{ qrCode: string; assetId: string }> = ({ qrCode, assetId }) => {
  return (
    <div className="qr-code-display">
      <div className="qr-code-container">
        {qrCode ? (
          <img src={qrCode} alt={`QR Code for ${assetId}`} className="qr-code-image" />
        ) : (
          <div className="qr-placeholder">
            <Spinner animation="border" />
          </div>
        )}
      </div>
      <div className="qr-label">
        <h5>{assetId}</h5>
        <p className="text-muted">Scan to view asset details</p>
      </div>
    </div>
  );
};

const AssetDetail: React.FC = () => {
  const [asset, setAsset] = useState<Asset | null>(null);
  const [qrCode, setQrCode] = useState<string>('');
  const [showQRModal, setShowQRModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      fetchAssetDetails(id);
    }
  }, [id]);

  const fetchAssetDetails = async (assetId: string) => {
    try {
      setLoading(true);
      setError('');

      // Fetch asset details
      const assetResponse = await api.get(`/api/assets/${assetId}`);
      setAsset(assetResponse.data);

      // Fetch QR code
      try {
        const qrResponse = await api.get<QRCodeResponse>(`/api/assets/${assetId}/qr-code`);
        setQrCode(qrResponse.data.qr_code);
      } catch (qrError) {
        console.error('Error fetching QR code:', qrError);
      }

      setLoading(false);
    } catch (error: any) {
      console.error('Error fetching asset details:', error);
      setError(error.response?.data?.detail || 'Failed to load asset details');
      setLoading(false);
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case 'available':
        return 'bg-success';
      case 'in_use':
      case 'in use':
        return 'bg-warning';
      case 'maintenance':
        return 'bg-danger';
      case 'disposed':
        return 'bg-secondary';
      default:
        return 'bg-info';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (value?: number) => {
    if (!value) return '$0.00';
    return `$${value.toFixed(2)}`;
  };

  const handlePrintQR = () => {
    const printWindow = window.open('', '_blank');
    if (printWindow && qrCode) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Asset Label - ${asset?.asset_id}</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
              }
              .label {
                text-align: center;
                border: 2px solid #000;
                padding: 20px;
                width: 300px;
              }
              .label img {
                width: 200px;
                height: 200px;
              }
              .label h2 {
                margin: 10px 0;
                font-size: 18px;
              }
              .label p {
                margin: 5px 0;
                font-size: 14px;
              }
            </style>
          </head>
          <body>
            <div class="label">
              <img src="${qrCode}" alt="QR Code" />
              <h2>${asset?.asset_id}</h2>
              <p>${asset?.name || ''}</p>
              <p>${asset?.brand || ''} ${asset?.model || ''}</p>
            </div>
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  const handleDownloadQR = () => {
    if (qrCode && asset) {
      const link = document.createElement('a');
      link.download = `Asset_QR_${asset.asset_id}.png`;
      link.href = qrCode;
      link.click();
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Spinner animation="border" role="status" variant="primary">
          <span className="visually-hidden">Loading asset details...</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <Alert variant="danger" className="border-0 shadow-sm">
          <Alert.Heading>
            <i className="bi bi-exclamation-triangle me-2"></i>Error Loading Asset
          </Alert.Heading>
          <p>{error}</p>
          <Button variant="outline-danger" onClick={() => navigate('/assets')}>
            <i className="bi bi-arrow-left me-2"></i>Back to Asset List
          </Button>
        </Alert>
      </div>
    );
  }

  if (!asset) {
    return (
      <div className="error-container">
        <Alert variant="warning" className="border-0 shadow-sm">
          <Alert.Heading>
            <i className="bi bi-search me-2"></i>Asset Not Found
          </Alert.Heading>
          <p>The requested asset could not be found.</p>
          <Button variant="outline-warning" onClick={() => navigate('/assets')}>
            <i className="bi bi-arrow-left me-2"></i>Back to Asset List
          </Button>
        </Alert>
      </div>
    );
  }

  return (
    <div className="asset-detail-container fade-in">
      {/* Header */}
      <div className="asset-header">
        <Row className="align-items-center">
          <Col md={8}>
            <h1>
              <i className="bi bi-laptop me-3"></i>Asset Details
            </h1>
            <div className="asset-id">{asset.asset_id}</div>
            <div className="asset-subtitle">
              {asset.name}
              <Badge className={`ms-3 status-badge ${getStatusBadgeClass(asset.status)}`}>
                {asset.status}
              </Badge>
            </div>
          </Col>
          <Col md={4}>
            <div className="action-buttons">
              <Button variant="light" onClick={() => setShowQRModal(true)}>
                <i className="bi bi-qr-code me-2"></i>QR Code
              </Button>
              <Button variant="warning" onClick={() => navigate(`/assets/${asset.asset_id}/edit`)}>
                <i className="bi bi-pencil me-2"></i>Edit
              </Button>
              <Button variant="outline-light" onClick={() => navigate('/assets')}>
                <i className="bi bi-arrow-left me-2"></i>Back
              </Button>
            </div>
          </Col>
        </Row>
      </div>

      {/* QR Code Section */}
      <Card className="qr-section mb-4">
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <i className="bi bi-qr-code me-2"></i>
              <strong>Asset QR Code & Label</strong>
            </div>
            <Button variant="outline-light" size="sm" onClick={() => setShowQRModal(true)}>
              <i className="bi bi-arrows-fullscreen me-1"></i>Full View
            </Button>
          </div>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col lg={8}>
              <div className="qr-preview-container">
                <div className="qr-code-box" onClick={() => setShowQRModal(true)}>
                  {qrCode ? (
                    <img src={qrCode} alt="QR Code" className="qr-code-preview" />
                  ) : (
                    <div className="qr-placeholder">
                      <Spinner animation="border" size="sm" />
                    </div>
                  )}
                </div>
                <div className="qr-info">
                  <div className="asset-id-display">{asset.asset_id}</div>
                  <div className="info-item">
                    <span className="info-label">Name:</span>
                    <span className="info-value">{asset.name}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Model:</span>
                    <span className="info-value">
                      {asset.brand && asset.model
                        ? `${asset.brand} ${asset.model}`
                        : asset.model || asset.brand || 'N/A'}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Status:</span>
                    <span className="info-value">
                      <Badge className={`status-badge ${getStatusBadgeClass(asset.status)}`}>
                        {asset.status}
                      </Badge>
                    </span>
                  </div>
                </div>
              </div>
            </Col>
            <Col lg={4}>
              <div className="qr-actions">
                <h6>
                  <i className="bi bi-lightning me-2"></i>Quick Actions
                </h6>
                <Button variant="success" className="w-100 mb-2" onClick={handlePrintQR}>
                  <i className="bi bi-printer me-2"></i>Print Label
                </Button>
                <Button variant="primary" className="w-100 mb-2" onClick={handleDownloadQR}>
                  <i className="bi bi-download me-2"></i>Download QR
                </Button>
                <Button
                  variant="outline-primary"
                  className="w-100"
                  onClick={() => navigate('/assets')}
                >
                  <i className="bi bi-arrow-left-right me-2"></i>Back to Assets
                </Button>
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Basic Information */}
      <Row>
        <Col lg={6}>
          <Card className="info-card mb-4">
            <Card.Header>
              <i className="bi bi-info-circle me-2"></i>Basic Information
            </Card.Header>
            <Card.Body>
              <div className="info-row">
                <div className="label">Asset ID:</div>
                <div className="value">
                  <code className="text-primary">{asset.asset_id}</code>
                </div>
              </div>
              <div className="info-row">
                <div className="label">Name:</div>
                <div className="value">{asset.name}</div>
              </div>
              <div className="info-row">
                <div className="label">Brand:</div>
                <div className="value">{asset.brand || 'N/A'}</div>
              </div>
              <div className="info-row">
                <div className="label">Model:</div>
                <div className="value">{asset.model || 'N/A'}</div>
              </div>
              <div className="info-row">
                <div className="label">Serial Number:</div>
                <div className="value">
                  <code>{asset.serial_number || 'N/A'}</code>
                </div>
              </div>
              <div className="info-row">
                <div className="label">Status:</div>
                <div className="value">
                  <Badge className={`status-badge ${getStatusBadgeClass(asset.status)}`}>
                    {asset.status}
                  </Badge>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={6}>
          <Card className="info-card mb-4">
            <Card.Header>
              <i className="bi bi-currency-dollar me-2"></i>Financial Information
            </Card.Header>
            <Card.Body>
              <div className="info-row">
                <div className="label">Purchase Date:</div>
                <div className="value">
                  {asset.purchase_date ? (
                    <>
                      <i className="bi bi-calendar me-2"></i>
                      {formatDate(asset.purchase_date)}
                    </>
                  ) : (
                    'N/A'
                  )}
                </div>
              </div>
              <div className="info-row">
                <div className="label">Purchase Price:</div>
                <div className="value">
                  <i className="bi bi-cash me-2"></i>
                  <strong>{formatCurrency(asset.value)}</strong>
                </div>
              </div>
              <div className="info-row">
                <div className="label">Created:</div>
                <div className="value">
                  <i className="bi bi-clock me-2"></i>
                  {formatDate(asset.created_at)}
                </div>
              </div>
              <div className="info-row">
                <div className="label">Last Updated:</div>
                <div className="value">
                  <i className="bi bi-clock-history me-2"></i>
                  {formatDate(asset.updated_at)}
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Technical Specifications */}
      {(asset.cpu || asset.ram || asset.hdd) && (
        <Card className="info-card mb-4">
          <Card.Header>
            <i className="bi bi-cpu me-2"></i>Technical Specifications
          </Card.Header>
          <Card.Body>
            <Row>
              {asset.cpu && (
                <Col md={4}>
                  <div className="info-row">
                    <div className="label">CPU:</div>
                    <div className="value">
                      <i className="bi bi-cpu me-2"></i>
                      {asset.cpu}
                    </div>
                  </div>
                </Col>
              )}
              {asset.ram && (
                <Col md={4}>
                  <div className="info-row">
                    <div className="label">RAM:</div>
                    <div className="value">
                      <i className="bi bi-memory me-2"></i>
                      {asset.ram}
                    </div>
                  </div>
                </Col>
              )}
              {asset.hdd && (
                <Col md={4}>
                  <div className="info-row">
                    <div className="label">Storage:</div>
                    <div className="value">
                      <i className="bi bi-hdd me-2"></i>
                      {asset.hdd}
                    </div>
                  </div>
                </Col>
              )}
            </Row>
          </Card.Body>
        </Card>
      )}

      {/* QR Code Modal */}
      <Modal show={showQRModal} onHide={() => setShowQRModal(false)} centered size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            <i className="bi bi-qr-code me-2"></i>Asset Label & QR Code - {asset.asset_id}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body className="text-center">
          <QRCodeDisplay qrCode={qrCode} assetId={asset.asset_id} />
          <div className="mt-3">
            <h5>{asset.name}</h5>
            <p className="text-muted">
              {asset.brand} {asset.model}
            </p>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="success" onClick={handlePrintQR}>
            <i className="bi bi-printer me-2"></i>Print
          </Button>
          <Button variant="primary" onClick={handleDownloadQR}>
            <i className="bi bi-download me-2"></i>Download
          </Button>
          <Button variant="secondary" onClick={() => setShowQRModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default AssetDetail;
