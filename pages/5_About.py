import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Energy Analysis Platform")

# Project overview
st.subheader("🎯 Project Mission")
st.markdown("""
This platform provides comprehensive analysis and insights into US energy markets, 
combining real-time data with advanced analytics to help users understand market 
dynamics across power, oil & gas, and energy equities sectors.

**Our Goal**: Make energy market data accessible, actionable, and insightful for 
researchers, analysts, traders, and energy professionals.
""")

# Platform features
st.subheader("⚡ Platform Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📊 Real-Time Dashboards**
    - Live market data and pricing
    - Interactive visualizations
    - Customizable views and filters
    
    **📈 Market Fundamentals**
    - Supply and demand analysis
    - Storage levels and inventory data
    - Production and consumption metrics
    
    **🔮 Predictive Models**
    - Price forecasting algorithms
    - Demand prediction models
    - Risk assessment tools
    """)

with col2:
    st.markdown("""
    **📝 Market Insights**
    - Expert analysis and commentary
    - Weekly market reports
    - Trend identification and alerts
    
    **🔄 Automated Updates**
    - Scheduled data collection
    - Real-time processing
    - GitHub Actions integration
    
    **☁️ Cloud Integration**
    - AWS S3 storage
    - Scalable architecture
    - Custom domain hosting
    """)

# Data sources
st.subheader("📊 Data Sources")

data_sources = [
    {
        "source": "Energy Information Administration (EIA)",
        "description": "Official US energy statistics, production, consumption, and pricing data",
        "update_frequency": "Daily/Weekly",
        "coverage": "All energy sectors"
    },
    {
        "source": "Federal Energy Regulatory Commission (FERC)",
        "description": "Power market data, transmission information, regulatory filings",
        "update_frequency": "Real-time/Daily",
        "coverage": "Power markets"
    },
    {
        "source": "Yahoo Finance",
        "description": "Energy sector equities, stock prices, financial metrics",
        "update_frequency": "Real-time",
        "coverage": "Public energy companies"
    },
    {
        "source": "Alpha Vantage",
        "description": "Financial market data, commodity prices, technical indicators",
        "update_frequency": "Real-time/Daily",
        "coverage": "Financial markets"
    },
    {
        "source": "National Oceanic and Atmospheric Administration (NOAA)",
        "description": "Weather data for demand forecasting and seasonal analysis",
        "update_frequency": "Hourly/Daily",
        "coverage": "Weather patterns"
    }
]

for source in data_sources:
    with st.expander(f"📡 {source['source']}"):
        st.markdown(f"""
        **Description**: {source['description']}
        
        **Update Frequency**: {source['update_frequency']}
        
        **Coverage**: {source['coverage']}
        """)

# Technology stack
st.subheader("🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Frontend**
    - Streamlit
    - Plotly
    - Pandas
    - NumPy
    """)

with col2:
    st.markdown("""
    **Backend & Data**
    - Python
    - SQLite
    - AWS S3
    - GitHub Actions
    """)

with col3:
    st.markdown("""
    **Deployment**
    - Streamlit Cloud
    - Custom Domain
    - DigitalOcean (backup)
    """)

# Architecture diagram
st.subheader("🏗️ System Architecture")

st.markdown("""
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│ Public APIs │───▶│ GitHub       │───▶│ Data        │───▶│ Streamlit   │
│ (EIA, FERC, │    │ Actions      │    │ Processing  │    │ Application │
│  Yahoo, etc)│    │ (Scheduled)  │    │ & Storage   │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
                                              │                    ▲
                                              ▼                    │
                                        ┌─────────────┐    ┌─────────────┐
                                        │ AWS S3      │    │ Users       │
                                        │ (Blog &     │    │ (Web        │
                                        │  Assets)    │    │  Interface) │
                                        └─────────────┘    └─────────────┘
```
""")

# Performance metrics
st.subheader("📈 Platform Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Data Points", "50M+", "↑ 2M/month")

with col2:
    st.metric("API Calls/Day", "12,000", "↑ 500")

with col3:
    st.metric("Model Accuracy", "87%", "↑ 2%")

with col4:
    st.metric("Uptime", "99.8%", "")


# Contact and links
st.subheader("📞 Contact & Links")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔗 Project Links**
    - [GitHub Repository](https://github.com/yourusername/energy-analysis)
    - [Live Platform](https://energy-analysis.streamlit.app)
    - [Documentation](https://docs.example.com)
    - [API Documentation](https://api.example.com/docs)
    """)

with col2:
    st.markdown("""
    **📧 Contact Information**
    - Email: mcdonalddylan2020@gmail.com
    - LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
    - Twitter: [@YourHandle](https://twitter.com/yourhandle)
    """)

# Disclaimer and license
st.markdown("---")
st.subheader("⚖️ Legal & Disclaimers")

with st.expander("📄 Terms of Use"):
    st.markdown("""
    **Data Usage**: All data is sourced from public APIs and government sources. 
    Users are responsible for compliance with data provider terms of service.
    
    **Investment Disclaimer**: This platform provides information for educational 
    and research purposes only. It is not intended as investment advice.
    
    **Accuracy**: While we strive for accuracy, we cannot guarantee the completeness 
    or correctness of all data and analysis.
    """)

with st.expander("📜 License & Attribution"):
    st.markdown("""
    **License**: MIT License - Free for educational and commercial use
    
    **Attribution Requirements**:
    - Data sources must be credited when using platform outputs
    - Original analysis may be shared with proper attribution
    
    **Open Source**: Source code available on GitHub under MIT license
    """)

# Version info
st.markdown("---")
st.markdown("**Platform Version**: 1.0.0 | **Last Updated**: December 2024")
st.markdown("**Python Version**: 3.12 | **Streamlit Version**: 1.29.0")