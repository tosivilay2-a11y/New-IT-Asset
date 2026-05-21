const { getConnection } = require('../config/database');

/**
 * Permission Middleware
 * Checks if user has required permissions (RBAC)
 */

/**
 * Check if user has specific permission
 * @param {String} permissionName - Permission name to check
 */
const requirePermission = (permissionName) => {
  return async (req, res, next) => {
    try {
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }
      
      const pool = await getConnection();
      
      // Get user's role
      const roleResult = await pool.query(
        'SELECT RoleID FROM Users WHERE UserID = $1',
        [req.user.userId]
      );
      
      if (roleResult.rows.length === 0) {
        return res.status(403).json({
          success: false,
          message: 'User role not found'
        });
      }
      
      const roleId = roleResult.rows[0].roleid;
      
      // Check if role has permission
      const permissionResult = await pool.query(`
        SELECT rp.RolePermissionID
        FROM RolePermissions rp
        INNER JOIN Permissions p ON rp.PermissionID = p.PermissionID
        WHERE rp.RoleID = $1 AND p.PermissionKey = $2
      `, [roleId, permissionName]);
      
      if (permissionResult.rows.length === 0) {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }
      
      next();
    } catch (error) {
      console.error('Permission check error:', error);
      return res.status(500).json({
        success: false,
        message: 'Permission check failed'
      });
    }
  };
};

/**
 * Check if user has any of the specified permissions
 * @param {Array} permissionNames - Array of permission names
 */
const requireAnyPermission = (permissionNames) => {
  return async (req, res, next) => {
    try {
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }
      
      const pool = await getConnection();
      
      const roleResult = await pool.query(
        'SELECT RoleID FROM Users WHERE UserID = $1',
        [req.user.userId]
      );
      
      if (roleResult.rows.length === 0) {
        return res.status(403).json({
          success: false,
          message: 'User role not found'
        });
      }
      
      const roleId = roleResult.rows[0].roleid;
      
      // Build query for multiple permissions
      const placeholders = permissionNames.map((_, i) => `$${i + 2}`).join(',');
      
      const permissionResult = await pool.query(`
        SELECT rp.RolePermissionID
        FROM RolePermissions rp
        INNER JOIN Permissions p ON rp.PermissionID = p.PermissionID
        WHERE rp.RoleID = $1 AND p.PermissionKey IN (${placeholders})
      `, [roleId, ...permissionNames]);
      
      if (permissionResult.rows.length === 0) {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }
      
      next();
    } catch (error) {
      console.error('Permission check error:', error);
      return res.status(500).json({
        success: false,
        message: 'Permission check failed'
      });
    }
  };
};

/**
 * Check if user has specific role
 * @param {String|Array} roles - Role name(s) to check
 */
const requireRole = (roles) => {
  const roleArray = Array.isArray(roles) ? roles : [roles];
  
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }
    
    if (!roleArray.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: 'Insufficient role privileges'
      });
    }
    
    next();
  };
};

/**
 * Check if user is admin
 */
const requireAdmin = requireRole('Admin');

/**
 * Check if user owns the resource or is admin
 * @param {Function} getResourceOwnerId - Function to get owner ID from request
 */
const requireOwnerOrAdmin = (getResourceOwnerId) => {
  return async (req, res, next) => {
    try {
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }
      
      // Admin can access everything
      if (req.user.role === 'Admin') {
        return next();
      }
      
      // Get resource owner ID
      const ownerId = await getResourceOwnerId(req);
      
      if (req.user.userId !== ownerId) {
        return res.status(403).json({
          success: false,
          message: 'Access denied'
        });
      }
      
      next();
    } catch (error) {
      console.error('Ownership check error:', error);
      return res.status(500).json({
        success: false,
        message: 'Authorization check failed'
      });
    }
  };
};

module.exports = {
  requirePermission,
  requireAnyPermission,
  requireRole,
  requireAdmin,
  requireOwnerOrAdmin
};
