const { getConnection } = require('../config/database');

const AssetModel = {
  // Get all assets with pagination and filters
  getAll: async (filters = {}) => {
    try {
      const pool = await getConnection();
      
      let query = `
        SELECT 
          a.*,
          u.firstname || ' ' || u.lastname as AssignedToName,
          u.email as AssignedToEmail
        FROM Assets a
        LEFT JOIN Users u ON a.AssignedTo = u.UserID
        WHERE 1=1
      `;

      const params = [];
      let paramCount = 1;
      
      if (filters.status) {
        query += ` AND a.Status = $${paramCount}`;
        params.push(filters.status);
        paramCount++;
      }
      
      if (filters.locationId) {
        query += ` AND a.LocationID = $${paramCount}`;
        params.push(filters.locationId);
        paramCount++;
      }
      
      if (filters.companyId) {
        query += ` AND a.CompanyID = $${paramCount}`;
        params.push(filters.companyId);
        paramCount++;
      }
      
      if (filters.mainCategory) {
        query += ` AND a.MainCategory = $${paramCount}`;
        params.push(filters.mainCategory);
        paramCount++;
      }
      
      if (filters.search) {
        query += ` AND (a.AssetID ILIKE $${paramCount} OR a.Brand ILIKE $${paramCount} OR a.ModelName ILIKE $${paramCount} OR a.SerialNumber ILIKE $${paramCount})`;
        params.push(`%${filters.search}%`);
        paramCount++;
      }

      query += ` ORDER BY a.CreatedAt DESC`;

      // Pagination
      const page = filters.page || 1;
      const limit = filters.limit || 50;
      const offset = (page - 1) * limit;
      
      query += ` LIMIT $${paramCount} OFFSET $${paramCount + 1}`;
      params.push(limit, offset);

      const result = await pool.query(query, params);

      // Get total count
      let countQuery = `SELECT COUNT(*) as total FROM Assets a WHERE 1=1`;
      const countParams = [];
      let countParamNum = 1;
      
      if (filters.status) {
        countQuery += ` AND a.Status = $${countParamNum}`;
        countParams.push(filters.status);
        countParamNum++;
      }
      if (filters.locationId) {
        countQuery += ` AND a.LocationID = $${countParamNum}`;
        countParams.push(filters.locationId);
        countParamNum++;
      }
      if (filters.companyId) {
        countQuery += ` AND a.CompanyID = $${countParamNum}`;
        countParams.push(filters.companyId);
        countParamNum++;
      }
      if (filters.mainCategory) {
        countQuery += ` AND a.MainCategory = $${countParamNum}`;
        countParams.push(filters.mainCategory);
        countParamNum++;
      }
      if (filters.search) {
        countQuery += ` AND (a.AssetID ILIKE $${countParamNum} OR a.Brand ILIKE $${countParamNum} OR a.ModelName ILIKE $${countParamNum} OR a.SerialNumber ILIKE $${countParamNum})`;
        countParams.push(`%${filters.search}%`);
      }

      const countResult = await pool.query(countQuery, countParams);
      const total = parseInt(countResult.rows[0].total);

      return {
        data: result.rows,
        pagination: {
          page,
          limit,
          total,
          totalPages: Math.ceil(total / limit)
        }
      };
    } catch (error) {
      throw error;
    }
  },

  // Get asset by ID
  getById: async (id) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(`
        SELECT 
          a.*,
          u.firstname || ' ' || u.lastname as AssignedToName,
          u.email as AssignedToEmail,
          u.department as AssignedToDepartment,
          creator.username as CreatedByName,
          modifier.username as ModifiedByName
        FROM Assets a
        LEFT JOIN Users u ON a.AssignedTo = u.UserID
        LEFT JOIN Users creator ON a.CreatedBy = creator.UserID
        LEFT JOIN Users modifier ON a.ModifiedBy = modifier.UserID
        WHERE a.AssetID = $1
      `, [id]);
      
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },

  // Get asset by code
  getByCode: async (assetCode) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(
        'SELECT * FROM Assets WHERE AssetID = $1',
        [assetCode]
      );
      
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  },

  // Create new asset
  create: async (assetData, userId) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(`
        INSERT INTO Assets (
          AssetID, MainCategory, Status, Category, ModelName, Brand, Model,
          CPU, Ram, HDD, WLANMACAddress, LANMACAddress, Description, SerialNumber,
          AssignedTo, Department, DatePurchase, DateFirstUse, Price, ReplacementCost,
          LocationID, LocationName, CurrentLocationID, CurrentLocationName,
          CompanyID, ProvinceID, CountryID, QRCode, CreatedBy
        )
        VALUES (
          $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
          $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29
        )
        RETURNING AssetID
      `, [
        assetData.assetCode,
        assetData.mainCategory,
        assetData.status || 'Available',
        assetData.category,
        assetData.modelName,
        assetData.brand,
        assetData.model,
        assetData.cpu,
        assetData.ram,
        assetData.hdd,
        assetData.wlanMacAddress,
        assetData.lanMacAddress,
        assetData.description,
        assetData.serialNumber,
        assetData.assignedTo,
        assetData.department,
        assetData.datePurchase,
        assetData.dateFirstUse,
        assetData.price,
        assetData.replacementCost,
        assetData.locationId,
        assetData.locationName,
        assetData.locationId, // CurrentLocationID same as LocationID initially
        assetData.locationName, // CurrentLocationName
        assetData.companyId,
        assetData.provinceId,
        assetData.countryId,
        assetData.qrCode,
        userId
      ]);
      
      return result.rows[0].assetid;
    } catch (error) {
      throw error;
    }
  },

  // Update asset
  update: async (id, assetData, userId) => {
    try {
      const pool = await getConnection();
      await pool.query(`
        UPDATE Assets SET
          MainCategory = $1,
          Status = $2,
          Category = $3,
          ModelName = $4,
          Brand = $5,
          Model = $6,
          CPU = $7,
          Ram = $8,
          HDD = $9,
          Description = $10,
          SerialNumber = $11,
          LocationID = $12,
          LocationName = $13,
          Price = $14,
          ReplacementCost = $15,
          ModifiedBy = $16,
          UpdatedAt = CURRENT_TIMESTAMP
        WHERE AssetID = $17
      `, [
        assetData.mainCategory,
        assetData.status,
        assetData.category,
        assetData.modelName,
        assetData.brand,
        assetData.model,
        assetData.cpu,
        assetData.ram,
        assetData.hdd,
        assetData.description,
        assetData.serialNumber,
        assetData.locationId,
        assetData.locationName,
        assetData.price,
        assetData.replacementCost,
        userId,
        id
      ]);
      
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Delete asset
  delete: async (id) => {
    try {
      const pool = await getConnection();
      await pool.query('DELETE FROM Assets WHERE AssetID = $1', [id]);
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Update QR code
  updateQRCode: async (id, qrCode) => {
    try {
      const pool = await getConnection();
      await pool.query(
        'UPDATE Assets SET QRCode = $1, UpdatedAt = CURRENT_TIMESTAMP WHERE AssetID = $2',
        [qrCode, id]
      );
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Assign asset to user
  assignToUser: async (assetId, userId, assignedBy) => {
    try {
      const pool = await getConnection();
      
      // Update asset
      await pool.query(`
        UPDATE Assets SET
          AssignedTo = $1,
          Status = 'In Use',
          DateAssigned = CURRENT_TIMESTAMP,
          ModifiedBy = $2,
          UpdatedAt = CURRENT_TIMESTAMP
        WHERE AssetID = $3
      `, [userId, assignedBy, assetId]);
      
      // Create assignment record
      await pool.query(`
        INSERT INTO AssetAssignments (AssetID, UserID, AssignedDate, Status, AssignedBy)
        VALUES ($1, $2, CURRENT_TIMESTAMP, 'Active', $3)
      `, [assetId, userId, assignedBy]);
      
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Unassign asset from user
  unassignFromUser: async (assetId, modifiedBy) => {
    try {
      const pool = await getConnection();
      
      // Update current assignment to returned
      await pool.query(`
        UPDATE AssetAssignments 
        SET ReturnedDate = CURRENT_TIMESTAMP, Status = 'Returned'
        WHERE AssetID = $1 AND Status = 'Active'
      `, [assetId]);
      
      // Update asset
      await pool.query(`
        UPDATE Assets SET
          AssignedTo = NULL,
          Status = 'Available',
          DateAssigned = NULL,
          ModifiedBy = $1,
          UpdatedAt = CURRENT_TIMESTAMP
        WHERE AssetID = $2
      `, [modifiedBy, assetId]);
      
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Transfer asset to new location
  transferLocation: async (assetId, newLocationId, newLocationName, modifiedBy) => {
    try {
      const pool = await getConnection();
      await pool.query(`
        UPDATE Assets SET
          CurrentLocationID = $1,
          CurrentLocationName = $2,
          ModifiedBy = $3,
          UpdatedAt = CURRENT_TIMESTAMP
        WHERE AssetID = $4
      `, [newLocationId, newLocationName, modifiedBy, assetId]);
      
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Get asset history (from audit logs)
  getHistory: async (assetId) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(`
        SELECT 
          al.*,
          u.username as UserName
        FROM AssetAuditLog al
        LEFT JOIN Users u ON al.ChangedBy = u.UserID
        WHERE al.AssetID = $1
        ORDER BY al.ChangedAt DESC
      `, [assetId]);
      
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  // Get assets by location
  getByLocation: async (locationId) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(`
        SELECT 
          a.*,
          u.firstname || ' ' || u.lastname as AssignedToName
        FROM Assets a
        LEFT JOIN Users u ON a.AssignedTo = u.UserID
        WHERE a.CurrentLocationID = $1
        ORDER BY a.AssetID
      `, [locationId]);
      
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  // Get assets by user
  getByUser: async (userId) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(`
        SELECT 
          a.*
        FROM Assets a
        WHERE a.AssignedTo = $1
        ORDER BY a.AssetID
      `, [userId]);
      
      return result.rows;
    } catch (error) {
      throw error;
    }
  },

  // Get dashboard statistics
  getStatistics: async (filters = {}) => {
    try {
      const pool = await getConnection();
      
      let whereClause = 'WHERE 1=1';
      const params = [];
      let paramCount = 1;
      
      if (filters.companyId) {
        whereClause += ` AND a.CompanyID = $${paramCount}`;
        params.push(filters.companyId);
        paramCount++;
      }
      
      if (filters.locationId) {
        whereClause += ` AND a.CurrentLocationID = $${paramCount}`;
        params.push(filters.locationId);
        paramCount++;
      }

      const result = await pool.query(`
        SELECT 
          COUNT(*) as TotalAssets,
          SUM(CASE WHEN a.Status = 'Available' THEN 1 ELSE 0 END) as Available,
          SUM(CASE WHEN a.Status = 'In Use' THEN 1 ELSE 0 END) as InUse,
          SUM(CASE WHEN a.Status = 'Maintenance' THEN 1 ELSE 0 END) as Maintenance,
          SUM(CASE WHEN a.Status = 'Disposed' THEN 1 ELSE 0 END) as Disposed,
          SUM(COALESCE(a.Price, 0)) as TotalValue
        FROM Assets a
        ${whereClause}
      `, params);
      
      return result.rows[0];
    } catch (error) {
      throw error;
    }
  }
};

module.exports = AssetModel;
