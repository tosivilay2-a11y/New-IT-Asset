const QRCode = require('qrcode');
const { sql, getConnection } = require('../config/database');

/**
 * QR Code Service
 * Handles QR code generation, storage, and retrieval
 */

const QRCodeService = {
  /**
   * Generate QR code for asset
   * @param {String} assetCode - Asset code to encode
   * @param {Object} options - QR code options
   * @returns {String} Base64 encoded QR code image
   */
  generateQRCode: async (assetCode, options = {}) => {
    try {
      const qrOptions = {
        errorCorrectionLevel: options.errorCorrectionLevel || 'M',
        type: options.type || 'image/png',
        quality: options.quality || 0.92,
        margin: options.margin || 1,
        width: options.width || 300,
        color: {
          dark: options.darkColor || '#000000',
          light: options.lightColor || '#FFFFFF'
        }
      };

      // Generate QR code as data URL
      const qrCodeDataURL = await QRCode.toDataURL(assetCode, qrOptions);
      
      return qrCodeDataURL;
    } catch (error) {
      throw new Error(`QR code generation failed: ${error.message}`);
    }
  },

  /**
   * Generate and save QR code for asset
   * @param {Number} assetId - Asset ID
   * @param {String} assetCode - Asset code
   * @returns {String} QR code data URL
   */
  generateAndSaveQRCode: async (assetId, assetCode) => {
    try {
      // Generate QR code
      const qrCodeDataURL = await QRCodeService.generateQRCode(assetCode);
      
      // Save to database
      const pool = await getConnection();
      await pool.request()
        .input('assetId', sql.Int, assetId)
        .input('qrCode', sql.NVarChar(sql.MAX), qrCodeDataURL)
        .query(`
          UPDATE Assets 
          SET QRCode = @qrCode, UpdatedAt = GETDATE() 
          WHERE AssetID = @assetId
        `);
      
      return qrCodeDataURL;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Bulk generate QR codes for multiple assets
   * @param {Array} assetIds - Array of asset IDs
   * @returns {Array} Array of results with assetId and qrCode
   */
  bulkGenerateQRCodes: async (assetIds) => {
    try {
      const pool = await getConnection();
      const results = [];
      
      for (const assetId of assetIds) {
        // Get asset code
        const assetResult = await pool.request()
          .input('assetId', sql.Int, assetId)
          .query('SELECT AssetCode FROM Assets WHERE AssetID = @assetId');
        
        if (assetResult.recordset.length === 0) {
          results.push({
            assetId,
            success: false,
            error: 'Asset not found'
          });
          continue;
        }
        
        const assetCode = assetResult.recordset[0].AssetCode;
        
        try {
          const qrCode = await QRCodeService.generateAndSaveQRCode(assetId, assetCode);
          results.push({
            assetId,
            assetCode,
            success: true,
            qrCode
          });
        } catch (error) {
          results.push({
            assetId,
            assetCode,
            success: false,
            error: error.message
          });
        }
      }
      
      return results;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get QR code for asset
   * @param {Number} assetId - Asset ID
   * @returns {String} QR code data URL
   */
  getQRCode: async (assetId) => {
    try {
      const pool = await getConnection();
      const result = await pool.request()
        .input('assetId', sql.Int, assetId)
        .query('SELECT QRCode FROM Assets WHERE AssetID = @assetId');
      
      if (result.recordset.length === 0) {
        throw new Error('Asset not found');
      }
      
      return result.recordset[0].QRCode;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Decode QR code and get asset
   * @param {String} assetCode - Asset code from QR scan
   * @returns {Object} Asset details
   */
  getAssetByQRCode: async (assetCode) => {
    try {
      const pool = await getConnection();
      const result = await pool.request()
        .input('assetCode', sql.NVarChar, assetCode)
        .query(`
          SELECT 
            a.*,
            mc.CategoryName as MainCategoryName,
            c.CategoryName as CategoryName,
            s.StatusName,
            l.LocationName,
            cl.LocationName as CurrentLocationName,
            u.FullName as AssignedToName
          FROM Assets a
          LEFT JOIN MainCategories mc ON a.MainCategoryID = mc.MainCategoryID
          LEFT JOIN Categories c ON a.CategoryID = c.CategoryID
          LEFT JOIN AssetStatuses s ON a.StatusID = s.StatusID
          LEFT JOIN Locations l ON a.LocationID = l.LocationID
          LEFT JOIN Locations cl ON a.CurrentLocationID = cl.CurrentLocationID
          LEFT JOIN Users u ON a.AssignedTo = u.UserID
          WHERE a.AssetCode = @assetCode
        `);
      
      if (result.recordset.length === 0) {
        throw new Error('Asset not found');
      }
      
      return result.recordset[0];
    } catch (error) {
      throw error;
    }
  },

  /**
   * Generate printable QR code labels
   * @param {Array} assetIds - Array of asset IDs
   * @returns {Array} Array of label data
   */
  generatePrintableLabels: async (assetIds) => {
    try {
      const pool = await getConnection();
      const labels = [];
      
      for (const assetId of assetIds) {
        const result = await pool.request()
          .input('assetId', sql.Int, assetId)
          .query(`
            SELECT 
              AssetID,
              AssetCode,
              Brand,
              ModelName,
              QRCode
            FROM Assets 
            WHERE AssetID = @assetId
          `);
        
        if (result.recordset.length > 0) {
          const asset = result.recordset[0];
          
          // Generate QR code if not exists
          let qrCode = asset.QRCode;
          if (!qrCode) {
            qrCode = await QRCodeService.generateAndSaveQRCode(assetId, asset.AssetCode);
          }
          
          labels.push({
            assetId: asset.AssetID,
            assetCode: asset.AssetCode,
            brand: asset.Brand,
            model: asset.ModelName,
            qrCode: qrCode
          });
        }
      }
      
      return labels;
    } catch (error) {
      throw error;
    }
  }
};

module.exports = QRCodeService;
