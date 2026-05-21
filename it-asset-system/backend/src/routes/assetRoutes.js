const express = require('express');
const router = express.Router();
const AssetController = require('../controllers/assetController');
const { authMiddleware } = require('../middleware/authMiddleware');
const { requirePermission } = require('../middleware/permissionMiddleware');
const { auditAsset, captureOldData } = require('../middleware/auditMiddleware');
const AssetModel = require('../models/assetModel');

// Helper to get old asset data
const getOldAssetData = async (req) => {
  const assetId = parseInt(req.params.id);
  return await AssetModel.getById(assetId);
};

/**
 * Asset Routes
 * All routes require authentication
 */

// Get all assets (with pagination and filters)
router.get('/', 
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getAllAssets
);

// Get dashboard statistics
router.get('/statistics',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getStatistics
);

// Preview Asset ID (before creating)
router.get('/preview-id',
  authMiddleware,
  requirePermission('asset.create'),
  AssetController.previewAssetId
);

// Get asset by ID
router.get('/:id',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getAssetById
);

// Get asset by code
router.get('/code/:code',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getAssetByCode
);

// Get asset history
router.get('/:id/history',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getAssetHistory
);

// Get assets by location
router.get('/location/:locationId',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getAssetsByLocation
);

// Get assets by user
router.get('/user/:userId',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getAssetsByUser
);

// Create new asset
router.post('/',
  authMiddleware,
  requirePermission('asset.create'),
  auditAsset('CREATE'),
  AssetController.createAsset
);

// Update asset
router.put('/:id',
  authMiddleware,
  requirePermission('asset.update'),
  captureOldData(getOldAssetData),
  auditAsset('UPDATE'),
  AssetController.updateAsset
);

// Delete asset
router.delete('/:id',
  authMiddleware,
  requirePermission('asset.delete'),
  captureOldData(getOldAssetData),
  auditAsset('DELETE'),
  AssetController.deleteAsset
);

// Assign asset to user
router.post('/:id/assign',
  authMiddleware,
  requirePermission('asset.assign'),
  auditAsset('UPDATE'),
  AssetController.assignAsset
);

// Unassign asset from user
router.post('/:id/unassign',
  authMiddleware,
  requirePermission('asset.assign'),
  auditAsset('UPDATE'),
  AssetController.unassignAsset
);

// Transfer asset to new location
router.post('/:id/transfer',
  authMiddleware,
  requirePermission('asset.transfer'),
  auditAsset('UPDATE'),
  AssetController.transferAsset
);

// Generate QR code for asset
router.post('/:id/qr-code',
  authMiddleware,
  requirePermission('asset.update'),
  AssetController.generateQRCode
);

// Bulk generate QR codes
router.post('/qr-codes/bulk',
  authMiddleware,
  requirePermission('asset.update'),
  AssetController.bulkGenerateQRCodes
);

// Scan QR code
router.post('/qr-codes/scan',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.scanQRCode
);

// Get printable QR labels
router.post('/qr-codes/labels',
  authMiddleware,
  requirePermission('asset.view'),
  AssetController.getPrintableLabels
);

module.exports = router;
