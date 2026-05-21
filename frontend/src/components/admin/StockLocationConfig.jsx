/**
 * Stock Location Configuration
 * Allows admin to set the default stock location for checked-in assets
 */
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './StockLocationConfig.css';

function StockLocationConfig() {
  const [companies, setCompanies] = useState([]);
  const [locations, setLocations] = useState([]);
  const [stockLocations, setStockLocations] = useState([]);
  const [selectedStockLocation, setSelectedStockLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Create new stock location form
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newStockForm, setNewStockForm] = useState({
    stockname: '',
    locationid: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Fetch companies, physical locations, and stock locations in parallel
      const [compResponse, locResponse, stockResponse] = await Promise.all([
        api.get('/companies/'),
        api.get('/locations/'),
        api.get('/stock-locations/')
      ]);
      
      setCompanies(compResponse.data || []);
      setLocations(locResponse.data || []);
      setStockLocations(stockResponse.data || []);
      
      // Find the default stock location
      const defaultStock = (stockResponse.data || []).find(s => s.stockdefault);
      if (defaultStock) {
        setSelectedStockLocation(defaultStock.stockid);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setError('Failed to load stock location configuration data.');
      setLoading(false);
    }
  };

  const handleCreateStockLocation = async (e) => {
    e.preventDefault();
    
    if (!newStockForm.stockname.trim()) {
      setError('Please enter a stock location name');
      return;
    }
    
    if (!newStockForm.locationid) {
      setError('Please select a physical location');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Create new stock location
      await api.post('/stock-locations/', {
        stockname: newStockForm.stockname.trim(),
        locationid: parseInt(newStockForm.locationid)
      });
      
      setSuccess(`Stock location "${newStockForm.stockname}" created successfully!`);
      setNewStockForm({ stockname: '', locationid: '' });
      setShowCreateForm(false);
      
      // Reload stock locations
      await loadData();
      setLoading(false);
    } catch (error) {
      console.error('Error creating stock location:', error);
      setError(error.response?.data?.detail || 'Failed to create stock location');
      setLoading(false);
    }
  };

  const handleSetDefault = async (stockId) => {
    try {
      setLoading(true);
      setError('');
      
      // Call the set-default endpoint
      await api.post(`/stock-locations/set-default/${stockId}`);
      
      setSuccess('Stock location set as default successfully!');
      setTimeout(() => setSuccess(''), 3000);
      
      // Reload stock locations to update the UI
      await loadData();
      setLoading(false);
    } catch (error) {
      console.error('Error setting default stock location:', error);
      setError('Failed to set default stock location');
      setLoading(false);
    }
  };

  const handleSaveStockLocation = async () => {
    if (!selectedStockLocation) {
      setError('Please select a stock location');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Call the set-default endpoint
      await api.post(`/stock-locations/set-default/${selectedStockLocation}`);
      
      setSuccess('Stock location set as default successfully!');
      setTimeout(() => setSuccess(''), 3000);
      
      // Reload stock locations to update the UI
      await loadData();
      setLoading(false);
    } catch (error) {
      console.error('Error saving stock location:', error);
      setError('Failed to save stock location');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  const selectedStockLocationData = stockLocations.find(s => s.stockid === selectedStockLocation);
  const selectedPhysicalLoc = selectedStockLocationData 
    ? locations.find(l => l.id === selectedStockLocationData.locationid)
    : null;
  const selectedComp = selectedPhysicalLoc
    ? companies.find(c => c.companyid === selectedPhysicalLoc.companyid)
    : null;

  return (
    <div className="stock-location-config">
      <div className="config-card">
        <div className="card-header">
          <h3>📍 Stock Location Configuration</h3>
          <p className="card-subtitle">Set the default stock location where assets return after check-in</p>
        </div>

        <div className="card-body">
          {error && (
            <div className="alert alert-error">
              {error}
              <button onClick={() => setError('')} className="close-btn">✕</button>
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              {success}
              <button onClick={() => setSuccess('')} className="close-btn">✕</button>
            </div>
          )}

          <div className="form-group">
            <label>Select Stock Location *</label>
            <select
              value={selectedStockLocation || ''}
              onChange={(e) => setSelectedStockLocation(parseInt(e.target.value) || null)}
              className="form-control"
            >
              <option value="">-- Choose a stock location --</option>
              {stockLocations.map((stock) => {
                const physical = locations.find(l => l.id === stock.locationid);
                const labelSuffix = physical ? ` - ${physical.name}` : '';
                return (
                  <option key={stock.stockid} value={stock.stockid}>
                    {stock.stockname}{labelSuffix}
                  </option>
                );
              })}
            </select>
            <small>Select the stock location where assets will be returned after check-in</small>
          </div>

          {selectedStockLocationData && (
            <div className="info-box">
              <div className="info-item">
                <strong>Selected Stock Location:</strong>
                <span>{selectedStockLocationData.stockname}</span>
              </div>
              <div className="info-item">
                <strong>Stock ID:</strong>
                <span>{selectedStockLocationData.stockid}</span>
              </div>
              <div className="info-item">
                <strong>Physical Location:</strong>
                <span>{selectedPhysicalLoc ? selectedPhysicalLoc.name : `ID: ${selectedStockLocationData.locationid}`}</span>
              </div>
              {selectedComp && (
                <div className="info-item">
                  <strong>Company:</strong>
                  <span>{selectedComp.companyname}</span>
                </div>
              )}
            </div>
          )}

          <div className="button-group">
            <button
              onClick={handleSaveStockLocation}
              className="btn btn-primary"
              disabled={!selectedStockLocation || loading}
            >
              {loading ? 'Setting...' : '⭐ Set Default'}
            </button>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="btn btn-secondary"
              disabled={loading}
            >
              {showCreateForm ? '✕ Cancel' : '➕ Create New Stock Location'}
            </button>
            <button
              onClick={loadData}
              className="btn btn-secondary"
              disabled={loading}
            >
              🔄 Refresh
            </button>
          </div>
        </div>
      </div>

      {showCreateForm && (
        <div className="config-card">
          <div className="card-header">
            <h3>➕ Create New Stock Location</h3>
            <p className="card-subtitle">Add a new stock location to the system</p>
          </div>

          <div className="card-body">
            <form onSubmit={handleCreateStockLocation}>
              <div className="form-group">
                <label>Stock Location Name *</label>
                <input
                  type="text"
                  value={newStockForm.stockname}
                  onChange={(e) => setNewStockForm({...newStockForm, stockname: e.target.value})}
                  placeholder="e.g., Main Warehouse, Branch Office, etc."
                  className="form-control"
                  required
                />
                <small>Enter a descriptive name for this stock location</small>
              </div>

              <div className="form-group">
                <label>Physical Location *</label>
                <select
                  value={newStockForm.locationid}
                  onChange={(e) => setNewStockForm({...newStockForm, locationid: e.target.value})}
                  className="form-control"
                  required
                >
                  <option value="">-- Select a physical location --</option>
                  {locations.map((loc) => {
                    const company = companies.find(c => c.companyid === loc.companyid);
                    const label = company ? `${loc.name} (${company.companyname})` : loc.name;
                    return (
                      <option key={loc.id} value={loc.id}>
                        {label}
                      </option>
                    );
                  })}
                </select>
                <small>Select the physical location for this stock location</small>
              </div>

              <div className="button-group">
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="btn btn-secondary"
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Creating...' : '✅ Create Stock Location'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="info-card">
        <div className="card-header">
          <h4>ℹ️ How It Works</h4>
        </div>
        <div className="card-body">
          <ul className="info-list">
            <li>
              <strong>Check-Out:</strong> Asset is assigned to staff member, location unchanged
            </li>
            <li>
              <strong>Check-In:</strong> Asset location is automatically set to this stock location
            </li>
            <li>
              <strong>Status:</strong> Asset status is set based on condition (Good/Fair = Available, Damaged = Maintenance, Broken = Retired)
            </li>
            <li>
              <strong>Assignment:</strong> Asset is unassigned from staff member
            </li>
          </ul>
        </div>
      </div>

      <div className="info-card">
        <div className="card-header">
          <h4>📋 Available Stock Locations</h4>
        </div>
        <div className="card-body">
          {stockLocations.length === 0 ? (
            <p className="no-data">No stock locations available. Create one using the button above.</p>
          ) : (
            <div className="location-list">
              {stockLocations.map((stock) => {
                const location = locations.find(l => l.id === stock.locationid);
                const company = location ? companies.find(c => c.companyid === location.companyid) : null;
                return (
                  <div key={stock.stockid} className={`location-item ${stock.stockdefault ? 'default' : ''}`}>
                    <div className="location-header">
                      <div className="location-name">
                        {stock.stockname}
                        {stock.stockdefault && <span className="default-badge">⭐ DEFAULT</span>}
                      </div>
                      {!stock.stockdefault && (
                        <button
                          onClick={() => handleSetDefault(stock.stockid)}
                          className="btn btn-sm btn-set-default"
                          disabled={loading}
                          title="Set as default"
                        >
                          ✓ Stock Default
                        </button>
                      )}
                    </div>
                    <div className="location-id">
                      Stock ID: {stock.stockid} | Location: {location ? location.name : `Location #${stock.locationid}`}
                      {company && ` | Company: ${company.companyname}`}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default StockLocationConfig;
