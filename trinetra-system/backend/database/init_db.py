from database.session import engine
from models.database import Base
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Create SQL tables
def init_sql_db():
    Base.metadata.create_all(bind=engine)
    print("SQL Database tables created successfully!")

# Initialize MongoDB collections
async def init_mongo_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.trinetra_analytics
    
    # Create collections if they don't exist
    collections = [
        "footfall",
        "customer_journeys",
        "heatmap",
        "behavior_metrics",
        "emotions"
    ]
    
    for collection in collections:
        if collection not in await db.list_collection_names():
            await db.create_collection(collection)
    
    # Create indexes
    await db.footfall.create_index("timestamp")
    await db.customer_journeys.create_index("customer_id")
    await db.heatmap.create_index([("camera_id", 1), ("timestamp", -1)])
    await db.behavior_metrics.create_index("customer_id")
    
    print("MongoDB collections and indexes created successfully!")

if __name__ == "__main__":
    # Initialize SQL database
    init_sql_db()
    
    # Initialize MongoDB
    asyncio.run(init_mongo_db())
