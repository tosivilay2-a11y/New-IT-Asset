/**
 * Asset ID Generator Component
 * Interactive tool to understand asset ID format
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AssetIDGenerator.css';

const API_BASE_URL = 'http://localhost:8000';

function AssetIDGenerator() {
  const [categories, setCategories] = useState([]);
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [companies, setCompanies] = useState([]);
  
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedProvince, setSelectedProvince] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  
  const [previewData, setPreviewData] = useState(null);

  useEffect(() => {
    loadCategories();
    loadCountries();
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      loadProvinces(selectedCountry);
    }
  }, [selectedCountry]);

  useEffect(() => {
    if (selectedProvince) {
      loadCompanies(selectedProvince);
    }
  }, [selectedProvince]);

  useEffect(() => {
    if (selectedCategory && selectedCountry && selectedProvince && selectedCompany) {
      fetchPreview();
    }
  }, [selectedCategory, selectedCountry, selectedProvince, selectedCompany]);

  const loadCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/main-categories`);
      setCategories(response.data);
    } catch (err) {
      console.error('Failed to load categories', err);
    }
  };

  const loadCountries = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/countries`);
      setCountries(response.data);
    } catch (err) {
      console.error('Failed to load countries', err);
    }
  };

  const loadProvinces = async (countryId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/provinces?country_id=${countryId}`);
      setProvinces(response.data);
    } catch (err) {
      console.error('Failed to load provinces', err);
    }
  };

  const loadCompanies = async (provinceId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/companies?province_id=${provinceId}`);
      setCompanies(response.data);
    } catch (err) {
      console.error('Failed to load companies', err);
    }
  };

  const fetchPreview = async () => {
    try {
      const category = categories.find(c => c.maincategoryid === parseInt(selectedCategory));
      const response = await axios.post(`${API_BASE_URL}/asset-utils/preview-asset-id`, {
        main_category: category.categoryname,
        country_id: parseInt(selectedCountry),
        province_id: parseInt(selectedProvince),
        company_id: parseInt(selectedCompany)
      });
      setPreviewData(response.data);
    } catch (err) {
      console.error('Failed to fetch preview', err);
    }
  };

  return (
    <div className="asset-id-generator">
      <div className="generator-header">
        <h2>🔢 Asset ID Generator</h2>
        <p>Interactive tool to understand and preview asset ID format</p>
      </div>

      <div className="format-info">
        <h3>Asset ID Format</h3>
        <div className="format-pattern">
          <div className="pattern-part">
            <div className="part-label">Category</div>
            <div className="part-value">1 char</div>
          </div>
          <div className="pattern-separator">+</div>
          <div className="pattern-part">
            <div className="part-label">Country</div>
            <div className="part-value">2 chars</div>
          </div>
          <div className="pattern-separator">+</div>
          <div className="pattern-part">
            <div className="part-label">Province</div>
            <div className="part-value">3 chars</div>
          </div>
          <div className="pattern-separator">+</div>
          <div className="pattern-part">
            <div className="part-label">Company</div>
            <div className="part-value">4 chars</div>
          </div>
          <div className="pattern-separator">+</div>
          <div className="pattern-part">
            <div className="part-label">Year</div>
            <div className="part-value">2 chars</div>
          </div>
          <div className="pattern-separator">+</div>
          <div className="pattern-part">
            <div className="part-label">Sequence</div>
            <div className="part-value">3 chars</div>
          </div>
        </div>
        <div className="format-example">
          <strong>Example:</strong> MLALPBAVIS25015 = Monitor, Lao, Luang Prabang, AVIS, 2025, #015
        </div>
      </div>

      <div className="generator-form">
        <h3>Generate Preview</h3>
        <div className="form-grid">
          <div className="form-field">
            <label>Category</label>
            <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
              <option value="">Select Category</option>
              {categories.map(cat => (
                <option key={cat.maincategoryid} value={cat.maincategoryid}>
                  [{cat.categorycode}] {cat.categoryname}
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label>Country</label>
            <select value={selectedCountry} onChange={(e) => setSelectedCountry(e.target.value)}>
              <option value="">Select Country</option>
              {countries.map(country => (
                <option key={country.countryid} value={country.countryid}>
                  {country.countryname} ({country.countrycode})
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label>Province</label>
            <select value={selectedProvince} onChange={(e) => setSelectedProvince(e.target.value)} disabled={!selectedCountry}>
              <option value="">Select Province</option>
              {provinces.map(province => (
                <option key={province.provinceid} value={province.provinceid}>
                  {province.provincename} ({province.provincecode})
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label>Company</label>
            <select value={selectedCompany} onChange={(e) => setSelectedCompany(e.target.value)} disabled={!selectedProvince}>
              <option value="">Select Company</option>
              {companies.map(company => (
                <option key={company.companyid} value={company.companyid}>
                  {company.companyname} ({company.companycode})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {previewData && (
        <div className="preview-result">
          <h3>Generated Asset ID</h3>
          <div className="preview-id">{previewData.asset_id}</div>
          <div className="preview-breakdown">
            <div className="breakdown-item">
              <div className="breakdown-label">Category</div>
              <div className="breakdown-code">{previewData.components.category_code}</div>
            </div>
            <div className="breakdown-item">
              <div className="breakdown-label">Country</div>
              <div className="breakdown-code">{previewData.components.country_code}</div>
            </div>
            <div className="breakdown-item">
              <div className="breakdown-label">Province</div>
              <div className="breakdown-code">{previewData.components.province_code}</div>
            </div>
            <div className="breakdown-item">
              <div className="breakdown-label">Company</div>
              <div className="breakdown-code">{previewData.components.company_code}</div>
            </div>
            <div className="breakdown-item">
              <div className="breakdown-label">Year</div>
              <div className="breakdown-code">{String(previewData.components.year).slice(-2)}</div>
            </div>
            <div className="breakdown-item">
              <div className="breakdown-label">Sequence</div>
              <div className="breakdown-code">{String(previewData.components.sequence).padStart(3, '0')}</div>
            </div>
          </div>
          <div className="preview-note">
            💡 This is a preview. Actual sequence number will be assigned when asset is created.
          </div>
        </div>
      )}
    </div>
  );
}

export default AssetIDGenerator;
