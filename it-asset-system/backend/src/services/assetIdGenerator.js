const { sql, getConnection } = require('../config/database');

/**
 * Asset ID Generator Service
 * Format: [Category][Country][Province][Company][Year][Sequence]
 * Example: COMP-TH-BKK-ABC-2026-0001
 */

const AssetIdGenerator = {
  /**
   * Generate next Asset ID
   * @param {Object} params - { mainCategoryId, countryId, provinceId, companyId }
   * @returns {String} Generated Asset ID
   */
  generateAssetId: async (params) => {
    const { mainCategoryId, countryId, provinceId, companyId } = params;
    
    try {
      const pool = await getConnection();
      
      // Get category code
      const categoryResult = await pool.request()
        .input('mainCategoryId', sql.Int, mainCategoryId)
        .query('SELECT CategoryCode FROM MainCategories WHERE MainCategoryID = @mainCategoryId');
      
      if (!categoryResult.recordset[0]) {
        throw new Error('Main category not found');
      }
      const categoryCode = categoryResult.recordset[0].CategoryCode;
      
      // Get country code
      const countryResult = await pool.request()
        .input('countryId', sql.Int, countryId)
        .query('SELECT CountryCode FROM Countries WHERE CountryID = @countryId');
      
      if (!countryResult.recordset[0]) {
        throw new Error('Country not found');
      }
      const countryCode = countryResult.recordset[0].CountryCode;
      
      // Get province code
      const provinceResult = await pool.request()
        .input('provinceId', sql.Int, provinceId)
        .query('SELECT ProvinceCode FROM Provinces WHERE ProvinceID = @provinceId');
      
      if (!provinceResult.recordset[0]) {
        throw new Error('Province not found');
      }
      const provinceCode = provinceResult.recordset[0].ProvinceCode;
      
      // Get company code
      const companyResult = await pool.request()
        .input('companyId', sql.Int, companyId)
        .query('SELECT CompanyCode FROM Companies WHERE CompanyID = @companyId');
      
      if (!companyResult.recordset[0]) {
        throw new Error('Company not found');
      }
      const companyCode = companyResult.recordset[0].CompanyCode;
      
      // Get current year
      const year = new Date().getFullYear();
      
      // Get or create sequence
      const sequence = await AssetIdGenerator.getNextSequence(
        mainCategoryId,
        countryId,
        provinceId,
        companyId,
        year
      );
      
      // Format: COMP-TH-BKK-ABC-2026-0001
      const assetId = `${categoryCode}-${countryCode}-${provinceCode}-${companyCode}-${year}-${sequence}`;
      
      return assetId;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get next sequence number
   * @param {Number} mainCategoryId
   * @param {Number} countryId
   * @param {Number} provinceId
   * @param {Number} companyId
   * @param {Number} year
   * @returns {String} Formatted sequence (e.g., "0001")
   */
  getNextSequence: async (mainCategoryId, countryId, provinceId, companyId, year) => {
    try {
      const pool = await getConnection();
      
      // Check if sequence exists
      const existingSeq = await pool.request()
        .input('mainCategoryId', sql.Int, mainCategoryId)
        .input('countryId', sql.Int, countryId)
        .input('provinceId', sql.Int, provinceId)
        .input('companyId', sql.Int, companyId)
        .input('year', sql.Int, year)
        .query(`
          SELECT CurrentSequence 
          FROM AssetSequences 
          WHERE MainCategoryID = @mainCategoryId 
            AND CountryID = @countryId 
            AND ProvinceID = @provinceId 
            AND CompanyID = @companyId 
            AND Year = @year
        `);
      
      let nextSequence;
      
      if (existingSeq.recordset.length > 0) {
        // Update existing sequence
        const currentSeq = existingSeq.recordset[0].CurrentSequence;
        nextSequence = currentSeq + 1;
        
        await pool.request()
          .input('mainCategoryId', sql.Int, mainCategoryId)
          .input('countryId', sql.Int, countryId)
          .input('provinceId', sql.Int, provinceId)
          .input('companyId', sql.Int, companyId)
          .input('year', sql.Int, year)
          .input('nextSequence', sql.Int, nextSequence)
          .query(`
            UPDATE AssetSequences 
            SET CurrentSequence = @nextSequence, 
                UpdatedAt = GETDATE()
            WHERE MainCategoryID = @mainCategoryId 
              AND CountryID = @countryId 
              AND ProvinceID = @provinceId 
              AND CompanyID = @companyId 
              AND Year = @year
          `);
      } else {
        // Create new sequence
        nextSequence = 1;
        
        await pool.request()
          .input('mainCategoryId', sql.Int, mainCategoryId)
          .input('countryId', sql.Int, countryId)
          .input('provinceId', sql.Int, provinceId)
          .input('companyId', sql.Int, companyId)
          .input('year', sql.Int, year)
          .input('currentSequence', sql.Int, nextSequence)
          .query(`
            INSERT INTO AssetSequences (
              MainCategoryID, CountryID, ProvinceID, CompanyID, Year, CurrentSequence
            ) VALUES (
              @mainCategoryId, @countryId, @provinceId, @companyId, @year, @currentSequence
            )
          `);
      }
      
      // Format sequence with leading zeros (4 digits)
      return nextSequence.toString().padStart(4, '0');
    } catch (error) {
      throw error;
    }
  },

  /**
   * Preview Asset ID without incrementing sequence
   * @param {Object} params - { mainCategoryId, countryId, provinceId, companyId }
   * @returns {String} Preview of Asset ID
   */
  previewAssetId: async (params) => {
    const { mainCategoryId, countryId, provinceId, companyId } = params;
    
    try {
      const pool = await getConnection();
      
      // Get codes
      const categoryResult = await pool.request()
        .input('mainCategoryId', sql.Int, mainCategoryId)
        .query('SELECT CategoryCode FROM MainCategories WHERE MainCategoryID = @mainCategoryId');
      const categoryCode = categoryResult.recordset[0]?.CategoryCode || 'XXX';
      
      const countryResult = await pool.request()
        .input('countryId', sql.Int, countryId)
        .query('SELECT CountryCode FROM Countries WHERE CountryID = @countryId');
      const countryCode = countryResult.recordset[0]?.CountryCode || 'XX';
      
      const provinceResult = await pool.request()
        .input('provinceId', sql.Int, provinceId)
        .query('SELECT ProvinceCode FROM Provinces WHERE ProvinceID = @provinceId');
      const provinceCode = provinceResult.recordset[0]?.ProvinceCode || 'XXX';
      
      const companyResult = await pool.request()
        .input('companyId', sql.Int, companyId)
        .query('SELECT CompanyCode FROM Companies WHERE CompanyID = @companyId');
      const companyCode = companyResult.recordset[0]?.CompanyCode || 'XXX';
      
      const year = new Date().getFullYear();
      
      // Get current sequence (without incrementing)
      const seqResult = await pool.request()
        .input('mainCategoryId', sql.Int, mainCategoryId)
        .input('countryId', sql.Int, countryId)
        .input('provinceId', sql.Int, provinceId)
        .input('companyId', sql.Int, companyId)
        .input('year', sql.Int, year)
        .query(`
          SELECT CurrentSequence 
          FROM AssetSequences 
          WHERE MainCategoryID = @mainCategoryId 
            AND CountryID = @countryId 
            AND ProvinceID = @provinceId 
            AND CompanyID = @companyId 
            AND Year = @year
        `);
      
      const nextSeq = seqResult.recordset.length > 0 
        ? seqResult.recordset[0].CurrentSequence + 1 
        : 1;
      
      const sequence = nextSeq.toString().padStart(4, '0');
      
      return `${categoryCode}-${countryCode}-${provinceCode}-${companyCode}-${year}-${sequence}`;
    } catch (error) {
      throw error;
    }
  }
};

module.exports = AssetIdGenerator;
