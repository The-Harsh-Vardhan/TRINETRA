import streamlit as st
import cv2
from datetime import datetime

def render_camera_feed(camera):
    st.subheader(f"{camera['type'].title()} Camera")
    # Placeholder for camera feed
    st.image("https://via.placeholder.com/640x480.png?text=Camera+Feed", 
            caption=f"Camera ID: {camera['id']}")
    
    # Real-time metrics
    col1, col2 = st.columns(2)
    col1.metric("People Count", "25", "+2")
    col2.metric("Alerts", "0", "0")

def live_monitoring_page():
    st.title("Live Monitoring")
    
    # Camera configuration
    cameras = [
        {"id": 0, "type": "entrance", "source": 0},
        {"id": 1, "type": "store", "source": 1},
        {"id": 2, "type": "billing", "source": 2},
        {"id": 3, "type": "parking", "source": 3}
    ]
    
    # Display camera feeds in a grid
    cols = st.columns(2)
    for idx, camera in enumerate(cameras):
        with cols[idx % 2]:
            render_camera_feed(camera)
            
    # Alert Section
    st.sidebar.subheader("Recent Alerts")
    alerts = [
        {"time": "14:30", "type": "High Occupancy", "location": "Entrance"},
        {"time": "14:25", "type": "Suspicious Activity", "location": "Aisle 3"}
    ]
    
    for alert in alerts:
        st.sidebar.warning(
            f"{alert['time']} - {alert['type']}\n"
            f"Location: {alert['location']}"
        )
