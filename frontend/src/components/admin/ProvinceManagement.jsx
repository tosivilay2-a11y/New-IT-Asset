/**
 * Province Management Component
 * CRUD operations for provinces
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminManagement.css';

const API_BASE_URL = 'http://localhost:8000';

function ProvinceManagement() {
  const [provinces, setProvinces] = useState([]);
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingProvince, setEditingProvince] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [formData, setFormData] = useState({
    provincename: '',
    provincecode: '',
    countryid: '',
    isactive: true
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [provincesRes, countriesRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/provinces`),
        axios.get(`${API_BASE_URL}/countries`)
      ]);
      setProvinces(provincesRes.data);
      setCountries(countriesRes.data);
    } catch (err) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingProvince(null);
    setFormData({ provincename: '', provincecode: '', countryid: '', isactive: true });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (province) => {
    setEditingProvince(province);
    setFormData({
      provincename: province.provincename,
      provincecode: province.provincecode,
      countryid: province.countryid,
      isactive: province.isactive
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this province?')) return;

    try {
      await axios.delete(`${API_BASE_URL}/provinces/${id}`);
      setSuccess('Province deleted successfully');
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to delete province');
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      if (editingProvince) {
        await axios.put(`${API_BASE_URL}/provinces/${editingProvince.provinceid}`, formData);
        setSuccess('Province updated successfully');
      } else {
        await axios.post(`${API_BASE_URL}/provinces`, formData);
        setSuccess('Province created successfully');
      }
      
      setShowModal(false);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save province');
      console.error(err);
    }
  };

  const getCountryName = (countryId) => {
    const country = countries.find(c => c.countryid === countryId);
    return country ? `${country.countryname} (${country.countrycode})` : 'Unknown';
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">🏛️ Province Management</h2>
          <p className="management-subtitle">Manage provinces/states for location hierarchy</p>
        </div>
        <button className="btn-add" onClick={handleAdd}>
          <span>+</span>
          <span>Add Province</span>
        </button>
      </div>

      {success && <div className="success-message">{success}</div>}
      {error && !showModal && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading provinces...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Province Name</th>
              <th>Code</th>
              <th>Country</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {provinces.length === 0 ? (
              <tr>
                <td colSpan="6" className="no-data">No provinces found</td>
              </tr>
            ) : (
              provinces.map(province => (
                <tr key={province.provinceid}>
                  <td>{province.provinceid}</td>
                  <td>{province.provincename}</td>
                  <td>
                    <span className="code-badge">{province.provincecode}</span>
                  </td>
                  <td>{getCountryName(province.countryid)}</td>
                  <td>
                    <span className={`status-badge ${province.isactive ? 'active' : 'inactive'}`}>
                      <span className="status-dot"></span>
                      {province.isactive ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn-action edit" onClick={() => handleEdit(province)}>
                        ✏️ Edit
                      </button>
                      <button className="btn-action delete" onClick={() => handleDelete(province.provinceid)}>
                        🗑️ Delete
                      </button>
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
              <h3>{editingProvince ? 'Edit Province' : 'Add New Province'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}

                <div className="form-group">
                  <label>Province Name <span className="required">*</span></label>
                  <input
                    type="text"
                    value={formData.provincename}
                    onChange={(e) => setFormData({ ...formData, provincename: e.target.value })}
                    required
                    placeholder="e.g., Vientiane Capital"
                  />
                </div>

                <div className="form-group">
                  <label>Province Code (3 characters) <span className="required">*</span></label>
                  <input
                    type="text"
                    value={formData.provincecode}
                    onChange={(e) => setFormData({ ...formData, provincecode: e.target.value.toUpperCase() })}
                    required
                    maxLength="3"
                    placeholder="e.g., VTE"
                    style={{ textTransform: 'uppercase' }}
                  />
                  <div className="help-text">3-letter province code</div>
                </div>

                <div className="form-group">
                  <label>Country <span className="required">*</span></label>
                  <select
                    value={formData.countryid}
                    onChange={(e) => setFormData({ ...formData, countryid: parseInt(e.target.value) })}
                    required
                  >
                    <option value="">Select Country</option>
                    {countries.map(country => (
                      <option key={country.countryid} value={country.countryid}>
                        {country.countryname} ({country.countrycode})
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={formData.isactive}
                      onChange={(e) => setFormData({ ...formData, isactive: e.target.checked })}
                      style={{ marginRight: '8px' }}
                    />
                    Active
                  </label>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  {editingProvince ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProvinceManagement;
