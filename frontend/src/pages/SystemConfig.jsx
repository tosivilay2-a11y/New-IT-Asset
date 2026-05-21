/**
 * System Configuration Page
 * Admin interface for managing Countries, Provinces, Companies, Categories, and Staff
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CountryManagement from '../components/admin/CountryManagement';
import ProvinceManagement from '../components/admin/ProvinceManagement';
import CompanyManagement from '../components/admin/CompanyManagement';
import LocationManagement from '../components/admin/LocationManagement';
import CategoryManagement from '../components/admin/CategoryManagement';
import StaffManagement from '../components/admin/StaffManagement';
import DepartmentManagement from '../components/admin/DepartmentManagement';
import CostCenterManagement from '../components/admin/CostCenterManagement';
import StockLocationConfig from '../components/admin/StockLocationConfig';
import AssetIDGenerator from '../components/admin/AssetIDGenerator';
import DataImport from '../components/admin/DataImport';
import './SystemConfig.css';

function SystemConfig() {
  const [activeTab, setActiveTab] = useState('generator');
  const navigate = useNavigate();

  const tabs = [
    { id: 'data-import', label: '📊 Data Import', icon: '📊' },
    { id: 'generator', label: '🔢 Asset ID Generator', icon: '🔢' },
    { id: 'storage', label: '☁️ File Storage', icon: '☁️' },
    { id: 'stock-location', label: '📍 Stock Location', icon: '📍' },
    { id: 'locations', label: '📍 Location Management', icon: '📍' },
    { id: 'staff', label: '👥 Staff Management', icon: '👥' },
    { id: 'departments', label: '📁 Departments', icon: '📁' },
    { id: 'cost-centers', label: '💰 Cost Centers', icon: '💰' },
    { id: 'countries', label: '🌍 Countries', icon: '🌍' },
    { id: 'provinces', label: '🏛️ Provinces', icon: '🏛️' },
    { id: 'companies', label: '🏢 Companies', icon: '🏢' },
    { id: 'categories', label: '📦 Categories', icon: '📦' },
  ];

  const handleTabClick = (tabId) => {
    if (tabId === 'storage') {
      navigate('/admin/storage');
    } else {
      setActiveTab(tabId);
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'data-import':
        return <DataImport />;
      case 'generator':
        return <AssetIDGenerator />;
      case 'stock-location':
        return <StockLocationConfig />;
      case 'locations':
        return <LocationManagement />;
      case 'staff':
        return <StaffManagement />;
      case 'departments':
        return <DepartmentManagement />;
      case 'cost-centers':
        return <CostCenterManagement />;
      case 'countries':
        return <CountryManagement />;
      case 'provinces':
        return <ProvinceManagement />;
      case 'companies':
        return <CompanyManagement />;
      case 'categories':
        return <CategoryManagement />;
      default:
        return null;
    }
  };

  return (
    <div className="system-config">
      <div className="page-header">
        <div>
          <h1>⚙️ System Configuration</h1>
          <p className="page-subtitle">Manage system settings, locations, staff, and asset ID patterns</p>
        </div>
      </div>

      <div className="config-tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`config-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => handleTabClick(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>

      <div className="config-content">
        {renderTabContent()}
      </div>
    </div>
  );
}

export default SystemConfig;
