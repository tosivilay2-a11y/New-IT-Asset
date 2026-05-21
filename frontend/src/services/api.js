import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-clear stale token on 401 so the user gets redirected to login cleanly
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      // Redirect to login if not already there
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => {
    // OAuth2PasswordRequestForm expects application/x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    return api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  register: (data) => api.post('/auth/register', data),
  getCurrentUser: () => api.get('/users/me'),
};

export const assetsAPI = {
  getAll: (params) => api.get('/assets/', { params }),
  getById: (id) => api.get(`/assets/${id}`),
  getOne: (id) => api.get(`/assets/${id}`),
  create: (data) => {
    // Check if data contains files
    if (data.po_attachment && Array.isArray(data.po_attachment) && data.po_attachment.length > 0) {
      return assetsAPI.createWithFiles(data);
    }
    return api.post('/assets/', data);
  },
  createWithFile: (data) => {
    const formData = new FormData();
    const { po_attachment: file, ...assetData } = data;
    formData.append('asset_data', JSON.stringify(assetData));
    if (file) formData.append('po_attachment', file);
    return api.post('/assets/with-file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  createWithFiles: (data) => {
    const { po_attachment: files, ...assetData } = data;
    const fileArray = Array.isArray(files) ? files : [files];
    
    // Create asset first without files
    return api.post('/assets/', assetData).then(response => {
      const assetId = response.data.assetid;
      // Then upload each file sequentially
      return fileArray.reduce((promise, file) => {
        return promise.then(() => {
          if (file instanceof File) {
            return assetsAPI.updateWithFile(assetId, { ...assetData, po_attachment: file });
          }
          return Promise.resolve();
        });
      }, Promise.resolve()).then(() => response);
    });
  },
  update: (id, data) => {
    // Check if data contains files
    if (data.po_attachment && Array.isArray(data.po_attachment) && data.po_attachment.length > 0) {
      return assetsAPI.updateWithFiles(id, data);
    }
    return api.put(`/assets/${id}`, data);
  },
  updateWithFile: (id, data) => {
    const formData = new FormData();
    const { po_attachment: file, ...assetData } = data;
    formData.append('asset_data', JSON.stringify(assetData));
    if (file) formData.append('po_attachment', file);
    return api.put(`/assets/${id}/with-file`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  updateWithFiles: (id, data) => {
    const { po_attachment: files, ...assetData } = data;
    const fileArray = Array.isArray(files) ? files : [files];
    
    // Upload each file sequentially
    return fileArray.reduce((promise, file) => {
      return promise.then(() => {
        if (file instanceof File) {
          return assetsAPI.updateWithFile(id, { ...assetData, po_attachment: file });
        }
        return Promise.resolve();
      });
    }, Promise.resolve());
  },
  delete: (id) => api.delete(`/assets/${id}`),
};

export const inventoryAPI = {
  getAll: (params) => api.get('/inventory/', { params }),
  create: (data) => api.post('/inventory/', data),
  createTransaction: (data) => api.post('/inventory/transaction', data),
  getAlerts: () => api.get('/inventory/alerts'),
};

export const auditsAPI = {
  getAll: (params) => api.get('/audits/', { params }),
  create: (data) => api.post('/audits/', data),
  addRecord: (auditId, data) => api.post(`/audits/${auditId}/records`, data),
  getReport: (auditId) => api.get(`/audits/${auditId}/report`),
  complete: (auditId) => api.put(`/audits/${auditId}/complete`),
};

export const dataImportAPI = {
  downloadAssetTemplate: () =>
    api.get('/data-import/assets/template', { responseType: 'blob' }),
  exportAssets: () =>
    api.get('/data-import/assets/export', { responseType: 'blob' }),
  importAssets: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/data-import/assets/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  downloadStaffTemplate: () =>
    api.get('/data-import/staff/template', { responseType: 'blob' }),
  exportStaff: () =>
    api.get('/data-import/staff/export', { responseType: 'blob' }),
  importStaff: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/data-import/staff/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const configAPI = {
  getAll: (category) => api.get('/config/', { params: { category } }),
  getStorageConfig: () => api.get('/config/storage'),
  getStorageStatus: () => api.get('/config/storage/status'),
  updateStorageConfig: (data) => api.post('/config/storage', data),
  testStorageConfig: (data) => api.post('/config/storage/test', data),
  getConfig: (key) => api.get(`/config/${key}`),
  createConfig: (data) => api.post('/config/', data),
  updateConfig: (key, data) => api.put(`/config/${key}`, data),
  deleteConfig: (key) => api.delete(`/config/${key}`),
};

export const assetRequestsAPI = {
  getAll: () => api.get('/asset-requests/'),
  create: (data) => api.post('/asset-requests/', data),
  update: (id, data) => api.put(`/asset-requests/${id}`, data),
  assign: (id, assetcode, notes) => api.post(`/asset-requests/${id}/assign`, { assetcode, notes }),
};

export default api;
