/**
 * Company Management Component
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminManagement.css';

const API_BASE_URL = 'http://localhost:8000';

function CompanyManagement() {
  const [companies, setCompanies] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCompany, setEditingCompany] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [formData, setFormData] = useState({
    companyname: '',
    companycode: '',
    provinceid: '',
    address: '',
    phone: '',
    email: '',
    isactive: true
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [companiesRes, provincesRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/companies`),
        axios.get(`${API_BASE_URL}/provinces`)
      ]);
      setCompanies(companiesRes.data);
      setProvinces(provincesRes.data);
    } catch (err) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingCompany(null);
    setFormData({ companyname: '', companycode: '', provinceid: '', address: '', phone: '', email: '', isactive: true });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (company) => {
    setEditingCompany(company);
    setFormData({
      companyname: company.companyname,
      companycode: company.companycode,
      provinceid: company.provinceid || '',
      address: company.address || '',
      phone: company.phone || '',
      email: company.email || '',
      isactive: company.isactive
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure?')) return;
    try {
      await axios.delete(`${API_BASE_URL}/companies/${id}`);
      setSuccess('Company deleted');
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to delete');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCompany) {
        await axios.put(`${API_BASE_URL}/companies/${editingCompany.companyid}`, formData);
        setSuccess('Company updated');
      } else {
        await axios.post(`${API_BASE_URL}/companies`, formData);
        setSuccess('Company created');
      }
      setShowModal(false);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save');
    }
  };

  const getProvinceName = (provinceId) => {
    const province = provinces.find(p => p.provinceid === provinceId);
    return province ? `${province.provincename} (${province.provincecode})` : 'N/A';
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">🏢 Company Management</h2>
          <p className="management-subtitle">Manage companies for location hierarchy</p>
        </div>
        <button className="btn-add" onClick={handleAdd}>+ Add Company</button>
      </div>

      {success && <div className="success-message">{success}</div>}
      {error && !showModal && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Company Name</th>
              <th>Code</th>
              <th>Province</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {companies.length === 0 ? (
              <tr><td colSpan="6" className="no-data">No companies found</td></tr>
            ) : (
              companies.map(company => (
                <tr key={company.companyid}>
                  <td>{company.companyid}</td>
                  <td>{company.companyname}</td>
                  <td><span className="code-badge">{company.companycode}</span></td>
                  <td>{getProvinceName(company.provinceid)}</td>
                  <td>
                    <span className={`status-badge ${company.isactive ? 'active' : 'inactive'}`}>
                      <span className="status-dot"></span>
                      {company.isactive ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn-action edit" onClick={() => handleEdit(company)}>✏️ Edit</button>
                      <button className="btn-action delete" onClick={() => handleDelete(company.companyid)}>🗑️ Delete</button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingCompany ? 'Edit Company' : 'Add New Company'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}
                <div className="form-group">
                  <label>Company Name <span className="required">*</span></label>
                  <input type="text" value={formData.companyname} onChange={(e) => setFormData({ ...formData, companyname: e.target.value })} required placeholder="e.g., AVIS Rent A Car" />
                </div>
                <div className="form-group">
                  <label>Company Code (4 characters) <span className="required">*</span></label>
                  <input type="text" value={formData.companycode} onChange={(e) => setFormData({ ...formData, companycode: e.target.value.toUpperCase() })} required maxLength="4" placeholder="e.g., AVIS" style={{ textTransform: 'uppercase' }} />
                  <div className="help-text">4-letter company code</div>
                </div>
                <div className="form-group">
                  <label>Province</label>
                  <select value={formData.provinceid} onChange={(e) => setFormData({ ...formData, provinceid: parseInt(e.target.value) || '' })}>
                    <option value="">Select Province (Optional)</option>
                    {provinces.map(province => (
                      <option key={province.provinceid} value={province.provinceid}>{province.provincename} ({province.provincecode})</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Address</label>
                  <textarea value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} placeholder="Company address" />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Phone</label>
                    <input type="text" value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} placeholder="+856-21-123456" />
                  </div>
                  <div className="form-group">
                    <label>Email</label>
                    <input type="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} placeholder="info@company.com" />
                  </div>
                </div>
                <div className="form-group">
                  <label>
                    <input type="checkbox" checked={formData.isactive} onChange={(e) => setFormData({ ...formData, isactive: e.target.checked })} style={{ marginRight: '8px' }} />
                    Active
                  </label>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">{editingCompany ? 'Update' : 'Create'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default CompanyManagement;
