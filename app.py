import streamlit as st
import os
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="US Energy Markets Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">⚡ US Energy Markets Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Energy Analysis Platform
    
    This platform provides comprehensive analysis of US energy markets including:
    - **Power Markets**: Grid data, pricing, demand/supply metrics
    - **Oil & Gas**: Production, pricing, inventory levels  
    - **Energy Equities**: Stock performance, sector analysis
    - **Market Insights**: Data-driven commentary and analysis
    """)
    
    # Navigation info
    st.sidebar.markdown("## 📊 Navigation")
    st.sidebar.markdown("""
    Use the pages in the sidebar to explore:
    - **Dashboard**: Market overview and key metrics
    - **Fundamentals**: Core market data and trends
    - **Models**: Predictive analytics and forecasting
    - **Insights**: Blog-style market analysis
    - **About**: Project information
    """)
    
    # Quick stats placeholder
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Natural Gas Price",
            value="$2.85/MMBtu",
            delta="0.12"
        )
    
    with col2:
        st.metric(
            label="Crude Oil (WTI)",
            value="$78.45/bbl",
            delta="-1.23"
        )
    
    with col3:
        st.metric(
            label="Power Demand",
            value="425 GW",
            delta="15"
        )
    
    with col4:
        st.metric(
            label="Energy Sector Index",
            value="145.8",
            delta="2.1"
        )
    
    # Getting started section
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    1. **Explore the Dashboard** - Get an overview of current market conditions
    2. **Check Fundamentals** - Dive into supply, demand, and pricing data
    3. **View Models** - See predictive analytics and forecasts
    4. **Read Insights** - Market commentary and analysis
    """)

if __name__ == "__main__":
    main()