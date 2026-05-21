"""
Asset ID Generator Service
Format: [Category][Country][Province][Company][Year][Sequence]
Example: MLALPBAVIS25015
- M = Monitor (1 char)
- LA = Lao (2 chars)
- LPB = Luang Prabang (3 chars)
- AVIS = Company (4 chars)
- 25 = Year 2025 (2 chars)
- 015 = Sequence (3 chars)
Total: 15 characters
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from ..models.asset_sequence import AssetSequence
from ..models.country import Country
from ..models.province import Province
from ..models.company import Company
from ..models.main_category import MainCategory
import re

class AssetIDGenerator:
    
    @staticmethod
    def preview_asset_id(
        db: Session,
        main_category: str,
        country_id: int,
        province_id: int,
        company_id: int,
        purchase_date: str = None
    ) -> str:
        """
        Preview asset ID without incrementing sequence
        Used for showing preview in forms before saving
        
        Args:
            db: Database session
            main_category: Main category name (e.g., 'Computer', 'Monitor')
            country_id: Country ID
            province_id: Province ID
            company_id: Company ID
            purchase_date: Purchase date (optional, defaults to today)
            
        Returns:
            Preview of asset ID string
        """
        # Get category code
        category = db.query(MainCategory).filter(
            MainCategory.categoryname == main_category
        ).first()
        if not category:
            raise ValueError(f"Category '{main_category}' not found")
        category_code = category.categorycode
        
        # Get country code
        country = db.query(Country).filter(Country.countryid == country_id).first()
        if not country:
            raise ValueError(f"Country with ID {country_id} not found")
        country_code = country.countrycode
        
        # Get province code
        province = db.query(Province).filter(Province.provinceid == province_id).first()
        if not province:
            raise ValueError(f"Province with ID {province_id} not found")
        province_code = province.provincecode
        
        # Get company code
        company = db.query(Company).filter(Company.companyid == company_id).first()
        if not company:
            raise ValueError(f"Company with ID {company_id} not found")
        company_code = company.companycode
        
        # Get year (2 digits)
        if purchase_date:
            try:
                year = datetime.fromisoformat(purchase_date.replace('Z', '+00:00')).year
            except:
                year = datetime.now().year
        else:
            year = datetime.now().year
        year_code = str(year)[-2:]
        
        # Get next sequence (without incrementing)
        sequence_record = db.query(AssetSequence).filter(
            and_(
                AssetSequence.countryid == country_id,
                AssetSequence.companyid == company_id,
                AssetSequence.sequenceyear == year
            )
        ).first()
        
        next_sequence = (sequence_record.lastsequence + 1) if sequence_record else 1
        sequence_code = str(next_sequence).zfill(3)
        
        # Format: CategoryCode(1) + CountryCode(2) + ProvinceCode(3) + CompanyCode(4) + Year(2) + Sequence(3)
        asset_id = f"{category_code}{country_code}{province_code}{company_code}{year_code}{sequence_code}"
        
        return asset_id
    
    @staticmethod
    def generate_asset_id(
        db: Session,
        main_category: str,
        country_id: int,
        province_id: int,
        company_id: int,
        purchase_date: str = None
    ) -> str:
        """
        Generate unique asset ID and increment sequence
        ONLY call when actually saving the asset!
        
        Args:
            db: Database session
            main_category: Main category name (e.g., 'Computer', 'Monitor')
            country_id: Country ID
            province_id: Province ID
            company_id: Company ID
            purchase_date: Purchase date (optional, defaults to today)
            
        Returns:
            Generated asset ID string
        """
        # Get category code
        category = db.query(MainCategory).filter(
            MainCategory.categoryname == main_category
        ).first()
        if not category:
            raise ValueError(f"Category '{main_category}' not found")
        category_code = category.categorycode
        
        # Get country code
        country = db.query(Country).filter(Country.countryid == country_id).first()
        if not country:
            raise ValueError(f"Country with ID {country_id} not found")
        country_code = country.countrycode
        
        # Get province code
        province = db.query(Province).filter(Province.provinceid == province_id).first()
        if not province:
            raise ValueError(f"Province with ID {province_id} not found")
        province_code = province.provincecode
        
        # Get company code
        company = db.query(Company).filter(Company.companyid == company_id).first()
        if not company:
            raise ValueError(f"Company with ID {company_id} not found")
        company_code = company.companycode
        
        # Get year (2 digits)
        if purchase_date:
            try:
                year = datetime.fromisoformat(purchase_date.replace('Z', '+00:00')).year
            except:
                year = datetime.now().year
        else:
            year = datetime.now().year
        year_code = str(year)[-2:]
        
        # Get or create sequence record
        sequence_record = db.query(AssetSequence).filter(
            and_(
                AssetSequence.countryid == country_id,
                AssetSequence.companyid == company_id,
                AssetSequence.sequenceyear == year
            )
        ).first()
        
        if not sequence_record:
            # Create new sequence record
            sequence_record = AssetSequence(
                countryid=country_id,
                companyid=company_id,
                sequenceyear=year,
                year=year,
                lastsequence=1
            )
            db.add(sequence_record)
            db.flush()
            sequence_num = 1
        else:
            # Increment existing sequence
            sequence_record.lastsequence += 1
            sequence_record.updatedat = datetime.utcnow()
            db.flush()
            sequence_num = sequence_record.lastsequence
        
        sequence_code = str(sequence_num).zfill(3)
        
        # Format: CategoryCode(1) + CountryCode(2) + ProvinceCode(3) + CompanyCode(4) + Year(2) + Sequence(3)
        asset_id = f"{category_code}{country_code}{province_code}{company_code}{year_code}{sequence_code}"
        
        db.commit()
        return asset_id
    
    @staticmethod
    def validate_asset_id(asset_id: str) -> bool:
        """
        Validate asset ID format
        Format: 15 characters total
        [Category(1)][Country(2)][Province(3)][Company(4)][Year(2)][Sequence(3)]
        
        Returns:
            True if valid, False otherwise
        """
        # Pattern: 1 letter + 2 letters + 3 letters + 4 letters + 2 digits + 3 digits = 15 chars
        pattern = r'^[A-Z]{1}[A-Z]{2}[A-Z]{3}[A-Z]{4}\d{2}\d{3}$'
        return bool(re.match(pattern, asset_id))
    
    @staticmethod
    def parse_asset_id(asset_id: str) -> dict:
        """
        Parse asset ID into components
        
        Returns:
            Dictionary with parsed components
        """
        if len(asset_id) != 15:
            return None
        
        return {
            'category_code': asset_id[0:1],
            'country_code': asset_id[1:3],
            'province_code': asset_id[3:6],
            'company_code': asset_id[6:10],
            'year': int('20' + asset_id[10:12]),
            'sequence': int(asset_id[12:15])
        }
    
    @staticmethod
    def get_next_sequence(db: Session, country_id: int, company_id: int) -> int:
        """
        Get next sequence number without incrementing
        
        Returns:
            Next sequence number
        """
        current_year = datetime.now().year
        
        sequence = db.query(AssetSequence).filter(
            and_(
                AssetSequence.countryid == country_id,
                AssetSequence.companyid == company_id,
                AssetSequence.sequenceyear == current_year
            )
        ).first()
        
        if not sequence:
            return 1
        
        return sequence.lastsequence + 1
