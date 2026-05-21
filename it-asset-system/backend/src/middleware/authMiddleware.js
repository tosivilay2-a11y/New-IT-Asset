const jwt = require('jsonwebtoken');
const { getConnection } = require('../config/database');

/**
 * Authentication Middleware
 * Validates JWT tokens and attaches user to request
 */

const authMiddleware = async (req, res, next) => {
  try {
    // Get token from header
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        success: false,
        message: 'No token provided'
      });
    }
    
    const token = authHeader.substring(7); // Remove 'Bearer ' prefix
    
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Get user from database
    const pool = await getConnection();
    const result = await pool.query(`
      SELECT 
        u.UserID,
        u.Username,
        u.Email,
        u.FirstName || ' ' || u.LastName as FullName,
        u.IsActive,
        ur.RoleName
      FROM Users u
      LEFT JOIN UserRoles ur ON u.RoleID = ur.RoleID
      WHERE u.UserID = $1 AND u.IsActive = TRUE
    `, [decoded.userId]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({
        success: false,
        message: 'User not found or inactive'
      });
    }
    
    const user = result.rows[0];
    
    // Attach user to request
    req.user = {
      userId: user.userid,
      username: user.username,
      email: user.email,
      fullName: user.fullname,
      role: user.rolename
    };
    
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        success: false,
        message: 'Invalid token'
      });
    }
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        message: 'Token expired'
      });
    }
    
    console.error('Auth middleware error:', error);
    return res.status(500).json({
      success: false,
      message: 'Authentication failed'
    });
  }
};

/**
 * Optional authentication middleware
 * Attaches user if token is valid, but doesn't require it
 */
const optionalAuth = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return next();
    }
    
    const token = authHeader.substring(7);
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    const pool = await getConnection();
    const result = await pool.query(`
      SELECT 
        u.UserID,
        u.Username,
        u.Email,
        u.FirstName || ' ' || u.LastName as FullName,
        ur.RoleName
      FROM Users u
      LEFT JOIN UserRoles ur ON u.RoleID = ur.RoleID
      WHERE u.UserID = $1 AND u.IsActive = TRUE
    `, [decoded.userId]);
    
    if (result.rows.length > 0) {
      const user = result.rows[0];
      req.user = {
        userId: user.userid,
        username: user.username,
        email: user.email,
        fullName: user.fullname,
        role: user.rolename
      };
    }
    
    next();
  } catch (error) {
    // Ignore errors for optional auth
    next();
  }
};

module.exports = {
  authMiddleware,
  optionalAuth
};
