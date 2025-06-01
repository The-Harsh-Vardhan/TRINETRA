from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import motor.motor_asyncio
import json
import os
from bson import ObjectId

from models.database import Base, Customer, Transaction, EmotionRecord, Vehicle, Camera
from models.analytics import FootfallAnalytics, CustomerJourney, HeatmapData, BehaviorMetrics
from database.session import get_db

app = FastAPI(title="TRINETRA API", description="Backend API for TRINETRA Surveillance System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
analytics_db = client.trinetra_analytics

# Basic health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "TRINETRA API is running"}

# Camera endpoints
@app.get("/api/camera-config")
async def get_camera_config():
    """Get camera configuration"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'camera_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return JSONResponse(content=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/api/stats")
async def get_current_stats():
    """Get current statistics"""
    try:
        stats = await analytics_db.stats.find_one(
            sort=[('timestamp', -1)]
        )
        if not stats:
            return {
                "people_inside": 0,
                "daily_footfall": 0,
                "active_staff": 0
            }
        return {
            "people_inside": stats.get("people_inside", 0),
            "daily_footfall": stats.get("daily_footfall", 0),
            "active_staff": stats.get("active_staff", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/footfall")
async def get_footfall_analytics(
    start_date: datetime = None,
    end_date: datetime = None,
    camera_id: int = None
):
    """Get footfall analytics data"""
    try:
        query = {}
        if start_date:
            query["timestamp"] = {"$gte": start_date}
        if end_date:
            query["timestamp"] = {"$lte": end_date}
        if camera_id is not None:
            query["camera_id"] = camera_id
            
        cursor = analytics_db.footfall.find(query).sort("timestamp", 1)
        data = await cursor.to_list(length=1000)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Customer endpoints
@app.get("/api/customers")
async def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of customers"""
    try:
        customers = db.query(Customer).offset(skip).limit(limit).all()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get customer details"""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vehicle endpoints
@app.get("/api/vehicles")
async def get_vehicles(
    license_plate: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get vehicle records"""
    try:
        query = db.query(Vehicle)
        if license_plate:
            query = query.filter(Vehicle.license_plate.ilike(f"%{license_plate}%"))
        vehicles = query.offset(skip).limit(limit).all()
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Transaction endpoints
@app.get("/transactions/", response_model=List[dict])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    customer_id: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    if customer_id:
        query = query.filter(Transaction.customer_id == customer_id)
    transactions = query.offset(skip).limit(limit).all()
    return transactions

# Emotion analytics endpoints
@app.get("/emotions/{customer_id}")
async def get_customer_emotions(
    customer_id: str,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(EmotionRecord).filter(EmotionRecord.customer_id == customer_id)
    if start_date and end_date:
        query = query.filter(
            EmotionRecord.timestamp >= start_date,
            EmotionRecord.timestamp <= end_date
        )
    emotions = query.all()
    return emotions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
