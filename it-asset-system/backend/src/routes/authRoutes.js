const express = require('express');
const router = express.Router();
const AuthController = require('../controllers/authController');
const { authMiddleware } = require('../middleware/authMiddleware');

/**
 * Authentication Routes
 */

// Login
router.post('/login', AuthController.login);

// Register
router.post('/register', AuthController.register);

// Get current user profile (requires authentication)
router.get('/profile', authMiddleware, AuthController.getProfile);

// Update profile (requires authentication)
router.put('/profile', authMiddleware, AuthController.updateProfile);

// Change password (requires authentication)
router.post('/change-password', authMiddleware, AuthController.changePassword);

// Refresh token (requires authentication)
router.post('/refresh-token', authMiddleware, AuthController.refreshToken);

module.exports = router;
