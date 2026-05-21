/**
 * Cost Center Management Component
 * Country -> Province -> Company cascade only (no department)
 */
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './AdminManagement.css';
import './CostCenterManagement.css';

function CostCenterManagement() {
  const [costCenters, setCostCenters] = useState([]);
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCC, setEditingCC] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const emptyForm = {
    costcentername: '',
    costcentercode: '',
    countryid: '',
    provinceid: '',
    companyid: '',
    description: '',
    isactive: true,
  };

  const [formData, setFormData] = useState(emptyForm);

  useEffect(() => { loadData(); }, []);

  // Cascading derived lists: Country -> Province -> Company
  const filteredProvinces = formData.countryid
    ? provinces.filter(p => p.countryid === parseInt(formData.countryid))
    : [];

  const filteredCompanies = formData.provinceid
    ? companies.filter(c => c.provinceid === parseInt(formData.provinceid))
    : [];

  // Sequential cascade handlers
  const handleCountryChange = (val) => {
    setFormData(prev => ({ ...prev, countryid: parseInt(val) || '', provinceid: '', companyid: '' }));
  };
  const handleProvinceChange = (val) => {
    setFormData(prev => ({ ...prev, provinceid: parseInt(val) || '', companyid: '' }));
  };
  const handleCompanyChange = (val) => {
    setFormData(prev => ({ ...prev, companyid: parseInt(val) || '' }));
  };

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [ccRes, countriesRes, provincesRes, companiesRes] = await Promise.all([
        api.get('/cost-centers/'),
        api.get('/countries/'),
        api.get('/provinces/'),
        api.get('/companies/'),
      ]);
      setCostCenters(ccRes.data || []);
      setCountries(countriesRes.data || []);
      setProvinces(provincesRes.data || []);
      setCompanies(companiesRes.data || []);
    } catch (err) {
      console.error('Error loading cost center data:', err);
      setError('Failed to load data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingCC(null);
    setFormData(emptyForm);
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (cc) => {
    setEditingCC(cc);
    setFormData({
      costcentername: cc.costcentername,
      costcentercode: cc.costcentercode,
      countryid: cc.countryid || '',
      provinceid: cc.provinceid || '',
      companyid: cc.companyid || '',
      description: cc.description || '',
      isactive: cc.isactive,
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this cost center?')) return;
    try {
      await api.delete(`/cost-centers/${id}`);
      setSuccess('Cost center deleted successfully!');
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to delete cost center.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.costcentercode || !formData.costcentername) {
      setError('Cost Center Name and Code are required.');
      return;
    }
    if (!formData.countryid) {
      setError('Country is required.');
      return;
    }

    const payload = {
      costcentername: formData.costcentername,
      costcentercode: formData.costcentercode.toUpperCase(),
      countryid: parseInt(formData.countryid),
      provinceid: formData.provinceid ? parseInt(formData.provinceid) : null,
      companyid: formData.companyid ? parseInt(formData.companyid) : null,
      description: formData.description || null,
      isactive: formData.isactive,
    };

    try {
      if (editingCC) {
        await api.put(`/cost-centers/${editingCC.costcenterid}`, payload);
        setSuccess('Cost center updated successfully!');
      } else {
        await api.post('/cost-centers/', payload);
        setSuccess('Cost center created successfully!');
      }
      setShowModal(false);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save cost center.');
    }
  };

  const getName = (list, idKey, nameKey, id) => {
    const item = list.find(x => x[idKey] === id);
    return item ? item[nameKey] : '-';
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">💰 Cost Center Management</h2>
          <p className="management-subtitle">
            Manage budget cost centers linked to Country → Province → Company
          </p>
        </div>
        <button className="btn-add cc-btn-add" onClick={handleAdd}>+ Add Cost Center</button>
      </div>

      {success && <div className="success-message">{success}</div>}
      {error && !showModal && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading cc-loading">
          <span className="cc-spinner" />
          Loading cost centers...
        </div>
      ) : (
        <div className="cc-table-wrapper">
          <table className="data-table cc-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Code</th>
                <th>Cost Center Name</th>
                <th>Country</th>
                <th>Province</th>
                <th>Company</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {costCenters.length === 0 ? (
                <tr><td colSpan="8" className="no-data">No cost centers found. Click "+ Add Cost Center" to create one.</td></tr>
              ) : (
                costCenters.map(cc => (
                  <tr key={cc.costcenterid}>
                    <td className="cc-id">{cc.costcenterid}</td>
                    <td><span className="cc-code-badge">{cc.costcentercode}</span></td>
                    <td><strong>{cc.costcentername}</strong></td>
                    <td className="cc-location-cell">{getName(countries, 'countryid', 'countryname', cc.countryid)}</td>
                    <td className="cc-location-cell">{getName(provinces, 'provinceid', 'provincename', cc.provinceid)}</td>
                    <td className="cc-location-cell">{getName(companies, 'companyid', 'companyname', cc.companyid)}</td>
                    <td>
                      <span className={`status-badge ${cc.isactive ? 'active' : 'inactive'}`}>
                        <span className="status-dot" />
                        {cc.isactive ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button className="btn-action edit" onClick={() => handleEdit(cc)}>✏️ Edit</button>
                        <button className="btn-action delete" onClick={() => handleDelete(cc.costcenterid)}>🗑️ Delete</button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content cc-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header cc-modal-header">
              <div className="cc-modal-title-wrap">
                <span className="cc-modal-icon">💰</span>
                <h3>{editingCC ? 'Edit Cost Center' : 'Add New Cost Center'}</h3>
              </div>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}

                {/* Name + Code */}
                <div className="form-row">
                  <div className="form-group" style={{ flex: 2 }}>
                    <label>Cost Center Name <span className="required">*</span></label>
                    <input
                      type="text"
                      value={formData.costcentername}
                      onChange={e => setFormData({ ...formData, costcentername: e.target.value })}
                      required
                      placeholder="e.g., IT Operations Budget"
                    />
                  </div>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Code <span className="required">*</span></label>
                    <input
                      type="text"
                      value={formData.costcentercode}
                      onChange={e => setFormData({ ...formData, costcentercode: e.target.value.toUpperCase() })}
                      required
                      placeholder="e.g., CC-IT-001"
                      style={{ textTransform: 'uppercase' }}
                    />
                  </div>
                </div>

                {/* Cascade header */}
                <div className="cc-cascade-header">
                  <span>🌍 Geographic &amp; Organizational Mapping</span>
                  <span className="cc-cascade-hint">Select in order: Country → Province → Company</span>
                </div>

                {/* Country */}
                <div className="form-group">
                  <label>Country <span className="required">*</span></label>
                  <select
                    value={formData.countryid}
                    onChange={e => handleCountryChange(e.target.value)}
                    required
                    className="cc-select"
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
                  <label>Province / Region <span className="cc-optional-label">(optional)</span></label>
                  <select
                    value={formData.provinceid}
                    onChange={e => handleProvinceChange(e.target.value)}
                    disabled={!formData.countryid}
                    className={`cc-select ${!formData.countryid ? 'cc-select-disabled' : ''}`}
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
                  <label>Company / Subsidiary <span className="cc-optional-label">(optional)</span></label>
                  <select
                    value={formData.companyid}
                    onChange={e => handleCompanyChange(e.target.value)}
                    disabled={!formData.provinceid}
                    className={`cc-select ${!formData.provinceid ? 'cc-select-disabled' : ''}`}
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

                {/* Description */}
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={formData.description}
                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Brief description of this cost center's purpose..."
                    rows="2"
                  />
                </div>

                {/* Active */}
                <div className="form-group">
                  <label className="cc-checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.isactive}
                      onChange={e => setFormData({ ...formData, isactive: e.target.checked })}
                    />
                    <span>Active</span>
                  </label>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary cc-btn-save">
                  {editingCC ? '💾 Update' : '✅ Create Cost Center'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default CostCenterManagement;
