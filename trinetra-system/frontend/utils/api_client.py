import requests
from datetime import datetime
from typing import Dict, List, Optional

class TRINETRAAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            return None
    
    def check_health(self) -> bool:
        """Check if the API is running"""
        try:
            result = self._make_request("GET", "/")
            return result is not None and result.get("status") == "ok"
        except:
            return False
            
    def get_cameras(self) -> List[Dict]:
        """Get camera configuration"""
        result = self._make_request("GET", "/api/camera-config")
        if result and 'cameras' in result:
            return result['cameras']
        return []
            response = self._make_request("GET", "/")
            return response is not None and response.get("status") == "ok"
        except:
            return False
    
    def get_camera_config(self) -> Dict:
        """Get camera configuration"""
        return self._make_request("GET", "/api/camera-config") or {}
    
    def get_current_stats(self) -> Dict:
        """Get current statistics"""
        return self._make_request("GET", "/api/stats") or {
            "people_inside": 0,
            "daily_footfall": 0,
            "active_staff": 0
        }
    
    def get_footfall_analytics(self, start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None,
                             camera_id: Optional[int] = None) -> List[Dict]:
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        if camera_id:
            params["camera_id"] = camera_id
        return self._make_request("GET", "/analytics/footfall", params=params)
    
    def get_heatmap_data(self, camera_id: int, timestamp: Optional[datetime] = None) -> List[Dict]:
        params = {"camera_id": camera_id}
        if timestamp:
            params["timestamp"] = timestamp.isoformat()
        return self._make_request("GET", "/analytics/heatmap", params=params)
    
    def get_customer_journey(self, customer_id: str) -> List[Dict]:
        return self._make_request("GET", f"/analytics/customer-journey/{customer_id}")
    
    # Camera endpoints
    def get_cameras(self) -> List[Dict]:
        return self._make_request("GET", "/cameras/")
    
    def add_camera(self, camera_data: Dict) -> Dict:
        return self._make_request("POST", "/cameras/", data=camera_data)
    
    # Transaction endpoints
    def get_transactions(self, skip: int = 0, limit: int = 100, customer_id: Optional[str] = None) -> List[Dict]:
        params = {"skip": skip, "limit": limit}
        if customer_id:
            params["customer_id"] = customer_id
        return self._make_request("GET", "/transactions/", params=params)

# Create a singleton instance
api_client = TRINETRAAPIClient()
