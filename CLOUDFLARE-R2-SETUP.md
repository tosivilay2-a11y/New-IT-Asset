# Cloudflare R2 File Storage Setup

This guide explains how to configure Cloudflare R2 for file storage in the IT Asset Management System.

## Features Added

✅ **Dual Storage Support**: Choose between local storage or Cloudflare R2  
✅ **Configuration UI**: Easy-to-use web interface for setup  
✅ **Connection Testing**: Test your R2 configuration before saving  
✅ **Secure Credentials**: Encrypted storage of sensitive keys  
✅ **Automatic Fallback**: Falls back to local storage if R2 fails  

## Backend Components

### 1. Configuration Management
- **Models**: `backend/app/models/system_config.py` - Database model for storing configurations
- **Schemas**: `backend/app/schemas/system_config.py` - Pydantic schemas for API validation
- **Routes**: `backend/app/routes/config.py` - API endpoints for configuration management

### 2. Cloud Storage Service
- **Service**: `backend/app/services/cloud_storage_service.py` - Unified storage service supporting both local and R2
- **Integration**: Updated `file_upload_service.py` to use the new cloud storage service

### 3. Configuration
- **Settings**: Updated `backend/app/core/config.py` to include R2 settings
- **Environment**: Added R2 configuration to `.env` file

## Frontend Components

### 1. Storage Configuration Page
- **Component**: `frontend/src/pages/StorageConfig.jsx` - Main configuration interface
- **Styles**: `frontend/src/pages/StorageConfig.css` - Styling for the configuration page
- **API**: Added `configAPI` to `frontend/src/services/api.js`

### 2. Navigation Integration
- **Routes**: Added storage config route to `App.js`
- **Admin Panel**: Integrated storage config into the system configuration tabs

## Setup Instructions

### Step 1: Cloudflare R2 Setup

1. **Create Cloudflare Account**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
   - Sign up or log in to your account

2. **Enable R2 Storage**
   - Navigate to R2 Object Storage in the sidebar
   - Create a new bucket or use an existing one
   - Note your bucket name

3. **Create API Token**
   - Go to "Manage R2 API tokens"
   - Click "Create API token"
   - Set permissions: Object Read & Write
   - Note your Account ID, Access Key ID, and Secret Access Key

### Step 2: Backend Configuration

1. **Install Dependencies**
   ```bash
   pip install boto3==1.34.34 botocore==1.34.34
   ```

2. **Update Environment Variables**
   Add to your `backend/.env` file:
   ```env
   # File Storage Configuration
   STORAGE_TYPE=r2
   
   # Cloudflare R2 Configuration
   R2_ACCOUNT_ID=your-account-id
   R2_ACCESS_KEY_ID=your-access-key-id
   R2_SECRET_ACCESS_KEY=your-secret-access-key
   R2_BUCKET_NAME=your-bucket-name
   R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
   R2_PUBLIC_URL=https://your-domain.com
   ```

3. **Create Database Table**
   ```bash
   python backend/create_system_config_table.py
   ```

### Step 3: Frontend Configuration

1. **Access Configuration Page**
   - Start the frontend: `npm start`
   - Navigate to Admin → File Storage
   - Or go directly to `/admin/storage`

2. **Configure Storage**
   - Select "Cloudflare R2" as storage type
   - Fill in your R2 credentials
   - Click "Test Connection" to verify
   - Save configuration

### Step 4: Testing

1. **Test File Upload**
   - Create a new asset with a PO attachment
   - Verify the file is uploaded to R2
   - Check that the file URL is returned correctly

2. **Verify Storage**
   - Check your R2 bucket for uploaded files
   - Files should be stored in `po_attachments/` folder

## Configuration Options

### Storage Types

**Local Storage**
- Files stored on server filesystem
- Path: `backend/uploads/po_attachments/`
- Pros: Simple, no external dependencies
- Cons: Limited scalability, backup complexity

**Cloudflare R2**
- Files stored in R2 object storage
- S3-compatible API
- Pros: Scalable, fast, cost-effective, global CDN
- Cons: Requires setup and credentials

