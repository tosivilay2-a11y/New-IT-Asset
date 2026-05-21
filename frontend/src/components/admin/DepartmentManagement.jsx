/**
 * Department Management Component
 * Country -> Province -> Company -> Cost Center cascade
 */
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './AdminManagement.css';

function DepartmentManagement() {
  const [departments, setDepartments] = useState([]);
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [costCenters, setCostCenters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingDept, setEditingDept] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const emptyForm = {
    departmentname: '',
    departmentcode: '',
    countryid: '',
    provinceid: '',
    companyid: '',
    costcenterid: '',
    description: '',
    isactive: true,
  };

  const [formData, setFormData] = useState(emptyForm);

  useEffect(() => { loadData(); }, []);

  // Cascading derived lists: Country -> Province -> Company -> CostCenter
  const filteredProvinces = formData.countryid
    ? provinces.filter(p => p.countryid === parseInt(formData.countryid))
    : [];

  const filteredCompanies = formData.provinceid
    ? companies.filter(c => c.provinceid === parseInt(formData.provinceid))
    : [];

  // Cost centers filtered by same company (and province/country if set)
  const filteredCostCenters = costCenters.filter(cc => {
    if (!formData.companyid) return false;
    if (cc.companyid && cc.companyid !== parseInt(formData.companyid)) return false;
    if (cc.provinceid && formData.provinceid && cc.provinceid !== parseInt(formData.provinceid)) return false;
    if (cc.countryid && formData.countryid && cc.countryid !== parseInt(formData.countryid)) return false;
    return true;
  });

  // Cascade handlers
  const handleCountryChange = (val) => {
    setFormData(prev => ({ ...prev, countryid: parseInt(val) || '', provinceid: '', companyid: '', costcenterid: '' }));
  };
  const handleProvinceChange = (val) => {
    setFormData(prev => ({ ...prev, provinceid: parseInt(val) || '', companyid: '', costcenterid: '' }));
  };
  const handleCompanyChange = (val) => {
    setFormData(prev => ({ ...prev, companyid: parseInt(val) || '', costcenterid: '' }));
  };

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [deptsRes, countriesRes, provincesRes, companiesRes, ccRes] = await Promise.all([
        api.get('/departments/'),
        api.get('/countries/'),
        api.get('/provinces/'),
        api.get('/companies/'),
        api.get('/cost-centers/'),
      ]);
      setDepartments(deptsRes.data || []);
      setCountries(countriesRes.data || []);
      setProvinces(provincesRes.data || []);
      setCompanies(companiesRes.data || []);
      setCostCenters(ccRes.data || []);
    } catch (err) {
      console.error('Error loading department data:', err);
      setError('Failed to load department configuration data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingDept(null);
    setFormData(emptyForm);
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (dept) => {
    setEditingDept(dept);
    setFormData({
      departmentname: dept.departmentname,
      departmentcode: dept.departmentcode,
      countryid: dept.countryid || '',
      provinceid: dept.provinceid || '',
      companyid: dept.companyid || '',
      costcenterid: dept.costcenterid || '',
      description: dept.description || '',
      isactive: dept.isactive,
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this department?')) return;
    try {
      await api.delete(`/departments/${id}`);
      setSuccess('Department deleted successfully!');
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to delete department.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.companyid) {
      setError('Company / Subsidiary is required.');
      return;
    }

    const payload = {
      departmentname: formData.departmentname,
      departmentcode: formData.departmentcode,
      companyid: parseInt(formData.companyid),
      countryid: formData.countryid ? parseInt(formData.countryid) : null,
      provinceid: formData.provinceid ? parseInt(formData.provinceid) : null,
      costcenterid: formData.costcenterid ? parseInt(formData.costcenterid) : null,
      description: formData.description || null,
      isactive: formData.isactive,
    };

    try {
      if (editingDept) {
        await api.put(`/departments/${editingDept.departmentid}`, payload);
        setSuccess('Department updated successfully!');
      } else {
        await api.post('/departments/', payload);
        setSuccess('Department created successfully!');
      }
      setShowModal(false);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save department.');
    }
  };

  // Helper lookups
  const getName = (list, idKey, nameKey, id) => {
    const item = list.find(x => x[idKey] === id);
    return item ? item[nameKey] : '-';
  };
  const getCompanyName = (id) => getName(companies, 'companyid', 'companyname', id);
  const getCountryName = (id) => {
    const c = countries.find(x => x.countryid === id);
    return c ? `${c.countryname} (${c.countrycode})` : '-';
  };
  const getProvinceName = (id) => {
    const p = provinces.find(x => x.provinceid === id);
    return p ? `${p.provincename} (${p.provincecode})` : '-';
  };
  const getCostCenterName = (id) => {
    const cc = costCenters.find(x => x.costcenterid === id);
    return cc ? cc.costcentercode : null;
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">📁 Department Management</h2>
          <p className="management-subtitle">
            Configure departments — link to Country, Province, Company and a Cost Center
          </p>
        </div>
        <button className="btn-add" onClick={handleAdd}>+ Add Department</button>
      </div>

      {success && <div className="success-message">{success}</div>}
      {error && !showModal && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading departments...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Department Name</th>
              <th>Code</th>
              <th>Cost Center</th>
              <th>Subsidiary</th>
              <th>Country</th>
              <th>Province</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {departments.length === 0 ? (
              <tr><td colSpan="9" className="no-data">No departments found</td></tr>
            ) : (
              departments.map(dept => (
                <tr key={dept.departmentid}>
                  <td>{dept.departmentid}</td>
                  <td><strong>{dept.departmentname}</strong></td>
                  <td><span className="code-badge">{dept.departmentcode}</span></td>
                  <td>
                    {dept.costcenterid ? (
                      <span style={{
                        display: 'inline-block',
                        padding: '2px 10px',
                        background: 'rgba(99,102,241,0.1)',
                        color: '#6366f1',
                        border: '1px solid rgba(99,102,241,0.2)',
                        borderRadius: '5px',
                        fontFamily: 'monospace',
                        fontWeight: 700,
                        fontSize: '12px',
                      }}>
                        {getCostCenterName(dept.costcenterid) || `CC#${dept.costcenterid}`}
                      </span>
                    ) : (
                      <span style={{ color: '#cbd5e1' }}>—</span>
                    )}
                  </td>
                  <td>{getCompanyName(dept.companyid)}</td>
                  <td>{getCountryName(dept.countryid)}</td>
                  <td>{getProvinceName(dept.provinceid)}</td>
                  <td>
                    <span className={`status-badge ${dept.isactive ? 'active' : 'inactive'}`}>
                      <span className="status-dot" />
                      {dept.isactive ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn-action edit" onClick={() => handleEdit(dept)}>✏️ Edit</button>
                      <button className="btn-action delete" onClick={() => handleDelete(dept.departmentid)}>🗑️ Delete</button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingDept ? 'Edit Department' : 'Add New Department'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}

                {/* Name + Code */}
                <div className="form-row">
                  <div className="form-group" style={{ flex: 2 }}>
                    <label>Department Name <span className="required">*</span></label>
                    <input
                      type="text"
                      value={formData.departmentname}
                      onChange={e => setFormData({ ...formData, departmentname: e.target.value })}
                      required
                      placeholder="e.g., Information Technology"
                    />
                  </div>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Code <span className="required">*</span></label>
                    <input
                      type="text"
                      value={formData.departmentcode}
                      onChange={e => setFormData({ ...formData, departmentcode: e.target.value.toUpperCase() })}
                      required
                      placeholder="e.g., IT"
                      style={{ textTransform: 'uppercase' }}
                    />
                  </div>
                </div>

                {/* Cascade hint */}
                <div style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  background: 'linear-gradient(90deg, #f0f4ff, #f5f3ff)',
                  border: '1px solid #e0e7ff', borderRadius: '8px',
                  padding: '10px 16px', marginBottom: '16px',
                  fontSize: '13px', fontWeight: 600, color: '#4338ca',
                }}>
                  <span>🌍 Location &amp; Organization</span>
                  <span style={{ fontSize: '11px', color: '#818cf8', fontWeight: 400 }}>
                    Select in order: Country → Province → Company → Cost Center
                  </span>
                </div>

                {/* Country */}
                <div className="form-group">
                  <label>Country Mapping <span className="required">*</span></label>
                  <select
                    value={formData.countryid}
                    onChange={e => handleCountryChange(e.target.value)}
                    required
                  >
                    <option value="">— Select Country —</option>
                    {countries.map(c => (
                      <option key={c.countryid} value={c.countryid}>
                        {c.countryname} ({c.countrycode})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Province */}
                <div className="form-group">
                  <label>Province Mapping <span className="required">*</span></label>
                  <select
                    value={formData.provinceid}
                    onChange={e => handleProvinceChange(e.target.value)}
                    disabled={!formData.countryid}
                    required
                  >
                    <option value="">
                      {!formData.countryid ? '— Select Country First —' : '— Select Province —'}
                    </option>
                    {filteredProvinces.map(p => (
                      <option key={p.provinceid} value={p.provinceid}>
                        {p.provincename} ({p.provincecode})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Company */}
                <div className="form-group">
                  <label>Subsidiary / Company <span className="required">*</span></label>
                  <select
                    value={formData.companyid}
                    onChange={e => handleCompanyChange(e.target.value)}
                    disabled={!formData.provinceid}
                    required
                  >
                    <option value="">
                      {!formData.provinceid ? '— Select Province First —' : '— Select Company —'}
                    </option>
                    {filteredCompanies.map(c => (
                      <option key={c.companyid} value={c.companyid}>
                        {c.companyname} ({c.companycode})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Cost Center */}
                <div className="form-group">
                  <label>
                    Cost Center
                    <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: 400, marginLeft: '6px' }}>(optional)</span>
                  </label>
                  <select
                    value={formData.costcenterid}
                    onChange={e => setFormData({ ...formData, costcenterid: parseInt(e.target.value) || '' })}
                    disabled={!formData.companyid}
                    style={!formData.companyid ? { background: '#f8f8fc', color: '#94a3b8', cursor: 'not-allowed' } : {}}
                  >
                    <option value="">
                      {!formData.companyid
                        ? '— Select Company First —'
                        : filteredCostCenters.length === 0
                          ? '— No cost centers for this company —'
                          : '— Select Cost Center —'}
                    </option>
                    {filteredCostCenters.map(cc => (
                      <option key={cc.costcenterid} value={cc.costcenterid}>
                        {cc.costcentercode} — {cc.costcentername}
                      </option>
                    ))}
                  </select>
                  {formData.companyid && filteredCostCenters.length === 0 && (
                    <p className="help-text" style={{ color: '#f59e0b' }}>
                      ⚠ No cost centers linked to this company yet. Create one in the 💰 Cost Centers tab first.
                    </p>
                  )}
                </div>

                {/* Description */}
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={formData.description}
                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Short department description..."
                    rows="2"
                  />
                </div>

                {/* Active */}
                <div className="form-group">
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={formData.isactive}
                      onChange={e => setFormData({ ...formData, isactive: e.target.checked })}
                      style={{ width: '16px', height: '16px', accentColor: '#3498db' }}
                    />
                    Active
                  </label>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">{editingDept ? 'Update' : 'Create'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default DepartmentManagement;
