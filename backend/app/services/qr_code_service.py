"""
QR Code Generation Service
"""
import qrcode
from io import BytesIO
import base64
from typing import Optional
import os

class QRCodeService:
    
    @staticmethod
    def generate_qr_code(
        data: str,
        size: int = 300,
        border: int = 2,
        error_correction: str = 'M'
    ) -> str:
        """
        Generate QR code and return as base64 string
        
        Args:
            data: Data to encode (usually asset ID)
            size: Size of QR code in pixels
            border: Border size
            error_correction: Error correction level (L, M, Q, H)
            
        Returns:
            Base64 encoded PNG image
        """
        # Error correction mapping
        ec_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=ec_map.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
            box_size=10,
            border=border
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Resize if needed
        if size != 300:
            img = img.resize((size, size))
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def generate_qr_code_file(
        data: str,
        filepath: str,
        size: int = 300
    ) -> bool:
        """
        Generate QR code and save to file
        
        Args:
            data: Data to encode
            filepath: Path to save file
            size: Size of QR code
            
        Returns:
            True if successful
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=2
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save
            img.save(filepath)
            return True
            
        except Exception as e:
            print(f"Error generating QR code file: {e}")
            return False
    
    @staticmethod
    def generate_asset_qr(asset_id: str, asset_name: str = None) -> str:
        """
        Generate QR code specifically for assets
        Encodes asset ID and optionally name
        
        Returns:
            Base64 encoded QR code
        """
        if asset_name:
            data = f"ASSET:{asset_id}|NAME:{asset_name}"
        else:
            data = f"ASSET:{asset_id}"
        
        return QRCodeService.generate_qr_code(data, size=300)
    
    @staticmethod
    def generate_bulk_qr_codes(asset_ids: list) -> dict:
        """
        Generate QR codes for multiple assets
        
        Args:
            asset_ids: List of asset IDs
            
        Returns:
            Dictionary mapping asset_id to QR code
        """
        qr_codes = {}
        
        for asset_id in asset_ids:
            try:
                qr_codes[asset_id] = QRCodeService.generate_asset_qr(asset_id)
            except Exception as e:
                print(f"Error generating QR for {asset_id}: {e}")
                qr_codes[asset_id] = None
        
        return qr_codes
    
    @staticmethod
    def decode_asset_qr(qr_data: str) -> dict:
        """
        Decode asset QR code data
        
        Returns:
            Dictionary with asset_id and name
        """
        result = {'asset_id': None, 'name': None}
        
        if qr_data.startswith('ASSET:'):
            parts = qr_data.split('|')
            result['asset_id'] = parts[0].replace('ASSET:', '')
            
            if len(parts) > 1 and 'NAME:' in parts[1]:
                result['name'] = parts[1].replace('NAME:', '')
        
        return result
