import React, { useState, useEffect } from 'react';
import { inventoryAPI } from '../services/api';

function Inventory() {
  const [items, setItems] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showTransaction, setShowTransaction] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    quantity: 0,
    min_quantity: 10,
    unit_price: '',
  });
  const [transactionData, setTransactionData] = useState({
    inventory_item_id: '',
    transaction_type: 'stock_in',
    quantity: '',
    reference: '',
  });

  useEffect(() => {
    loadInventory();
  }, []);

  const loadInventory = async () => {
    try {
      const response = await inventoryAPI.getAll();
      setItems(response.data);
    } catch (error) {
      console.error('Error loading inventory:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await inventoryAPI.create(formData);
      setShowForm(false);
      setFormData({ name: '', sku: '', quantity: 0, min_quantity: 10, unit_price: '' });
      loadInventory();
    } catch (error) {
      alert('Error creating inventory item');
    }
  };

  const handleTransaction = async (e) => {
    e.preventDefault();
    try {
      await inventoryAPI.createTransaction(transactionData);
      setShowTransaction(false);
      setTransactionData({ inventory_item_id: '', transaction_type: 'stock_in', quantity: '', reference: '' });
      loadInventory();
    } catch (error) {
      alert('Error creating transaction');
    }
  };

  return (
    <div className="container">
      <div className="page-header">
        <h1>Inventory</h1>
        <div>
          <button onClick={() => setShowForm(!showForm)} className="btn btn-primary" style={{marginRight: '10px'}}>
            {showForm ? 'Cancel' : 'Add Item'}
          </button>
          <button onClick={() => setShowTransaction(!showTransaction)} className="btn btn-success">
            Record Transaction
          </button>
        </div>
      </div>

      {showForm && (
        <div className="card">
          <h2>Add Inventory Item</h2>
          <form onSubmit={handleSubmit}>
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
              <label>SKU</label>
              <input
                type="text"
                value={formData.sku}
                onChange={(e) => setFormData({...formData, sku: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Initial Quantity</label>
              <input
                type="number"
                value={formData.quantity}
                onChange={(e) => setFormData({...formData, quantity: parseInt(e.target.value)})}
              />
            </div>
            <div className="form-group">
              <label>Minimum Quantity</label>
              <input
                type="number"
                value={formData.min_quantity}
                onChange={(e) => setFormData({...formData, min_quantity: parseInt(e.target.value)})}
              />
            </div>
            <button type="submit" className="btn btn-success">Create Item</button>
          </form>
        </div>
      )}

      {showTransaction && (
        <div className="card">
          <h2>Record Transaction</h2>
          <form onSubmit={handleTransaction}>
            <div className="form-group">
              <label>Item</label>
              <select
                value={transactionData.inventory_item_id}
                onChange={(e) => setTransactionData({...transactionData, inventory_item_id: e.target.value})}
                required
              >
                <option value="">Select Item</option>
                {items.map(item => (
                  <option key={item.id} value={item.id}>{item.name} ({item.sku})</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Type</label>
              <select
                value={transactionData.transaction_type}
                onChange={(e) => setTransactionData({...transactionData, transaction_type: e.target.value})}
              >
                <option value="stock_in">Stock In</option>
                <option value="stock_out">Stock Out</option>
              </select>
            </div>
            <div className="form-group">
              <label>Quantity</label>
              <input
                type="number"
                value={transactionData.quantity}
                onChange={(e) => setTransactionData({...transactionData, quantity: parseInt(e.target.value)})}
                required
              />
            </div>
            <button type="submit" className="btn btn-success">Record Transaction</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Inventory Items</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>SKU</th>
              <th>Quantity</th>
              <th>Min Quantity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.sku}</td>
                <td>{item.quantity}</td>
                <td>{item.min_quantity}</td>
                <td>
                  {item.quantity <= item.min_quantity ? (
                    <span className="status-badge status-maintenance">Low Stock</span>
                  ) : (
                    <span className="status-badge status-available">OK</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Inventory;
