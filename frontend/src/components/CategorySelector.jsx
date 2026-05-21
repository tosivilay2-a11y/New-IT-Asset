/**
 * CategorySelector Component
 * Dropdown for selecting main asset category
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CategorySelector.css';

const API_BASE_URL = 'http://localhost:8000';

function CategorySelector({ 
  value, 
  onChange, 
  required = false,
  disabled = false,
  showCode = true 
}) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/main-categories`);
      setCategories(response.data);
    } catch (err) {
      setError('Failed to load categories');
      console.error('Error loading categories:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const categoryName = e.target.value;
    const category = categories.find(c => c.categoryname === categoryName);
    
    if (onChange) {
      onChange({
        categoryName: categoryName,
        categoryCode: category?.categorycode || null,
        categoryId: category?.maincategoryid || null
      });
    }
  };

  return (
    <div className="category-selector">
      {error && <div className="category-error">{error}</div>}
      
      <select
        value={value || ''}
        onChange={handleChange}
        disabled={disabled || loading}
        required={required}
        className="category-select"
      >
        <option value="">Select Category</option>
        {categories.map(category => (
          <option key={category.maincategoryid} value={category.categoryname}>
            {showCode && `[${category.categorycode}] `}
            {category.categoryname}
          </option>
        ))}
      </select>
    </div>
  );
}

export default CategorySelector;
