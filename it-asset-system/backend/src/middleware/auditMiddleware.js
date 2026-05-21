const { sql, getConnection } = require('../config/database');

/**
 * Audit Middleware
 * Automatically logs all CUD (Create, Update, Delete) operations
 */

/**
 * Create audit log entry
 * @param {Object} logData - Audit log data
 */
const createAuditLog = async (logData) => {
  try {
    const pool = await getConnection();
    await pool.request()
      .input('userId', sql.Int, logData.userId)
      .input('action', sql.NVarChar, logData.action)
      .input('tableName', sql.NVarChar, logData.tableName)
      .input('recordId', sql.Int, logData.recordId || null)
      .input('oldValue', sql.NVarChar(sql.MAX), logData.oldValue ? JSON.stringify(logData.oldValue) : null)
      .input('newValue', sql.NVarChar(sql.MAX), logData.newValue ? JSON.stringify(logData.newValue) : null)
      .input('ipAddress', sql.NVarChar, logData.ipAddress || null)
      .input('userAgent', sql.NVarChar, logData.userAgent || null)
      .query(`
        INSERT INTO AuditLogs (
          UserID, Action, TableName, RecordID, 
          OldValue, NewValue, IPAddress, UserAgent
        ) VALUES (
          @userId, @action, @tableName, @recordId,
          @oldValue, @newValue, @ipAddress, @userAgent
        )
      `);
  } catch (error) {
    console.error('Audit log creation failed:', error);
    // Don't throw error - audit failure shouldn't break the main operation
  }
};

/**
 * Audit middleware for asset operations
 * @param {String} action - CREATE, UPDATE, DELETE
 */
const auditAsset = (action) => {
  return async (req, res, next) => {
    try {
      const originalJson = res.json.bind(res);
      
      res.json = async function(data) {
        // Only log successful operations
        if (data.success) {
          const logData = {
            userId: req.user?.userId,
            action: action,
            tableName: 'Assets',
            recordId: data.data?.assetId || req.params.id,
            ipAddress: req.ip || req.connection.remoteAddress,
            userAgent: req.headers['user-agent']
          };
          
          // For UPDATE, capture old and new values
          if (action === 'UPDATE' && req.oldAssetData) {
            logData.oldValue = req.oldAssetData;
            logData.newValue = req.body;
          }
          
          // For CREATE, capture new values
          if (action === 'CREATE') {
            logData.newValue = req.body;
          }
          
          // For DELETE, capture old values
          if (action === 'DELETE' && req.oldAssetData) {
            logData.oldValue = req.oldAssetData;
          }
          
          await createAuditLog(logData);
        }
        
        return originalJson(data);
      };
      
      next();
    } catch (error) {
      console.error('Audit middleware error:', error);
      next(); // Continue even if audit fails
    }
  };
};

/**
 * Generic audit middleware
 * @param {String} tableName - Table name
 * @param {String} action - CREATE, UPDATE, DELETE
 */
const audit = (tableName, action) => {
  return async (req, res, next) => {
    try {
      const originalJson = res.json.bind(res);
      
      res.json = async function(data) {
        if (data.success) {
          const logData = {
            userId: req.user?.userId,
            action: action,
            tableName: tableName,
            recordId: data.data?.id || req.params.id,
            ipAddress: req.ip || req.connection.remoteAddress,
            userAgent: req.headers['user-agent']
          };
          
          if (action === 'UPDATE' && req.oldData) {
            logData.oldValue = req.oldData;
            logData.newValue = req.body;
          }
          
          if (action === 'CREATE') {
            logData.newValue = req.body;
          }
          
          if (action === 'DELETE' && req.oldData) {
            logData.oldValue = req.oldData;
          }
          
          await createAuditLog(logData);
        }
        
        return originalJson(data);
      };
      
      next();
    } catch (error) {
      console.error('Audit middleware error:', error);
      next();
    }
  };
};

/**
 * Capture old data before update/delete
 * @param {Function} getDataFunction - Function to retrieve old data
 */
const captureOldData = (getDataFunction) => {
  return async (req, res, next) => {
    try {
      const oldData = await getDataFunction(req);
      req.oldData = oldData;
      req.oldAssetData = oldData; // For backward compatibility
      next();
    } catch (error) {
      console.error('Error capturing old data:', error);
      next(); // Continue even if capture fails
    }
  };
};

module.exports = {
  createAuditLog,
  auditAsset,
  audit,
  captureOldData
};
