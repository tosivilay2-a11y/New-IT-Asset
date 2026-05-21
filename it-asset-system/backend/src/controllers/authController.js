const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { getConnection } = require('../config/database');

const AuthController = {
  /**
   * User login
   */
  login: async (req, res) => {
    try {
      const { username, password } = req.body;

      if (!username || !password) {
        return res.status(400).json({
          success: false,
          message: 'Username and password are required'
        });
      }

      const pool = await getConnection();
      
      // Get user by username or email
      const result = await pool.query(`
        SELECT 
          u.UserID,
          u.Username,
          u.Email,
          u.Password as PasswordHash,
          u.FirstName || ' ' || u.LastName as FullName,
          u.IsActive,
          ur.RoleName,
          ur.RoleID
        FROM Users u
        LEFT JOIN UserRoles ur ON u.RoleID = ur.RoleID
        WHERE (u.Username = $1 OR u.Email = $1)
      `, [username]);

      if (result.rows.length === 0) {
        return res.status(401).json({
          success: false,
          message: 'Invalid credentials'
        });
      }

      const user = result.rows[0];

      // Check if user is active
      if (!user.isactive) {
        return res.status(401).json({
          success: false,
          message: 'Account is inactive'
        });
      }

      // Verify password
      const isValidPassword = await bcrypt.compare(password, user.passwordhash);
      if (!isValidPassword) {
        return res.status(401).json({
          success: false,
          message: 'Invalid credentials'
        });
      }

      // Generate JWT token
      const token = jwt.sign(
        {
          userId: user.userid,
          username: user.username,
          role: user.rolename
        },
        process.env.JWT_SECRET,
        { expiresIn: process.env.JWT_EXPIRES_IN || '24h' }
      );

      res.json({
        success: true,
        message: 'Login successful',
        data: {
          token,
          user: {
            userId: user.userid,
            username: user.username,
            email: user.email,
            fullName: user.fullname,
            role: user.rolename
          }
        }
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({
        success: false,
        message: 'Login failed',
        error: error.message
      });
    }
  },

  /**
   * User registration
   */
  register: async (req, res) => {
    try {
      const { username, email, password, firstName, lastName, employeeId } = req.body;

      // Validate required fields
      if (!username || !email || !password || !firstName || !lastName) {
        return res.status(400).json({
          success: false,
          message: 'All fields are required'
        });
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return res.status(400).json({
          success: false,
          message: 'Invalid email format'
        });
      }

      // Validate password strength
      if (password.length < 6) {
        return res.status(400).json({
          success: false,
          message: 'Password must be at least 6 characters'
        });
      }

      const pool = await getConnection();

      // Check if username exists
      const usernameCheck = await pool.query(
        'SELECT UserID FROM Users WHERE Username = $1',
        [username]
      );

      if (usernameCheck.rows.length > 0) {
        return res.status(400).json({
          success: false,
          message: 'Username already exists'
        });
      }

      // Check if email exists
      const emailCheck = await pool.query(
        'SELECT UserID FROM Users WHERE Email = $1',
        [email]
      );

      if (emailCheck.rows.length > 0) {
        return res.status(400).json({
          success: false,
          message: 'Email already exists'
        });
      }

      // Hash password
      const passwordHash = await bcrypt.hash(password, 10);

      // Get default role (User role)
      const roleResult = await pool.query(
        "SELECT RoleID FROM UserRoles WHERE RoleName = 'User' LIMIT 1"
      );
      const roleId = roleResult.rows[0]?.roleid || 3;

      // Generate employee ID if not provided
      const finalEmployeeId = employeeId || `EMP${Date.now()}`;

      // Create user
      const result = await pool.query(`
        INSERT INTO Users (
          EmployeeID, Username, Email, Password, FirstName, LastName, 
          UserType, RoleID, IsActive
        )
        VALUES ($1, $2, $3, $4, $5, $6, 'Staff', $7, TRUE)
        RETURNING UserID
      `, [finalEmployeeId, username, email, passwordHash, firstName, lastName, roleId]);

      const userId = result.rows[0].userid;

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        data: {
          userId,
          username,
          email,
          fullName: `${firstName} ${lastName}`
        }
      });
    } catch (error) {
      console.error('Registration error:', error);
      res.status(500).json({
        success: false,
        message: 'Registration failed',
        error: error.message
      });
    }
  },

  /**
   * Get current user profile
   */
  getProfile: async (req, res) => {
    try {
      const pool = await getConnection();
      const result = await pool.query(`
        SELECT 
          u.UserID,
          u.Username,
          u.Email,
          u.FirstName || ' ' || u.LastName as FullName,
          u.FirstName,
          u.LastName,
          u.Department,
          u.Position,
          u.IsActive,
          u.CreatedAt,
          ur.RoleName
        FROM Users u
        LEFT JOIN UserRoles ur ON u.RoleID = ur.RoleID
        WHERE u.UserID = $1
      `, [req.user.userId]);

      if (result.rows.length === 0) {
        return res.status(404).json({
          success: false,
          message: 'User not found'
        });
      }

      res.json({
        success: true,
        data: result.rows[0]
      });
    } catch (error) {
      console.error('Get profile error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve profile',
        error: error.message
      });
    }
  },

  /**
   * Update user profile
   */
  updateProfile: async (req, res) => {
    try {
      const { firstName, lastName, email } = req.body;

      if (!firstName && !lastName && !email) {
        return res.status(400).json({
          success: false,
          message: 'No fields to update'
        });
      }

      const pool = await getConnection();

      // Check if email is already used by another user
      if (email) {
        const emailCheck = await pool.query(
          'SELECT UserID FROM Users WHERE Email = $1 AND UserID != $2',
          [email, req.user.userId]
        );

        if (emailCheck.rows.length > 0) {
          return res.status(400).json({
            success: false,
            message: 'Email already in use'
          });
        }
      }

      // Build update query
      const updates = [];
      const values = [];
      let paramCount = 1;

      if (firstName) {
        updates.push(`FirstName = $${paramCount}`);
        values.push(firstName);
        paramCount++;
      }

      if (lastName) {
        updates.push(`LastName = $${paramCount}`);
        values.push(lastName);
        paramCount++;
      }

      if (email) {
        updates.push(`Email = $${paramCount}`);
        values.push(email);
        paramCount++;
      }

      updates.push(`UpdatedAt = CURRENT_TIMESTAMP`);
      values.push(req.user.userId);

      await pool.query(`
        UPDATE Users 
        SET ${updates.join(', ')}
        WHERE UserID = $${paramCount}
      `, values);

      res.json({
        success: true,
        message: 'Profile updated successfully'
      });
    } catch (error) {
      console.error('Update profile error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to update profile',
        error: error.message
      });
    }
  },

  /**
   * Change password
   */
  changePassword: async (req, res) => {
    try {
      const { currentPassword, newPassword } = req.body;

      if (!currentPassword || !newPassword) {
        return res.status(400).json({
          success: false,
          message: 'Current and new passwords are required'
        });
      }

      if (newPassword.length < 6) {
        return res.status(400).json({
          success: false,
          message: 'New password must be at least 6 characters'
        });
      }

      const pool = await getConnection();

      // Get current password hash
      const result = await pool.query(
        'SELECT Password FROM Users WHERE UserID = $1',
        [req.user.userId]
      );

      if (result.rows.length === 0) {
        return res.status(404).json({
          success: false,
          message: 'User not found'
        });
      }

      // Verify current password
      const isValidPassword = await bcrypt.compare(
        currentPassword,
        result.rows[0].password
      );

      if (!isValidPassword) {
        return res.status(401).json({
          success: false,
          message: 'Current password is incorrect'
        });
      }

      // Hash new password
      const newPasswordHash = await bcrypt.hash(newPassword, 10);

      // Update password
      await pool.query(
        'UPDATE Users SET Password = $1, UpdatedAt = CURRENT_TIMESTAMP WHERE UserID = $2',
        [newPasswordHash, req.user.userId]
      );

      res.json({
        success: true,
        message: 'Password changed successfully'
      });
    } catch (error) {
      console.error('Change password error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to change password',
        error: error.message
      });
    }
  },

  /**
   * Refresh token
   */
  refreshToken: async (req, res) => {
    try {
      // User is already authenticated via authMiddleware
      const token = jwt.sign(
        {
          userId: req.user.userId,
          username: req.user.username,
          role: req.user.role
        },
        process.env.JWT_SECRET,
        { expiresIn: process.env.JWT_EXPIRES_IN || '24h' }
      );

      res.json({
        success: true,
        message: 'Token refreshed successfully',
        data: { token }
      });
    } catch (error) {
      console.error('Refresh token error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to refresh token',
        error: error.message
      });
    }
  }
};

module.exports = AuthController;
