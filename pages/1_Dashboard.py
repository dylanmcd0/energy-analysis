import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Energy Markets Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
market_view = st.sidebar.selectbox(
    "Market View",
    ["Overview", "Power", "Oil & Gas", "Equities"]
)

time_range = st.sidebar.selectbox(
    "Time Range",
    ["1D", "1W", "1M", "3M", "1Y", "YTD"]
)

# Main dashboard content
if market_view == "Overview":
    st.subheader("Market Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Natural Gas", "$2.85/MMBtu", "↑ 4.2%")
    with col2:
        st.metric("Crude Oil (WTI)", "$78.45/bbl", "↓ 1.6%")
    with col3:
        st.metric("Power Demand", "425 GW", "↑ 3.5%")
    with col4:
        st.metric("Energy Index", "145.8", "↑ 1.4%")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Trends")
        # Placeholder chart
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        sample_data = pd.DataFrame({
            'Date': dates,
            'Natural Gas': 2.5 + (dates.dayofyear / 365) * 0.7 + pd.Series(range(len(dates))).apply(lambda x: 0.1 * (x % 30 - 15) / 15),
            'Crude Oil': 70 + (dates.dayofyear / 365) * 15 + pd.Series(range(len(dates))).apply(lambda x: 2 * (x % 30 - 15) / 15)
        })
        
        fig = px.line(sample_data, x='Date', y=['Natural Gas', 'Crude Oil'],
                     title="Energy Commodity Prices")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Regional Power Demand")
        # Placeholder regional data
        regions = ['Northeast', 'Southeast', 'Midwest', 'West', 'Texas']
        demand = [95, 120, 88, 105, 142]
        
        fig = px.bar(x=regions, y=demand, title="Current Power Demand by Region (GW)")
        st.plotly_chart(fig, use_container_width=True)

elif market_view == "Power":
    st.subheader("Power Markets")
    st.info("Power market data and analysis will be displayed here")
    
elif market_view == "Oil & Gas":
    st.subheader("Oil & Gas Markets")
    st.info("Oil & gas market data and analysis will be displayed here")
    
elif market_view == "Equities":
    st.subheader("Energy Equities")
    st.info("Energy sector equity analysis will be displayed here")

# Data freshness indicator
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Status**")
st.sidebar.success("✅ Live - Updated 2 mins ago")
st.sidebar.markdown("Next update: 15:30 EST")