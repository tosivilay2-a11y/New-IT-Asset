import React, { useState, useEffect } from 'react';
import { assetsAPI } from '../services/api';
import api from '../services/api';
import './AssetsManagement.css';

function AssetsManagement() {
  const [assets, setAssets] = useState([]);
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [currentTab, setCurrentTab] = useState('basic');
  
  // Filters
  const [filters, setFilters] = useState({
    year: 'all',
    category: 'all',
    location: 'all',
    status: 'all'
  });

  // Form data for new asset
  const [formData, setFormData] = useState({
    // Basic Information
    main_category: '',
    country: '',
    province: '',
    company: '',
    location: '',
    purchase_date: '',
    asset_id: '',
    
    // Asset Details
    status: 'Available',
    category: '',
    brand: '',
    model: '',
    model_name: '',
    serial_number: '',
    sn_type: '',
    description: '',
    
    // Technical Specs
    processor: '',
    ram: '',
    storage: '',
    graphics: '',
    display: '',
    os: '',
    
    // Assignment
    assigned_to: '',
    department: '',
    assignment_date: '',
    
    // Purchase Info
    supplier: '',
    purchase_cost: '',
    warranty_end: '',
    invoice_number: ''
  });

  useEffect(() => {
    loadAssets();
  }, [filters]);

  const loadAssets = async () => {
    try {
      setLoading(true);
      const [assetsResponse, staffResponse] = await Promise.all([
        assetsAPI.getAll(),
        api.get('/staff/')
      ]);
      setAssets(assetsResponse.data || []);
      setStaff(staffResponse.data || []);
    } catch (error) {
      console.error('Error loading assets:', error);
      setAssets([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({ ...prev, [filterName]: value }));
  };

  const clearFilters = () => {
    setFilters({
      year: 'all',
      category: 'all',
      location: 'all',
      status: 'all'
    });
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await assetsAPI.create(formData);
      setShowAddModal(false);
      resetForm();
      loadAssets();
      alert('Asset created successfully!');
    } catch (error) {
      console.error('Error creating asset:', error);
      alert('Error creating asset. Please try again.');
    }
  };

  const resetForm = () => {
    setFormData({
      main_category: '',
      country: '',
      province: '',
      company: '',
      location: '',
      purchase_date: '',
      asset_id: '',
      status: 'Available',
      category: '',
      brand: '',
      model: '',
      model_name: '',
      serial_number: '',
      sn_type: '',
      description: '',
      processor: '',
      ram: '',
      storage: '',
      graphics: '',
      display: '',
      os: '',
      assigned_to: '',
      department: '',
      assignment_date: '',
      supplier: '',
      purchase_cost: '',
      warranty_end: '',
      invoice_number: ''
    });
    setCurrentTab('basic');
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this asset?')) {
      try {
        await assetsAPI.delete(id);
        loadAssets();
        alert('Asset deleted successfully!');
      } catch (error) {
        console.error('Error deleting asset:', error);
        alert('Error deleting asset.');
      }
    }
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

  const filteredAssets = assets.filter(asset => {
    if (filters.year !== 'all' && !asset.assetcode?.includes(filters.year)) return false;
    if (filters.category !== 'all' && asset.main_category_name !== filters.category) return false;
    if (filters.location !== 'all' && asset.location_name !== filters.location) return false;
    if (filters.status !== 'all' && asset.status_name !== filters.status) return false;
    return true;
  });

  return (
    <div className="assets-management">
      <div className="page-header">
        <h1>Asset Management</h1>
        <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>
          + Add New Asset
        </button>
      </div>

      {/* Filters Section */}
      <div className="filters-section">
        <div className="filter-group">
          <label>Year</label>
          <select value={filters.year} onChange={(e) => handleFilterChange('year', e.target.value)}>
            <option value="all">All Years</option>
            <option value="2026">2026</option>
            <option value="2025">2025</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Main Category</label>
          <select value={filters.category} onChange={(e) => handleFilterChange('category', e.target.value)}>
            <option value="all">All Categories</option>
            <option value="Laptop">Laptop</option>
            <option value="Desktop">Desktop</option>
            <option value="Monitor">Monitor</option>
            <option value="Printer">Printer</option>
            <option value="Network">Network Equipment</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Location</label>
          <select value={filters.location} onChange={(e) => handleFilterChange('location', e.target.value)}>
            <option value="all">All Locations</option>
            <option value="Vientiane">Vientiane</option>
            <option value="Administration">Administration</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Status</label>
          <select value={filters.status} onChange={(e) => handleFilterChange('status', e.target.value)}>
            <option value="all">All Status</option>
            <option value="Available">Available</option>
            <option value="In Use">In Use</option>
            <option value="Maintenance">Maintenance</option>
            <option value="Retired">Retired</option>
          </select>
        </div>

        <button className="btn btn-secondary" onClick={clearFilters}>
          Clear Filters
        </button>
      </div>

      {/* Assets Table */}
      <div className="assets-table-container">
        <div className="table-info">
          Showing {filteredAssets.length} of {assets.length} assets
        </div>
        
        {loading ? (
          <div className="loading">Loading assets...</div>
        ) : (
          <table className="assets-table">
            <thead>
              <tr>
                <th>ASSET ID</th>
                <th>ASSET NAME</th>
                <th>CATEGORY</th>
                <th>COST CENTER LOCATION</th>
                <th>CURRENT LOCATION</th>
                <th>STATUS</th>
                <th>ASSIGNED TO</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              {filteredAssets.length === 0 ? (
                <tr>
                  <td colSpan="8" className="no-data">No assets found</td>
                </tr>
              ) : (
                filteredAssets.map(asset => (
                  <tr key={asset.assetid}>
                    <td className="asset-id">{asset.assetcode || 'N/A'}</td>
                    <td>{asset.assetname || 'N/A'}</td>
                    <td>
                      {asset.main_category_name && (
                        <span className="category-badge">{asset.main_category_name}</span>
                      )}
                    </td>
                    <td>{asset.location_name || 'Unknown'}</td>
                    <td>{asset.location_name || 'Unknown'}</td>
                    <td>
                      <span className={`status-badge ${getStatusBadgeClass(asset.status_name)}`}>
                        {asset.status_name || 'Available'}
                      </span>
                    </td>
                    <td>
                      {asset.assignedto ? (() => {
                        const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                        return assignedStaff ? (
                          <div className="assigned-staff">
                            <div className="staff-name">{assignedStaff.fullname}</div>
                            <div className="staff-id">{assignedStaff.employeeid}</div>
                          </div>
                        ) : `Staff #${asset.assignedto}`;
                      })() : (
                        <div className="assigned-staff">
                          <div className="staff-name">{asset.location_name || 'Unknown Location'}</div>
                          <div className="staff-id">Stock</div>
                        </div>
                      )}
                    </td>
                    <td className="actions-cell">
                      <button className="btn-icon btn-view" title="View">
                        <span>👁️</span>
                      </button>
                      <button className="btn-icon btn-edit" title="Edit">
                        <span>✏️</span>
                      </button>
                      <button 
                        className="btn-icon btn-delete" 
                        title="Delete"
                        onClick={() => handleDelete(asset.assetid)}
                      >
                        <span>🗑️</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* Add Asset Modal */}
      {showAddModal && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Add New Asset</h2>
              <button className="btn-close" onClick={() => setShowAddModal(false)}>×</button>
            </div>

            <div className="modal-tabs">
              <button 
                className={`tab ${currentTab === 'basic' ? 'active' : ''}`}
                onClick={() => setCurrentTab('basic')}
              >
                Basic Information
              </button>
              <button 
                className={`tab ${currentTab === 'technical' ? 'active' : ''}`}
                onClick={() => setCurrentTab('technical')}
              >
                Technical Specs
              </button>
              <button 
                className={`tab ${currentTab === 'assignment' ? 'active' : ''}`}
                onClick={() => setCurrentTab('assignment')}
              >
                Assignment
              </button>
              <button 
                className={`tab ${currentTab === 'purchase' ? 'active' : ''}`}
                onClick={() => setCurrentTab('purchase')}
              >
                Purchase Info
              </button>
              <button 
                className={`tab ${currentTab === 'qr' ? 'active' : ''}`}
                onClick={() => setCurrentTab('qr')}
              >
                QR Code & Label
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {/* Basic Information Tab */}
                {currentTab === 'basic' && (
                  <div className="form-section">
                    <div className="info-banner">
                      <strong>Asset ID Generation Fields</strong> (Required for auto-generating Asset ID)
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Main Category *</label>
                        <select 
                          value={formData.main_category}
                          onChange={(e) => handleInputChange('main_category', e.target.value)}
                          required
                        >
                          <option value="">Select Category</option>
                          <option value="Laptop">Laptop</option>
                          <option value="Desktop">Desktop</option>
                          <option value="Monitor">Monitor</option>
                          <option value="Printer">Printer</option>
                          <option value="Network">Network Equipment</option>
                        </select>
                      </div>

                      <div className="form-group">
                        <label>Province *</label>
                        <select 
                          value={formData.province}
                          onChange={(e) => handleInputChange('province', e.target.value)}
                          required
                        >
                          <option value="">Select Province</option>
                          <option value="Vientiane">Vientiane</option>
                          <option value="Luang Prabang">Luang Prabang</option>
                          <option value="Savannakhet">Savannakhet</option>
                        </select>
                        <small>Province code is used in Asset ID</small>
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Country *</label>
                        <select 
                          value={formData.country}
                          onChange={(e) => handleInputChange('country', e.target.value)}
                          required
                        >
                          <option value="">Select Country</option>
                          <option value="Lao (LA)">Lao (LA)</option>
                        </select>
                        <small>Country code is used in Asset ID and requires country</small>
                      </div>

                      <div className="form-group">
                        <label>Company</label>
                        <select 
                          value={formData.company}
                          onChange={(e) => handleInputChange('company', e.target.value)}
                        >
                          <option value="">Select Company First</option>
                        </select>
                        <small>Companies filtered by selected province</small>
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Location</label>
                        <select 
                          value={formData.location}
                          onChange={(e) => handleInputChange('location', e.target.value)}
                        >
                          <option value="">Select Company First</option>
                        </select>
                        <small>OR</small>
                      </div>

                      <div className="form-group">
                        <label>Purchase Date *</label>
                        <input 
                          type="date"
                          value={formData.purchase_date}
                          onChange={(e) => handleInputChange('purchase_date', e.target.value)}
                          required
                        />
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Asset ID *</label>
                      <input 
                        type="text"
                        value={formData.asset_id}
                        onChange={(e) => handleInputChange('asset_id', e.target.value)}
                        placeholder="Auto-generated (15 chars)"
                        readOnly
                      />
                      <small>✓ Asset ID: [Category][Country][Province][Company][Year][Sequence]</small>
                    </div>

                    <h3>Asset Details</h3>
                    
                    <div className="form-row">
                      <div className="form-group">
                        <label>Status *</label>
                        <select 
                          value={formData.status}
                          onChange={(e) => handleInputChange('status', e.target.value)}
                          required
                        >
                          <option value="Available">Available</option>
                          <option value="In Use">In Use</option>
                          <option value="Maintenance">Maintenance</option>
                          <option value="Retired">Retired</option>
                        </select>
                      </div>

                      <div className="form-group">
                        <label>Category</label>
                        <select 
                          value={formData.category}
                          onChange={(e) => handleInputChange('category', e.target.value)}
                        >
                          <option value="">Select Type</option>
                          <option value="Laptop">Laptop</option>
                          <option value="Desktop">Desktop</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Brand</label>
                        <input 
                          type="text"
                          value={formData.brand}
                          onChange={(e) => handleInputChange('brand', e.target.value)}
                          placeholder="e.g. Dell, HP, Apple"
                        />
                      </div>

                      <div className="form-group">
                        <label>Model Name</label>
                        <input 
                          type="text"
                          value={formData.model_name}
                          onChange={(e) => handleInputChange('model_name', e.target.value)}
                          placeholder="e.g. XPS 15, MacBook Pro"
                        />
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Model</label>
                        <input 
                          type="text"
                          value={formData.model}
                          onChange={(e) => handleInputChange('model', e.target.value)}
                          placeholder="Model number"
                        />
                      </div>

                      <div className="form-group">
                        <label>S/N Type</label>
                        <input 
                          type="text"
                          value={formData.sn_type}
                          onChange={(e) => handleInputChange('sn_type', e.target.value)}
                          placeholder="Serial number type"
                        />
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Serial Number</label>
                      <input 
                        type="text"
                        value={formData.serial_number}
                        onChange={(e) => handleInputChange('serial_number', e.target.value)}
                        placeholder="Serial number"
                      />
                    </div>

                    <div className="form-group">
                      <label>Description</label>
                      <textarea 
                        value={formData.description}
                        onChange={(e) => handleInputChange('description', e.target.value)}
                        placeholder="Additional details about the asset"
                        rows="3"
                      />
                    </div>
                  </div>
                )}

                {/* Technical Specs Tab */}
                {currentTab === 'technical' && (
                  <div className="form-section">
                    <h3>Technical Specifications</h3>
                    
                    <div className="form-row">
                      <div className="form-group">
                        <label>Processor</label>
                        <input 
                          type="text"
                          value={formData.processor}
                          onChange={(e) => handleInputChange('processor', e.target.value)}
                          placeholder="e.g. Intel Core i7-11800H"
                        />
                      </div>

                      <div className="form-group">
                        <label>RAM</label>
                        <input 
                          type="text"
                          value={formData.ram}
                          onChange={(e) => handleInputChange('ram', e.target.value)}
                          placeholder="e.g. 16GB DDR4"
                        />
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Storage</label>
                        <input 
                          type="text"
                          value={formData.storage}
                          onChange={(e) => handleInputChange('storage', e.target.value)}
                          placeholder="e.g. 512GB SSD"
                        />
                      </div>

                      <div className="form-group">
                        <label>Graphics</label>
                        <input 
                          type="text"
                          value={formData.graphics}
                          onChange={(e) => handleInputChange('graphics', e.target.value)}
                          placeholder="e.g. NVIDIA RTX 3060"
                        />
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Display</label>
                        <input 
                          type="text"
                          value={formData.display}
                          onChange={(e) => handleInputChange('display', e.target.value)}
                          placeholder="e.g. 15.6 inch FHD"
                        />
                      </div>

                      <div className="form-group">
                        <label>Operating System</label>
                        <input 
                          type="text"
                          value={formData.os}
                          onChange={(e) => handleInputChange('os', e.target.value)}
                          placeholder="e.g. Windows 11 Pro"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* Assignment Tab */}
                {currentTab === 'assignment' && (
                  <div className="form-section">
                    <h3>Assignment Information</h3>
                    
                    <div className="form-row">
                      <div className="form-group">
                        <label>Assigned To</label>
                        <input 
                          type="text"
                          value={formData.assigned_to}
                          onChange={(e) => handleInputChange('assigned_to', e.target.value)}
                          placeholder="Employee name"
                        />
                      </div>

                      <div className="form-group">
                        <label>Department</label>
                        <input 
                          type="text"
                          value={formData.department}
                          onChange={(e) => handleInputChange('department', e.target.value)}
                          placeholder="Department name"
                        />
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Assignment Date</label>
                      <input 
                        type="date"
                        value={formData.assignment_date}
                        onChange={(e) => handleInputChange('assignment_date', e.target.value)}
                      />
                    </div>
                  </div>
                )}

                {/* Purchase Info Tab */}
                {currentTab === 'purchase' && (
                  <div className="form-section">
                    <h3>Purchase Information</h3>
                    
                    <div className="form-row">
                      <div className="form-group">
                        <label>Supplier</label>
                        <input 
                          type="text"
                          value={formData.supplier}
                          onChange={(e) => handleInputChange('supplier', e.target.value)}
                          placeholder="Supplier name"
                        />
                      </div>

                      <div className="form-group">
                        <label>Purchase Cost</label>
                        <input 
                          type="number"
                          step="0.01"
                          value={formData.purchase_cost}
                          onChange={(e) => handleInputChange('purchase_cost', e.target.value)}
                          placeholder="0.00"
                        />
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Invoice Number</label>
                        <input 
                          type="text"
                          value={formData.invoice_number}
                          onChange={(e) => handleInputChange('invoice_number', e.target.value)}
                          placeholder="Invoice number"
                        />
                      </div>

                      <div className="form-group">
                        <label>Warranty End Date</label>
                        <input 
                          type="date"
                          value={formData.warranty_end}
                          onChange={(e) => handleInputChange('warranty_end', e.target.value)}
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* QR Code Tab */}
                {currentTab === 'qr' && (
                  <div className="form-section">
                    <h3>QR Code & Label</h3>
                    <div className="qr-preview">
                      <p>QR Code will be generated after asset creation</p>
                      <div className="qr-placeholder">
                        <span>QR Code Preview</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Asset
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default AssetsManagement;
