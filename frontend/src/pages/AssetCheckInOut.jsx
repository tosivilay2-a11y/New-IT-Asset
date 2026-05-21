import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './AssetCheckInOut.css';

function AssetCheckInOut() {
  const [assignedAssets, setAssignedAssets] = useState([]);
  const [users, setUsers] = useState([]);
  const [staff, setStaff] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [stockLocations, setStockLocations] = useState([]);
  const [selectedStockLocation, setSelectedStockLocation] = useState(null);
  const [defaultStockLocation, setDefaultStockLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Modal states
  const [showCheckoutModal, setShowCheckoutModal] = useState(false);
  const [showCheckinModal, setShowCheckinModal] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState(null);
  
  // Form data
  const [checkoutForm, setCheckoutForm] = useState({
    assetId: '',
    staffId: '',
    reason: ''
  });
  
  const [checkinForm, setCheckinForm] = useState({
    assetId: '',
    condition: 'Good',
    reason: '',
    physicalCondition: {
      screen: 'Good',
      keyboard: 'Good',
      battery: 'Good',
      ports: 'Good',
      casing: 'Good'
    },
    functionalTest: {
      bootUp: true,
      wifi: true,
      audio: true,
      camera: true,
      performance: 'Good'
    },
    accessories: {
      charger: true,
      mouse: false,
      bag: false,
      cables: false
    }
  });

  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        await Promise.all([
          fetchAssignedAssets(),
          fetchUsers(),
          fetchStaff(),
          fetchCompanies(),
          fetchStockLocations()
        ]);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const getErrorMessage = (error) => {
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      // Handle array of validation errors
      if (Array.isArray(detail)) {
        return detail.map(err => err.msg || err).join(', ');
      }
      // Handle string error
      if (typeof detail === 'string') {
        return detail;
      }
      // Handle object error
      if (typeof detail === 'object' && detail.msg) {
        return detail.msg;
      }
    }
    return error.message || 'An error occurred';
  };

  const fetchAssignedAssets = async () => {
    try {
      const response = await api.get('/assets/');
      const assets = response.data.filter(asset => asset.assignedto);
      setAssignedAssets(assets || []);
    } catch (error) {
      console.error('Error fetching assigned assets:', error);
      setError('Failed to fetch assigned assets');
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users/');
      setUsers(response.data || []);
    } catch (error) {
      console.error('Error fetching users:', error);
      setError('Failed to fetch users');
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

  const fetchStockLocations = async () => {
    try {
      const response = await api.get('/stock-locations/');
      const locations = response.data || [];
      setStockLocations(locations);
      
      // Find and set the default stock location
      const defaultLocation = locations.find(loc => loc.stockdefault);
      if (defaultLocation) {
        setDefaultStockLocation(defaultLocation.stockid);
        setSelectedStockLocation(defaultLocation.stockid);
      }
    } catch (error) {
      console.error('Error fetching stock locations:', error);
      // Stock locations are optional, don't set error
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    // Validate inputs
    if (!checkoutForm.assetId.trim()) {
      setError('Please enter an Asset ID');
      return;
    }
    if (!checkoutForm.staffId) {
      setError('Please select a staff member');
      return;
    }
    
    try {
      setLoading(true);
      
      // Find the asset by assetcode - search all assets, not just assigned ones
      let asset = null;
      try {
        const allAssetsResponse = await api.get('/assets/?limit=1000');
        asset = allAssetsResponse.data.find(a => a.assetcode === checkoutForm.assetId);
      } catch (err) {
        console.error('Error fetching all assets:', err);
      }
      
      if (!asset) {
        setError('Asset not found');
        setLoading(false);
        return;
      }
      
      // Check if asset is available (statusid = 1 for Available)
      if (asset.statusid !== 1) {
        const statusName = asset.status_name || asset.status || `Status ${asset.statusid}`;
        setError(`Cannot checkout asset. Current status: ${statusName}. Only "Available" assets can be checked out.`);
        setLoading(false);
        return;
      }
      
      // Check if asset is already assigned
      if (asset.assignedto) {
        setError('Asset is already assigned to someone. Please check it in first before assigning to another person.');
        setLoading(false);
        return;
      }

      // Business rule: only Good condition assets can be checked out
      if ((asset.condition || '').toLowerCase() !== 'good') {
        setError(`Cannot checkout asset. Current condition: ${asset.condition || 'Unknown'}. Only "Good" condition assets can be checked out.`);
        setLoading(false);
        return;
      }
      
      const staffId = parseInt(checkoutForm.staffId);
      if (isNaN(staffId)) {
        setError('Invalid staff selection');
        setLoading(false);
        return;
      }
      
      // Get staff member's company ID to use as asset location
      const selectedStaff = staff.find(s => s.staffid === staffId);
      if (!selectedStaff) {
        setError('Staff member not found');
        setLoading(false);
        return;
      }
      
      // Use dedicated checkout endpoint so stockid is always set to 0 (stored as [0] in DB integer[])
      await api.post(`/assets/${asset.assetid}/checkout`, null, {
        params: { assignedto: staffId }
      });

      // Keep additional updates here for fields not handled by checkout endpoint
      // Do NOT change locationid: original asset location should remain fixed.
      await api.put(`/assets/${asset.assetid}`, {
        statusid: 2  // In Use status
      });
      
      // Record checkout history: move from asset base location to staff location
      const checkoutLocationAfter = selectedStaff.locationid || selectedStaff.companyid || asset.locationid;
      await api.post('/asset-history/', {
        assetid: asset.assetid,
        action: 'CHECKOUT',
        staffid: staffId,
        reason: checkoutForm.reason,
        condition_before: asset.condition || 'Good',
        condition_after: 'Good',
        location_before: asset.locationid,
        location_after: checkoutLocationAfter,
        notes: `Checked out to staff member ${selectedStaff.fullname}`
      });
      
      setSuccess(`Asset ${checkoutForm.assetId} successfully checked out to ${selectedStaff?.fullname}!`);
      setCheckoutForm({ assetId: '', staffId: '', reason: '' });
      setShowCheckoutModal(false);
      await fetchAssignedAssets();
      
    } catch (error) {
      setError(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const handleCheckin = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      setLoading(true);
      
      let assetToProcess = selectedAsset;
      
      // If no asset selected (manual entry), find by assetcode
      if (!assetToProcess && checkinForm.assetId) {
        try {
          const allAssetsResponse = await api.get('/assets/?limit=1000');
          assetToProcess = allAssetsResponse.data.find(a => a.assetcode === checkinForm.assetId);
        } catch (err) {
          console.error('Error fetching all assets for check-in:', err);
        }
      }

      // Check if we found the asset
      if (!assetToProcess || !assetToProcess.assetid) {
        setError(`Asset with ID "${checkinForm.assetId}" not found`);
        setLoading(false);
        return;
      }

      // Check if asset is actually checked out
      if (!assetToProcess.assignedto) {
        setError(`Asset ${assetToProcess.assetcode} is not currently assigned to anyone.`);
        setLoading(false);
        return;
      }

      const finalStockId = selectedStockLocation || defaultStockLocation;
      if (!finalStockId) {
        setError('Please select a stock location for check-in');
        setLoading(false);
        return;
      }
      
      // Determine location: use selected stock location, fallback to default, then staff's location
      let locationId = null;
      
      // Use selected stock location's locationid
      if (selectedStockLocation) {
        const selectedStock = stockLocations.find(s => s.stockid === selectedStockLocation);
        if (selectedStock) {
          locationId = selectedStock.locationid;
        }
      } 
      // Fallback to default stock location's locationid
      else if (defaultStockLocation) {
        const defaultStock = stockLocations.find(s => s.stockid === defaultStockLocation);
        if (defaultStock) {
          locationId = defaultStock.locationid;
        }
      } 
      // Fallback to staff member's location if stock location not available
      else if (assetToProcess.assignedto) {
        const staffMember = staff.find(s => s.staffid === assetToProcess.assignedto);
        if (staffMember && staffMember.locationid) {
          locationId = staffMember.locationid;
        }
      }
      
      // Use dedicated check-in endpoint so stock + condition + report are persisted together
      await api.post(`/assets/${assetToProcess.assetid}/checkin`, {
        condition: checkinForm.condition,
        reason: checkinForm.reason,
        physicalCondition: checkinForm.physicalCondition,
        functionalTest: checkinForm.functionalTest,
        accessories: checkinForm.accessories
      }, {
        params: { stockid: finalStockId }
      });
      
      // Record check-in history
      await api.post('/asset-history/', {
        assetid: assetToProcess.assetid,
        action: 'CHECKIN',
        reason: checkinForm.reason,
        condition_before: assetToProcess.condition || 'Good',
        condition_after: checkinForm.condition,
        location_before: assetToProcess.locationid,
        location_after: locationId,
        notes: `Checked in. Stock Location: ${finalStockId}. Condition: ${checkinForm.condition}`
      });
      
      setSuccess(`Asset ${assetToProcess.assetcode} successfully checked in!`);
      setCheckinForm({
        assetId: '',
        condition: 'Good',
        reason: '',
        physicalCondition: {
          screen: 'Good',
          keyboard: 'Good',
          battery: 'Good',
          ports: 'Good',
          casing: 'Good'
        },
        functionalTest: {
          bootUp: true,
          wifi: true,
          audio: true,
          camera: true,
          performance: 'Good'
        },
        accessories: {
          charger: true,
          mouse: false,
          bag: false,
          cables: false
        }
      });
      setShowCheckinModal(false);
      setSelectedAsset(null);
      await fetchAssignedAssets();
      
    } catch (error) {
      setError(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const openCheckinModal = (asset) => {
    setSelectedAsset(asset);
    setCheckinForm({
      assetId: asset ? asset.assetcode : '',
      condition: 'Good',
      reason: '',
      physicalCondition: {
        screen: 'Good',
        keyboard: 'Good',
        battery: 'Good',
        ports: 'Good',
        casing: 'Good'
      },
      functionalTest: {
        bootUp: true,
        wifi: true,
        audio: true,
        camera: true,
        performance: 'Good'
      },
      accessories: {
        charger: true,
        mouse: false,
        bag: false,
        cables: false
      }
    });
    setShowCheckinModal(true);
  };

  if (loading && assignedAssets.length === 0) {
    return (
      <div className="loading-container">
        <div className="spinner">Loading...</div>
      </div>
    );
  }

  return (
    <div className="checkinout-container">
      <div className="page-header-checkinout">
        <div>
          <h2>📦 Asset Check-In/Check-Out</h2>
          <p className="text-muted">Manage asset assignments and returns</p>
        </div>
        <div className="button-group">
          <button 
            onClick={() => {
              setCheckoutForm({ assetId: '', staffId: '', reason: '' });
              setShowCheckoutModal(true);
            }} 
            className="btn btn-primary"
          >
            📤 Check Out Asset
          </button>
          <button 
            onClick={() => openCheckinModal(null)} 
            className="btn btn-success"
          >
            📥 Check In Asset
          </button>
          <button 
            onClick={async () => {
              setLoading(true);
              await Promise.all([fetchAssignedAssets(), fetchUsers()]);
              setLoading(false);
            }} 
            className="btn btn-secondary"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={() => setError('')} className="close-alert">✕</button>
        </div>
      )}
      
      {success && (
        <div className="alert alert-success">
          {success}
          <button onClick={() => setSuccess('')} className="close-alert">✕</button>
        </div>
      )}

      <div className="tabs-container">
        <div className="tab-content">
          <div className="tab-header">
            <h3>Currently Assigned Assets ({assignedAssets.length})</h3>
          </div>
          
          {assignedAssets.length === 0 ? (
            <div className="empty-state">
              <p>No assets are currently assigned</p>
              <button 
                onClick={() => setShowCheckoutModal(true)} 
                className="btn btn-primary"
              >
                Check Out First Asset
              </button>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="assets-table">
                <thead>
                  <tr>
                    <th>Asset ID</th>
                    <th>Asset Name</th>
                    <th>Category</th>
                    <th>Assigned To (Staff)</th>
                    <th>Company</th>
                    <th>Assigned By</th>
                    <th>Assigned Date</th>
                    <th>Condition</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {assignedAssets.map((asset) => {
                    const assignedStaff = staff.find(s => s.staffid === asset.assignedto);
                    const assignedByUser = users.find(u => u.userid === asset.createdby);
                    return (
                      <tr key={asset.assetid}>
                        <td>
                          <code>{asset.assetcode}</code>
                        </td>
                        <td>{asset.assetname}</td>
                        <td>
                          <span className="badge">
                            {asset.main_category_name || asset.main_category || asset.category_name || asset.category || asset.maincategoryid || 'N/A'}
                          </span>
                        </td>
                        <td>
                          <div className="user-info">
                            <div className="user-name">
                              {assignedStaff ? assignedStaff.fullname : `Staff #${asset.assignedto}`}
                            </div>
                            <div className="user-email">{assignedStaff?.employeeid}</div>
                          </div>
                        </td>
                        <td>
                          <div className="company-info">
                            {(() => {
                              const company = companies.find(c => c.companyid === assignedStaff?.companyid);
                              return company ? company.companyname : (assignedStaff?.companyid ? `Company #${assignedStaff.companyid}` : 'N/A');
                            })()}
                          </div>
                        </td>
                        <td>
                          <div className="user-info">
                            <div className="user-name">
                              {assignedByUser ? `${assignedByUser.firstname} ${assignedByUser.lastname}` : 'System'}
                            </div>
                            <div className="user-email">{assignedByUser?.email}</div>
                          </div>
                        </td>
                        <td>
                          {asset.assigneddate ? new Date(asset.assigneddate).toLocaleDateString() : '-'}
                        </td>
                        <td>
                          <span className={`condition-badge condition-${asset.condition?.toLowerCase()}`}>
                            {asset.condition || 'Good'}
                          </span>
                        </td>
                        <td>
                          <div className="action-buttons">
                            <button
                              onClick={() => openCheckinModal(asset)}
                              className="btn btn-sm btn-success"
                              title="Check In"
                            >
                              📥 Check In
                            </button>
                            <button
                              onClick={() => navigate(`/assets/${asset.assetid}`)}
                              className="btn btn-sm btn-info"
                              title="View Details"
                            >
                              👁️ View
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Checkout Modal */}
      {showCheckoutModal && (
        <div className="modal-overlay" onClick={() => setShowCheckoutModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📤 Check Out Asset</h2>
              <button 
                className="close-btn"
                onClick={() => setShowCheckoutModal(false)}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCheckout}>
              <div className="modal-body">
                <div className="form-group">
                  <label>Asset ID *</label>
                  <input
                    type="text"
                    value={checkoutForm.assetId}
                    onChange={(e) => setCheckoutForm({...checkoutForm, assetId: e.target.value})}
                    placeholder="e.g., ASSET001"
                    className="form-control"
                    required
                  />
                  <small>Enter the exact Asset ID</small>
                </div>
                
                <div className="form-group">
                  <label>Assign To Staff Member *</label>
                  <select
                    value={checkoutForm.staffId}
                    onChange={(e) => setCheckoutForm({...checkoutForm, staffId: e.target.value})}
                    className="form-control"
                    required
                  >
                    <option value="">Select Staff Member</option>
                    {staff.map((staffMember) => (
                      <option key={staffMember.staffid} value={staffMember.staffid}>
                        {staffMember.fullname} ({staffMember.employeeid})
                      </option>
                    ))}
                  </select>
                </div>

                {checkoutForm.staffId && (
                  <div className="user-details-card">
                    {(() => {
                      const selectedStaff = staff.find(s => s.staffid === parseInt(checkoutForm.staffId));
                      if (selectedStaff) {
                        return (
                          <div>
                            <div className="detail-row">
                              <strong>Name:</strong> {selectedStaff.fullname}
                            </div>
                            <div className="detail-row">
                              <strong>Employee ID:</strong> {selectedStaff.employeeid}
                            </div>
                            <div className="detail-row">
                              <strong>Email:</strong> {selectedStaff.email}
                            </div>
                            <div className="detail-row">
                              <strong>Department:</strong> {selectedStaff.department}
                            </div>
                            <div className="detail-row">
                              <strong>Position:</strong> {selectedStaff.position}
                            </div>
                          </div>
                        );
                      }
                      return null;
                    })()}
                  </div>
                )}
                
                <div className="form-group">
                  <label>Reason for Assignment</label>
                  <textarea
                    value={checkoutForm.reason}
                    onChange={(e) => setCheckoutForm({...checkoutForm, reason: e.target.value})}
                    placeholder="e.g., New hire equipment, Replacement device, etc."
                    className="form-control"
                    rows="3"
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowCheckoutModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Processing...' : 'Check Out Asset'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Checkin Modal */}
      {showCheckinModal && (
        <div className="modal-overlay" onClick={() => setShowCheckinModal(false)}>
          <div className="modal-content modal-lg" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📥 Check In Asset</h2>
              <button 
                className="close-btn"
                onClick={() => setShowCheckinModal(false)}
              >
                ✕
              </button>
            </div>

            <div className="asset-details-banner search-banner">
              <div className="form-group mb-0">
                <label style={{ color: 'white' }}>Asset ID / Code *</label>
                <input
                  type="text"
                  value={checkinForm.assetId}
                  onChange={(e) => setCheckinForm({...checkinForm, assetId: e.target.value})}
                  placeholder="e.g., ASSET001"
                  className="form-control"
                  disabled={!!selectedAsset}
                  required
                />
              </div>
              {selectedAsset && (
                <>
                  <div className="detail-item">
                    <strong>Asset Name:</strong> {selectedAsset.assetname}
                  </div>
                  <div className="detail-item">
                    <strong>Currently Assigned To:</strong> {
                      (() => {
                        const assignedStaff = staff.find(s => s.staffid === selectedAsset.assignedto);
                        if (assignedStaff?.fullname) return assignedStaff.fullname;
                        const assignedUser = users.find(u => u.userid === selectedAsset.assignedto);
                        if (assignedUser) {
                          const fullName = `${assignedUser.firstname || ''} ${assignedUser.lastname || ''}`.trim();
                          return fullName || assignedUser.email || `User #${selectedAsset.assignedto}`;
                        }
                        return selectedAsset.assigned_user_name || 'Unassigned';
                      })()
                    }
                  </div>
                </>
              )}
              {!selectedAsset && checkinForm.assetId && (
                <div className="detail-item info-text">
                  <small>Enter the exact Asset Code to lookup assignment details during check-in</small>
                </div>
              )}
            </div>
            
            <form onSubmit={handleCheckin}>
              <div className="modal-body">
                <div className="tabs-checkin">
                  <div className="tab-section">
                    <h4>🔍 Physical Condition</h4>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Screen Condition</label>
                        <select
                          value={checkinForm.physicalCondition.screen}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            physicalCondition: {...checkinForm.physicalCondition, screen: e.target.value}
                          })}
                          className="form-control"
                        >
                          <option value="Good">✅ Good - No scratches or cracks</option>
                          <option value="Fair">⚠️ Fair - Minor scratches</option>
                          <option value="Damaged">❌ Damaged - Cracks or dead pixels</option>
                          <option value="Broken">🔴 Broken - Not functional</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Keyboard Condition</label>
                        <select
                          value={checkinForm.physicalCondition.keyboard}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            physicalCondition: {...checkinForm.physicalCondition, keyboard: e.target.value}
                          })}
                          className="form-control"
                        >
                          <option value="Good">✅ Good - All keys working</option>
                          <option value="Fair">⚠️ Fair - Some keys sticky</option>
                          <option value="Damaged">❌ Damaged - Missing/broken keys</option>
                          <option value="Broken">🔴 Broken - Not functional</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Battery Condition</label>
                        <select
                          value={checkinForm.physicalCondition.battery}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            physicalCondition: {...checkinForm.physicalCondition, battery: e.target.value}
                          })}
                          className="form-control"
                        >
                          <option value="Good">✅ Good - Holds charge well</option>
                          <option value="Fair">⚠️ Fair - Reduced battery life</option>
                          <option value="Damaged">❌ Damaged - Very poor battery</option>
                          <option value="Broken">🔴 Broken - No battery/won't charge</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Ports & Connections</label>
                        <select
                          value={checkinForm.physicalCondition.ports}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            physicalCondition: {...checkinForm.physicalCondition, ports: e.target.value}
                          })}
                          className="form-control"
                        >
                          <option value="Good">✅ Good - All ports working</option>
                          <option value="Fair">⚠️ Fair - Some ports loose</option>
                          <option value="Damaged">❌ Damaged - Some ports broken</option>
                          <option value="Broken">🔴 Broken - Major port issues</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Casing/Body Condition</label>
                      <select
                        value={checkinForm.physicalCondition.casing}
                        onChange={(e) => setCheckinForm({
                          ...checkinForm,
                          physicalCondition: {...checkinForm.physicalCondition, casing: e.target.value}
                        })}
                        className="form-control"
                      >
                        <option value="Good">✅ Good - No damage</option>
                        <option value="Fair">⚠️ Fair - Minor scratches/dents</option>
                        <option value="Damaged">❌ Damaged - Visible damage</option>
                        <option value="Broken">🔴 Broken - Structural damage</option>
                      </select>
                    </div>
                  </div>

                  <div className="tab-section">
                    <h4>⚡ Functional Test</h4>
                    <div className="checkbox-group">
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.functionalTest.bootUp}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            functionalTest: {...checkinForm.functionalTest, bootUp: e.target.checked}
                          })}
                        />
                        ✅ System boots up properly
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.functionalTest.wifi}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            functionalTest: {...checkinForm.functionalTest, wifi: e.target.checked}
                          })}
                        />
                        📶 WiFi connects successfully
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.functionalTest.audio}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            functionalTest: {...checkinForm.functionalTest, audio: e.target.checked}
                          })}
                        />
                        🔊 Audio works properly
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.functionalTest.camera}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            functionalTest: {...checkinForm.functionalTest, camera: e.target.checked}
                          })}
                        />
                        📷 Camera functions correctly
                      </label>
                    </div>

                    <div className="form-group">
                      <label>Overall Performance</label>
                      <select
                        value={checkinForm.functionalTest.performance}
                        onChange={(e) => setCheckinForm({
                          ...checkinForm,
                          functionalTest: {...checkinForm.functionalTest, performance: e.target.value}
                        })}
                        className="form-control"
                      >
                        <option value="Excellent">🚀 Excellent - Fast and responsive</option>
                        <option value="Good">✅ Good - Normal performance</option>
                        <option value="Fair">⚠️ Fair - Somewhat slow</option>
                        <option value="Poor">❌ Poor - Very slow/laggy</option>
                      </select>
                    </div>
                  </div>

                  <div className="tab-section">
                    <h4>🎒 Accessories</h4>
                    <div className="checkbox-group">
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.accessories.charger}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            accessories: {...checkinForm.accessories, charger: e.target.checked}
                          })}
                        />
                        🔌 Power Charger
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.accessories.mouse}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            accessories: {...checkinForm.accessories, mouse: e.target.checked}
                          })}
                        />
                        🖱️ Mouse
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.accessories.bag}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            accessories: {...checkinForm.accessories, bag: e.target.checked}
                          })}
                        />
                        💼 Laptop Bag
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={checkinForm.accessories.cables}
                          onChange={(e) => setCheckinForm({
                            ...checkinForm,
                            accessories: {...checkinForm.accessories, cables: e.target.checked}
                          })}
                        />
                        🔗 Cables (USB, HDMI, etc.)
                      </label>
                    </div>
                  </div>

                  <div className="tab-section">
                    <h4>📋 Summary</h4>
                    
                    <div className="form-group">
                      <label>Stock Location <span className="required-mark">*</span></label>
                      <select
                        value={selectedStockLocation || ''}
                        onChange={(e) => setSelectedStockLocation(parseInt(e.target.value) || null)}
                        className="form-control"
                      >
                        <option value="">-- Select Stock Location --</option>
                        {stockLocations.map((location) => (
                          <option key={location.stockid} value={location.stockid}>
                            {location.stockdefault ? '⭐ ' : ''}{location.stockname}
                          </option>
                        ))}
                      </select>
                      <small>
                        {defaultStockLocation && !selectedStockLocation 
                          ? `Default: ${stockLocations.find(l => l.stockid === defaultStockLocation)?.stockname}`
                          : 'Select where asset will be stored after check-in'}
                      </small>
                    </div>
                    
                    <div className="form-group">
                      <label>Overall Condition *</label>
                      <select
                        value={checkinForm.condition}
                        onChange={(e) => setCheckinForm({...checkinForm, condition: e.target.value})}
                        className="form-control"
                        required
                      >
                        <option value="Good">✅ Good - Ready for immediate reuse</option>
                        <option value="Fair">⚠️ Fair - Minor cleaning/updates needed</option>
                        <option value="Damaged">❌ Damaged - Requires repair</option>
                        <option value="Broken">🔴 Broken - Cannot be repaired</option>
                      </select>
                    </div>
                    
                    <div className="form-group">
                      <label>Return Reason & Notes</label>
                      <textarea
                        value={checkinForm.reason}
                        onChange={(e) => setCheckinForm({...checkinForm, reason: e.target.value})}
                        placeholder="e.g., Employee departure, Equipment upgrade, End of project, etc."
                        className="form-control"
                        rows="3"
                      />
                    </div>

                    <div className="info-banner">
                      <strong>📋 Check-In Process:</strong>
                      <ul>
                        <li>Asset will be marked as: <strong>{
                          checkinForm.condition === 'Damaged' ? 'Under Repair' :
                          checkinForm.condition === 'Broken' ? 'Retired' : 'Available'
                        }</strong></li>
                        <li>Assignment will be cleared</li>
                        <li>Condition report will be saved</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowCheckinModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-success"
                  disabled={loading}
                >
                  {loading ? 'Processing Check-In...' : '📥 Complete Check-In'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default AssetCheckInOut;
