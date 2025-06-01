from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class FootfallAnalytics(BaseModel):
    timestamp: datetime
    camera_id: int
    entrance_count: int
    exit_count: int
    current_occupancy: int
    
    class Config:
        schema_extra = {
            "example": {
                "timestamp": datetime.now(),
                "camera_id": 1,
                "entrance_count": 50,
                "exit_count": 30,
                "current_occupancy": 20
            }
        }

class CustomerJourney(BaseModel):
    customer_id: str
    timestamp: datetime
    camera_id: int
    location: Dict[str, float]  # x, y coordinates
    zone: str
    duration: float  # time spent in seconds
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "timestamp": datetime.now(),
                "camera_id": 1,
                "location": {"x": 100.5, "y": 200.5},
                "zone": "electronics",
                "duration": 300.5
            }
        }

class HeatmapData(BaseModel):
    timestamp: datetime
    camera_id: int
    zone: str
    density: float  # 0 to 1
    average_dwell_time: float
    
    class Config:
        schema_extra = {
            "example": {
                "timestamp": datetime.now(),
                "camera_id": 1,
                "zone": "checkout",
                "density": 0.75,
                "average_dwell_time": 180.5
            }
        }

class BehaviorMetrics(BaseModel):
    customer_id: str
    timestamp: datetime
    metrics: Dict[str, float]  # Various behavioral metrics
    notes: str
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "timestamp": datetime.now(),
                "metrics": {
                    "engagement_score": 0.85,
                    "satisfaction_score": 0.9,
                    "loyalty_score": 0.7
                },
                "notes": "Regular customer with high engagement"
            }
        }
