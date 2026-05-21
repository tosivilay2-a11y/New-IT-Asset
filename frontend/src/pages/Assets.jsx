import React, { useState, useEffect } from 'react';
import { assetsAPI } from '../services/api';
import './Assets.css';

function Assets() {
  const [assets, setAssets] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    asset_id: '',
    name: '',
    value: '',
    status: 'available',
  });

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    try {
      const response = await assetsAPI.getAll();
      setAssets(response.data);
    } catch (error) {
      console.error('Error loading assets:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await assetsAPI.create(formData);
      setShowForm(false);
      setFormData({ asset_id: '', name: '', value: '', status: 'available' });
      loadAssets();
    } catch (error) {
      alert('Error creating asset');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this asset?')) {
      try {
        await assetsAPI.delete(id);
        loadAssets();
      } catch (error) {
        alert('Error deleting asset');
      }
    }
  };

  return (
    <div className="container">
      <div className="page-header">
        <h1>Assets</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
          {showForm ? 'Cancel' : 'Add Asset'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Add New Asset</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Asset ID</label>
              <input
                type="text"
                value={formData.asset_id}
                onChange={(e) => setFormData({...formData, asset_id: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Value</label>
              <input
                type="number"
                step="0.01"
                value={formData.value}
                onChange={(e) => setFormData({...formData, value: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({...formData, status: e.target.value})}
              >
                <option value="available">Available</option>
                <option value="in_use">In Use</option>
                <option value="maintenance">Maintenance</option>
                <option value="retired">Retired</option>
              </select>
            </div>
            <button type="submit" className="btn btn-success">Create Asset</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Asset List</h2>
        <table>
          <thead>
            <tr>
              <th>Asset ID</th>
              <th>Name</th>
              <th>Value</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {assets.map(asset => (
              <tr key={asset.id}>
                <td>{asset.asset_id}</td>
                <td>{asset.name}</td>
                <td>${asset.value || 0}</td>
                <td><span className={`status-badge status-${asset.status}`}>{asset.status}</span></td>
                <td>
                  <button onClick={() => handleDelete(asset.id)} className="btn btn-danger btn-sm">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Assets;
