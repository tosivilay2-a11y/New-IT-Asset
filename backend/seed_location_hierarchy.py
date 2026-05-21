"""
Seed Location Hierarchy Data
Populates Countries, Provinces, Companies, and Main Categories
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.country import Country
from app.models.province import Province
from app.models.company import Company
from app.models.main_category import MainCategory

def seed_location_hierarchy():
    db = SessionLocal()
    
    try:
        print("🌱 Seeding location hierarchy data...")
        
        # 1. Seed Countries
        print("\n📍 Creating countries...")
        countries_data = [
            {"countryname": "Lao PDR", "countrycode": "LA"},
            {"countryname": "Thailand", "countrycode": "TH"},
            {"countryname": "Vietnam", "countrycode": "VN"},
            {"countryname": "Cambodia", "countrycode": "KH"},
            {"countryname": "Myanmar", "countrycode": "MM"},
        ]
        
        countries = {}
        for data in countries_data:
            existing = db.query(Country).filter(Country.countrycode == data["countrycode"]).first()
            if not existing:
                country = Country(**data)
                db.add(country)
                db.flush()
                countries[data["countrycode"]] = country
                print(f"  ✅ Created country: {data['countryname']} ({data['countrycode']})")
            else:
                countries[data["countrycode"]] = existing
                print(f"  ⏭️  Country already exists: {data['countryname']}")
        
        db.commit()
        
        # 2. Seed Provinces
        print("\n🏛️  Creating provinces...")
        provinces_data = [
            # Lao PDR provinces
            {"provincename": "Vientiane Capital", "provincecode": "VTE", "countrycode": "LA"},
            {"provincename": "Luang Prabang", "provincecode": "LPB", "countrycode": "LA"},
            {"provincename": "Champasak", "provincecode": "CPS", "countrycode": "LA"},
            {"provincename": "Savannakhet", "provincecode": "SVK", "countrycode": "LA"},
            {"provincename": "Attapeu", "provincecode": "APU", "countrycode": "LA"},
            # Thailand provinces
            {"provincename": "Bangkok", "provincecode": "BKK", "countrycode": "TH"},
            {"provincename": "Chiang Mai", "provincecode": "CNX", "countrycode": "TH"},
            {"provincename": "Phuket", "provincecode": "HKT", "countrycode": "TH"},
        ]
        
        provinces = {}
        for data in provinces_data:
            country = countries.get(data["countrycode"])
            if country:
                existing = db.query(Province).filter(
                    Province.provincecode == data["provincecode"],
                    Province.countryid == country.countryid
                ).first()
                
                if not existing:
                    province = Province(
                        provincename=data["provincename"],
                        provincecode=data["provincecode"],
                        countryid=country.countryid
                    )
                    db.add(province)
                    db.flush()
                    provinces[data["provincecode"]] = province
                    print(f"  ✅ Created province: {data['provincename']} ({data['provincecode']})")
                else:
                    provinces[data["provincecode"]] = existing
                    print(f"  ⏭️  Province already exists: {data['provincename']}")
        
        db.commit()
        
        # 3. Seed Companies
        print("\n🏢 Creating companies...")
        companies_data = [
            {"companyname": "AVIS Rent A Car VTE", "companycode": "AVIS", "provincecode": "VTE"},
            {"companyname": "AVIS Rent A Car LPB", "companycode": "AVLP", "provincecode": "LPB"},
            {"companyname": "Ford Motor Company", "companycode": "FORD", "provincecode": "VTE"},
            {"companyname": "Efgl Corporation", "companycode": "EFGL", "provincecode": "VTE"},
            {"companyname": "Larv Company", "companycode": "LARV", "provincecode": "VTE"},
            {"companyname": "Rmag Industries", "companycode": "RMAG", "provincecode": "VTE"},
            {"companyname": "Common Services", "companycode": "COMN", "provincecode": "VTE"},
        ]
        
        for data in companies_data:
            province = provinces.get(data["provincecode"])
            if province:
                # Check if company with same code and province exists
                existing = db.query(Company).filter(
                    Company.companycode == data["companycode"],
                    Company.provinceid == province.provinceid
                ).first()
                
                if not existing:
                    company = Company(
                        companyname=data["companyname"],
                        companycode=data["companycode"],
                        provinceid=province.provinceid
                    )
                    db.add(company)
                    print(f"  ✅ Created company: {data['companyname']} ({data['companycode']}) in {data['provincecode']}")
                else:
                    print(f"  ⏭️  Company already exists: {data['companyname']} in {data['provincecode']}")
        
        db.commit()
        
        # 4. Seed Main Categories
        print("\n📦 Creating main categories...")
        categories_data = [
            {"categoryname": "Computer", "categorycode": "C", "description": "Desktop computers and workstations"},
            {"categoryname": "Laptop", "categorycode": "L", "description": "Laptop computers and notebooks"},
            {"categoryname": "Monitor", "categorycode": "M", "description": "Display monitors and screens"},
            {"categoryname": "Printer", "categorycode": "P", "description": "Printers and printing devices"},
            {"categoryname": "Network", "categorycode": "N", "description": "Network equipment (routers, switches)"},
            {"categoryname": "Server", "categorycode": "S", "description": "Server hardware"},
            {"categoryname": "Workstation", "categorycode": "W", "description": "High-performance workstations"},
            {"categoryname": "Tablet", "categorycode": "T", "description": "Tablet devices"},
            {"categoryname": "Phone", "categorycode": "H", "description": "Phones and mobile devices"},
            {"categoryname": "Accessory", "categorycode": "A", "description": "Accessories and peripherals"},
            {"categoryname": "Other", "categorycode": "O", "description": "Other equipment"},
            {"categoryname": "Desktop", "categorycode": "D", "description": "Desktop computers"},
            {"categoryname": "UPS", "categorycode": "U", "description": "Uninterruptible Power Supply"},
        ]
        
        for data in categories_data:
            existing = db.query(MainCategory).filter(
                MainCategory.categorycode == data["categorycode"]
            ).first()
            
            if not existing:
                category = MainCategory(**data)
                db.add(category)
                print(f"  ✅ Created category: {data['categoryname']} ({data['categorycode']})")
            else:
                print(f"  ⏭️  Category already exists: {data['categoryname']}")
        
        db.commit()
        
        print("\n✅ Location hierarchy seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"  Countries: {db.query(Country).count()}")
        print(f"  Provinces: {db.query(Province).count()}")
        print(f"  Companies: {db.query(Company).count()}")
        print(f"  Main Categories: {db.query(MainCategory).count()}")
        
    except Exception as e:
        print(f"\n❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_location_hierarchy()
