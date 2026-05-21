import React, { useState, useRef } from 'react';
import api from '../../services/api';
import './DataImport.css';

const API_URL = 'http://localhost:8000';

function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

async function fetchFile(path, filename) {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Download failed (${res.status})`);
  }
  const blob = await res.blob();
  downloadBlob(blob, filename);
}

function ImportPanel({
  title,
  description,
  templatePath,
  templateFilename,
  exportPath,
  exportFilename,
  importPath,
}) {
  const fileRef = useRef(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleDownloadTemplate = async () => {
    setError('');
    try {
      setLoading(true);
      await fetchFile(templatePath, templateFilename);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    setError('');
    try {
      setLoading(true);
      await fetchFile(exportPath, exportFilename);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async () => {
    if (!file) {
      setError('Please select a file (.xlsx, .xls, or .csv)');
      return;
    }
    setError('');
    setResult(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const res = await api.post(importPath, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
      setFile(null);
      if (fileRef.current) fileRef.current.value = '';
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : err.message || 'Import failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="import-panel">
      <div className="import-panel-header">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>

      <div className="import-actions">
        <button
          type="button"
          className="btn btn-outline"
          onClick={handleDownloadTemplate}
          disabled={loading}
        >
          📄 Download Template
        </button>
        <button
          type="button"
          className="btn btn-outline"
          onClick={handleExport}
          disabled={loading}
        >
          📤 Export to Excel
        </button>
      </div>

      <div className="import-upload">
        <label className="file-label">
          <input
            ref={fileRef}
            type="file"
            accept=".xlsx,.xls,.csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <span className="file-picker">
            {file ? file.name : 'Choose Excel or CSV file…'}
          </span>
        </label>
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleImport}
          disabled={loading || !file}
        >
          {loading ? 'Processing…' : '📥 Import'}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {result && (
        <div className={`import-result ${result.error_count > 0 ? 'has-errors' : 'success'}`}>
          <p>
            <strong>{result.imported_count}</strong> record(s) imported
            {result.error_count > 0 && (
              <>, <strong>{result.error_count}</strong> error(s)</>
            )}
          </p>
          {result.errors?.length > 0 && (
            <ul className="import-errors">
              {result.errors.map((msg, i) => (
                <li key={i}>{msg}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}

function DataImport() {
  const [activeSection, setActiveSection] = useState('assets');

  const sections = [
    { id: 'assets', label: '1. Import Batch Asset File', icon: '💻' },
    { id: 'staff', label: '2. Import Staff Detail', icon: '👥' },
  ];

  return (
    <div className="data-import">
      <div className="data-import-intro">
        <h3>📊 Data Import & Export</h3>
        <p>
          Import assets or staff in bulk from Excel/CSV, or export current data to Excel.
          Download a template first, fill in your data, then upload.
        </p>
      </div>

      <div className="import-subnav">
        {sections.map((s) => (
          <button
            key={s.id}
            type="button"
            className={`import-subtab ${activeSection === s.id ? 'active' : ''}`}
            onClick={() => setActiveSection(s.id)}
          >
            <span>{s.icon}</span> {s.label}
          </button>
        ))}
      </div>

      {activeSection === 'assets' && (
        <ImportPanel
          title="Batch Asset Import"
          description="Import sheet columns match public.assets exactly (assetcode, maincategoryid, countryid, etc.). Use dropdowns or copy IDs from ref_* sheets. Required: assetcode, assetname, maincategoryid, countryid, provinceid, companyid, locationid, statusid. assetid is not imported."
          templatePath="/data-import/assets/template"
          templateFilename="asset_import_template.xlsx"
          exportPath="/data-import/assets/export"
          exportFilename={`assets_export_${new Date().toISOString().slice(0, 10)}.xlsx`}
          importPath="/data-import/assets/import"
        />
      )}

      {activeSection === 'staff' && (
        <ImportPanel
          title="Staff Detail Import"
          description="Import staff records from Excel or CSV. Required: Employee ID and Full Name. Company and Location can use names or codes from your system."
          templatePath="/data-import/staff/template"
          templateFilename="staff_import_template.xlsx"
          exportPath="/data-import/staff/export"
          exportFilename={`staff_export_${new Date().toISOString().slice(0, 10)}.xlsx`}
          importPath="/data-import/staff/import"
        />
      )}
    </div>
  );
}

export default DataImport;
