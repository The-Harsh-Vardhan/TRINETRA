import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def display_customer_profile(customer_data):
    st.subheader("Customer Profile")
    
    # Basic info
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Visit Count:**", customer_data["visit_count"])
        st.write("**Total Spent:**", f"${customer_data['total_spent']}")
        st.write("**Last Visit:**", customer_data["last_visit"])
    
    with col2:
        st.write("**Favorite Items:**")
        for item in customer_data["favorite_items"]:
            st.write(f"- {item}")

def display_customer_journey(journey_data):
    st.subheader("Customer Journey")
    
    # Timeline chart
    fig = px.timeline(
        journey_data,
        x_start="timestamp",
        x_end="end_time",
        y="location",
        title="Customer Journey Timeline"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Journey details
    st.dataframe(journey_data)

def customer_insights_page():
    st.title("Customer Insights")
    
    # Customer search
    customer_id = st.text_input("Search Customer ID")
    
    if customer_id:
        # Sample customer data
        customer_data = {
            "id": customer_id,
            "visit_count": 15,
            "total_spent": 2500,
            "last_visit": "2025-06-01",
            "favorite_items": ["Electronics", "Clothing", "Books"]
        }
        
        # Display customer profile
        display_customer_profile(customer_data)
        
        # Sample journey data
        journey_data = pd.DataFrame({
            "timestamp": pd.date_range(start="2025-06-01 14:00", periods=5, freq="10min"),
            "end_time": pd.date_range(start="2025-06-01 14:10", periods=5, freq="10min"),
            "location": ["Entrance", "Electronics", "Clothing", "Checkout", "Exit"]
        })
        
        # Display customer journey
        display_customer_journey(journey_data)
        
        # Additional insights
        st.subheader("Customer Insights")
        
        # Behavior metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Loyalty Score", "85%", "+5%")
        col2.metric("Average Basket Size", "$166", "+$12")
        col3.metric("Visit Frequency", "Weekly", "↗")
        
        # Shopping preferences
        st.subheader("Shopping Preferences")
        preferences = pd.DataFrame({
            "Category": ["Electronics", "Clothing", "Books", "Groceries"],
            "Spend": [1200, 800, 300, 200]
        })
        
        fig = px.pie(preferences, values="Spend", names="Category",
                    title="Shopping Category Distribution")
        st.plotly_chart(fig, use_container_width=True)
