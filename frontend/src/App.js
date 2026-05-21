import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import AssetsManagement from './pages/AssetsManagement';
import AssetsManagementEnhanced from './pages/AssetsManagementEnhanced';
import AssetDetailView from './pages/AssetDetailView';
import AssetFormNew from './pages/AssetFormNew';
import AssetCheckInOut from './pages/AssetCheckInOut';
import Inventory from './pages/Inventory';
import Audits from './pages/Audits';
import SystemConfig from './pages/SystemConfig';
import StorageConfig from './pages/StorageConfig';
import UserManagement from './pages/UserManagement';
import ChangePassword from './pages/ChangePassword';
import AssetRequests from './pages/AssetRequests';
import Navbar from './components/Navbar';
import { authAPI } from './services/api';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getCurrentUser()
        .then(res => {
          setUser(res.data);
          setLoading(false);
        })
        .catch((err) => {
          // If backend is down (network error), don't clear the token —
          // just stop loading so the user can retry via the login page message.
          // If it's a 401 (invalid/expired token), the interceptor already cleared it.
          if (!err.response) {
            // Network error — backend not reachable, token may still be valid
            console.warn('Backend not reachable on startup, clearing session.');
          }
          localStorage.removeItem('token');
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = async (token, userData) => {
    try {
      localStorage.setItem('token', token);
      // Fetch fresh user data to ensure we have the latest
      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
      setUser(userData); // Fallback to provided data
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        {user && <Navbar user={user} onLogout={handleLogout} />}
        <Routes>
          <Route path="/login" element={!user ? <Login onLogin={handleLogin} /> : <Navigate to="/" />} />
          <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/assets" element={user ? <AssetsManagementEnhanced /> : <Navigate to="/login" />} />
          <Route path="/assets/new" element={user ? <AssetFormNew /> : <Navigate to="/login" />} />
          <Route path="/assets/:id" element={user ? <AssetDetailView /> : <Navigate to="/login" />} />
          <Route path="/assets/:id/edit" element={user ? <AssetFormNew isEdit={true} /> : <Navigate to="/login" />} />
          <Route path="/assets/original" element={user ? <AssetsManagement /> : <Navigate to="/login" />} />
          <Route path="/assets/simple" element={user ? <Assets /> : <Navigate to="/login" />} />
          <Route path="/assets/checkinout" element={user ? <AssetCheckInOut /> : <Navigate to="/login" />} />
          <Route path="/inventory" element={user ? <Inventory /> : <Navigate to="/login" />} />
          <Route path="/audits" element={user ? <Audits /> : <Navigate to="/login" />} />
          <Route path="/admin/config" element={user ? <SystemConfig /> : <Navigate to="/login" />} />
          <Route path="/admin/storage" element={user ? <StorageConfig /> : <Navigate to="/login" />} />
          <Route path="/admin/users" element={user ? <UserManagement /> : <Navigate to="/login" />} />
          <Route path="/profile/change-password" element={user ? <ChangePassword /> : <Navigate to="/login" />} />
          <Route path="/assets/requests" element={user ? <AssetRequests user={user} /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
