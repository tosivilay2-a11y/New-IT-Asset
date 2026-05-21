const AssetModel = require('../models/assetModel');
const AssetIdGenerator = require('../services/assetIdGenerator');
const QRCodeService = require('../services/qrCodeService');

const AssetController = {
  /**
   * Get all assets with pagination and filters
   */
  getAllAssets: async (req, res) => {
    try {
      const filters = {
        page: parseInt(req.query.page) || 1,
        limit: parseInt(req.query.limit) || 50,
        statusId: req.query.statusId ? parseInt(req.query.statusId) : null,
        locationId: req.query.locationId ? parseInt(req.query.locationId) : null,
        companyId: req.query.companyId ? parseInt(req.query.companyId) : null,
        mainCategoryId: req.query.mainCategoryId ? parseInt(req.query.mainCategoryId) : null,
        search: req.query.search || null
      };

      const result = await AssetModel.getAll(filters);

      res.json({
        success: true,
        data: result.data,
        pagination: result.pagination
      });
    } catch (error) {
      console.error('Get all assets error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve assets',
        error: error.message
      });
    }
  },

  /**
   * Get asset by ID
   */
  getAssetById: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);
      const asset = await AssetModel.getById(assetId);

      if (!asset) {
        return res.status(404).json({
          success: false,
          message: 'Asset not found'
        });
      }

      res.json({
        success: true,
        data: asset
      });
    } catch (error) {
      console.error('Get asset by ID error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve asset',
        error: error.message
      });
    }
  },

  /**
   * Get asset by code
   */
  getAssetByCode: async (req, res) => {
    try {
      const assetCode = req.params.code;
      const asset = await AssetModel.getByCode(assetCode);

      if (!asset) {
        return res.status(404).json({
          success: false,
          message: 'Asset not found'
        });
      }

      res.json({
        success: true,
        data: asset
      });
    } catch (error) {
      console.error('Get asset by code error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve asset',
        error: error.message
      });
    }
  },

  /**
   * Preview Asset ID
   */
  previewAssetId: async (req, res) => {
    try {
      const { mainCategoryId, countryId, provinceId, companyId } = req.query;

      if (!mainCategoryId || !countryId || !provinceId || !companyId) {
        return res.status(400).json({
          success: false,
          message: 'Missing required parameters'
        });
      }

      const assetId = await AssetIdGenerator.previewAssetId({
        mainCategoryId: parseInt(mainCategoryId),
        countryId: parseInt(countryId),
        provinceId: parseInt(provinceId),
        companyId: parseInt(companyId)
      });

      res.json({
        success: true,
        data: { assetId }
      });
    } catch (error) {
      console.error('Preview asset ID error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to preview asset ID',
        error: error.message
      });
    }
  },

  /**
   * Create new asset
   */
  createAsset: async (req, res) => {
    try {
      const assetData = req.body;

      // Validate required fields
      if (!assetData.mainCategoryId || !assetData.countryId || 
          !assetData.provinceId || !assetData.companyId || 
          !assetData.statusId || !assetData.locationId) {
        return res.status(400).json({
          success: false,
          message: 'Missing required fields'
        });
      }

      // Generate Asset ID
      const assetCode = await AssetIdGenerator.generateAssetId({
        mainCategoryId: assetData.mainCategoryId,
        countryId: assetData.countryId,
        provinceId: assetData.provinceId,
        companyId: assetData.companyId
      });

      assetData.assetCode = assetCode;

      // Create asset
      const assetId = await AssetModel.create(assetData, req.user.userId);

      // Generate QR code
      const qrCode = await QRCodeService.generateAndSaveQRCode(assetId, assetCode);

      // Get created asset
      const asset = await AssetModel.getById(assetId);

      res.status(201).json({
        success: true,
        message: 'Asset created successfully',
        data: {
          assetId,
          assetCode,
          qrCode,
          asset
        }
      });
    } catch (error) {
      console.error('Create asset error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to create asset',
        error: error.message
      });
    }
  },

  /**
   * Update asset
   */
  updateAsset: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);
      const assetData = req.body;

      // Check if asset exists
      const existingAsset = await AssetModel.getById(assetId);
      if (!existingAsset) {
        return res.status(404).json({
          success: false,
          message: 'Asset not found'
        });
      }

      // Update asset
      await AssetModel.update(assetId, assetData, req.user.userId);

      // Get updated asset
      const asset = await AssetModel.getById(assetId);

      res.json({
        success: true,
        message: 'Asset updated successfully',
        data: { assetId, asset }
      });
    } catch (error) {
      console.error('Update asset error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to update asset',
        error: error.message
      });
    }
  },

  /**
   * Delete asset
   */
  deleteAsset: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);

      // Check if asset exists
      const existingAsset = await AssetModel.getById(assetId);
      if (!existingAsset) {
        return res.status(404).json({
          success: false,
          message: 'Asset not found'
        });
      }

      await AssetModel.delete(assetId);

      res.json({
        success: true,
        message: 'Asset deleted successfully'
      });
    } catch (error) {
      console.error('Delete asset error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to delete asset',
        error: error.message
      });
    }
  },

  /**
   * Assign asset to user
   */
  assignAsset: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);
      const { userId } = req.body;

      if (!userId) {
        return res.status(400).json({
          success: false,
          message: 'User ID is required'
        });
      }

      await AssetModel.assignToUser(assetId, userId, req.user.userId);

      const asset = await AssetModel.getById(assetId);

      res.json({
        success: true,
        message: 'Asset assigned successfully',
        data: { assetId, asset }
      });
    } catch (error) {
      console.error('Assign asset error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to assign asset',
        error: error.message
      });
    }
  },

  /**
   * Unassign asset from user
   */
  unassignAsset: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);

      await AssetModel.unassignFromUser(assetId, req.user.userId);

      const asset = await AssetModel.getById(assetId);

      res.json({
        success: true,
        message: 'Asset unassigned successfully',
        data: { assetId, asset }
      });
    } catch (error) {
      console.error('Unassign asset error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to unassign asset',
        error: error.message
      });
    }
  },

  /**
   * Transfer asset to new location
   */
  transferAsset: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);
      const { locationId } = req.body;

      if (!locationId) {
        return res.status(400).json({
          success: false,
          message: 'Location ID is required'
        });
      }

      await AssetModel.transferLocation(assetId, locationId, req.user.userId);

      const asset = await AssetModel.getById(assetId);

      res.json({
        success: true,
        message: 'Asset transferred successfully',
        data: { assetId, asset }
      });
    } catch (error) {
      console.error('Transfer asset error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to transfer asset',
        error: error.message
      });
    }
  },

  /**
   * Get asset history
   */
  getAssetHistory: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);
      const history = await AssetModel.getHistory(assetId);

      res.json({
        success: true,
        data: history
      });
    } catch (error) {
      console.error('Get asset history error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve asset history',
        error: error.message
      });
    }
  },

  /**
   * Get assets by location
   */
  getAssetsByLocation: async (req, res) => {
    try {
      const locationId = parseInt(req.params.locationId);
      const assets = await AssetModel.getByLocation(locationId);

      res.json({
        success: true,
        data: assets
      });
    } catch (error) {
      console.error('Get assets by location error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve assets',
        error: error.message
      });
    }
  },

  /**
   * Get assets by user
   */
  getAssetsByUser: async (req, res) => {
    try {
      const userId = parseInt(req.params.userId);
      const assets = await AssetModel.getByUser(userId);

      res.json({
        success: true,
        data: assets
      });
    } catch (error) {
      console.error('Get assets by user error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve assets',
        error: error.message
      });
    }
  },

  /**
   * Get dashboard statistics
   */
  getStatistics: async (req, res) => {
    try {
      const filters = {
        companyId: req.query.companyId ? parseInt(req.query.companyId) : null,
        locationId: req.query.locationId ? parseInt(req.query.locationId) : null
      };

      const stats = await AssetModel.getStatistics(filters);

      res.json({
        success: true,
        data: stats
      });
    } catch (error) {
      console.error('Get statistics error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve statistics',
        error: error.message
      });
    }
  },

  /**
   * Generate QR code for asset
   */
  generateQRCode: async (req, res) => {
    try {
      const assetId = parseInt(req.params.id);

      const asset = await AssetModel.getById(assetId);
      if (!asset) {
        return res.status(404).json({
          success: false,
          message: 'Asset not found'
        });
      }

      const qrCode = await QRCodeService.generateAndSaveQRCode(assetId, asset.AssetCode);

      res.json({
        success: true,
        message: 'QR code generated successfully',
        data: { assetId, qrCode }
      });
    } catch (error) {
      console.error('Generate QR code error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to generate QR code',
        error: error.message
      });
    }
  },

  /**
   * Bulk generate QR codes
   */
  bulkGenerateQRCodes: async (req, res) => {
    try {
      const { assetIds } = req.body;

      if (!assetIds || !Array.isArray(assetIds)) {
        return res.status(400).json({
          success: false,
          message: 'Asset IDs array is required'
        });
      }

      const results = await QRCodeService.bulkGenerateQRCodes(assetIds);

      res.json({
        success: true,
        message: 'QR codes generated',
        data: results
      });
    } catch (error) {
      console.error('Bulk generate QR codes error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to generate QR codes',
        error: error.message
      });
    }
  },

  /**
   * Scan QR code and get asset
   */
  scanQRCode: async (req, res) => {
    try {
      const { assetCode } = req.body;

      if (!assetCode) {
        return res.status(400).json({
          success: false,
          message: 'Asset code is required'
        });
      }

      const asset = await QRCodeService.getAssetByQRCode(assetCode);

      res.json({
        success: true,
        data: asset
      });
    } catch (error) {
      console.error('Scan QR code error:', error);
      res.status(404).json({
        success: false,
        message: 'Asset not found',
        error: error.message
      });
    }
  },

  /**
   * Get printable QR labels
   */
  getPrintableLabels: async (req, res) => {
    try {
      const { assetIds } = req.body;

      if (!assetIds || !Array.isArray(assetIds)) {
        return res.status(400).json({
          success: false,
          message: 'Asset IDs array is required'
        });
      }

      const labels = await QRCodeService.generatePrintableLabels(assetIds);

      res.json({
        success: true,
        data: labels
      });
    } catch (error) {
      console.error('Get printable labels error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to generate labels',
        error: error.message
      });
    }
  }
};

module.exports = AssetController;
