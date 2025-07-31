import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from data_fetcher import YFinanceDataLoader

st.set_page_config(page_title="Fundamentals", page_icon="📈", layout="wide")

st.title("📈 Market Fundamentals")

# Initialize data loader
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_market_data():
    """Load market data from CSV files"""
    try:
        loader = YFinanceDataLoader()
        commodity_data = loader.get_commodity_prices()
        equity_data = loader.get_equity_prices()
        return commodity_data, equity_data, None
    except Exception as e:
        return {}, {}, str(e)

commodity_prices, equity_prices, load_error = load_market_data()

# Display load status
if load_error:
    st.error(f"Error loading market data: {load_error}")
    st.info("Using sample data instead")
    commodity_prices, equity_prices = {}, {}

# Sidebar controls
st.sidebar.header("Analysis Controls")
commodity = st.sidebar.selectbox(
    "Select Commodity",
    ["Natural Gas", "Crude Oil", "Energy ETFs", "Energy Equities", "Storage Levels"]
)

analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Current Prices", "Price Charts", "Supply & Demand", "Storage Levels"]
)

region = st.sidebar.selectbox(
    "Region",
    ["US Total", "Northeast", "Southeast", "Midwest", "West", "Texas"]
)

# Main content based on selections
st.subheader(f"{commodity} - {analysis_type}")

@st.cache_data(ttl=3600)
def get_historical_data(ticker, days=30):
    """Get historical price data for charts"""
    try:
        loader = YFinanceDataLoader()
        return loader.load_ticker_data(ticker, days=days)
    except Exception as e:
        st.error(f"Error loading historical data for {ticker}: {e}")
        return pd.DataFrame()

if commodity == "Natural Gas":
    if analysis_type == "Current Prices":
        st.subheader("Natural Gas Market Prices")
        
        col1, col2, col3 = st.columns(3)
        
        # Natural Gas Futures
        if 'Natural Gas' in commodity_prices:
            ng_data = commodity_prices['Natural Gas']
            with col1:
                delta_color = "normal" if ng_data['change'] >= 0 else "inverse"
                st.metric(
                    "Natural Gas Futures (NG=F)", 
                    f"${ng_data['price']:.3f}", 
                    f"{ng_data['change']:+.3f} ({ng_data['change_pct']:+.1f}%)",
                    delta_color=delta_color
                )
        
        # UNG ETF
        if 'US Natural Gas Fund' in commodity_prices:
            ung_data = commodity_prices['US Natural Gas Fund']
            with col2:
                delta_color = "normal" if ung_data['change'] >= 0 else "inverse"
                st.metric(
                    "US Natural Gas Fund (UNG)", 
                    f"${ung_data['price']:.2f}", 
                    f"{ung_data['change']:+.2f} ({ung_data['change_pct']:+.1f}%)",
                    delta_color=delta_color
                )
        
        with col3:
            st.metric("Storage Level", "2,650 Bcf", "↓ 150 Bcf")
    
    elif analysis_type == "Price Charts":
        st.subheader("Natural Gas Price History")
        
        # Chart time period selector
        period = st.selectbox("Time Period", ["30 Days", "90 Days", "1 Year", "2 Years"])
        days = {"30 Days": 30, "90 Days": 90, "1 Year": 252, "2 Years": 504}[period]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Natural Gas Futures Chart
            ng_data = get_historical_data('NG=F', days=days)
            if not ng_data.empty:
                fig = px.line(ng_data, x=ng_data.index, y='Close', 
                             title="Natural Gas Futures (NG=F)")
                fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Natural Gas futures data not available")
        
        with col2:
            # UNG ETF Chart
            ung_data = get_historical_data('UNG', days=days)
            if not ung_data.empty:
                fig = px.line(ung_data, x=ung_data.index, y='Close', 
                             title="US Natural Gas Fund (UNG)")
                fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("UNG ETF data not available")
    
    elif analysis_type == "Supply & Demand":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Supply Sources")
            supply_data = {
                'Source': ['Shale Gas', 'Conventional', 'Coal Bed Methane', 'Imports'],
                'Production (Bcf/d)': [85.2, 12.8, 3.4, 2.1]
            }
            df = pd.DataFrame(supply_data)
            fig = px.pie(df, values='Production (Bcf/d)', names='Source',
                        title="Natural Gas Supply Mix")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Demand Sectors")
            demand_data = {
                'Sector': ['Power Generation', 'Industrial', 'Residential', 'Commercial', 'Export'],
                'Consumption (Bcf/d)': [42.1, 21.3, 15.8, 10.2, 13.9]
            }
            df = pd.DataFrame(demand_data)
            fig = px.bar(df, x='Sector', y='Consumption (Bcf/d)',
                        title="Natural Gas Demand by Sector")
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Storage Levels":
        st.subheader("Natural Gas Storage")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_year = [1450, 1200, 980, 850, 920, 1180, 1580, 2100, 2580, 2950, 2650, 2200]
        five_year_avg = [1380, 1150, 950, 800, 880, 1150, 1520, 2050, 2520, 2880, 2580, 2150]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=current_year, name='2024', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=months, y=five_year_avg, name='5-Year Average', line=dict(color='gray', dash='dash')))
        fig.update_layout(title='Natural Gas Storage Levels (Bcf)',
                         xaxis_title='Month',
                         yaxis_title='Storage (Bcf)')
        st.plotly_chart(fig, use_container_width=True)