### R2 Configuration Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| Account ID | Yes | Your Cloudflare account ID | `abc123def456` |
| Access Key ID | Yes | R2 API token access key | `R2_ACCESS_KEY_123` |
| Secret Access Key | Yes | R2 API token secret | `secret_key_456` |
| Bucket Name | Yes | Name of your R2 bucket | `my-assets-bucket` |
| Endpoint URL | Yes | R2 endpoint for your account | `https://abc123.r2.cloudflarestorage.com` |
| Public URL | No | Custom domain or R2.dev URL | `https://files.mycompany.com` |

## API Endpoints

### Configuration Management
- `GET /config/storage` - Get current storage configuration
- `POST /config/storage` - Update storage configuration
- `POST /config/storage/test` - Test storage connection
- `GET /config/` - Get all configurations
- `POST /config/` - Create new configuration
- `PUT /config/{key}` - Update specific configuration
- `DELETE /config/{key}` - Delete configuration

### Example API Usage

```javascript
// Get current storage config
const config = await configAPI.getStorageConfig();

// Update storage config
const newConfig = {
  storage_type: "r2",
  r2_account_id: "your-account-id",
  r2_access_key_id: "your-access-key",
  r2_secret_access_key: "your-secret-key",
  r2_bucket_name: "your-bucket",
  r2_endpoint_url: "https://your-account.r2.cloudflarestorage.com",
  r2_public_url: "https://your-domain.com"
};
await configAPI.updateStorageConfig(newConfig);

// Test connection
const testResult = await configAPI.testStorageConfig(newConfig);
```

## Security Considerations

1. **Credential Protection**
   - Secret keys are masked in the UI
   - Sensitive data marked as encrypted in database
   - Environment variables used for initial setup

2. **Access Control**
   - Configuration endpoints require authentication
   - Only admin users should access storage configuration

3. **File Security**
   - File uploads validated for type and size
   - Directory traversal protection
   - Unique filenames prevent conflicts

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify account ID and credentials
   - Check bucket name and permissions
   - Ensure endpoint URL is correct

2. **Files Not Uploading**
   - Check file size limits (10MB default)
   - Verify allowed file types
   - Check R2 bucket permissions

3. **Public URLs Not Working**
   - Configure custom domain in Cloudflare
   - Set up R2.dev subdomain
   - Check CORS settings if needed

### Debug Steps

1. **Test Connection**
   - Use the "Test Connection" button in the UI
   - Check browser console for errors
   - Review backend logs

2. **Verify Configuration**
   - Check environment variables
   - Verify database configuration
   - Test with minimal R2 setup

3. **File Upload Testing**
   - Try uploading small files first
   - Check R2 bucket contents
   - Verify file URLs are accessible

## Migration from Local Storage

1. **Backup Existing Files**
   ```bash
   cp -r backend/uploads/po_attachments/ backup/
   ```

2. **Configure R2**
   - Set up R2 bucket and credentials
   - Test connection thoroughly

3. **Update Configuration**
   - Change storage type to "r2"
   - Save and test configuration

4. **Optional: Migrate Files**
   - Upload existing files to R2
   - Update database file paths
   - Verify all files accessible

## Cost Considerations

Cloudflare R2 pricing (as of 2024):
- Storage: $0.015/GB/month
- Class A operations: $4.50/million
- Class B operations: $0.36/million
- Egress: Free (major advantage over AWS S3)

For typical asset management usage:
- 1000 files × 1MB average = ~$0.015/month storage
- File uploads/downloads: minimal cost
- No egress charges for file downloads

## Support

For issues with this implementation:
1. Check the troubleshooting section above
2. Review backend logs for detailed error messages
3. Test with minimal configuration first
4. Verify Cloudflare R2 setup independently

For Cloudflare R2 specific issues:
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [Cloudflare Community](https://community.cloudflare.com/)
- [R2 API Reference](https://developers.cloudflare.com/r2/api/)