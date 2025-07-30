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
    ### Welcome to my Energy Analysis Platform
    
    This platform aims to provide analysis of US energy markets for my own learning including:
    - **Power Markets**: Grid data, pricing, demand/supply metrics
    - **Oil & Gas**: Production, pricing, inventory levels  
    - **Energy Equities**: Stock performance, sector analysis
    - **Market Insights**: Data-driven commentary and analysis
    """)
    
    # Navigation info
    st.sidebar.markdown("## 📊 Navigation")  
    st.sidebar.markdown("""
    Use the sidebar to explore:
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

    # Coming soon section
    st.markdown("---")
    st.markdown("### 🚀 Coming Soon")
    st.markdown("""
    1. **EIA Energy Daily** - Include EIA daily insight on Dashboard page including AI summary
    2. **More In-Depth Models** - Spark spreads, crack spreads, Monte Carlo simulations
    4. **Inisghts** - Ability to post blog-style insights
    """)

if __name__ == "__main__":
    main()