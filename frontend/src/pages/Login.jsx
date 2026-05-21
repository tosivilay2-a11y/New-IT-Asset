import React, { useState } from 'react';
import { authAPI } from '../services/api';
import './Login.css';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      console.log('Attempting login for:', email);
      const response = await authAPI.login(email, password);
      console.log('Login response:', response.data);
      
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      
      const userResponse = await authAPI.getCurrentUser();
      console.log('User data:', userResponse.data);
      
      onLogin(token, userResponse.data);
    } catch (err) {
      console.error('Login error:', err);
      
      if (err.response) {
        // Server responded with error
        console.error('Error response:', err.response.data);
        setError(err.response.data.detail || 'Invalid email or password');
      } else if (err.request) {
        // Request made but no response
        console.error('No response from server');
        setError('Cannot connect to backend. Please wait a moment and try again — the server may still be starting up.');
      } else {
        // Something else happened
        console.error('Error:', err.message);
        setError('An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Asset Management System</h2>
        <form onSubmit={handleSubmit}>
          {error && <div className="alert alert-danger">{error}</div>}
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@example.com"
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="admin123"
              required
              disabled={loading}
            />
          </div>
          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div style={{marginTop: '20px', fontSize: '12px', color: '#666', textAlign: 'center'}}>
          <p>Default credentials:</p>
          <p>Admin: admin@example.com / admin123</p>
          <p>Staff: staff@example.com / staff123</p>
        </div>
      </div>
    </div>
  );
}

export default Login;
