/**
 * Country Management Component
 * CRUD operations for countries
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminManagement.css';

const API_BASE_URL = 'http://localhost:8000';

function CountryManagement() {
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCountry, setEditingCountry] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [formData, setFormData] = useState({
    countryname: '',
    countrycode: '',
    isactive: true
  });

  useEffect(() => {
    loadCountries();
  }, []);

  const loadCountries = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/countries`);
      setCountries(response.data);
    } catch (err) {
      setError('Failed to load countries');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingCountry(null);
    setFormData({ countryname: '', countrycode: '', isactive: true });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (country) => {
    setEditingCountry(country);
    setFormData({
      countryname: country.countryname,
      countrycode: country.countrycode,
      isactive: country.isactive
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this country?')) return;

    try {
      await axios.delete(`${API_BASE_URL}/countries/${id}`);
      setSuccess('Country deleted successfully');
      loadCountries();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to delete country');
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      if (editingCountry) {
        await axios.put(`${API_BASE_URL}/countries/${editingCountry.countryid}`, formData);
        setSuccess('Country updated successfully');
      } else {
        await axios.post(`${API_BASE_URL}/countries`, formData);
        setSuccess('Country created successfully');
      }
      
      setShowModal(false);
      loadCountries();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save country');
      console.error(err);
    }
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">🌍 Country Management</h2>
          <p className="management-subtitle">Manage countries for location hierarchy</p>
        </div>
        <button className="btn-add" onClick={handleAdd}>
          <span>+</span>
          <span>Add Country</span>
        </button>
      </div>

      {success && <div className="success-message">{success}</div>}
      {error && !showModal && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading countries...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Country Name</th>
              <th>Code</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {countries.length === 0 ? (
              <tr>
                <td colSpan="6" className="no-data">No countries found</td>
              </tr>
            ) : (
              countries.map(country => (
                <tr key={country.countryid}>
                  <td>{country.countryid}</td>
                  <td>{country.countryname}</td>
                  <td>
                    <span className="code-badge">{country.countrycode}</span>
                  </td>
                  <td>
                    <span className={`status-badge ${country.isactive ? 'active' : 'inactive'}`}>
                      <span className="status-dot"></span>
                      {country.isactive ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>{new Date(country.createdat).toLocaleDateString()}</td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn-action edit" onClick={() => handleEdit(country)}>
                        ✏️ Edit
                      </button>
                      <button className="btn-action delete" onClick={() => handleDelete(country.countryid)}>
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
              <h3>{editingCountry ? 'Edit Country' : 'Add New Country'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}

                <div className="form-group">
                  <label>Country Name <span className="required">*</span></label>
                  <input
                    type="text"
                    value={formData.countryname}
                    onChange={(e) => setFormData({ ...formData, countryname: e.target.value })}
                    required
                    placeholder="e.g., Lao PDR"
                  />
                </div>

                <div className="form-group">
                  <label>Country Code (2 characters) <span className="required">*</span></label>
                  <input
                    type="text"
                    value={formData.countrycode}
                    onChange={(e) => setFormData({ ...formData, countrycode: e.target.value.toUpperCase() })}
                    required
                    maxLength="2"
                    placeholder="e.g., LA"
                    style={{ textTransform: 'uppercase' }}
                  />
                  <div className="help-text">2-letter ISO country code</div>
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
                  {editingCountry ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default CountryManagement;
