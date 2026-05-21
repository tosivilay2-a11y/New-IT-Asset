/**
 * Enhanced Asset Form - Create and Edit
 * Adapted from TypeScript version with read-only fields for edit mode
 */
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api, { assetsAPI } from '../services/api';
import LocationSelector from '../components/LocationSelector';
import CategorySelector from '../components/CategorySelector';
import AssetIDPreview from '../components/AssetIDPreview';
import './AssetFormNew.css';

function AssetFormNew({ isEdit = false }) {
  const navigate = useNavigate();
  const { id } = useParams();
  
  // Determine edit mode
  const editMode = isEdit || !!id;
  
  const [asset, setAsset] = useState({
    // Asset ID Generation Fields (read-only in edit)
    main_category: 'Computer',
    country_id: null,
    province_id: null,
    company_id: null,
    purchase_date: new Date().toISOString().split('T')[0],
    
    // Basic Information
    assetname: '',
    status: 'Available',
    category: '',
    manufacturer: '',
    modelnumber: '',
    serialnumber: '',
    
    // Hardware Specifications
    cpu: '',
    ram: '',
    hdd: '',
    wlan_mac: '',
    lan_mac: '',
    computer_name: '',
    accessories: '',
    
    // Location & Assignment
    locationid: null,  // Changed from 0 to null - backend will auto-assign
    departmentid: null,
    assignedto: null,
    assigneddate: '',
    
    // Financial/Purchasing
    purchaseprice: 0,
    currentvalue: 0,
    warrantyexpiry: '',
    po_number: '',
    po_attachment: [],   // array of File objects (newly selected)
    po_attachment_path: '',  // existing files from backend (JSON string)
    po_attachment_existing: [],  // parsed existing files
    cost_center: '',
    
    // Additional
    notes: '',
    condition: 'Good'
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [activeTab, setActiveTab] = useState('basic');
  const [costCenters, setCostCenters] = useState([]);

  useEffect(() => {
    const initForm = async () => {
      try {
        setLoading(true);
        await fetchCostCenters();
        if (editMode && id) {
          await fetchAsset(id);
        } else {
          setLoading(false);
        }
      } catch (err) {
        console.error('Error initializing form:', err);
        setError('Failed to initialize form');
        setLoading(false);
      }
    };
    initForm();
  }, [editMode, id]);

  const fetchCostCenters = async () => {
    try {
      const response = await api.get('/cost-centers/');
      setCostCenters(response.data || []);
    } catch (err) {
      console.error('Error fetching cost centers:', err);
    }
  };

  const fetchAsset = async (assetId) => {
    try {
      setLoading(true);
      const response = await assetsAPI.getById(assetId);
      const assetData = response.data;

      // Parse hardware specs from specifications JSON
      let specs = {};
      try { specs = assetData.specifications ? JSON.parse(assetData.specifications) : {}; } catch(e) {}

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

      // Map backend fields to form fields
      setAsset({
        // Asset ID Generation Fields (read-only in edit)
        assetcode: assetData.assetcode || '',
        main_category: assetData.main_category_name || assetData.main_category || 'Computer',
        country_id: assetData.countryid,
        province_id: assetData.provinceid,
        company_id: assetData.companyid,
        // Store names for display in readonly fields
        country_name: assetData.country_name || '',
        province_name: assetData.province_name || '',
        company_name: assetData.company_name || '',
        purchase_date: assetData.purchasedate ? assetData.purchasedate.split('T')[0] : '',

        // Basic Information
        assetname: assetData.assetname || '',
        status: assetData.status_name || assetData.status || 'Available',
        category: assetData.category || '',
        manufacturer: assetData.manufacturer || '',
        modelnumber: assetData.modelnumber || '',
        serialnumber: assetData.serialnumber || '',

        // Hardware Specifications — from specifications JSON
        cpu: specs.cpu || '',
        ram: specs.ram || '',
        hdd: specs.hdd || '',
        wlan_mac: specs.wlan_mac || '',
        lan_mac: specs.lan_mac || '',
        computer_name: specs.computer_name || '',
        accessories: specs.accessories || '',

        // Location & Assignment
        locationid: assetData.locationid || 0,
        departmentid: assetData.departmentid,
        assignedto: assetData.assignedto,
        assigneddate: assetData.assigneddate ? assetData.assigneddate.split('T')[0] : '',

        // Financial/Purchasing
        purchaseprice: assetData.purchaseprice || 0,
        currentvalue: assetData.currentvalue || 0,
        warrantyexpiry: assetData.warrantyexpiry ? assetData.warrantyexpiry.split('T')[0] : '',
        po_number: assetData.po_number || '',
        cost_center: assetData.cost_center || '',
        po_attachment: [],
        po_attachment_path: assetData.po_attachment_path || '',
        po_attachment_existing: existingAttachments,

        // Additional
        notes: assetData.notes || '',
        condition: assetData.condition || 'Good'
      });

      setLoading(false);
    } catch (error) {
      console.error('Error fetching asset:', error);
      setError('Failed to fetch asset');
      setLoading(false);
    }
  };

  const handleChange = (field, value) => {
    setAsset(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleLocationChange = (locationData) => {
    setAsset(prev => ({
      ...prev,
      country_id: locationData.countryId,
      province_id: locationData.provinceId,
      company_id: locationData.companyId
    }));
  };

  const handleCategoryChange = (categoryData) => {
    setAsset(prev => ({
      ...prev,
      main_category: categoryData.categoryName
    }));
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    if (!files.length) return;

    const allowedTypes = [
      'application/pdf', 'image/jpeg', 'image/png', 'image/gif',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ];

    const valid = [];
    for (const file of files) {
      if (file.size > 10 * 1024 * 1024) {
        alert(`${file.name} exceeds 10MB limit`);
        continue;
      }
      if (!allowedTypes.includes(file.type)) {
        alert(`${file.name} is not a supported file type`);
        continue;
      }
      valid.push(file);
    }

    if (valid.length) {
      setAsset(prev => ({ ...prev, po_attachment: [...(prev.po_attachment || []), ...valid] }));
    }
    e.target.value = '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      const newFiles = asset.po_attachment || [];
      const newFileList = newFiles.filter(f => f instanceof File);

      if (editMode && id) {
        // For edit: send remaining existing files + new files
        const dataToSend = { ...asset };
        
        // Build the complete list of files to keep:
        // - Existing files that weren't deleted (po_attachment_existing)
        // - New files to upload (po_attachment)
        const filesToKeep = [...(asset.po_attachment_existing || [])];
        
        // Remove fields that shouldn't be sent
        delete dataToSend.po_attachment_existing;
        delete dataToSend.po_attachment_path;
        
        // Send the updated file list to backend
        dataToSend.po_attachment_path = JSON.stringify(filesToKeep);
        
        if (newFileList.length > 0) {
          await assetsAPI.updateWithFiles(id, { ...dataToSend, po_attachment: newFileList });
        } else {
          await assetsAPI.update(id, dataToSend);
        }
        setSuccess('Asset updated successfully');
      } else {
        // For create: send all new files
        const dataToSend = { ...asset };
        delete dataToSend.po_attachment_existing;
        delete dataToSend.po_attachment_path;
        
        if (newFileList.length > 0) {
          await assetsAPI.createWithFiles({ ...dataToSend, po_attachment: newFileList });
        } else {
          await assetsAPI.create(dataToSend);
        }
        setSuccess('Asset created successfully');
      }

      setTimeout(() => navigate('/assets'), 1500);
    } catch (error) {
      console.error('Error saving asset:', error);
      setError(error.response?.data?.detail || 'Failed to save asset');
    } finally {
      setSaving(false);
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'basic':
        return (
          <div className="tab-content">
            <h3>Basic Information</h3>

            {/* Asset ID Preview/Display */}
            {editMode ? (
              <div className="asset-id-display-edit">
                <div className="existing-asset-id">
                  <h4>Asset ID (Cannot be changed)</h4>
                  <div className="asset-id-value">{asset.assetcode || asset}</div>
                  <p className="asset-id-note">
                    <span>🔒</span> Asset ID is locked after creation to maintain data integrity
                  </p>
                </div>
              </div>
            ) : (
              <AssetIDPreview
                mainCategory={asset.main_category}
                countryId={asset.country_id}
                provinceId={asset.province_id}
                companyId={asset.company_id}
                purchaseDate={asset.purchase_date}
              />
            )}

            {/* Main Category */}
            <div className="form-group">
              <label>Main Category <span className="required">*</span></label>
              {editMode ? (
                <div className="readonly-field">
                  <input
                    type="text"
                    value={asset.main_category}
                    readOnly
                    className="form-control readonly"
                  />
                  <small className="readonly-note">
                    <span>🔒</span> Cannot be changed - used to generate Asset ID
                  </small>
                </div>
              ) : (
                <CategorySelector
                  value={asset.main_category}
                  onChange={handleCategoryChange}
                  required={true}
                />
              )}
            </div>

            {/* Location */}
            <div className="form-group">
              <label>Location <span className="required">*</span></label>
              {editMode ? (
                <div className="readonly-field">
                  <div className="location-readonly">
                    <div className="location-item">
                      <span className="location-label">Country:</span>
                      <span className="location-value">{asset.country_name || `ID: ${asset.country_id}`}</span>
                    </div>
                    <div className="location-item">
                      <span className="location-label">Province:</span>
                      <span className="location-value">{asset.province_name || `ID: ${asset.province_id}`}</span>
                    </div>
                    <div className="location-item">
                      <span className="location-label">Company:</span>
                      <span className="location-value">{asset.company_name || `ID: ${asset.company_id}`}</span>
                    </div>
                  </div>
                  <small className="readonly-note">
                    <span>🔒</span> Cannot be changed - used to generate Asset ID
                  </small>
                </div>
              ) : (
                <LocationSelector
                  value={{
                    countryId: asset.country_id,
                    provinceId: asset.province_id,
                    companyId: asset.company_id
                  }}
                  onChange={handleLocationChange}
                  required={true}
                />
              )}
            </div>

            {/* Purchase Date */}
            <div className="form-group">
              <label>Purchase Date <span className="required">*</span></label>
              {editMode ? (
                <div className="readonly-field">
                  <input
                    type="text"
                    value={asset.purchase_date ? new Date(asset.purchase_date).toLocaleDateString() : 'N/A'}
                    readOnly
                    className="form-control readonly"
                  />
                  <small className="readonly-note">
                    <span>🔒</span> Cannot be changed - used to generate Asset ID
                  </small>
                </div>
              ) : (
                <input
                  type="date"
                  value={asset.purchase_date}
                  onChange={(e) => handleChange('purchase_date', e.target.value)}
                  required
                  className="form-control"
                />
              )}
            </div>

            {/* Editable Fields */}
            <div className="form-row">
              <div className="form-group">
                <label>Asset Name <span className="required">*</span></label>
                <input
                  type="text"
                  value={asset.assetname}
                  onChange={(e) => handleChange('assetname', e.target.value)}
                  placeholder="Asset name"
                  required
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Status <span className="required">*</span></label>
                <select
                  value={asset.status}
                  onChange={(e) => handleChange('status', e.target.value)}
                  required
                  className="form-control"
                >
                  <option value="Available">Available</option>
                  <option value="In Use">In Use</option>
                  <option value="Maintenance">Maintenance</option>
                  <option value="Retired">Retired</option>
                  <option value="Disposed">Disposed</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Brand/Manufacturer</label>
                <input
                  type="text"
                  value={asset.manufacturer}
                  onChange={(e) => handleChange('manufacturer', e.target.value)}
                  placeholder="e.g., Dell, HP, Lenovo"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Model</label>
                <input
                  type="text"
                  value={asset.modelnumber}
                  onChange={(e) => handleChange('modelnumber', e.target.value)}
                  placeholder="e.g., Latitude 5420"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Serial Number</label>
              <input
                type="text"
                value={asset.serialnumber}
                onChange={(e) => handleChange('serialnumber', e.target.value)}
                placeholder="Serial number"
                className="form-control"
              />
            </div>
          </div>
        );

      case 'hardware':
        return (
          <div className="tab-content">
            <h3>Hardware Specifications</h3>

            <div className="form-row">
              <div className="form-group">
                <label>CPU</label>
                <input
                  type="text"
                  value={asset.cpu}
                  onChange={(e) => handleChange('cpu', e.target.value)}
                  placeholder="e.g., Intel Core i7-11800H"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>RAM</label>
                <input
                  type="text"
                  value={asset.ram}
                  onChange={(e) => handleChange('ram', e.target.value)}
                  placeholder="e.g., 16GB DDR4"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Storage (HDD/SSD)</label>
                <input
                  type="text"
                  value={asset.hdd}
                  onChange={(e) => handleChange('hdd', e.target.value)}
                  placeholder="e.g., 512GB SSD"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Computer Name</label>
                <input
                  type="text"
                  value={asset.computer_name}
                  onChange={(e) => handleChange('computer_name', e.target.value)}
                  placeholder="Computer hostname"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>WLAN MAC Address</label>
                <input
                  type="text"
                  value={asset.wlan_mac}
                  onChange={(e) => handleChange('wlan_mac', e.target.value)}
                  placeholder="XX:XX:XX:XX:XX:XX"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>LAN MAC Address</label>
                <input
                  type="text"
                  value={asset.lan_mac}
                  onChange={(e) => handleChange('lan_mac', e.target.value)}
                  placeholder="XX:XX:XX:XX:XX:XX"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Accessories</label>
              <input
                type="text"
                value={asset.accessories}
                onChange={(e) => handleChange('accessories', e.target.value)}
                placeholder="e.g., Mouse, Keyboard, Charger"
                className="form-control"
              />
            </div>
          </div>
        );

      case 'purchasing':
        return (
          <div className="tab-content">
            <h3>Purchasing Information</h3>

            <div className="form-row">
              <div className="form-group">
                <label>Purchase Price</label>
                <input
                  type="number"
                  step="0.01"
                  value={asset.purchaseprice}
                  onChange={(e) => handleChange('purchaseprice', parseFloat(e.target.value) || 0)}
                  placeholder="0.00"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Current Value</label>
                <input
                  type="number"
                  step="0.01"
                  value={asset.currentvalue}
                  onChange={(e) => handleChange('currentvalue', parseFloat(e.target.value) || 0)}
                  placeholder="0.00"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>PO Number</label>
                <input
                  type="text"
                  value={asset.po_number}
                  onChange={(e) => handleChange('po_number', e.target.value)}
                  placeholder="Purchase Order Number"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Cost Center</label>
                {(() => {
                  const hasMatchingCC = costCenters.some(cc => cc.costcentercode === asset.cost_center);
                  return (
                    <select
                      value={asset.cost_center}
                      onChange={(e) => handleChange('cost_center', e.target.value)}
                      className="form-control"
                    >
                      <option value="">-- Select Cost Center --</option>
                      {!hasMatchingCC && asset.cost_center && (
                        <option value={asset.cost_center}>
                          {asset.cost_center} (Legacy/Unregistered)
                        </option>
                      )}
                      {costCenters.map(cc => (
                        <option key={cc.costcenterid} value={cc.costcentercode}>
                          {cc.costcentercode} {cc.costcentername ? `- ${cc.costcentername}` : ''}
                        </option>
                      ))}
                    </select>
                  );
                })()}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Warranty Expiry</label>
                <input
                  type="date"
                  value={asset.warrantyexpiry}
                  onChange={(e) => handleChange('warrantyexpiry', e.target.value)}
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Attach PO Document</label>
              
              {/* Show existing attachments in edit mode */}
              {editMode && asset.po_attachment_existing && asset.po_attachment_existing.length > 0 && (
                <div className="existing-attachments">
                  <h4>Current Attachments ({asset.po_attachment_existing.length})</h4>
                  <div className="file-list existing">
                    {asset.po_attachment_existing.map((fileUrl, idx) => {
                      // Extract filename from URL
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

              {/* File upload for new files */}
              <div className="file-upload-container">
                <input
                  type="file"
                  id="po-attachment"
                  onChange={handleFileChange}
                  accept=".pdf,.jpg,.jpeg,.png,.gif,.doc,.docx,.xls,.xlsx"
                  className="file-input"
                  multiple
                />
                <label htmlFor="po-attachment" className="file-upload-label">
                  <span className="file-upload-icon">📎</span>
                  <span className="file-upload-text">
                    {(asset.po_attachment || []).length > 0
                      ? `${asset.po_attachment.length} new file(s) selected`
                      : (editMode ? 'Add more PO file(s)...' : 'Choose PO file(s)...')}
                  </span>
                </label>
                
                {/* Show newly selected files */}
                {(asset.po_attachment || []).length > 0 && (
                  <div className="file-list new">
                    <h4>New Files to Upload ({asset.po_attachment.length})</h4>
                    {asset.po_attachment.map((file, idx) => (
                      <div key={`new-${idx}`} className="file-info new-file">
                        <span className="file-name">📄 {file.name}</span>
                        <span className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                        <button
                          type="button"
                          className="file-remove"
                          onClick={() => setAsset(prev => ({
                            ...prev,
                            po_attachment: prev.po_attachment.filter((_, i) => i !== idx)
                          }))}
                          title="Remove this file"
                        >✕</button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <small className="file-help">
                Supported formats: PDF, Images (JPG, PNG, GIF), Word, Excel. Max size: 10MB
              </small>
            </div>

            <div className="form-group">
              <label>Condition</label>
              <select
                value={asset.condition}
                onChange={(e) => handleChange('condition', e.target.value)}
                className="form-control"
              >
                <option value="Excellent">Excellent</option>
                <option value="Good">Good</option>
                <option value="Fair">Fair</option>
                <option value="Poor">Poor</option>
              </select>
            </div>
          </div>
        );

      case 'notes':
        return (
          <div className="tab-content">
            <h3>Additional Information</h3>

            <div className="form-group">
              <label>Notes</label>
              <textarea
                value={asset.notes}
                onChange={(e) => handleChange('notes', e.target.value)}
                rows="6"
                placeholder="Additional notes about this asset..."
                className="form-control"
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading asset...</p>
      </div>
    );
  }

  return (
    <div className="asset-form-new">
      <div className="form-header">
        <h1>{editMode ? 'Edit Asset' : 'Add New Asset'}</h1>
        {editMode && (
          <div className="asset-id-header">
            Asset ID: <span className="asset-id-code">{asset.assetcode || id}</span>
          </div>
        )}
      </div>

      {error && (
        <div className="alert alert-error">
          <span>⚠️</span> {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          <span>✅</span> {success}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Tab Navigation */}
        <div className="form-tabs">
          <button
            type="button"
            className={`tab-btn ${activeTab === 'basic' ? 'active' : ''}`}
            onClick={() => setActiveTab('basic')}
          >
            1. Basic Info
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'hardware' ? 'active' : ''}`}
            onClick={() => setActiveTab('hardware')}
          >
            2. Hardware
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'purchasing' ? 'active' : ''}`}
            onClick={() => setActiveTab('purchasing')}
          >
            3. Purchasing
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'notes' ? 'active' : ''}`}
            onClick={() => setActiveTab('notes')}
          >
            4. Notes
          </button>
        </div>

        {/* Tab Content */}
        <div className="form-body">
          {renderTabContent()}
        </div>

        {/* Form Actions */}
        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/assets')}
            disabled={saving}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={saving}
          >
            {saving ? 'Saving...' : (editMode ? 'Update Asset' : 'Create Asset')}
          </button>
        </div>
      </form>
    </div>
  );
}

export default AssetFormNew;