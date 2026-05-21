import React, { useState, useEffect } from 'react';
import { auditsAPI, inventoryAPI } from '../services/api';

function Audits() {
  const [audits, setAudits] = useState([]);
  const [items, setItems] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [selectedAudit, setSelectedAudit] = useState(null);
  const [auditName, setAuditName] = useState('');
  const [recordData, setRecordData] = useState({
    inventory_item_id: '',
    expected_quantity: '',
    actual_quantity: '',
    notes: '',
  });

  useEffect(() => {
    loadAudits();
    loadInventory();
  }, []);

  const loadAudits = async () => {
    try {
      const response = await auditsAPI.getAll();
      setAudits(response.data);
    } catch (error) {
      console.error('Error loading audits:', error);
    }
  };

  const loadInventory = async () => {
    try {
      const response = await inventoryAPI.getAll();
      setItems(response.data);
    } catch (error) {
      console.error('Error loading inventory:', error);
    }
  };

  const handleCreateAudit = async (e) => {
    e.preventDefault();
    try {
      await auditsAPI.create({ name: auditName });
      setShowForm(false);
      setAuditName('');
      loadAudits();
    } catch (error) {
      alert('Error creating audit');
    }
  };

  const handleAddRecord = async (e) => {
    e.preventDefault();
    try {
      await auditsAPI.addRecord(selectedAudit, recordData);
      setRecordData({ inventory_item_id: '', expected_quantity: '', actual_quantity: '', notes: '' });
      alert('Record added successfully');
    } catch (error) {
      alert('Error adding record');
    }
  };

  const handleCompleteAudit = async (auditId) => {
    try {
      await auditsAPI.complete(auditId);
      loadAudits();
      alert('Audit completed');
    } catch (error) {
      alert('Error completing audit');
    }
  };

  return (
    <div className="container">
      <div className="page-header">
        <h1>Audits</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
          {showForm ? 'Cancel' : 'New Audit'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Create Audit Session</h2>
          <form onSubmit={handleCreateAudit}>
            <div className="form-group">
              <label>Audit Name</label>
              <input
                type="text"
                value={auditName}
                onChange={(e) => setAuditName(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-success">Create Audit</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Audit Sessions</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {audits.map(audit => (
              <tr key={audit.id}>
                <td>{audit.name}</td>
                <td><span className={`status-badge status-${audit.status === 'completed' ? 'available' : 'in_use'}`}>
                  {audit.status}
                </span></td>
                <td>{new Date(audit.created_at).toLocaleDateString()}</td>
                <td>
                  {audit.status === 'in_progress' && (
                    <>
                      <button
                        onClick={() => setSelectedAudit(audit.id)}
                        className="btn btn-primary btn-sm"
                        style={{marginRight: '5px'}}
                      >
                        Add Records
                      </button>
                      <button
                        onClick={() => handleCompleteAudit(audit.id)}
                        className="btn btn-success btn-sm"
                      >
                        Complete
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedAudit && (
        <div className="card">
          <h2>Add Audit Record</h2>
          <form onSubmit={handleAddRecord}>
            <div className="form-group">
              <label>Item</label>
              <select
                value={recordData.inventory_item_id}
                onChange={(e) => setRecordData({...recordData, inventory_item_id: e.target.value})}
                required
              >
                <option value="">Select Item</option>
                {items.map(item => (
                  <option key={item.id} value={item.id}>{item.name} (Current: {item.quantity})</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Expected Quantity</label>
              <input
                type="number"
                value={recordData.expected_quantity}
                onChange={(e) => setRecordData({...recordData, expected_quantity: parseInt(e.target.value)})}
                required
              />
            </div>
            <div className="form-group">
              <label>Actual Quantity</label>
              <input
                type="number"
                value={recordData.actual_quantity}
                onChange={(e) => setRecordData({...recordData, actual_quantity: parseInt(e.target.value)})}
                required
              />
            </div>
            <div className="form-group">
              <label>Notes</label>
              <input
                type="text"
                value={recordData.notes}
                onChange={(e) => setRecordData({...recordData, notes: e.target.value})}
              />
            </div>
            <button type="submit" className="btn btn-success">Add Record</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default Audits;
