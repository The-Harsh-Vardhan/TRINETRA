import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_footfall_chart(data):
    fig = px.line(data, x="timestamp", y="count", title="Hourly Footfall")
    return fig

def create_heatmap():
    x = list(range(10))
    y = list(range(10))
    z = [[x + y for x in range(10)] for y in range(10)]
    fig = go.Figure(data=go.Heatmap(z=z))
    fig.update_layout(title="Customer Density Heatmap")
    return fig

def create_emotion_chart(data):
    fig = px.pie(data, values="Percentage", names="Emotion",
                 title="Customer Emotions Distribution")
    return fig

def analytics_page():
    st.title("Analytics Dashboard")
    
    # Time range selector
    time_range = st.selectbox(
        "Select Time Range",
        ["Last Hour", "Today", "Last 7 Days", "Last 30 Days", "Custom"]
    )
    
    if time_range == "Custom":
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date")
        end_date = col2.date_input("End Date")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Footfall", "Heatmap", "Customer Behavior"])
    
    with tab1:
        st.subheader("Footfall Analytics")
        
        # Sample data
        dates = pd.date_range(start="2025-06-01", periods=24, freq="H")
        footfall_data = pd.DataFrame({
            "timestamp": dates,
            "count": [20, 25, 30, 35, 45, 50, 60, 70, 80, 85, 90, 95,
                     90, 85, 80, 75, 70, 65, 55, 45, 35, 30, 25, 20]
        })
        
        st.plotly_chart(create_footfall_chart(footfall_data), use_container_width=True)
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Visitors", "1,234", "+10%")
        col2.metric("Average Time Spent", "45 mins", "-5%")
        col3.metric("Return Rate", "28%", "+2%")
    
    with tab2:
        st.subheader("Store Heatmap")
        st.plotly_chart(create_heatmap(), use_container_width=True)
        
        # Zone analysis
        st.subheader("Zone Analysis")
        zone_data = pd.DataFrame({
            "Zone": ["Electronics", "Clothing", "Grocery", "Checkout"],
            "Average Dwell Time": [15, 25, 10, 5],
            "Peak Hours": ["14:00-16:00", "12:00-14:00", "18:00-20:00", "17:00-19:00"]
        })
        st.dataframe(zone_data)
    
    with tab3:
        st.subheader("Customer Behavior Analysis")
        
        # Sample emotion data
        emotion_data = pd.DataFrame({
            "Emotion": ["Happy", "Neutral", "Satisfied", "Confused", "Unhappy"],
            "Percentage": [45, 30, 15, 7, 3]
        })
        
        st.plotly_chart(create_emotion_chart(emotion_data), use_container_width=True)
        
        # Behavior metrics
        col1, col2 = st.columns(2)
        col1.metric("Average Satisfaction", "8.5/10", "+0.5")
        col2.metric("Customer Engagement", "75%", "+5%")
