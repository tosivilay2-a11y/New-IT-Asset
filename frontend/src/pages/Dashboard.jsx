import React, { useState, useEffect } from 'react';
import { assetsAPI, inventoryAPI } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    totalAssets: 0,
    availableAssets: 0,
    lowStockItems: 0,
  });
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const assetsRes = await assetsAPI.getAll();
      const alertsRes = await inventoryAPI.getAlerts();
      
      const assets = assetsRes.data;
      setStats({
        totalAssets: assets.length,
        availableAssets: assets.filter(a => a.status === 'available').length,
        lowStockItems: alertsRes.data.length,
      });
      setAlerts(alertsRes.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    }
  };

  return (
    <div className="container">
      <h1>Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Assets</h3>
          <p className="stat-number">{stats.totalAssets}</p>
        </div>
        <div className="stat-card">
          <h3>Available Assets</h3>
          <p className="stat-number">{stats.availableAssets}</p>
        </div>
        <div className="stat-card alert-card">
          <h3>Low Stock Alerts</h3>
          <p className="stat-number">{stats.lowStockItems}</p>
        </div>
      </div>

      {alerts.length > 0 && (
        <div className="card">
          <h2>Low Stock Alerts</h2>
          <table>
            <thead>
              <tr>
                <th>Item</th>
                <th>SKU</th>
                <th>Current Stock</th>
                <th>Min Stock</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map(item => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>{item.sku}</td>
                  <td>{item.quantity}</td>
                  <td>{item.min_quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
