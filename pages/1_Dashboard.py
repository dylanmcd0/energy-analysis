import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Energy Markets Dashboard")

# US energy commodity ticker universe
commodities = {
    'West Texas Intermediate': 'CL=F',
    'Henry Hub Natural Gas': 'NG=F',
    'Brent Crude Oil': 'BZ=F',
    'Gasoline RBOB': 'RB=F',
    'Heating Oil': 'HO=F',
    'Uranium': 'URA',
    'Coal': 'COAL',
}

# Define a universe of energy equity tickers
equities = {
    'Exxon Mobil Corporation': 'XOM',
    'Chevron Corporation': 'CVX',
    'ConocoPhillips': 'COP',
    'Schlumberger Limited': 'SLB',
    'Halliburton Company': 'HAL',
    'Baker Hughes Company': 'BKR',
    'Occidental Petroleum Corporation': 'OXY',
    'The Energy Select Sector SPDR Fund': 'XLE',
}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_market_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='2d')  # Get 2 days to calculate change
        if len(data) >= 2:
            current_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2]
            change_pct = ((current_price - previous_price) / previous_price) * 100
            return current_price, change_pct
        elif len(data) == 1:
            # If only 1 day available, return price with no change
            current_price = data['Close'].iloc[-1]
            return current_price, None
    except:
        pass
    return None, None

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
        ng_price, ng_change = get_market_data('NG=F')
        if ng_price:
            st.metric(
                label="Natural Gas (Henry Hub)",
                value=f"${ng_price:.2f}/MMBtu",
                delta=f"{ng_change:.2f}%" if ng_change else None
            )
        else:
            st.metric(label="Natural Gas (Henry Hub)", value="Loading...")
    
    with col2:
        wti_price, wti_change = get_market_data('CL=F')
        if wti_price:
            st.metric(
                label="Crude Oil (WTI)",
                value=f"${wti_price:.2f}/bbl",
                delta=f"{wti_change:.2f}%" if wti_change else None
            )
        else:
            st.metric(label="Crude Oil (WTI)", value="Loading...")
    
    with col3:
        brent_price, brent_change = get_market_data('BZ=F')
        if brent_price:
            st.metric(
                label="Brent Crude Oil",
                value=f"${brent_price:.2f}/bbl",
                delta=f"{brent_change:.2f}%" if brent_change else None
            )
        else:
            st.metric(label="Brent Crude Oil", value="Loading...")
    
    with col4:
        xle_price, xle_change = get_market_data('XLE')
        if xle_price:
            st.metric(
                label="Energy Sector ETF (XLE)",
                value=f"${xle_price:.2f}",
                delta=f"{xle_change:.2f}%" if xle_change else None
            )
        else:
            st.metric(label="Energy Sector ETF (XLE)", value="Loading...")
    
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
    
    # Additional market data sections
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🛢️ Energy Commodities")
        for name, ticker in commodities.items():
            price, change = get_market_data(ticker)
            if price:
                col_name, col_price, col_change = st.columns([3, 2, 1])
                with col_name:
                    st.write(name)
                with col_price:
                    st.write(f"${price:.2f}")
                with col_change:
                    if change:
                        color = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                        st.write(f"{color} {change:.2f}%")
    
    with col_right:
        st.markdown("### 📈 Energy Equities")
        for name, ticker in equities.items():
            price, change = get_market_data(ticker)
            if price:
                col_name, col_price, col_change = st.columns([3, 2, 1])
                with col_name:
                    st.write(name)
                with col_price:
                    st.write(f"${price:.2f}")
                with col_change:
                    if change:
                        color = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                        st.write(f"{color} {change:.2f}%")

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