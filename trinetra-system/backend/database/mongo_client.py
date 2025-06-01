from pymongo import MongoClient
from typing import Dict, Any

class MongoDB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['trinetra']
        
        # Initialize collections
        self.footfall = self.db['footfall']
        self.customer_journeys = self.db['customer_journeys']
        self.heatmap = self.db['heatmap']
        self.behavior_metrics = self.db['behavior_metrics']

    async def insert_footfall(self, data: Dict[str, Any]):
        return self.footfall.insert_one(data)

    async def insert_customer_journey(self, data: Dict[str, Any]):
        return self.customer_journeys.insert_one(data)

    async def insert_heatmap_data(self, data: Dict[str, Any]):
        return self.heatmap.insert_one(data)

    async def insert_behavior_metric(self, data: Dict[str, Any]):
        return self.behavior_metrics.insert_one(data)

    async def get_daily_footfall(self, date: str):
        return self.footfall.find({'date': date})

    async def get_customer_journey(self, customer_id: str):
        return self.customer_journeys.find({'customer_id': customer_id})

mongodb = MongoDB()
