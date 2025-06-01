import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import requests
from utils.api_client import TRINETRAAPIClient

# Import API client
from utils.api_client import TRINETRAAPIClient

# Page configuration
st.set_page_config(
    page_title="TRINETRA Dashboard",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'api_client' not in st.session_state:
    st.session_state.api_client = TRINETRAAPIClient()

# Get API client instance
api_client = st.session_state.api_client

# Sidebar navigation
st.sidebar.title("TRINETRA")
st.sidebar.subheader("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Live Monitoring", "Analytics", "Customer Insights", "Vehicle Tracking"]
)

# Main content
st.title(page)

if page == "Live Monitoring":
    st.subheader("Live Camera Feeds")
    
    # Display camera feeds
    col1, col2 = st.columns(2)

    # Entrance camera
    with col1:
        st.subheader("Entrance Camera")
        video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_videos', 'entrance.mp4')
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.error("Entrance video not found")
            st.info("Please place entrance.mp4 in the test_videos folder")
        
        # Display metrics
        st.metric("People Count", "25", "+3")

    # Store camera
    with col2:
        st.subheader("Store Camera")
        video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_videos', 'store.mp4')
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.error("Store video not found")
            st.info("Please place store.mp4 in the test_videos folder")
          # Display metrics for store area
        st.metric("Active Customers", "12", "+2")
        st.metric("Staff Present", "8", "-1")

elif page == "Analytics":
    st.subheader("Analytics Dashboard")
    
    # Time range selector
    time_range = st.selectbox(
        "Select Time Range",
        ["Last Hour", "Today", "Last 7 Days", "Last 30 Days", "Custom"]
    )
    
    # Calculate date range based on selection
    end_date = datetime.now()
    if time_range == "Last Hour":
        start_date = end_date - timedelta(hours=1)
    elif time_range == "Today":
        start_date = end_date.replace(hour=0, minute=0, second=0)
    elif time_range == "Last 7 Days":
        start_date = end_date - timedelta(days=7)
    elif time_range == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    else:  # Custom
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date")
        end_date = col2.date_input("End Date")
    
    # Display analytics
    tab1, tab2 = st.tabs(["Footfall", "Behavior"])
    
    with tab1:
        try:
            footfall_data = api_client.get_footfall_analytics(start_date=start_date, end_date=end_date)
            df = pd.DataFrame(footfall_data)
            fig = px.line(df, x="timestamp", y="count", title="Footfall Over Time")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching footfall data: {str(e)}")

elif page == "Customer Insights":
    customer_id = st.text_input("Search Customer ID")
    if customer_id:
        try:
            # Get customer details
            customer = api_client.get_customer(customer_id)
            
            # Get customer journey
            journey = api_client.get_customer_journey(customer_id)
            
            # Get transactions
            transactions = api_client.get_transactions(customer_id=customer_id)
            
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Visit Count", str(customer['visit_count']))
                total_spent = sum(t['total_amount'] for t in transactions)
                st.metric("Total Spent", f"${total_spent:,.2f}")
            with col2:
                st.metric("Last Visit", customer['last_visit'].split('T')[0])
                loyalty_score = min(100, (customer['visit_count'] * 10))
                st.metric("Loyalty Score", f"{loyalty_score}%")
            
            # Display journey timeline
            st.subheader("Customer Journey")
            for event in journey:
                st.write(f"{event['timestamp']}: {event['action']}")
                
        except Exception as e:
            st.error(f"Error fetching customer data: {str(e)}")

elif page == "Vehicle Tracking":
    license_plate = st.text_input("Search License Plate")
    if license_plate:
        try:
            # Get vehicle data from database
            vehicles = api_client.get_vehicles(license_plate=license_plate)
            if vehicles:
                vehicle = vehicles[0]
                st.json({
                    "license_plate": vehicle['license_plate'],
                    "visits": vehicle['visit_count'],
                    "last_seen": vehicle['last_seen'],
                    "customer_id": vehicle['customer_id']
                })
            else:
                st.warning("No vehicle found with this license plate")
        except Exception as e:
            st.error(f"Error fetching vehicle data: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
try:
    # Check API health
    api_client._make_request("GET", "/")
    st.sidebar.success("All Systems Operational")
except Exception as e:
    st.sidebar.error("API Connection Error")

st.sidebar.markdown(f"Last Updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
