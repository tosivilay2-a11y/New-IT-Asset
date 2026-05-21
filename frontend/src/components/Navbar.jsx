import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar({ user, onLogout }) {
  const [showUserMenu, setShowUserMenu] = useState(false);

  const getUserName = () => {
    if (user.firstname && user.lastname) {
      return `${user.firstname} ${user.lastname}`;
    }
    return user.email || 'User';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">Asset Management</Link>
        <div className="navbar-links">
          <Link to="/">Dashboard</Link>
          <Link to="/assets">Assets</Link>
          <Link to="/assets/checkinout">📦 Check In/Out</Link>
          <Link to="/inventory">Inventory</Link>
          <Link to="/audits">Audits</Link>
          <Link to="/admin/config">⚙️ Admin</Link>
        </div>
        <div className="navbar-user">
          <div className="user-menu-container">
            <button 
              className="user-profile-btn"
              onClick={() => setShowUserMenu(!showUserMenu)}
              title={`${getUserName()} (${user.role})`}
            >
              <span className="user-avatar">{getUserName().charAt(0).toUpperCase()}</span>
              <span className="user-name">{getUserName()}</span>
              <span className="dropdown-arrow">▼</span>
            </button>
            
            {showUserMenu && (
              <div className="user-dropdown-menu">
                <div className="user-info">
                  <div className="user-name-full">{getUserName()}</div>
                  <div className="user-email">{user.email}</div>
                  <div className="user-role">{user.role}</div>
                </div>
                <hr />
                <Link 
                  to="/admin/users" 
                  className="dropdown-item"
                  onClick={() => setShowUserMenu(false)}
                >
                  👥 Manage Users
                </Link>
                <Link 
                  to="/profile/change-password" 
                  className="dropdown-item"
                  onClick={() => setShowUserMenu(false)}
                >
                  🔐 Change Password
                </Link>
                <hr />
                <button 
                  onClick={() => {
                    setShowUserMenu(false);
                    onLogout();
                  }} 
                  className="dropdown-item logout-btn"
                >
                  🚪 Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