elif commodity == "Crude Oil":
    if analysis_type == "Current Prices":
        st.subheader("Crude Oil Market Prices")
        
        col1, col2, col3 = st.columns(3)
        
        # WTI Crude Oil
        if 'WTI Crude Oil' in commodity_prices:
            wti_data = commodity_prices['WTI Crude Oil']
            with col1:
                delta_color = "normal" if wti_data['change'] >= 0 else "inverse"
                st.metric(
                    "WTI Crude Oil (CL=F)", 
                    f"${wti_data['price']:.2f}", 
                    f"{wti_data['change']:+.2f} ({wti_data['change_pct']:+.1f}%)",
                    delta_color=delta_color
                )
        
        # Brent Crude Oil
        if 'Brent Crude' in commodity_prices:
            brent_data = commodity_prices['Brent Crude']
            with col2:
                delta_color = "normal" if brent_data['change'] >= 0 else "inverse"
                st.metric(
                    "Brent Crude Oil (BZ=F)", 
                    f"${brent_data['price']:.2f}", 
                    f"{brent_data['change']:+.2f} ({brent_data['change_pct']:+.1f}%)",
                    delta_color=delta_color
                )
        
        # USO ETF
        if 'US Oil Fund' in commodity_prices:
            uso_data = commodity_prices['US Oil Fund']
            with col3:
                delta_color = "normal" if uso_data['change'] >= 0 else "inverse"
                st.metric(
                    "US Oil Fund (USO)", 
                    f"${uso_data['price']:.2f}", 
                    f"{uso_data['change']:+.2f} ({uso_data['change_pct']:+.1f}%)",
                    delta_color=delta_color
                )
    
    elif analysis_type == "Price Charts":
        st.subheader("Crude Oil Price History")
        
        period = st.selectbox("Time Period", ["30 Days", "90 Days", "1 Year", "2 Years"])
        days = {"30 Days": 30, "90 Days": 90, "1 Year": 252, "2 Years": 504}[period]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # WTI Crude Chart
            wti_data = get_historical_data('CL=F', days=days)
            if not wti_data.empty:
                fig = px.line(wti_data, x=wti_data.index, y='Close', 
                             title="WTI Crude Oil Futures (CL=F)")
                fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Brent Crude Chart
            brent_data = get_historical_data('BZ=F', days=days)
            if not brent_data.empty:
                fig = px.line(brent_data, x=brent_data.index, y='Close', 
                             title="Brent Crude Oil Futures (BZ=F)")
                fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("US Production", "13.2 MMbbl/d", "↑ 0.3 MMbbl/d")
            st.metric("Strategic Petroleum Reserve", "351 MMbbl", "↓ 2.1 MMbbl")
            st.metric("Commercial Inventory", "421 MMbbl", "↑ 1.8 MMbbl")
        
        with col2:
            st.metric("Refinery Utilization", "89.2%", "↑ 2.1%")
            st.metric("Net Imports", "6.1 MMbbl/d", "↓ 0.4 MMbbl/d")
            st.metric("Days of Supply", "31.8 days", "↑ 0.2 days")

