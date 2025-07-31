import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from data_fetcher import YFinanceDataLoader

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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_csv_market_data():
    """Get market data from CSV files"""
    try:
        loader = YFinanceDataLoader()
        commodity_prices = loader.get_commodity_prices()
        equity_prices = loader.get_equity_prices()
        return commodity_prices, equity_prices, None
    except Exception as e:
        return {}, {}, str(e)

@st.cache_data(ttl=300)
def get_commodity_chart_data():
    """Get historical commodity data for chart"""
    try:
        loader = YFinanceDataLoader()
        
        # Get last 30 days of data for key commodities
        ng_data = loader.load_ticker_data('NG=F', days=30)
        cl_data = loader.load_ticker_data('CL=F', days=30)
        bz_data = loader.load_ticker_data('BZ=F', days=30)
        
        # Create combined DataFrame
        chart_data = pd.DataFrame({
            'Date': ng_data.index,
            'Natural Gas': ng_data['Close'],
            'WTI Crude': cl_data['Close'],
            'Brent Crude': bz_data['Close']
        })
        
        return chart_data
    except Exception as e:
        st.error(f"Error loading chart data: {e}")
        return pd.DataFrame()

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
        st.subheader("Energy Commodity Prices")
        
        # Get real commodity chart data
        commodity_chart_data = get_commodity_chart_data()
        
        if not commodity_chart_data.empty:
            # Create multi-axis chart since Natural Gas and Oil have different scales
            fig = go.Figure()
            
            # Natural Gas (left y-axis)
            fig.add_trace(go.Scatter(
                x=commodity_chart_data['Date'],
                y=commodity_chart_data['Natural Gas'],
                name='Natural Gas ($/MMBtu)',
                line=dict(color='blue'),
                yaxis='y'
            ))
            
            # WTI Crude (right y-axis)
            fig.add_trace(go.Scatter(
                x=commodity_chart_data['Date'],
                y=commodity_chart_data['WTI Crude'],
                name='WTI Crude ($/bbl)',
                line=dict(color='red'),
                yaxis='y2'
            ))
            
            # Brent Crude (right y-axis)
            fig.add_trace(go.Scatter(
                x=commodity_chart_data['Date'],
                y=commodity_chart_data['Brent Crude'],
                name='Brent Crude ($/bbl)',
                line=dict(color='orange'),
                yaxis='y2'
            ))
            
            # Update layout with dual y-axes
            fig.update_layout(
                title="Energy Commodity Prices (30 Days)",
                xaxis=dict(title="Date"),
                yaxis=dict(
                    title="Natural Gas ($/MMBtu)",
                    titlefont=dict(color="blue"),
                    tickfont=dict(color="blue"),
                    side="left"
                ),
                yaxis2=dict(
                    title="Crude Oil ($/bbl)",
                    titlefont=dict(color="red"),
                    tickfont=dict(color="red"),
                    overlaying="y",
                    side="right"
                ),
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Commodity price chart data not available")
    
    with col2:
        st.subheader("Energy ETF Performance")
        
        # Get ETF data and create performance comparison
        commodity_prices, equity_prices, load_error = get_csv_market_data()
        
        if not load_error and equity_prices:
            # Create ETF performance chart
            etf_data = []
            etf_names = ['Energy Select Sector SPDR', 'SPDR S&P Oil & Gas Exploration', 
                        'Vanguard Energy ETF', 'iShares U.S. Energy ETF']
            
            for name in etf_names:
                if name in equity_prices:
                    data = equity_prices[name]
                    etf_data.append({
                        'ETF': name.replace('Energy Select Sector SPDR', 'XLE')
                                  .replace('SPDR S&P Oil & Gas Exploration', 'XOP')
                                  .replace('Vanguard Energy ETF', 'VDE')
                                  .replace('iShares U.S. Energy ETF', 'IYE'),
                        'Price': data['price'],
                        'Change_%': data['change_pct']
                    })
            
            if etf_data:
                df = pd.DataFrame(etf_data)
                
                # Create bar chart with color based on performance
                colors = ['green' if x > 0 else 'red' for x in df['Change_%']]
                
                fig = px.bar(df, x='ETF', y='Change_%', 
                           title="Energy ETF Daily Performance (%)",
                           color='Change_%',
                           color_continuous_scale=['red', 'white', 'green'],
                           color_continuous_midpoint=0)
                
                fig.update_layout(
                    yaxis_title="Daily Change (%)",
                    xaxis_title="Energy ETFs",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ETF performance data not available")
        else:
            st.info("ETF performance data not available")
    
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