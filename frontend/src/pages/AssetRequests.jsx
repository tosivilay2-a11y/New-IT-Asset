import React, { useState, useEffect } from 'react';
import { assetRequestsAPI, assetsAPI } from '../services/api';
import api from '../services/api';
import './AssetRequests.css';

function AssetRequests({ user }) {
  const [requests, setRequests] = useState([]);
  const [availableAssets, setAvailableAssets] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Active Tab: admin defaults to IT queue, HR/others default to HR Portal
  const isAdmin = user && user.role === 'admin';
  const [activeTab, setActiveTab] = useState(isAdmin ? 'it' : 'hr');

  // IT Assignment state
  const [assigningRequestId, setAssigningRequestId] = useState(null);
  const [selectedAssetCode, setSelectedAssetCode] = useState('');
  const [assignmentNotes, setAssignmentNotes] = useState('');
  
  // HR Form state
  const [form, setForm] = useState({
    staff_name: '',
    staff_email: '',
    department: '',
    position: '',
    company_name: '',
    asset_type: 'Computer',
    priority: 'Medium',
    reason: '',
    notes: ''
  });

  // Filter requests
  const [statusFilter, setStatusFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadData();
  }, [user]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Fetch request tickets
      const requestsRes = await assetRequestsAPI.getAll();
      setRequests(requestsRes.data || []);

      // If admin, also fetch available assets and other helper lists
      if (isAdmin) {
        await fetchAvailableAssets();
      }

      // Fetch metadata lists for form options
      await fetchMetadata();
    } catch (err) {
      console.error('Error loading request portal data:', err);
      setError('Failed to fetch data from the server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableAssets = async () => {
    try {
      const assetsRes = await api.get('/assets/?limit=1000');
      // Status ID 1 = Available, condition Good is required for checkout
      const available = (assetsRes.data || []).filter(
        asset => asset.statusid === 1 && (asset.condition || '').toLowerCase() === 'good'
      );
      setAvailableAssets(available);
    } catch (err) {
      console.error('Error fetching available assets:', err);
    }
  };

  const fetchMetadata = async () => {
    try {
      const [companiesRes, deptsRes] = await Promise.allSettled([
        api.get('/companies/'),
        api.get('/departments/')
      ]);

      if (companiesRes.status === 'fulfilled') {
        setCompanies(companiesRes.value.data || []);
      }
      if (deptsRes.status === 'fulfilled') {
        setDepartments(deptsRes.value.data || []);
      }
    } catch (err) {
      console.error('Error loading metadata lists:', err);
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleHRSubmit = async (e) => {
    e.preventDefault();
    if (!form.staff_name.trim()) {
      setError('Staff Name is required.');
      return;
    }
    
    try {
      setSubmitting(true);
      setError('');
      setSuccess('');

      await assetRequestsAPI.create(form);
      
      setSuccess(`Request ticket successfully submitted for ${form.staff_name}!`);
      
      // Reset form
      setForm({
        staff_name: '',
        staff_email: '',
        department: '',
        position: '',
        company_name: '',
        asset_type: 'Computer',
        priority: 'Medium',
        reason: '',
        notes: ''
      });

      // Reload ticket list
      const requestsRes = await assetRequestsAPI.getAll();
      setRequests(requestsRes.data || []);
    } catch (err) {
      console.error('Error submitting HR request:', err);
      setError(err.response?.data?.detail || 'Failed to submit the request. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleITAssign = async (e) => {
    e.preventDefault();
    if (!selectedAssetCode) {
      setError('Please select a computer asset to assign.');
      return;
    }

    try {
      setSubmitting(true);
      setError('');
      setSuccess('');

      const response = await assetRequestsAPI.assign(
        assigningRequestId,
        selectedAssetCode,
        assignmentNotes
      );

      setSuccess(response.data.message || 'Asset successfully signed and assigned!');
      setAssigningRequestId(null);
      setSelectedAssetCode('');
      setAssignmentNotes('');

      // Refresh everything
      const requestsRes = await assetRequestsAPI.getAll();
      setRequests(requestsRes.data || []);
      await fetchAvailableAssets();
    } catch (err) {
      console.error('Error in asset assignment:', err);
      setError(err.response?.data?.detail || 'Failed to complete assignment. Verify asset availability.');
    } finally {
      setSubmitting(false);
    }
  };

  const getPriorityBadgeClass = (priority) => {
    switch ((priority || '').toLowerCase()) {
      case 'urgent': return 'priority-urgent';
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      default: return 'priority-low';
    }
  };

  const getStatusBadgeClass = (status) => {
    switch ((status || '').toLowerCase()) {
      case 'assigned': return 'status-assigned';
      case 'rejected': return 'status-rejected';
      default: return 'status-pending';
    }
  };

  // Filter requests lists
  const filteredRequests = requests.filter(req => {
    const matchesStatus = statusFilter === 'All' || req.status === statusFilter;
    const matchesSearch = 
      (req.staff_name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (req.department || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (req.position || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (req.requested_by || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (req.assigned_assetcode || '').toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  return (
    <div className="requests-portal-container">
      {/* Premium Header Accent */}
      <div className="portal-header-bg">
        <div className="portal-header-content">
          <h1>Asset Provisioning Portal</h1>
          <p>Seamless hardware request workflows for HR and IT Operations</p>
        </div>
      </div>

      <div className="container portal-layout">
        {/* Navigation Tabs */}
        <div className="portal-tabs">
          <button 
            className={`tab-btn ${activeTab === 'hr' ? 'active' : ''}`}
            onClick={() => { setActiveTab('hr'); setError(''); setSuccess(''); }}
          >
            📋 HR Request Portal
          </button>
          
          {isAdmin && (
            <button 
              className={`tab-btn ${activeTab === 'it' ? 'active' : ''}`}
              onClick={() => { setActiveTab('it'); setError(''); setSuccess(''); }}
            >
              💻 IT Provisioning Queue
            </button>
          )}
        </div>

        {/* Message banners */}
        {error && (
          <div className="portal-alert error-banner">
            <span className="alert-icon">⚠️</span>
            <div className="alert-text">{error}</div>
            <button className="alert-close" onClick={() => setError('')}>&times;</button>
          </div>
        )}
        
        {success && (
          <div className="portal-alert success-banner">
            <span className="alert-icon">✨</span>
            <div className="alert-text">{success}</div>
            <button className="alert-close" onClick={() => setSuccess('')}>&times;</button>
          </div>
        )}

        {loading ? (
          <div className="portal-loader">
            <div className="spinner"></div>
            <p>Gathering provisioning workflows...</p>
          </div>
        ) : (
          <div className="portal-content-body">
            
            {/* TAB: HR PORTAL */}
            {activeTab === 'hr' && (
              <div className="hr-portal-grid">
                
                {/* Form column */}
                <div className="glass-panel form-panel">
                  <div className="panel-header">
                    <h2>Submit Equipment Request</h2>
                    <p>Request computer setups for incoming or current staff members.</p>
                  </div>
                  
                  <form onSubmit={handleHRSubmit} className="premium-form">
                    <div className="form-row-double">
                      <div className="form-group-premium">
                        <label>Staff Full Name <span className="req">*</span></label>
                        <input
                          type="text"
                          name="staff_name"
                          value={form.staff_name}
                          onChange={handleFormChange}
                          placeholder="e.g. Somchai Jaidee"
                          required
                        />
                      </div>
                      
                      <div className="form-group-premium">
                        <label>Staff Email Address</label>
                        <input
                          type="email"
                          name="staff_email"
                          value={form.staff_email}
                          onChange={handleFormChange}
                          placeholder="e.g. somchai.j@company.com"
                        />
                      </div>
                    </div>

                    <div className="form-row-double">
                      <div className="form-group-premium">
                        <label>Company / Subsidiary</label>
                        <select 
                          name="company_name" 
                          value={form.company_name} 
                          onChange={handleFormChange}
                        >
                          <option value="">-- Select Company --</option>
                          {companies.map(c => (
                            <option key={c.companyid} value={c.companyname}>{c.companyname}</option>
                          ))}
                          <option value="Non-listed">Other / Non-listed</option>
                        </select>
                      </div>

                      <div className="form-group-premium">
                        <label>Department</label>
                        <select 
                          name="department" 
                          value={form.department} 
                          onChange={handleFormChange}
                        >
                          <option value="">-- Select Department --</option>
                          {departments.map(d => (
                            <option key={d.deptid} value={d.deptname}>{d.deptname}</option>
                          ))}
                          <option value="HR">Human Resources</option>
                          <option value="IT">Information Technology</option>
                          <option value="Marketing">Marketing</option>
                          <option value="Sales">Sales</option>
                          <option value="Finance">Finance</option>
                          <option value="Operations">Operations</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-row-double">
                      <div className="form-group-premium">
                        <label>Staff Position / Title</label>
                        <input
                          type="text"
                          name="position"
                          value={form.position}
                          onChange={handleFormChange}
                          placeholder="e.g. Senior Frontend Developer"
                        />
                      </div>

                      <div className="form-group-premium">
                        <label>Equipment Type Requested</label>
                        <select name="asset_type" value={form.asset_type} onChange={handleFormChange}>
                          <option value="Computer">Laptop / Computer</option>
                          <option value="Desktop">Desktop PC</option>
                          <option value="Tablet">Tablet / iPad</option>
                          <option value="Mobile">Mobile Phone</option>
                        </select>
                      </div>
                    </div>

                    <div className="form-group-premium">
                      <label>Priority Urgency</label>
                      <div className="priority-selector">
                        {['Low', 'Medium', 'High', 'Urgent'].map(p => (
                          <label 
                            key={p} 
                            className={`priority-option ${form.priority === p ? 'active' : ''}`}
                          >
                            <input 
                              type="radio" 
                              name="priority" 
                              value={p} 
                              checked={form.priority === p}
                              onChange={handleFormChange}
                            />
                            {p}
                          </label>
                        ))}
                      </div>
                    </div>

                    <div className="form-group-premium">
                      <label>Business Need / Onboarding Reason</label>
                      <textarea
                        name="reason"
                        value={form.reason}
                        onChange={handleFormChange}
                        placeholder="e.g. New developer onboarding on June 1st. Requires high-spec machine."
                        rows="3"
                      ></textarea>
                    </div>

                    <div className="form-group-premium">
                      <label>Additional Notes / Software Requirements</label>
                      <textarea
                        name="notes"
                        value={form.notes}
                        onChange={handleFormChange}
                        placeholder="e.g. Needs Visual Studio Code, Docker Desktop, and Git pre-installed."
                        rows="2"
                      ></textarea>
                    </div>

                    <button 
                      type="submit" 
                      className="premium-submit-btn" 
                      disabled={submitting}
                    >
                      {submitting ? 'Submitting Request...' : '🚀 Submit Request Ticket'}
                    </button>
                  </form>
                </div>

                {/* Queue list column */}
                <div className="glass-panel list-panel">
                  <div className="panel-header">
                    <h2>Submitted Requests</h2>
                    <p>Track status and computer assignments for your team tickets.</p>
                  </div>

                  <div className="panel-search-bar">
                    <input 
                      type="text" 
                      placeholder="Search requests..." 
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      className="search-input"
                    />
                  </div>

                  <div className="requests-ticket-list">
                    {filteredRequests.length === 0 ? (
                      <div className="empty-tickets">
                        <div className="empty-icon">📁</div>
                        <p>No asset request tickets found.</p>
                      </div>
                    ) : (
                      filteredRequests.map(req => (
                        <div key={req.requestid} className="ticket-card">
                          <div className="ticket-header">
                            <div>
                              <span className="ticket-id">#{req.requestid}</span>
                              <span className={`badge ${getPriorityBadgeClass(req.priority)}`}>
                                {req.priority}
                              </span>
                            </div>
                            <span className={`badge ${getStatusBadgeClass(req.status)}`}>
                              {req.status}
                            </span>
                          </div>

                          <div className="ticket-body">
                            <h3>{req.staff_name}</h3>
                            <div className="ticket-meta">
                              <span><strong>Email:</strong> {req.staff_email || 'N/A'}</span>
                              <span><strong>Dept:</strong> {req.department || 'N/A'}</span>
                              <span><strong>Pos:</strong> {req.position || 'N/A'}</span>
                              <span><strong>Company:</strong> {req.company_name || 'N/A'}</span>
                            </div>
                            
                            {req.reason && (
                              <p className="ticket-reason">
                                <strong>Reason:</strong> {req.reason}
                              </p>
                            )}

                            {req.status === 'Assigned' && (
                              <div className="ticket-assignment-info">
                                <span className="assigned-icon">✔️</span>
                                <div>
                                  <strong>Assigned Asset:</strong>{' '}
                                  <code className="asset-code-badge">{req.assigned_assetcode}</code>
                                  {req.assigned_at && (
                                    <span className="assigned-date">
                                      {' '}on {new Date(req.assigned_at).toLocaleDateString()}
                                    </span>
                                  )}
                                </div>
                              </div>
                            )}

                            {req.notes && (
                              <p className="ticket-notes">
                                <strong>IT/HR Notes:</strong> {req.notes}
                              </p>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>

              </div>
            )}

            {/* TAB: IT PROVISIONING QUEUE */}
            {activeTab === 'it' && isAdmin && (
              <div className="glass-panel it-queue-panel">
                <div className="panel-header flex-header">
                  <div>
                    <h2>IT Provisioning Queue</h2>
                    <p>Review and fulfill equipment tickets by signing and checking out available computers.</p>
                  </div>
                  <div className="filter-controls">
                    <div className="filter-group">
                      <label>Status:</label>
                      <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
                        <option value="All">All Statuses</option>
                        <option value="Pending">Pending</option>
                        <option value="Assigned">Assigned</option>
                      </select>
                    </div>
                    <div className="filter-group">
                      <label>Search:</label>
                      <input 
                        type="text" 
                        placeholder="Search staff, dept, code..." 
                        value={searchQuery}
                        onChange={e => setSearchQuery(e.target.value)}
                      />
                    </div>
                  </div>
                </div>

                <div className="it-queue-table-container">
                  {filteredRequests.length === 0 ? (
                    <div className="empty-tickets">
                      <div className="empty-icon">🎉</div>
                      <p>All clean! No tickets match the filters.</p>
                    </div>
                  ) : (
                    <table className="premium-table">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Staff Details</th>
                          <th>Subsidiary & Dept</th>
                          <th>Equipment & Priority</th>
                          <th>Requested By</th>
                          <th>Status</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredRequests.map(req => (
                          <React.Fragment key={req.requestid}>
                            <tr className={`request-row ${assigningRequestId === req.requestid ? 'row-expanded' : ''}`}>
                              <td><strong>#{req.requestid}</strong></td>
                              <td>
                                <div className="staff-primary">{req.staff_name}</div>
                                <div className="staff-secondary">{req.staff_email}</div>
                                <div className="staff-secondary text-italic">{req.position}</div>
                              </td>
                              <td>
                                <div>{req.company_name || 'N/A'}</div>
                                <div className="dept-label">{req.department || 'N/A'}</div>
                              </td>
                              <td>
                                <div>💻 {req.asset_type}</div>
                                <span className={`badge ${getPriorityBadgeClass(req.priority)}`}>
                                  {req.priority}
                                </span>
                              </td>
                              <td className="requested-by-cell">
                                <span title={req.requested_by}>{req.requested_by?.split('@')[0]}</span>
                                <div className="request-time">
                                  {new Date(req.created_at).toLocaleDateString()}
                                </div>
                              </td>
                              <td>
                                <span className={`badge ${getStatusBadgeClass(req.status)}`}>
                                  {req.status}
                                </span>
                                {req.status === 'Assigned' && (
                                  <div className="assigned-code">
                                    <code>{req.assigned_assetcode}</code>
                                  </div>
                                )}
                              </td>
                              <td>
                                {req.status === 'Pending' ? (
                                  <button 
                                    className="action-btn assign-btn"
                                    onClick={() => {
                                      setAssigningRequestId(
                                        assigningRequestId === req.requestid ? null : req.requestid
                                      );
                                      setSelectedAssetCode('');
                                      setAssignmentNotes('');
                                    }}
                                  >
                                    🔑 {assigningRequestId === req.requestid ? 'Close' : 'Sign & Assign'}
                                  </button>
                                ) : (
                                  <span className="signed-stamp">✓ Fulfill Completed</span>
                                )}
                              </td>
                            </tr>

                            {/* Sub-row for signing computer */}
                            {assigningRequestId === req.requestid && (
                              <tr className="assign-sub-row">
                                <td colSpan="7">
                                  <div className="signing-panel glass-panel">
                                    <div className="signing-header">
                                      <h3>Sign and Assign Computer Setup to {req.staff_name}</h3>
                                      <p>Select an available device in Good condition to complete the checkout.</p>
                                    </div>
                                    
                                    <form onSubmit={handleITAssign} className="signing-form">
                                      <div className="form-group-premium">
                                        <label>Select Available Computer Asset <span className="req">*</span></label>
                                        <select 
                                          value={selectedAssetCode}
                                          onChange={e => setSelectedAssetCode(e.target.value)}
                                          required
                                        >
                                          <option value="">-- Choose Asset (Asset Code | Name | Brand) --</option>
                                          {availableAssets.map(asset => (
                                            <option key={asset.assetid} value={asset.assetcode}>
                                              [{asset.assetcode}] {asset.assetname} - {asset.brand || 'N/A'} {asset.model || 'N/A'} (Cond: {asset.condition})
                                            </option>
                                          ))}
                                        </select>
                                        <p className="select-helper-text">
                                          * Only computers marked as <strong>Available</strong> and in <strong>Good</strong> condition are displayed here.
                                        </p>
                                      </div>

                                      <div className="form-group-premium">
                                        <label>IT Provisioning Notes (Optional)</label>
                                        <textarea
                                          value={assignmentNotes}
                                          onChange={e => setAssignmentNotes(e.target.value)}
                                          placeholder="Enter details like accessories supplied, software licenses loaded, or setup checklist remarks..."
                                          rows="2"
                                        ></textarea>
                                      </div>

                                      <div className="signing-actions">
                                        <button 
                                          type="submit" 
                                          className="btn btn-success confirm-assign-btn"
                                          disabled={submitting}
                                        >
                                          {submitting ? 'Provisioning Asset...' : '✍️ Fulfill & Checkout Asset'}
                                        </button>
                                        <button 
                                          type="button" 
                                          className="btn btn-danger cancel-assign-btn"
                                          onClick={() => setAssigningRequestId(null)}
                                        >
                                          Cancel
                                        </button>
                                      </div>
                                    </form>
                                  </div>
                                </td>
                              </tr>
                            )}
                          </React.Fragment>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
}

export default AssetRequests;
