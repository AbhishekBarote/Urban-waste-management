# mumbai.py
import pandas as pd
from sqlalchemy import create_engine, text
import json

# Database configuration
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "abhi1234",
    "database": "food_demand_db"
}

# Create database connection
engine = create_engine(
    f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
)

def create_charities_table():
    """Create Charities table if not exists"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Charities (
        charity_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address TEXT,
        area VARCHAR(100),
        contact_phone VARCHAR(20),
        contact_email VARCHAR(100),
        accepted_categories JSON,
        operating_hours JSON,
        capacity_kg DECIMAL(10,2),
        latitude DECIMAL(9,6),
        longitude DECIMAL(9,6),
        verification_status ENUM('verified', 'unverified') DEFAULT 'unverified',
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_query))
        conn.commit()
    print("Charities table created successfully")

def insert_sample_charities():
    """Insert sample Mumbai charity data with verification"""
    charities = [
        {
            "name": "Robin Hood Army - Mumbai Chapter",
            "address": "Various locations across Mumbai",
            "area": "Multiple",
            "contact_phone": "+912266665555",
            "contact_email": "mumbai@robinhoodarmy.com",
            "accepted_categories": ["cooked_food", "packaged_goods"],
            "operating_hours": {"weekdays": "18:00-22:00", "weekends": "10:00-22:00"},
            "capacity_kg": 1000,
            "latitude": 19.0760,
            "longitude": 72.8777,
            "verification_status": "verified"
        },
        {
            "name": "ISKCON Mumbai Food Relief",
            "address": "Hare Krishna Land, Juhu, Mumbai",
            "area": "Juhu",
            "contact_phone": "+912226203123",
            "contact_email": "food@iskconmumbai.com",
            "accepted_categories": ["raw_grains", "vegetables", "cooked_food"],
            "operating_hours": {"daily": "06:00-21:00"},
            "capacity_kg": 2000,
            "latitude": 19.1077,
            "longitude": 72.8263,
            "verification_status": "verified"
        },
        {
            "name": "NGO Darpan Registered Organization",
            "address": "Dharavi Cross Road, Mumbai",
            "area": "Dharavi",
            "contact_phone": "+912224067890",
            "contact_email": "info@dharavifoodbank.org",
            "accepted_categories": ["packaged_goods", "dry_rations"],
            "operating_hours": {"weekdays": "10:00-18:00"},
            "capacity_kg": 500,
            "latitude": 19.0392,
            "longitude": 72.8527,
            "verification_status": "verified"
        },
        {
            "name": "Sion Hospital Food Bank",
            "address": "Sion Hospital Complex, Sion",
            "area": "Sion",
            "contact_phone": "+912224055555",
            "accepted_categories": ["cooked_food", "fruits"],
            "operating_hours": {"daily": "24_hours"},
            "capacity_kg": 800,
            "latitude": 19.0400,
            "longitude": 72.8600,
            "verification_status": "verified"
        },
        {
            "name": "Mumbai Dabbawala Food Redistribution",
            "address": "Churchgate Station, Mumbai",
            "area": "South Mumbai",
            "contact_phone": "+912222832456",
            "accepted_categories": ["cooked_food", "fresh_meals"],
            "operating_hours": {"weekdays": "13:00-16:00"},
            "capacity_kg": 300,
            "latitude": 18.9356,
            "longitude": 72.8256,
            "verification_status": "verified"
        },
        {
            "name": "Akshaya Patra Foundation - Mumbai",
            "address": "Saki Vihar Road, Andheri East",
            "area": "Andheri",
            "contact_phone": "+912226785555",
            "contact_email": "mumbai@akshayapatra.org",
            "accepted_categories": ["raw_grains", "vegetables", "cooking_oil"],
            "operating_hours": {"daily": "07:00-19:00"},
            "capacity_kg": 5000,
            "latitude": 19.1179,
            "longitude": 72.8790,
            "verification_status": "verified"
        },
        {
            "name": "Smile Foundation - Mumbai Food Program",
            "address": "Bandra Kurla Complex, Bandra East",
            "area": "Bandra",
            "contact_phone": "+912226555123",
            "contact_email": "food@smilefoundationmum.in",
            "accepted_categories": ["packaged_goods", "dry_fruits"],
            "operating_hours": {"weekdays": "10:00-18:00"},
            "capacity_kg": 1500,
            "latitude": 19.0665,
            "longitude": 72.8647,
            "verification_status": "verified"
        },
        {
            "name": "Sion Community Kitchen",
            "address": "Sion Fort Road, Sion West",
            "area": "Sion",
            "contact_phone": "+912224567890",
            "accepted_categories": ["cooked_food", "bread"],
            "operating_hours": {"daily": "18:00-22:00"},
            "capacity_kg": 400,
            "latitude": 19.0428,
            "longitude": 72.8612,
            "verification_status": "verified"
        },
        {
            "name": "Colaba Food Bank",
            "address": "Shahid Bhagat Singh Rd, Colaba",
            "area": "South Mumbai",
            "contact_phone": "+912222123456",
            "contact_email": "info@colabafoodbank.org",
            "accepted_categories": ["canned_goods", "biscuits"],
            "operating_hours": {"daily": "09:00-21:00"},
            "capacity_kg": 750,
            "latitude": 18.9063,
            "longitude": 72.8109,
            "verification_status": "verified"
        },
        {
            "name": "Dharavi Women's Collective Kitchen",
            "address": "90 Feet Road, Dharavi",
            "area": "Dharavi",
            "contact_phone": "+919876543210",
            "accepted_categories": ["vegetables", "flour", "spices"],
            "operating_hours": {"weekdays": "08:00-17:00"},
            "capacity_kg": 300,
            "latitude": 19.0400,
            "longitude": 72.8550,
            "verification_status": "verified"
        }
    ]

    # Convert JSON fields to strings
    for charity in charities:
        charity['accepted_categories'] = json.dumps(charity['accepted_categories'])
        charity['operating_hours'] = json.dumps(charity['operating_hours'])

    df = pd.DataFrame(charities)
    
    # Insert data
    with engine.connect() as conn:
        df.to_sql(
            name='Charities',
            con=conn,
            if_exists='append',
            index=False,
            method='multi'
        )
        print(f"Successfully inserted {len(df)} verified charity records")

if __name__ == "__main__":
    create_charities_table()
    insert_sample_charities()
    print("Database setup completed successfully")