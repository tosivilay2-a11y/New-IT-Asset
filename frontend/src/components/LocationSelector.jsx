/**
 * LocationSelector Component
 * Cascading dropdowns for Country > Province > Company selection
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './LocationSelector.css';

const API_BASE_URL = 'http://localhost:8000';

function LocationSelector({ 
  value = {}, 
  onChange, 
  required = false,
  disabled = false,
  showLabels = true 
}) {
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [companies, setCompanies] = useState([]);
  
  const [selectedCountry, setSelectedCountry] = useState(value.countryId || '');
  const [selectedProvince, setSelectedProvince] = useState(value.provinceId || '');
  const [selectedCompany, setSelectedCompany] = useState(value.companyId || '');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load countries on mount
  useEffect(() => {
    loadCountries();
  }, []);

  // Load provinces when country changes
  useEffect(() => {
    if (selectedCountry) {
      loadProvinces(selectedCountry);
    } else {
      setProvinces([]);
      setCompanies([]);
      setSelectedProvince('');
      setSelectedCompany('');
    }
  }, [selectedCountry]);

  // Load companies when province changes
  useEffect(() => {
    if (selectedProvince) {
      loadCompanies(selectedProvince);
    } else {
      setCompanies([]);
      setSelectedCompany('');
    }
  }, [selectedProvince]);

  // Notify parent of changes
  useEffect(() => {
    if (onChange) {
      const country = countries.find(c => c.countryid === parseInt(selectedCountry));
      const province = provinces.find(p => p.provinceid === parseInt(selectedProvince));
      const company = companies.find(c => c.companyid === parseInt(selectedCompany));
      
      onChange({
        countryId: selectedCountry ? parseInt(selectedCountry) : null,
        provinceId: selectedProvince ? parseInt(selectedProvince) : null,
        companyId: selectedCompany ? parseInt(selectedCompany) : null,
        countryCode: country?.countrycode || null,
        provinceCode: province?.provincecode || null,
        companyCode: company?.companycode || null,
        countryName: country?.countryname || null,
        provinceName: province?.provincename || null,
        companyName: company?.companyname || null
      });
    }
  }, [selectedCountry, selectedProvince, selectedCompany]);

  const loadCountries = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/countries`);
      setCountries(response.data);
    } catch (err) {
      setError('Failed to load countries');
      console.error('Error loading countries:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadProvinces = async (countryId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/provinces?country_id=${countryId}`);
      setProvinces(response.data);
    } catch (err) {
      setError('Failed to load provinces');
      console.error('Error loading provinces:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadCompanies = async (provinceId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/companies?province_id=${provinceId}`);
      setCompanies(response.data);
    } catch (err) {
      setError('Failed to load companies');
      console.error('Error loading companies:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCountryChange = (e) => {
    setSelectedCountry(e.target.value);
    setSelectedProvince('');
    setSelectedCompany('');
  };

  const handleProvinceChange = (e) => {
    setSelectedProvince(e.target.value);
    setSelectedCompany('');
  };

  const handleCompanyChange = (e) => {
    setSelectedCompany(e.target.value);
  };

  return (
    <div className="location-selector">
      {error && <div className="location-error">{error}</div>}
      
      <div className="location-row">
        <div className="location-field">
          {showLabels && <label>Country {required && <span className="required">*</span>}</label>}
          <select
            value={selectedCountry}
            onChange={handleCountryChange}
            disabled={disabled || loading}
            required={required}
            className="location-select"
          >
            <option value="">Select Country</option>
            {countries.map(country => (
              <option key={country.countryid} value={country.countryid}>
                {country.countryname} ({country.countrycode})
              </option>
            ))}
          </select>
        </div>

        <div className="location-field">
          {showLabels && <label>Province {required && <span className="required">*</span>}</label>}
          <select
            value={selectedProvince}
            onChange={handleProvinceChange}
            disabled={disabled || loading || !selectedCountry}
            required={required}
            className="location-select"
          >
            <option value="">Select Province</option>
            {provinces.map(province => (
              <option key={province.provinceid} value={province.provinceid}>
                {province.provincename} ({province.provincecode})
              </option>
            ))}
          </select>
        </div>

        <div className="location-field">
          {showLabels && <label>Company {required && <span className="required">*</span>}</label>}
          <select
            value={selectedCompany}
            onChange={handleCompanyChange}
            disabled={disabled || loading || !selectedProvince}
            required={required}
            className="location-select"
          >
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
  );
}

export default LocationSelector;