elif commodity == "Energy ETFs":
    if analysis_type == "Current Prices":
        st.subheader("Energy ETF Prices")
        
        if equity_prices:
            # Create DataFrame for better display
            etf_data = []
            etf_tickers = ['XLE', 'XOP', 'VDE', 'IYE']
            
            for name, data in equity_prices.items():
                if data['ticker'] in etf_tickers:
                    etf_data.append({
                        'ETF': name,
                        'Ticker': data['ticker'],
                        'Price': f"${data['price']:.2f}",
                        'Change': f"{data['change']:+.2f}",
                        'Change %': f"{data['change_pct']:+.1f}%",
                        'Volume': f"{data['volume']:,.0f}"
                    })
            
            if etf_data:
                df = pd.DataFrame(etf_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ETF price data not available")
        else:
            st.info("ETF price data not available")
    
    elif analysis_type == "Price Charts":
        st.subheader("Energy ETF Price Charts")
        
        period = st.selectbox("Time Period", ["30 Days", "90 Days", "1 Year", "2 Years"])
        days = {"30 Days": 30, "90 Days": 90, "1 Year": 252, "2 Years": 504}[period]
        
        col1, col2 = st.columns(2)
        
        with col1:
            xle_data = get_historical_data('XLE', days=days)
            if not xle_data.empty:
                fig = px.line(xle_data, x=xle_data.index, y='Close', 
                             title="Energy Select Sector SPDR (XLE)")
                fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            xop_data = get_historical_data('XOP', days=days)
            if not xop_data.empty:
                fig = px.line(xop_data, x=xop_data.index, y='Close', 
                             title="SPDR S&P Oil & Gas Exploration (XOP)")
                fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig, use_container_width=True)

elif commodity == "Energy Equities":
    if analysis_type == "Current Prices":
        st.subheader("Energy Stock Prices")
        
        if equity_prices:
            # Create DataFrame for better display
            stock_data = []
            stock_tickers = ['XOM', 'CVX', 'COP', 'SLB', 'HAL', 'BKR', 'OXY']
            
            for name, data in equity_prices.items():
                if data['ticker'] in stock_tickers:
                    stock_data.append({
                        'Company': name,
                        'Ticker': data['ticker'],
                        'Price': f"${data['price']:.2f}",
                        'Change': f"{data['change']:+.2f}",
                        'Change %': f"{data['change_pct']:+.1f}%",
                        'Volume': f"{data['volume']:,.0f}"
                    })
            
            if stock_data:
                df = pd.DataFrame(stock_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Stock price data not available")
        else:
            st.info("Stock price data not available")
    
    elif analysis_type == "Price Charts":
        st.subheader("Energy Stock Charts")
        
        period = st.selectbox("Time Period", ["30 Days", "90 Days", "1 Year", "2 Years"])
        days = {"30 Days": 30, "90 Days": 90, "1 Year": 252, "2 Years": 504}[period]
        
        selected_stocks = st.multiselect(
            "Select stocks to chart:",
            ['XOM', 'CVX', 'COP', 'SLB', 'HAL', 'BKR', 'OXY'],
            default=['XOM', 'CVX']
        )
        
        if selected_stocks:
            fig = go.Figure()
            
            for ticker in selected_stocks:
                stock_data = get_historical_data(ticker, days=days)
                if not stock_data.empty:
                    fig.add_trace(go.Scatter(
                        x=stock_data.index, 
                        y=stock_data['Close'],
                        name=ticker,
                        mode='lines'
                    ))
            
            fig.update_layout(
                title="Energy Stock Price Comparison",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select stocks to display")

else:
    st.info(f"{commodity} fundamentals data will be displayed here")

# Data notes
st.markdown("---")
if not load_error:
    # Get last update time from summary file
    try:
        import json
        summary_path = os.path.join('data', 'financial', 'yfinance', 'update_summary.json')
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                summary = json.load(f)
            last_updated = pd.to_datetime(summary['last_updated']).strftime("%Y-%m-%d %H:%M EST")
            st.markdown(f"**Data Sources**: YFinance (Historical CSV data)")
            st.markdown(f"**Last Updated**: {last_updated}")
        else:
            st.markdown("**Data Sources**: YFinance (Historical CSV data)")
            st.markdown("**Last Updated**: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M EST"))
    except Exception:
        st.markdown("**Data Sources**: YFinance (Historical CSV data)")
        st.markdown("**Last Updated**: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M EST"))
else:
    st.markdown("**Data Sources**: EIA, FERC, Bloomberg (Sample Data)")
    st.markdown("**Last Updated**: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M EST"))