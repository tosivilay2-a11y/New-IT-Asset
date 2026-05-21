/**
 * AssetIDPreview Component
 * Shows preview of auto-generated asset ID
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AssetIDPreview.css';

const API_BASE_URL = 'http://localhost:8000';

function AssetIDPreview({ 
  mainCategory, 
  countryId, 
  provinceId, 
  companyId, 
  purchaseDate 
}) {
  const [previewData, setPreviewData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (mainCategory && countryId && provinceId && companyId) {
      fetchPreview();
    } else {
      setPreviewData(null);
    }
  }, [mainCategory, countryId, provinceId, companyId, purchaseDate]);

  const fetchPreview = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post(`${API_BASE_URL}/asset-utils/preview-asset-id`, {
        main_category: mainCategory,
        country_id: countryId,
        province_id: provinceId,
        company_id: companyId,
        purchase_date: purchaseDate || null
      });
      
      setPreviewData(response.data);
    } catch (err) {
      setError('Failed to generate preview');
      console.error('Error fetching asset ID preview:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderBreakdown = () => {
    if (!previewData?.components) return null;

    const { components } = previewData;
    
    return (
      <div className="asset-id-breakdown">
        <div className="breakdown-item">
          <div className="breakdown-label">Category</div>
          <div className="breakdown-value">{components.category_code}</div>
        </div>
        <div className="breakdown-item">
          <div className="breakdown-label">Country</div>
          <div className="breakdown-value">{components.country_code}</div>
        </div>
        <div className="breakdown-item">
          <div className="breakdown-label">Province</div>
          <div className="breakdown-value">{components.province_code}</div>
        </div>
        <div className="breakdown-item">
          <div className="breakdown-label">Company</div>
          <div className="breakdown-value">{components.company_code}</div>
        </div>
        <div className="breakdown-item">
          <div className="breakdown-label">Year</div>
          <div className="breakdown-value">{components.year}</div>
        </div>
        <div className="breakdown-item">
          <div className="breakdown-label">Sequence</div>
          <div className="breakdown-value">{String(components.sequence).padStart(3, '0')}</div>
        </div>
      </div>
    );
  };

  return (
    <div className="asset-id-preview">
      <div className="asset-id-preview-header">
        <div className="asset-id-preview-title">Asset ID Preview</div>
        {previewData && (
          <div className="asset-id-preview-status">
            <span className="status-dot"></span>
            <span>Auto-generated</span>
          </div>
        )}
      </div>

      <div className="asset-id-display">
        {loading && (
          <div className="asset-id-loading">Generating preview...</div>
        )}
        
        {error && (
          <div className="asset-id-error">{error}</div>
        )}
        
        {!loading && !error && previewData && (
          <div className="asset-id-value">{previewData.asset_id}</div>
        )}
        
        {!loading && !error && !previewData && (
          <div className="asset-id-placeholder">
            Select category and location to preview ID
          </div>
        )}
      </div>

      {previewData && renderBreakdown()}

      <div className="asset-id-info">
        💡 This ID will be automatically generated when you save the asset
      </div>
    </div>
  );
}

export default AssetIDPreview;
