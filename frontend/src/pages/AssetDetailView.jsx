/**
 * Enhanced Asset Detail View
 * Comprehensive asset information display with QR code generation
 */
import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import QRCode from 'qrcode';
import { assetsAPI } from '../services/api';
import api from '../services/api';
import './AssetDetailView.css';

// Real QR Code component using the qrcode package
const AssetQRCode = ({ assetId, size = 150 }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (canvasRef.current && assetId) {
      QRCode.toCanvas(canvasRef.current, assetId, {
        width: size,
        margin: 2,
        color: { dark: '#000000', light: '#ffffff' }
      }).catch(console.error);
    }
  }, [assetId, size]);

  return <canvas ref={canvasRef} />;
};

// QR Code Display with print/download
const QRCodeDisplay = ({ assetId, assetName, companyName, purchaseDate, provinceName }) => {
  const [qrDataUrl, setQrDataUrl] = useState('');

  useEffect(() => {
    if (!assetId) return;
    QRCode.toDataURL(assetId, {
      width: 220,
      margin: 2,
      color: { dark: '#000000', light: '#ffffff' }
    }).then(setQrDataUrl).catch(console.error);
  }, [assetId]);

  const handleDownload = () => {
    if (!qrDataUrl) return;

    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 650;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#111111';
    ctx.lineWidth = 6;
    const x = 20, y = 20, w = canvas.width - 40, h = canvas.height - 40, r = 24;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
    ctx.stroke();

    ctx.fillStyle = '#111111';
    ctx.font = 'bold 52px Arial';
    ctx.fillText(assetName || 'Asset', 60, 120);
    ctx.font = '34px Arial';
    ctx.fillText(`Company: ${companyName || 'N/A'}`, 60, 205);
    ctx.fillText(`Purchase Date: ${purchaseDate || 'N/A'}`, 60, 265);
    ctx.fillText(`Province: ${provinceName || 'N/A'}`, 60, 325);
    ctx.font = 'bold 46px Consolas, monospace';
    ctx.fillText(assetId || '', 60, 410);

    const qrImg = new Image();
    qrImg.onload = () => {
      ctx.drawImage(qrImg, 860, 120, 280, 280);
      const link = document.createElement('a');
      link.download = `Asset_Sticker_${assetId}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    qrImg.src = qrDataUrl;
  };

  const handlePrint = () => {
    QRCode.toDataURL(assetId, { width: 300, margin: 2 }).then(url => {
      const printWindow = window.open('', '_blank');
      printWindow.document.write(`
        <html><head><title>Asset Label - ${assetId}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          .label {
            border: 2px solid #000;
            border-radius: 10px;
            padding: 14px;
            width: 520px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
          }
          .label-left { flex: 1; }
          .label-title { font-size: 24px; font-weight: 700; margin-bottom: 10px; }
          .label-row { font-size: 16px; margin-bottom: 6px; }
          .label-code { font-size: 20px; font-weight: 700; margin-top: 8px; font-family: monospace; }
          .label-right { width: 180px; text-align: center; }
          .qr { width: 160px; height: 160px; }
        </style></head>
        <body>
          <div class="label">
            <div class="label-left">
              <div class="label-title">${assetName || 'Asset'}</div>
              <div class="label-row"><strong>Company:</strong> ${companyName || 'N/A'}</div>
              <div class="label-row"><strong>Purchase Date:</strong> ${purchaseDate || 'N/A'}</div>
              <div class="label-row"><strong>Province:</strong> ${provinceName || 'N/A'}</div>
              <div class="label-code">${assetId}</div>
            </div>
            <div class="label-right">
              <img class="qr" src="${url}" />
            </div>
          </div>
          <script>window.onload = () => { window.print(); }</script>
        </body></html>
      `);
      printWindow.document.close();
    });
  };

  return (
    <div className="qr-code-display">
      <div style={{ border: '2px solid #111', borderRadius: '10px', padding: '14px', display: 'flex', justifyContent: 'space-between', gap: '16px', maxWidth: '700px', margin: '0 auto 16px auto', textAlign: 'left' }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: '28px', fontWeight: 700, marginBottom: '10px' }}>{assetName || 'Asset'}</div>
          <div style={{ fontSize: '16px', marginBottom: '6px' }}><strong>Company:</strong> {companyName || 'N/A'}</div>
          <div style={{ fontSize: '16px', marginBottom: '6px' }}><strong>Purchase Date:</strong> {purchaseDate || 'N/A'}</div>
          <div style={{ fontSize: '16px', marginBottom: '6px' }}><strong>Province:</strong> {provinceName || 'N/A'}</div>
          <div style={{ fontSize: '20px', fontWeight: 700, marginTop: '8px', fontFamily: 'monospace' }}>{assetId}</div>
        </div>
        <div style={{ width: '180px', textAlign: 'center' }}>
          {qrDataUrl ? <img src={qrDataUrl} alt="Asset QR" style={{ width: '160px', height: '160px' }} /> : null}
        </div>
      </div>
      <div className="qr-actions">
        <button className="btn btn-success" onClick={handlePrint}>
          <span>Print</span> Print Label
        </button>
        <button className="btn btn-primary" onClick={handleDownload}>
          <span>Download</span> Download Sticker
        </button>
      </div>
    </div>
  );
};

function AssetDetailView() {
  const [asset, setAsset] = useState(null);
  const [history, setHistory] = useState([]);
  const [staff, setStaff] = useState([]);
  const [users, setUsers] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [departments, setDepartments] = useState([]);
  const [costCenters, setCostCenters] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [conditionReports, setConditionReports] = useState([]);
  const [conditionLoading, setConditionLoading] = useState(false);
  const [error, setError] = useState('');
  const [showQRModal, setShowQRModal] = useState(false);
  const [showConditionModal, setShowConditionModal] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      fetchAssetDetails(id);
    }
  }, [id]);

  const fetchAssetHistory = async (assetId) => {
    try {
      setHistoryLoading(true);
      const response = await api.get(`/asset-history/asset/${assetId}`);
      setHistory(response.data || []);
    } catch (error) {
      console.error('Error fetching asset history:', error);
      // History is optional, don't set error
    } finally {
      setHistoryLoading(false);
    }
  };

  const fetchStaff = async () => {
    try {
      const response = await api.get('/staff/');
      setStaff(response.data || []);
    } catch (error) {
      console.error('Error fetching staff:', error);
      // Staff is optional, don't set error
    }
  };

  const fetchCompanies = async () => {
    try {
      const response = await api.get('/companies/');
      setCompanies(response.data || []);
    } catch (error) {
      console.error('Error fetching companies:', error);
      // Companies is optional, don't set error
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users/');
      setUsers(response.data || []);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchAssetDetails = async (assetId) => {
    try {
      setLoading(true);
      setError('');
      const response = await assetsAPI.getById(assetId);
      setAsset(response.data);
      // Fetch history and reference data for readable names
      await Promise.all([
        fetchAssetHistory(assetId),
        fetchStaff(),
        fetchCompanies(),
        fetchUsers(),
        fetchDepartments(),
        fetchCostCenters()
      ]);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching asset details:', error);
      setError('Failed to load asset details');
      setLoading(false);
    }
  };

  const fetchDepartments = async () => {
    try {
      const response = await api.get('/departments/');
      setDepartments(response.data || []);
    } catch (error) {
      console.error('Error fetching departments:', error);
    }
  };

  const fetchCostCenters = async () => {
    try {
      const response = await api.get('/cost-centers/');
      setCostCenters(response.data || []);
    } catch (error) {
      console.error('Error fetching cost centers:', error);
    }
  };

  const getDepartmentName = (assignedStaff) => {
    if (!assignedStaff) return 'N/A';
    if (assignedStaff.departmentid) {
      const dept = departments.find(d => d.departmentid === assignedStaff.departmentid);
      if (dept) return dept.departmentname;
    }
    return assignedStaff.department || 'N/A';
  };

  const getCostCenterCode = (assignedStaff) => {
    if (!assignedStaff || !assignedStaff.costcenterid) return 'N/A';
    const cc = costCenters.find(c => c.costcenterid === assignedStaff.costcenterid);
    return cc ? cc.costcentercode : `ID: ${assignedStaff.costcenterid}`;
  };

  const getCostCenterName = (assignedStaff) => {
    if (!assignedStaff || !assignedStaff.costcenterid) return '';
    const cc = costCenters.find(c => c.costcenterid === assignedStaff.costcenterid);
    return cc ? cc.costcentername : '';
  };

  const getStatusBadgeClass = (status) => {
    const statusMap = {
      'Available': 'status-available',
      'In Use': 'status-in-use',
      'Maintenance': 'status-maintenance',
      'Retired': 'status-retired',
      'Disposed': 'status-disposed'
    };
    return statusMap[status] || 'status-default';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (value) => {
    if (!value) return '$0.00';
    return `$${parseFloat(value).toFixed(2)}`;
  };

  const fetchConditionReports = async (assetId) => {
    try {
      setConditionLoading(true);
      const response = await api.get(`/assets/${assetId}/condition-reports`);
      setConditionReports(response.data || []);
    } catch (error) {
      console.error('Error fetching condition reports:', error);
      setConditionReports([]);
    } finally {
      setConditionLoading(false);
    }
  };

  const getActorName = (record) => {
    if (record.staff_name) return record.staff_name;
    if (record.user_name) return record.user_name;
    if (record.staffid) {
      const staffMember = staff.find(s => s.staffid === record.staffid);
      return staffMember?.fullname || `Staff #${record.staffid}`;
    }
    if (record.userid) {
      const user = users.find(u => u.userid === record.userid);
      if (!user) return `User #${record.userid}`;
      const fullName = `${user.firstname || ''} ${user.lastname || ''}`.trim();
      return fullName || user.full_name || user.email || `User #${record.userid}`;
    }
    return 'N/A';
  };

  const getLocationName = (locationId) => {
    if (!locationId) return '-';
    const location = locations.find(l => l.id === locationId);
    if (location?.name) return location.name;
    const company = companies.find(c => c.companyid === locationId);
    if (company?.companyname) return company.companyname;
    return `Location #${locationId}`;
  };

  const getHistoryLocationText = (record) => {
    const beforeName = record.location_before_name || getLocationName(record.location_before);
    const afterName = record.location_after_name || getLocationName(record.location_after);
    if (record.location_before && record.location_after) return `${beforeName} -> ${afterName}`;
    return afterName || beforeName || '-';
  };

  const renderKeyValueList = (obj) => {
    if (!obj || typeof obj !== 'object') return <span>-</span>;
    const entries = Object.entries(obj);
    if (!entries.length) return <span>-</span>;
    return (
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px 14px' }}>
        {entries.map(([key, value]) => (
          <div key={key} style={{ display: 'flex', justifyContent: 'space-between', gap: '8px', borderBottom: '1px dashed #e6e6e6', paddingBottom: '4px' }}>
            <span style={{ color: '#4b5563', textTransform: 'capitalize' }}>{key.replace(/([A-Z])/g, ' $1')}</span>
            <strong style={{ color: '#111827' }}>
              {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : String(value)}
            </strong>
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading asset details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-card">
          <h2>⚠️ Error Loading Asset</h2>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => navigate('/assets')}>
            ← Back to Asset List
          </button>
        </div>
      </div>
    );
  }

  if (!asset) {
    return (
      <div className="error-container">
        <div className="error-card">
          <h2>🔍 Asset Not Found</h2>
          <p>The requested asset could not be found.</p>
          <button className="btn btn-primary" onClick={() => navigate('/assets')}>
            ← Back to Asset List
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="asset-detail-view">
      {/* Header */}
      <div className="asset-header">
        <div className="header-content">
          <div className="header-left">
            <h1>
              <span className="icon">💻</span>
              Asset Details
            </h1>
            <div className="asset-id-display">{asset.assetcode}</div>
            <div className="asset-subtitle">
              {asset.manufacturer && asset.modelnumber 
                ? `${asset.manufacturer} ${asset.modelnumber}` 
                : asset.assetname || 'Asset Information'}
              <span className={`status-badge ${getStatusBadgeClass(asset.status_name || asset.status)}`}>
                {asset.status_name || asset.status || 'Available'}
              </span>
            </div>
          </div>
          <div className="header-actions">
            <button className="btn btn-light" onClick={() => setShowQRModal(true)}>
              <span>🔲</span> QR Code
            </button>
            <button className="btn btn-warning" onClick={() => navigate(`/assets/${asset.assetid}/edit`)}>
              <span>✏️</span> Edit
            </button>
            <button className="btn btn-secondary" onClick={() => navigate('/assets')}>
              <span>←</span> Back
            </button>
          </div>
        </div>
      </div>

      {/* QR Code Section */}
      <div className="info-card qr-section">
        <div className="card-header">
          <div className="header-title">
            <span className="icon">🔲</span>
            <strong>Asset QR Code & Label</strong>
          </div>
          <button className="btn-link" onClick={() => setShowQRModal(true)}>
            <span>⛶</span> Full View
          </button>
        </div>
        <div className="card-body">
          <div className="qr-preview-container">
            <div className="qr-code-box">
              <div className="qr-code-simple-preview" onClick={() => setShowQRModal(true)}>
                <AssetQRCode assetId={asset.assetcode} size={130} />
              </div>
            </div>
            <div className="qr-info">
              <div className="asset-id-large">{asset.assetcode}</div>
              <div className="info-item">
                <span className="info-label">Type:</span>
                <span className="info-value">{asset.main_category_name || asset.main_category || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Model:</span>
                <span className="info-value">
                  {asset.manufacturer && asset.modelnumber 
                    ? `${asset.manufacturer} ${asset.modelnumber}` 
                    : asset.assetname || 'N/A'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Serial:</span>
                <span className="info-value">{asset.serialnumber || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Status:</span>
                <span className={`status-badge ${getStatusBadgeClass(asset.status_name || asset.status)}`}>
                  {asset.status_name || asset.status || 'Available'}
                </span>
              </div>
              {asset.po_number && (
                <div className="info-item">
                  <span className="info-label">PO No:</span>
                  <span className="info-value">{asset.po_number}</span>
                </div>
              )}
              {asset.po_attachment_path && (
                <div className="info-item">
                  <span className="info-label">Attachments:</span>
                  <span className="info-value">
                    {(() => {
                      let files = [];
                      try { const p = JSON.parse(asset.po_attachment_path); files = Array.isArray(p) ? p : [asset.po_attachment_path]; } catch { files = [asset.po_attachment_path]; }
                      return <span className="attachment-link">📎 {files.length} file{files.length > 1 ? 's' : ''}</span>;
                    })()}
                  </span>
                </div>
              )}
            </div>
            <div className="qr-actions-side">
              <h6><span>⚡</span> Quick Actions</h6>
              <button className="btn btn-success" onClick={() => setShowQRModal(true)}>
                <span>🖨️</span> Print Label
              </button>
              <button
                className="btn btn-primary"
                onClick={async () => {
                  await fetchConditionReports(asset.assetid);
                  setShowConditionModal(true);
                }}
              >
                <span>📋</span> Asset Condition
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Asset ID Composition */}
      <div className="info-card composition-card">
        <div className="card-header">
          <span className="icon">🔑</span> Asset ID Composition
        </div>
        <div className="card-body">
          <div className="info-grid">
            <div className="info-item">
              <div className="label">Main Category:</div>
              <div className="value">
                <span className="badge badge-info">{asset.main_category_name || asset.main_category || 'N/A'}</span>
              </div>
            </div>
            <div className="info-item">
              <div className="label">Purchase Year:</div>
              <div className="value">
                {asset.purchasedate ? new Date(asset.purchasedate).getFullYear() : 'N/A'}
              </div>
            </div>
          </div>
          <p className="info-note">
            <span>ℹ️</span> Asset ID is generated from: Main Category + Country + Province + Company + Year + Sequence
          </p>
        </div>
      </div>

      {/* Location Detail */}
      <div className="info-card location-card">
        <div className="card-header">
          <span className="icon">📍</span> Asset Location Detail
        </div>
        <div className="card-body">
          <div className="info-grid">
            <div className="info-item">
              <div className="label">Country:</div>
              <div className="value">
                <span>🌍</span> {asset.country_name || asset.countryid || 'N/A'}
              </div>
            </div>
            <div className="info-item">
              <div className="label">Province:</div>
              <div className="value">
                <span>🗺️</span> {asset.province_name || asset.provinceid || 'N/A'}
              </div>
            </div>
            <div className="info-item">
              <div className="label">Company:</div>
              <div className="value">
                <span>🏢</span> {asset.company_name || asset.companyid || 'N/A'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="info-grid-2col">
        {/* Basic Information */}
        <div className="info-card">
          <div className="card-header">
            <span className="icon">ℹ️</span> Basic Information
          </div>
          <div className="card-body">
            <div className="info-row">
              <div className="label">Asset ID:</div>
              <div className="value">
                <code className="code-primary">{asset.assetcode}</code>
              </div>
            </div>
            <div className="info-row">
              <div className="label">Asset Name:</div>
              <div className="value">{asset.assetname || 'N/A'}</div>
            </div>
            <div className="info-row">
              <div className="label">Manufacturer:</div>
              <div className="value">{asset.manufacturer || 'N/A'}</div>
            </div>
            <div className="info-row">
              <div className="label">Model:</div>
              <div className="value">{asset.modelnumber || 'N/A'}</div>
            </div>
            <div className="info-row">
              <div className="label">Serial Number:</div>
              <div className="value">
                <code>{asset.serialnumber || 'N/A'}</code>
              </div>
            </div>
            <div className="info-row">
              <div className="label">Status:</div>
              <div className="value">
                <span className={`status-badge ${getStatusBadgeClass(asset.status_name || asset.status)}`}>
                  {asset.status_name || asset.status || 'Available'}
                </span>
              </div>
            </div>
            <div className="info-row">
              <div className="label">Condition:</div>
              <div className="value">{asset.condition || 'N/A'}</div>
            </div>
          </div>
        </div>

        {/* Financial Information */}
        <div className="info-card financial-card">
          <div className="card-header">
            <span className="icon">💰</span> Financial Information
          </div>
          <div className="card-body">
            <div className="info-row">
              <div className="label">Purchase Date:</div>
              <div className="value">
                {asset.purchasedate ? <><span>📅</span> {formatDate(asset.purchasedate)}</> : 'N/A'}
              </div>
            </div>
            <div className="info-row">
              <div className="label">Purchase Price:</div>
              <div className="value">
                <span>💵</span> <strong>{formatCurrency(asset.purchaseprice)}</strong>
              </div>
            </div>
            <div className="info-row">
              <div className="label">Current Value:</div>
              <div className="value">
                <span>💰</span> <strong>{formatCurrency(asset.currentvalue)}</strong>
              </div>
            </div>
            <div className="info-row">
              <div className="label">Warranty Expiry:</div>
              <div className="value">
                {asset.warrantyexpiry ? <><span>📅</span> {formatDate(asset.warrantyexpiry)}</> : 'N/A'}
              </div>
            </div>
            <div className="info-row">
              <div className="label">PO Number:</div>
              <div className="value">{asset.po_number || 'N/A'}</div>
            </div>
            <div className="info-row">
              <div className="label">Cost Center:</div>
              <div className="value">{asset.cost_center || 'N/A'}</div>
            </div>
            <div className="info-row po-attachment-row">
              <div className="label">PO Attachments:</div>
              <div className="value">
                {asset.po_attachment_path ? (() => {
                  // Parse — could be JSON array or single URL
                  let files = [];
                  try {
                    const parsed = JSON.parse(asset.po_attachment_path);
                    files = Array.isArray(parsed) ? parsed : [asset.po_attachment_path];
                  } catch {
                    files = [asset.po_attachment_path];
                  }

                  return (
                    <div className="po-inline-actions" style={{flexDirection:'column', alignItems:'flex-start', gap:'6px'}}>
                      {files.map((url, idx) => {
                        const fileName = url.split(/[\\/]/).pop();
                        return (
                          <div key={idx} style={{display:'flex', alignItems:'center', gap:'8px'}}>
                            <span className="po-filename">📎 {fileName}</span>
                            <a href={url} target="_blank" rel="noopener noreferrer" className="btn-file btn-file-view">
                              👁️ View
                            </a>
                            <a href={url} download={fileName} className="btn-file btn-file-download">
                              ⬇️ Download
                            </a>
                          </div>
                        );
                      })}
                    </div>
                  );
                })() : (
                  <span className="no-attachment">
                    No file attached —
                    <button className="btn-link-inline" onClick={() => navigate(`/assets/${asset.assetid}/edit`)}>
                      Edit to upload
                    </button>
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* PO Document Preview Card — only when file exists */}
      {asset.po_attachment_path && (() => {
        let files = [];
        try {
          const parsed = JSON.parse(asset.po_attachment_path);
          files = Array.isArray(parsed) ? parsed : [asset.po_attachment_path];
        } catch { files = [asset.po_attachment_path]; }
        if (!files.length) return null;

        return (
          <div className="info-card po-document-card" id="po-document-card">
            <div className="card-header">
              <span className="icon">📄</span> PO Documents ({files.length})
              {asset.po_number && <span className="po-number-badge">PO# {asset.po_number}</span>}
            </div>
            <div className="card-body">
              {files.map((url, idx) => {
                const fileName = url.split(/[\\/]/).pop();
                const isPdf = fileName.toLowerCase().endsWith('.pdf');
                const isImage = /\.(jpg|jpeg|png|gif)$/i.test(fileName);
                return (
                  <div key={idx} style={{marginBottom: idx < files.length - 1 ? '20px' : 0}}>
                    <div className="po-file-info">
                      <div className="po-file-icon">{isPdf ? '📕' : isImage ? '🖼️' : '📎'}</div>
                      <div className="po-file-details">
                        <div className="po-file-name">{fileName}</div>
                        <div className="po-file-type">{isPdf ? 'PDF Document' : isImage ? 'Image' : 'Document'}</div>
                      </div>
                      <div className="po-file-actions">
                        <a href={url} target="_blank" rel="noopener noreferrer" className="btn btn-outline-primary btn-sm">
                          👁️ View
                        </a>
                        <a href={url} download={fileName} className="btn btn-primary btn-sm">
                          ⬇️ Download
                        </a>
                      </div>
                    </div>
                    {isImage && (
                      <div className="po-image-preview">
                        <img src={url} alt={fileName} style={{maxWidth:'100%', maxHeight:'300px', borderRadius:'6px', marginTop:'10px'}} />
                      </div>
                    )}
                    {isPdf && (
                      <div className="po-pdf-preview">
                        <iframe src={url} title={fileName} width="100%" height="400px"
                          style={{border:'1px solid #e5e7eb', borderRadius:'6px', marginTop:'10px'}} />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        );
      })()}

      {/* Hardware Specifications - parsed from specifications JSON */}
      {(() => {
        let specs = {};
        try { specs = asset.specifications ? JSON.parse(asset.specifications) : {}; } catch(e) { return null; }
        const hasHw = specs.cpu || specs.ram || specs.hdd || specs.wlan_mac || specs.lan_mac || specs.computer_name || specs.accessories;
        if (!hasHw) return null;
        return (
          <div className="info-card">
            <div className="card-header">
              <span className="icon">🖥️</span> Hardware Specifications
            </div>
            <div className="card-body">
              <div className="info-grid">
                {specs.cpu && <div className="info-item"><div className="label">CPU:</div><div className="value">{specs.cpu}</div></div>}
                {specs.ram && <div className="info-item"><div className="label">RAM:</div><div className="value">{specs.ram}</div></div>}
                {specs.hdd && <div className="info-item"><div className="label">Storage:</div><div className="value">{specs.hdd}</div></div>}
                {specs.computer_name && <div className="info-item"><div className="label">Computer Name:</div><div className="value">{specs.computer_name}</div></div>}
                {specs.wlan_mac && <div className="info-item"><div className="label">WLAN MAC:</div><div className="value"><code>{specs.wlan_mac}</code></div></div>}
                {specs.lan_mac && <div className="info-item"><div className="label">LAN MAC:</div><div className="value"><code>{specs.lan_mac}</code></div></div>}
                {specs.accessories && <div className="info-item" style={{gridColumn:'1/-1'}}><div className="label">Accessories:</div><div className="value">{specs.accessories}</div></div>}
              </div>
            </div>
          </div>
        );
      })()}

      {/* Assignment Information */}
      {asset.assignedto && (
        <div className="info-card">
          <div className="card-header">
            <span className="icon">👤</span> Assignment Information
          </div>
          <div className="card-body">
            <div className="info-grid">
              <div className="info-item">
                <div className="label">Assigned To:</div>
                <div className="value">
                  <span>👤</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    return assignedStaff ? assignedStaff.fullname : `Staff #${asset.assignedto}`;
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Employee ID:</div>
                <div className="value">
                  <span>🆔</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    return assignedStaff ? assignedStaff.employeeid : 'N/A';
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Assignment Date:</div>
                <div className="value">
                  {asset.assigneddate ? (
                    <><span>📅</span> {formatDate(asset.assigneddate)}</>
                  ) : 'N/A'}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Department:</div>
                <div className="value">
                  <span>🏢</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    return getDepartmentName(assignedStaff);
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Cost Center:</div>
                <div className="value">
                  {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    if (!assignedStaff || !assignedStaff.costcenterid) return 'N/A';
                    const ccCode = getCostCenterCode(assignedStaff);
                    const ccName = getCostCenterName(assignedStaff);
                    return (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span className="cc-code-badge" style={{
                          display: 'inline-block',
                          padding: '2px 8px',
                          backgroundColor: '#f39c12',
                          color: 'white',
                          borderRadius: '4px',
                          fontSize: '11px',
                          fontWeight: '600'
                        }}>
                          {ccCode}
                        </span>
                        {ccName && <span style={{ fontSize: '13px', color: '#4a5568' }}>- {ccName}</span>}
                      </div>
                    );
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Cost Center ID:</div>
                <div className="value">
                  <span>🆔</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    return assignedStaff?.costcenterid || 'N/A';
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Position:</div>
                <div className="value">
                  <span>💼</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    return assignedStaff ? assignedStaff.position : 'N/A';
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Email:</div>
                <div className="value">
                  <span>📧</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    return assignedStaff ? assignedStaff.email : 'N/A';
                  })()}
                </div>
              </div>
              <div className="info-item">
                <div className="label">Company:</div>
                <div className="value">
                  <span>🏢</span> {(() => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    const company = companies.find(c => c.companyid === assignedStaff?.companyid);
                    return company ? company.companyname : (assignedStaff?.companyid ? `Company #${assignedStaff.companyid}` : 'N/A');
                  })()}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Notes */}
      {asset.notes && (
        <div className="info-card">
          <div className="card-header">
            <span className="icon">📝</span> Notes
          </div>
          <div className="card-body">
            <p className="notes-text">{asset.notes}</p>
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="info-card metadata-card">
        <div className="card-header">
          <span className="icon">📊</span> Record Information
        </div>
        <div className="card-body">
          <div className="info-grid">
            <div className="info-item">
              <div className="label">Created:</div>
              <div className="value">
                {new Date(asset.createdat).toLocaleString()}
              </div>
            </div>
            <div className="info-item">
              <div className="label">Last Updated:</div>
              <div className="value">
                {new Date(asset.updatedat).toLocaleString()}
              </div>
            </div>
            <div className="info-item">
              <div className="label">Created By:</div>
              <div className="value">{asset.created_by_name || (asset.createdby ? `User ${asset.createdby}` : 'N/A')}</div>
            </div>
            <div className="info-item">
              <div className="label">Active:</div>
              <div className="value">
                <span className={`badge ${asset.isactive ? 'badge-success' : 'badge-danger'}`}>
                  {asset.isactive ? '✓ Yes' : '✗ No'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Check-In/Check-Out History */}
      {history && history.length > 0 && (
        <div className="info-card history-card">
          <div className="card-header">
            <span className="icon">📋</span> Check-In/Check-Out History ({history.length})
          </div>
          <div className="card-body">
            {historyLoading ? (
              <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading history...</p>
              </div>
            ) : (
              <div className="history-table-container">
                <table className="history-table">
                  <thead>
                    <tr>
                      <th>Date & Time</th>
                      <th>Action</th>
                      <th>Staff/User</th>
                      <th>Reason</th>
                      <th>Condition</th>
                      <th>Location</th>
                      <th>Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((record, idx) => (
                      <tr key={idx} className={`history-row history-${record.action.toLowerCase()}`}>
                        <td className="date-time">
                          {new Date(record.created_at).toLocaleString()}
                        </td>
                        <td className="action">
                          <span className={`action-badge action-${record.action.toLowerCase()}`}>
                            {record.action === 'CHECKOUT' ? '📤 Check Out' : '📥 Check In'}
                          </span>
                        </td>
                        <td className="staff-user">
                          {getActorName(record)}
                        </td>
                        <td className="reason">
                          {record.reason || '-'}
                        </td>
                        <td className="condition">
                          {record.condition_before && record.condition_after ? (
                            <span className="condition-change">
                              {record.condition_before} → {record.condition_after}
                            </span>
                          ) : (
                            record.condition_after || record.condition_before || '-'
                          )}
                        </td>
                        <td className="location">
                          <span className="location-change">
                            {getHistoryLocationText(record)}
                          </span>
                        </td>
                        <td className="notes">
                          {record.notes ? (
                            <span title={record.notes} className="notes-preview">
                              {record.notes.substring(0, 30)}...
                            </span>
                          ) : (
                            '-'
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {showConditionModal && (
        <div className="modal-overlay" onClick={() => setShowConditionModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Asset Condition Reports</h2>
              <button className="modal-close" onClick={() => setShowConditionModal(false)}>×</button>
            </div>
            <div className="modal-body">
              {conditionLoading ? (
                <p>Loading condition reports...</p>
              ) : conditionReports.length === 0 ? (
                <p>No condition reports found.</p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {conditionReports.map((r) => (
                    <div
                      key={r.reportid}
                      style={{
                        border: '1px solid #e5e7eb',
                        borderRadius: '10px',
                        padding: '12px',
                        background: '#fafafa'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                        <div>
                          <strong>{r.action || '-'}</strong>
                          <div style={{ color: '#6b7280', fontSize: '12px' }}>
                            {r.created_at ? new Date(r.created_at).toLocaleString() : '-'}
                          </div>
                        </div>
                        <span className={`status-badge ${getStatusBadgeClass(r.overall_condition || '')}`}>
                          {r.overall_condition || '-'}
                        </span>
                      </div>

                      <div style={{ marginBottom: '10px' }}>
                        <h4 style={{ margin: '0 0 6px 0', fontSize: '14px' }}>Physical Condition</h4>
                        {renderKeyValueList(r.physical_condition)}
                      </div>

                      <div style={{ marginBottom: '10px' }}>
                        <h4 style={{ margin: '0 0 6px 0', fontSize: '14px' }}>Functional Test</h4>
                        {renderKeyValueList(r.functional_test)}
                      </div>

                      <div style={{ marginBottom: '10px' }}>
                        <h4 style={{ margin: '0 0 6px 0', fontSize: '14px' }}>Accessories</h4>
                        {renderKeyValueList(r.accessories)}
                      </div>

                      <div>
                        <h4 style={{ margin: '0 0 6px 0', fontSize: '14px' }}>Notes</h4>
                        <div style={{ color: '#374151' }}>{r.notes || '-'}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowConditionModal(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
      {/* QR Code Modal */}
      {showQRModal && (
        <div className="modal-overlay" onClick={() => setShowQRModal(false)}>
          <div className="modal-content qr-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>
                <span>🔲</span> Asset Label & QR Code - {asset.assetcode}
              </h2>
              <button className="modal-close" onClick={() => setShowQRModal(false)}>×</button>
            </div>
            <div className="modal-body text-center">
              <QRCodeDisplay 
                assetId={asset.assetcode} 
                assetName={asset.assetname}
                companyName={asset.company_name}
                purchaseDate={asset.purchasedate ? new Date(asset.purchasedate).toLocaleDateString() : null}
                provinceName={asset.province_name}
              />
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowQRModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AssetDetailView;








