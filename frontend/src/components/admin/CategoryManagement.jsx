/**
 * Category Management Component
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminManagement.css';

const API_BASE_URL = 'http://localhost:8000';

function CategoryManagement() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [formData, setFormData] = useState({
    categoryname: '',
    categorycode: '',
    description: '',
    isactive: true
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/main-categories`);
      setCategories(response.data);
    } catch (err) {
      setError('Failed to load categories');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingCategory(null);
    setFormData({ categoryname: '', categorycode: '', description: '', isactive: true });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleEdit = (category) => {
    setEditingCategory(category);
    setFormData({
      categoryname: category.categoryname,
      categorycode: category.categorycode,
      description: category.description || '',
      isactive: category.isactive
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure?')) return;
    try {
      await axios.delete(`${API_BASE_URL}/main-categories/${id}`);
      setSuccess('Category deleted');
      loadCategories();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to delete');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCategory) {
        await axios.put(`${API_BASE_URL}/main-categories/${editingCategory.maincategoryid}`, formData);
        setSuccess('Category updated');
      } else {
        await axios.post(`${API_BASE_URL}/main-categories`, formData);
        setSuccess('Category created');
      }
      setShowModal(false);
      loadCategories();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save');
    }
  };

  return (
    <div className="admin-management">
      <div className="management-header">
        <div>
          <h2 className="management-title">📦 Category Management</h2>
          <p className="management-subtitle">Manage main asset categories</p>
        </div>
        <button className="btn-add" onClick={handleAdd}>+ Add Category</button>
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
              <th>Category Name</th>
              <th>Code</th>
              <th>Description</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {categories.length === 0 ? (
              <tr><td colSpan="6" className="no-data">No categories found</td></tr>
            ) : (
              categories.map(category => (
                <tr key={category.maincategoryid}>
                  <td>{category.maincategoryid}</td>
                  <td>{category.categoryname}</td>
                  <td><span className="code-badge">{category.categorycode}</span></td>
                  <td>{category.description || 'N/A'}</td>
                  <td>
                    <span className={`status-badge ${category.isactive ? 'active' : 'inactive'}`}>
                      <span className="status-dot"></span>
                      {category.isactive ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn-action edit" onClick={() => handleEdit(category)}>✏️ Edit</button>
                      <button className="btn-action delete" onClick={() => handleDelete(category.maincategoryid)}>🗑️ Delete</button>
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
              <h3>{editingCategory ? 'Edit Category' : 'Add New Category'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {error && <div className="error-message">{error}</div>}
                <div className="form-group">
                  <label>Category Name <span className="required">*</span></label>
                  <input type="text" value={formData.categoryname} onChange={(e) => setFormData({ ...formData, categoryname: e.target.value })} required placeholder="e.g., Monitor" />
                </div>
                <div className="form-group">
                  <label>Category Code (1 character) <span className="required">*</span></label>
                  <input type="text" value={formData.categorycode} onChange={(e) => setFormData({ ...formData, categorycode: e.target.value.toUpperCase() })} required maxLength="1" placeholder="e.g., M" style={{ textTransform: 'uppercase' }} />
                  <div className="help-text">Single letter code for asset ID</div>
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} placeholder="Category description" />
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
                <button type="submit" className="btn-primary">{editingCategory ? 'Update' : 'Create'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default CategoryManagement;
