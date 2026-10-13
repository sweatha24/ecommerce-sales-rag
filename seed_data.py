import os
from datetime import datetime
from dotenv import load_dotenv
from config.database import DatabaseManager

# Load environment variables from .env
load_dotenv()

def seed_database():
    print("Connecting to MongoDB Atlas...")
    db_mgr = DatabaseManager()
    db = db_mgr.connect()
    
    # Apply MongoDB schema validation
    db_mgr.apply_schema_validation()

    sales_col = db['sales']
    
    # Clear existing data to prevent duplicate primary keys
    sales_col.delete_many({})

    # Sample transaction dataset
    sample_orders = [
        {
            "order_id": "ORD-1001",
            "store_id": "STORE-NORTH",
            "total_amount": 250.00,
            "created_at": datetime.utcnow().isoformat(),
            "items": [
                {"product_id": "P-101", "quantity": 2, "price": 100.00},
                {"product_id": "P-102", "quantity": 1, "price": 50.00}
            ]
        },
        {
            "order_id": "ORD-1002",
            "store_id": "STORE-NORTH",
            "total_amount": 150.00,
            "created_at": datetime.utcnow().isoformat(),
            "items": [
                {"product_id": "P-103", "quantity": 3, "price": 50.00}
            ]
        },
        {
            "order_id": "ORD-1003",
            "store_id": "STORE-SOUTH",
            "total_amount": 500.00,
            "created_at": datetime.utcnow().isoformat(),
            "items": [
                {"product_id": "P-104", "quantity": 1, "price": 500.00}
            ]
        },
        {
            "order_id": "ORD-1004",
            "store_id": "STORE-SOUTH",
            "total_amount": 80.00,
            "created_at": datetime.utcnow().isoformat(),
            "items": [
                {"product_id": "P-101", "quantity": 2, "price": 40.00}
            ]
        }
    ]

    sales_col.insert_many(sample_orders)
    print(f"Successfully seeded {len(sample_orders)} sample sales transactions into MongoDB!")

if __name__ == "__main__":
    seed_database()