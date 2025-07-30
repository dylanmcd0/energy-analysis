import streamlit as st

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
    - **Dashboard**: Live market data and key metrics
    - **Fundamentals**: Core market data and trends
    - **Models**: Predictive analytics and forecasting
    - **Insights**: Blog-style market analysis
    - **About**: Project information
    """)
    
    # Quick access buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 **Dashboard**
        Get real-time market data, price changes, and live monitoring of energy commodities and equities.
        """)
    
    with col2:
        st.markdown("""
        ### 📈 **Fundamentals** 
        Deep dive into supply, demand, inventory levels, and core market fundamentals.
        """)
    
    with col3:
        st.markdown("""
        ### 🔮 **Models**
        Access predictive analytics, forecasting models, and quantitative analysis.
        """)

    # Getting started section
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    1. **Visit the Dashboard** - Get live market data and price monitoring
    2. **Check Fundamentals** - Dive into supply, demand, and pricing data
    3. **Explore Models** - See predictive analytics and forecasts  
    4. **Read Insights** - Market commentary and analysis
    """)
    
    # Feature highlights
    st.markdown("---")
    st.markdown("### ⚡ Key Features")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📊 Real-time Data**
        - Live commodity prices
        - Energy equity tracking
        - Percent change calculations
        - Auto-refreshing metrics
        """)
    
    with col2:
        st.markdown("""
        **🔍 Comprehensive Coverage**
        - Oil & Gas markets
        - Power generation data
        - Energy sector equities
        - Regional analysis
        """)

if __name__ == "__main__":
    main()