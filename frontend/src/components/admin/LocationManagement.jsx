/**
 * Location Management Component
 * Country -> Province -> Company -> Physical Location CRUD
 */
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './AdminManagement.css';

function LocationManagement() {
  const [locations, setLocations] = useState([]);
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingLoc, setEditingLoc] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const emptyForm = {
    name: '',
    address: '',
    countryid: '',
    provinceid: '',
    companyid: '',
  };

  const [formData, setFormData] = useState(emptyForm);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [locationsRes, countriesRes, provincesRes, companiesRes] = await Promise.all([
        api.get('/locations/'),
        api.get('/countries/'),
        api.get('/provinces/'),
        api.get('/companies/'),
      ]);
      setLocations(locationsRes.data || []);
      setCountries(countriesRes.data || []);
      setProvinces(provincesRes.data || []);
      setCompanies(companiesRes.data || []);
    } catch (err) {
      console.error('Error loading location data:', err);
      setError('Failed to load physical location configuration data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // Cascading lists
  const filteredProvinces = formData.countryid
    ? provinces.filter(p => p.countryid === parseInt(formData.countryid))
    : [];

  const filteredCompanies = formData.provinceid
    ? companies.filter(c => c.provinceid === parseInt(formData.provinceid))
    : [];

  const handleCountryChange = (val) => {
    setFormData(prev => ({ ...prev, countryid: parseInt(val) || '', provinceid: '', companyid: '' }));
  };

  const handleProvinceChange = (val) => {
    setFormData(prev => ({ ...prev, provinceid: parseInt(val) || '', companyid: '' }));
  };

  const handleCompanyChange = (val) => {
    setFormData(prev => ({ ...prev, companyid: parseInt(val) || '' }));
  };

  const handleAdd = () => {
    setEditingLoc(null);
    setFormData(emptyForm);
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (loc) => {
    setEditingLoc(loc);
    
    // Resolve Country & Province from Company ID
    let resolvedCountryId = '';
    let resolvedProvinceId = '';
    
    if (loc.companyid) {
      const company = companies.find(c => c.companyid === loc.companyid);
      if (company && company.provinceid) {
        resolvedProvinceId = company.provinceid;
        const province = provinces.find(p => p.provinceid === company.provinceid);
        if (province && province.countryid) {
          resolvedCountryId = province.countryid;
        }
      }
    }

    setFormData({
      name: loc.name,
      address: loc.address || '',
      countryid: resolvedCountryId,
      provinceid: resolvedProvinceId,
      companyid: loc.companyid || '',
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this physical location?')) return;
    try {
      await api.delete(`/locations/${id}`);
      setSuccess('Physical location deleted successfully!');
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('Delete error:', err);
      setError(err.response?.data?.detail || 'Failed to delete physical location.');
      setTimeout(() => setError(null), 5000);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.companyid) {
      setError('Company / Subsidiary is required.');
      return;
    }
    if (!formData.name.trim()) {
      setError('Location name is required.');
      return;
    }

    const payload = {
      name: formData.name.trim(),
      address: formData.address.trim() || null,
      companyid: parseInt(formData.companyid),
    };

    try {
      if (editingLoc) {
        await api.put(`/locations/${editingLoc.id}`, payload);
        setSuccess('Physical location updated successfully!');
      } else {
        await api.post('/locations/', payload);
        setSuccess('Physical location created successfully!');
      }
      setShowModal(false);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('Submit error:', err);
      setError(err.response?.data?.detail || 'Failed to save physical location.');
    }
  };

  // Helper lookups
  const getCompanyName = (companyId) => {
    const comp = companies.find(c => c.companyid === companyId);
    return comp ? comp.companyname : '-';
  };

  const getProvinceAndCountryName = (companyId) => {
    const comp = companies.find(c => c.companyid === companyId);
    if (!comp || !comp.provinceid) return '-';
    
    const prov = provinces.find(p => p.provinceid === comp.provinceid);
    if (!prov) return '-';
    
    const country = countries.find(c => c.countryid === prov.countryid);
    const countryStr = country ? `, ${country.countrycode}` : '';
    
    return `${prov.provincename}${countryStr}`;
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">📍 Location Management</h2>
          <p className="management-subtitle">
            Configure physical offices, branches, and warehouses under each Company
          </p>
        </div>
        <button className="btn-add" onClick={handleAdd}>+ Add Location</button>
      </div>

      {success && <div className="success-message">{success}</div>}
      {error && !showModal && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading physical locations...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Location Name</th>
              <th>Address</th>
              <th>Company</th>
              <th>Geography</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {locations.length === 0 ? (
              <tr><td colSpan="6" className="no-data">No physical locations found</td></tr>
            ) : (
              locations.map(loc => (
                <tr key={loc.id}>
                  <td>{loc.id}</td>
                  <td><strong>{loc.name}</strong></td>
                  <td>{loc.address || <span style={{ color: '#cbd5e1' }}>—</span>}</td>
                  <td>{getCompanyName(loc.companyid)}</td>
                  <td>{getProvinceAndCountryName(loc.companyid)}</td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn-action edit" onClick={() => handleEdit(loc)}>✏️ Edit</button>
                      <button className="btn-action delete" onClick={() => handleDelete(loc.id)}>🗑️ Delete</button>
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
              <h3>{editingLoc ? 'Edit Physical Location' : 'Add New Physical Location'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}

                {/* Name */}
                <div className="form-group">
                  <label>Physical Location Name <span className="required">*</span></label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                    required
                    placeholder="e.g., Vientiane Head Office, Luang Prabang Branch, Warehouse A"
                  />
                </div>

                {/* Cascade hint */}
                <div style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  background: 'linear-gradient(90deg, #f0f4ff, #f5f3ff)',
                  border: '1px solid #e0e7ff', borderRadius: '8px',
                  padding: '10px 16px', marginBottom: '16px',
                  fontSize: '13px', fontWeight: 600, color: '#4338ca',
                }}>
                  <span>🏢 Subsidiary Hierarchy</span>
                  <span style={{ fontSize: '11px', color: '#818cf8', fontWeight: 400 }}>
                    Select in order: Country → Province → Company
                  </span>
                </div>

                {/* Country */}
                <div className="form-group">
                  <label>Country <span className="required">*</span></label>
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
                  <label>Province <span className="required">*</span></label>
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

                {/* Address */}
                <div className="form-group">
                  <label>Address</label>
                  <textarea
                    value={formData.address}
                    onChange={e => setFormData({ ...formData, address: e.target.value })}
                    placeholder="Physical address of the location..."
                    rows="3"
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">{editingLoc ? 'Update' : 'Create'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default LocationManagement;
