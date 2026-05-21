import React, { useState, useEffect } from 'react';
import { configAPI } from '../services/api';
import './StorageConfig.css';

function StorageConfig() {
  const [config, setConfig] = useState({
    storage_type: 'local',
    r2_account_id: '',
    r2_access_key_id: '',
    r2_secret_access_key: '',
    r2_bucket_name: '',
    r2_endpoint_url: '',
    r2_public_url: ''
  });

  const [liveStatus, setLiveStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    loadConfig();
    loadStatus();
  }, []);

  const loadConfig = async () => {
    try {
      setLoading(true);
      const response = await configAPI.getStorageConfig();
      setConfig(response.data);
    } catch (error) {
      showMessage('Failed to load configuration', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadStatus = async () => {
    try {
      const res = await configAPI.getStorageStatus();
      setLiveStatus(res.data);
    } catch {}
  };

  const showMessage = (text, type = 'info') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => { setMessage(''); setMessageType(''); }, 6000);
  };

  const handleChange = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setTestResult(null);
    try {
      await configAPI.updateStorageConfig(config);
      showMessage('Configuration saved and applied!', 'success');
      await loadStatus();
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Failed to save configuration', 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const response = await configAPI.testStorageConfig(config);
      setTestResult(response.data);
      if (response.data.success) {
        showMessage('Connection test successful!', 'success');
      } else {
        showMessage(`Test failed: ${response.data.message}`, 'error');
      }
    } catch (error) {
      setTestResult({ success: false, message: error.response?.data?.detail || 'Test failed' });
      showMessage('Connection test failed', 'error');
    } finally {
      setTesting(false);
    }
  };

  const generateEndpointUrl = () => {
    if (config.r2_account_id) {
      handleChange('r2_endpoint_url', `https://${config.r2_account_id}.r2.cloudflarestorage.com`);
    }
  };

  if (loading) return <div className="storage-config"><div className="loading">Loading configuration...</div></div>;

  return (
    <div className="storage-config">
      <div className="page-header">
        <h1>File Storage Configuration</h1>
        <p>Configure where uploaded PO attachments are stored</p>
      </div>

      {/* Live Status Banner */}
      {liveStatus && (
        <div className={`live-status-banner ${liveStatus.active_storage_type}`}>
          <span className="status-dot"></span>
          <strong>Active:</strong>&nbsp;
          {liveStatus.active_storage_type === 'r2'
            ? `Cloudflare R2 — bucket: ${liveStatus.bucket_name}`
            : 'Local Storage (server filesystem)'}
          <button className="btn-reload" onClick={loadStatus} title="Refresh status">↻</button>
        </div>
      )}

      {message && (
        <div className={`alert alert-${messageType}`}>{message}</div>
      )}

      <form onSubmit={handleSubmit} className="config-form">
        {/* Storage Type */}
        <div className="form-section">
          <h2>Storage Type</h2>
          <div className="storage-type-options">
            <label className="radio-option">
              <input type="radio" name="storage_type" value="local"
                checked={config.storage_type === 'local'}
                onChange={(e) => handleChange('storage_type', e.target.value)} />
              <div className="radio-content">
                <strong>Local Storage</strong>
                <p>Store files on the server's local filesystem</p>
                <div className="pros-cons">
                  <div className="pros">✓ Simple setup</div>
                  <div className="cons">✗ Limited scalability</div>
                </div>
              </div>
            </label>

            <label className="radio-option">
              <input type="radio" name="storage_type" value="r2"
                checked={config.storage_type === 'r2'}
                onChange={(e) => handleChange('storage_type', e.target.value)} />
              <div className="radio-content">
                <strong>Cloudflare R2</strong>
                <p>Store files in Cloudflare R2 object storage</p>
                <div className="pros-cons">
                  <div className="pros">✓ Scalable ✓ Fast ✓ Free egress</div>
                  <div className="cons">✗ Requires API token setup</div>
                </div>
              </div>
            </label>
          </div>
        </div>

        {/* R2 Config */}
        {config.storage_type === 'r2' && (
          <div className="form-section">
            <h2>Cloudflare R2 Configuration</h2>

            <div className="setup-guide">
              <h3>⚠️ API Token Requirements</h3>
              <ol>
                <li>Go to <a href="https://dash.cloudflare.com/r2/api-tokens" target="_blank" rel="noopener noreferrer">Cloudflare → R2 → Manage R2 API Tokens</a></li>
                <li>Click <strong>Create API Token</strong></li>
                <li>Set permission: <strong>Object Read &amp; Write</strong></li>
                <li>Scope to your bucket (or All buckets)</li>
                <li>Copy the new <strong>Access Key ID</strong> and <strong>Secret Access Key</strong></li>
              </ol>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Account ID <span className="required">*</span></label>
                <input type="text" value={config.r2_account_id}
                  onChange={(e) => handleChange('r2_account_id', e.target.value)}
                  placeholder="e.g. e100a0cfe124fdf7d88b279b7be79a95" required />
              </div>
              <div className="form-group">
                <label>Bucket Name <span className="required">*</span></label>
                <input type="text" value={config.r2_bucket_name}
                  onChange={(e) => handleChange('r2_bucket_name', e.target.value)}
                  placeholder="my-bucket" required />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Access Key ID <span className="required">*</span></label>
                <input type="text" value={config.r2_access_key_id}
                  onChange={(e) => handleChange('r2_access_key_id', e.target.value)}
                  placeholder="Paste Access Key ID" required />
              </div>
              <div className="form-group">
                <label>Secret Access Key <span className="required">*</span></label>
                <input type="password" value={config.r2_secret_access_key}
                  onChange={(e) => handleChange('r2_secret_access_key', e.target.value)}
                  placeholder={config.r2_secret_access_key === '***' ? 'Current key saved — paste new to update' : 'Paste Secret Access Key'} />
                <small>Only shown once in Cloudflare — paste it here</small>
              </div>
            </div>

            <div className="form-group">
              <label>Endpoint URL <span className="required">*</span></label>
              <div className="input-with-button">
                <input type="url" value={config.r2_endpoint_url}
                  onChange={(e) => handleChange('r2_endpoint_url', e.target.value)}
                  placeholder="https://your-account-id.r2.cloudflarestorage.com" required />
                <button type="button" onClick={generateEndpointUrl}
                  disabled={!config.r2_account_id} className="btn btn-secondary">
                  Auto-fill
                </button>
              </div>
            </div>

            <div className="form-group">
              <label>Public URL (Optional)</label>
              <input type="url" value={config.r2_public_url}
                onChange={(e) => handleChange('r2_public_url', e.target.value)}
                placeholder="https://pub-xxx.r2.dev" />
              <small>R2.dev subdomain or custom domain for public file access</small>
            </div>

            <div className="test-section">
              <button type="button" onClick={handleTest}
                disabled={testing || !config.r2_access_key_id || !config.r2_bucket_name}
                className="btn btn-outline test-btn">
                {testing ? 'Testing...' : '🔌 Test Connection'}
              </button>

              {testResult && (
                <div className={`test-result ${testResult.success ? 'success' : 'error'}`}>
                  <div className="test-status">
                    {testResult.success ? '✅' : '❌'} {testResult.message}
                  </div>
                  {testResult.details && (
                    <pre className="test-details">{JSON.stringify(testResult.details, null, 2)}</pre>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        <div className="form-actions">
          <button type="button" onClick={loadConfig} className="btn btn-secondary" disabled={saving}>Reset</button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save & Apply'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default StorageConfig;
