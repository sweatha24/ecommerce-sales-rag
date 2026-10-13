import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

load_dotenv()

# Setup logging for connection & execution errors
logging.basicConfig(
    filename='app_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("DB_NAME", "ecommerce_db")
        self.client = None
        self.db = None

    def connect(self):
        """Establishes a pooled connection to MongoDB Atlas or Local MongoDB."""
        try:
            # Connection pooling configured via maxPoolSize
            self.client = MongoClient(
                self.uri, 
                maxPoolSize=50, 
                minPoolSize=10, 
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client[self.db_name]
            # Ping database to confirm connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB.")
            return self.db
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            print("Database Connection Error. Check app_errors.log for details.")
            raise e

    def apply_schema_validation(self):
        """Enforces schema validation rules on the sales collection."""
        sales_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["order_id", "store_id", "total_amount", "items"],
                "properties": {
                    "order_id": {"bsonType": "string"},
                    "store_id": {"bsonType": "string"},
                    "total_amount": {"bsonType": "double"},
                    "items": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["product_id", "quantity", "price"],
                            "properties": {
                                "product_id": {"bsonType": "string"},
                                "quantity": {"bsonType": "int"},
                                "price": {"bsonType": "double"}
                            }
                        }
                    }
                }
            }
        }
        try:
            self.db.command('collMod', 'sales', validator=sales_validator)
            print("Schema validation successfully applied to 'sales' collection.")
        except OperationFailure:
            self.db.create_collection('sales', validator=sales_validator)
            print("Created 'sales' collection with schema validation.")