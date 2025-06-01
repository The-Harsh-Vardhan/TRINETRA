import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def display_vehicle_info(vehicle_data):
    st.subheader("Vehicle Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**License Plate:**", vehicle_data["license_plate"])
        st.write("**Total Visits:**", vehicle_data["visits"])
        st.write("**Last Seen:**", vehicle_data["last_seen"])
    
    with col2:
        st.write("**Linked Customer:**", vehicle_data["customer_id"])
        st.write("**Vehicle Type:**", vehicle_data["vehicle_type"])
        st.write("**Status:**", vehicle_data["status"])

def display_visit_history(visits):
    st.subheader("Visit History")
    
    # Create timeline chart
    fig = px.scatter(
        visits,
        x="timestamp",
        y="duration",
        size="duration",
        title="Visit Duration Timeline"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed history
    st.dataframe(visits)

def vehicle_tracking_page():
    st.title("Vehicle Tracking")
    
    # Vehicle search
    license_plate = st.text_input("Search License Plate")
    
    if license_plate:
        # Sample vehicle data
        vehicle_data = {
            "license_plate": license_plate,
            "visits": 8,
            "last_seen": "2025-06-01 14:30:00",
            "customer_id": "CUST_001",
            "vehicle_type": "Car",
            "status": "Regular Customer"
        }
        
        # Display vehicle information
        display_vehicle_info(vehicle_data)
        
        # Sample visit history
        visits = pd.DataFrame({
            "timestamp": pd.date_range(start="2025-05-01", periods=8, freq="D"),
            "duration": [30, 45, 60, 30, 45, 60, 30, 45],
            "purpose": ["Shopping", "Pickup", "Shopping", "Return",
                      "Shopping", "Shopping", "Pickup", "Shopping"]
        })
        
        # Display visit history
        display_visit_history(visits)
        
        # Additional analytics
        st.subheader("Visit Analytics")
        
        # Visit metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Duration", "45 mins", "+5 mins")
        col2.metric("Visit Frequency", "Weekly", "↗")
        col3.metric("Regular Status", "Yes", "↗")
        
        # Visit pattern analysis
        st.subheader("Visit Patterns")
        pattern_data = pd.DataFrame({
            "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "Visits": [3, 1, 2, 1, 1]
        })
        
        fig = px.bar(pattern_data, x="Day", y="Visits",
                    title="Visit Distribution by Day")
        st.plotly_chart(fig, use_container_width=True)
