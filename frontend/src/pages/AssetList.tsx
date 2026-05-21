import React, { useState, useEffect } from 'react';
import { Table, Button, Form, Row, Col, Modal, Badge, Spinner, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { Asset, AssetListResponse } from '../types/asset';
import api from '../services/api';
import './Assets.css';

const AssetList: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [filteredAssets, setFilteredAssets] = useState<Asset[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalAssets, setTotalAssets] = useState(0);
  const [itemsPerPage] = useState(50);
  
  // Filter states
  const [filterStatus, setFilterStatus] = useState('');
  
  const navigate = useNavigate();

  useEffect(() => {
    fetchAssets();
  }, [currentPage]);

  useEffect(() => {
    filterAssets();
  }, [assets, searchTerm, filterStatus]);

  const fetchAssets = async () => {
    try {
      setLoading(true);
      setError('');
      
      const skip = (currentPage - 1) * itemsPerPage;
      const response = await api.get<AssetListResponse>(
        `/api/assets/?skip=${skip}&limit=${itemsPerPage}`
      );
      
      setAssets(response.data.data);
      setTotalAssets(response.data.total);
      setLoading(false);
    } catch (error: any) {
      console.error('Error fetching assets:', error);
      setError(error.response?.data?.detail || 'Failed to fetch assets');
      setLoading(false);
    }
  };

  const filterAssets = () => {
    let filtered = assets;

    // Search term filter
    if (searchTerm) {
      filtered = filtered.filter(
        asset =>
          asset.asset_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
          asset.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          asset.brand?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          asset.model?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Status filter
    if (filterStatus) {
      filtered = filtered.filter(asset => asset.status === filterStatus);
    }

    setFilteredAssets(filtered);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setFilterStatus('');
  };

  const handleDelete = async () => {
    if (selectedAsset) {
      try {
        await api.delete(`/api/assets/${selectedAsset.asset_id}`);
        setSuccess(`Asset ${selectedAsset.asset_id} deleted successfully`);
        fetchAssets();
        setShowDeleteModal(false);
        setSelectedAsset(null);
      } catch (error: any) {
        setError(error.response?.data?.detail || 'Failed to delete asset');
      }
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case 'available':
        return 'bg-success';
      case 'in_use':
      case 'in use':
        return 'bg-warning';
      case 'maintenance':
        return 'bg-danger';
      case 'disposed':
        return 'bg-secondary';
      default:
        return 'bg-info';
    }
  };

  const totalPages = Math.ceil(totalAssets / itemsPerPage);

  if (loading && assets.length === 0) {
    return (
      <div className="loading-container">
        <Spinner animation="border" role="status" variant="primary">
          <span className="visually-hidden">Loading assets...</span>
        </Spinner>
      </div>
    );
  }

  return (
    <div className="assets-container">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-1">Assets</h2>
          <p className="text-muted mb-0">Manage your organization's assets</p>
        </div>
        <div className="d-flex gap-2">
          <Link to="/assets/new" className="btn btn-primary">
            <i className="bi bi-plus-circle me-2"></i>
            Add Asset
          </Link>
          <Button variant="outline-secondary" onClick={fetchAssets}>
            <i className="bi bi-arrow-clockwise me-2"></i>
            Refresh
          </Button>
        </div>
      </div>

      {error && (
        <Alert variant="danger" dismissible onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert variant="success" dismissible onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      {/* Search and Filters */}
      <Row className="mb-3">
        <Col md={8}>
          <Form.Control
            type="text"
            placeholder="Search by Asset ID, Name, Brand, or Model..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </Col>
        <Col md={4}>
          <Form.Select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="">All Status</option>
            <option value="available">Available</option>
            <option value="in_use">In Use</option>
            <option value="maintenance">Maintenance</option>
            <option value="disposed">Disposed</option>
          </Form.Select>
        </Col>
      </Row>

      <Row className="mb-3">
        <Col>
          <Button 
            variant="outline-secondary" 
            size="sm" 
            onClick={clearFilters}
          >
            Clear Filters
          </Button>
          <span className="ms-3 text-muted">
            Showing {filteredAssets.length} of {totalAssets} assets
          </span>
        </Col>
      </Row>

      {/* Assets Table */}
      <div className="table-responsive">
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Asset ID</th>
              <th>Name</th>
              <th>Brand/Model</th>
              <th>Status</th>
              <th>Purchase Date</th>
              <th>Value</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredAssets.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-4">
                  <p className="text-muted mb-0">No assets found</p>
                </td>
              </tr>
            ) : (
              filteredAssets.map((asset) => (
                <tr key={asset.id}>
                  <td>
                    <code>{asset.asset_id}</code>
                  </td>
                  <td>
                    <strong>{asset.name}</strong>
                  </td>
                  <td>
                    {asset.brand && asset.model ? 
                      `${asset.brand} ${asset.model}` : 
                      asset.brand || asset.model || '-'
                    }
                  </td>
                  <td>
                    <Badge className={getStatusBadgeClass(asset.status)}>
                      {asset.status}
                    </Badge>
                  </td>
                  <td>
                    {asset.purchase_date ? 
                      new Date(asset.purchase_date).toLocaleDateString() : 
                      '-'
                    }
                  </td>
                  <td>
                    {asset.value ? `$${asset.value.toFixed(2)}` : '-'}
                  </td>
                  <td>
                    <div className="d-flex gap-1">
                      <Link 
                        to={`/assets/${asset.asset_id}`} 
                        className="btn btn-sm btn-info" 
                        title="View Details"
                      >
                        <i className="bi bi-eye"></i>
                      </Link>
                      <Link 
                        to={`/assets/${asset.asset_id}/edit`} 
                        className="btn btn-sm btn-warning" 
                        title="Edit Asset"
                      >
                        <i className="bi bi-pencil"></i>
                      </Link>
                      <Button
                        variant="danger"
                        size="sm"
                        title="Delete Asset"
                        onClick={() => {
                          setSelectedAsset(asset);
                          setShowDeleteModal(true);
                        }}
                      >
                        <i className="bi bi-trash"></i>
                      </Button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="d-flex justify-content-center mt-3">
          <Button
            variant="outline-primary"
            size="sm"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            Previous
          </Button>
          <span className="mx-3 align-self-center">
            Page {currentPage} of {totalPages}
          </span>
          <Button
            variant="outline-primary"
            size="sm"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
          </Button>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to delete asset <strong>{selectedAsset?.asset_id}</strong> - {selectedAsset?.name}?
          <div className="mt-2 text-danger">
            <small>This action cannot be undone.</small>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default AssetList;
