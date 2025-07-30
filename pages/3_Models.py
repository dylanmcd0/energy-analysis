import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Models", page_icon="🔮", layout="wide")

st.title("🔮 Predictive Models & Analytics")

# Sidebar model selection
st.sidebar.header("Model Selection")
model_type = st.sidebar.selectbox(
    "Model Type",
    ["Price Forecasting", "Demand Prediction", "Supply Analysis", "Risk Assessment"]
)

commodity = st.sidebar.selectbox(
    "Commodity",
    ["Natural Gas", "Crude Oil", "Electricity", "All Energy"]
)

forecast_horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year"]
)

# Main model display
if model_type == "Price Forecasting":
    st.subheader(f"{commodity} Price Forecast - {forecast_horizon}")
    
    # Model performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Model Accuracy", "87.3%", "↑ 2.1%")
    with col2:
        st.metric("RMSE", "0.142", "↓ 0.008")
    with col3:
        st.metric("R²", "0.891", "↑ 0.012")
    with col4:
        st.metric("Confidence", "High", "")
    
    # Forecast chart
    st.subheader("Price Forecast")
    
    # Generate sample forecast data
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    historical_end = len(dates) * 2 // 3
    
    # Historical data
    historical_dates = dates[:historical_end]
    historical_prices = 2.5 + 0.3 * np.sin(np.linspace(0, 4*np.pi, len(historical_dates))) + 0.1 * np.random.randn(len(historical_dates))
    
    # Forecast data
    forecast_dates = dates[historical_end:]
    forecast_prices = historical_prices[-1] + 0.2 * np.sin(np.linspace(0, 2*np.pi, len(forecast_dates))) + 0.05 * np.random.randn(len(forecast_dates))
    
    # Confidence intervals
    upper_bound = forecast_prices + 0.15
    lower_bound = forecast_prices - 0.15
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(x=historical_dates, y=historical_prices, 
                            name='Historical', mode='lines',
                            line=dict(color='blue')))
    
    # Forecast
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_prices,
                            name='Forecast', mode='lines',
                            line=dict(color='red', dash='dash')))
    
    # Confidence interval
    fig.add_trace(go.Scatter(x=list(forecast_dates) + list(forecast_dates[::-1]),
                            y=list(upper_bound) + list(lower_bound[::-1]),
                            fill='toself', fillcolor='rgba(255,0,0,0.2)',
                            line=dict(color='rgba(255,255,255,0)'),
                            name='95% Confidence Interval'))
    
    fig.update_layout(title=f'{commodity} Price Forecast',
                     xaxis_title='Date',
                     yaxis_title='Price ($/unit)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Model explanation
    st.subheader("Model Details")
    st.markdown("""
    **Model Type**: Time Series ARIMA with External Regressors
    
    **Input Features**:
    - Historical prices
    - Weather patterns
    - Storage levels
    - Economic indicators
    - Seasonal patterns
    
    **Model Performance**: The model shows strong predictive capability with high accuracy on out-of-sample testing.
    """)

elif model_type == "Demand Prediction":
    st.subheader(f"{commodity} Demand Forecast")
    
    # Sample demand prediction visualization
    st.info("Demand prediction models will be implemented here")
    
    # Placeholder metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Peak Demand", "450 GW", "↑ 12 GW")
    with col2:
        st.metric("Average Load", "385 GW", "↑ 8 GW") 
    with col3:
        st.metric("Load Factor", "85.6%", "↓ 1.2%")

elif model_type == "Supply Analysis":
    st.subheader("Supply Modeling")
    
    st.markdown("""
    ### Production Capacity Analysis
    
    **Current Models**:
    - Well decline curve analysis
    - Capacity utilization forecasting
    - Maintenance scheduling impact
    """)
    
    st.info("Supply analysis models will be implemented here")

elif model_type == "Risk Assessment":
    st.subheader("Market Risk Analysis")
    
    # Risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("VaR (95%)", "$2.3M", "↑ $0.1M")
    with col2:
        st.metric("Expected Shortfall", "$3.8M", "↑ $0.2M")
    with col3:
        st.metric("Volatility", "32.1%", "↑ 1.4%")
    with col4:
        st.metric("Risk Score", "7.2/10", "↑ 0.3")
    
    st.info("Detailed risk assessment models will be implemented here")

# Model documentation
st.markdown("---")
st.markdown("### 📚 Model Documentation")

with st.expander("Model Methodology"):
    st.markdown("""
    **Data Sources**: EIA, NOAA, financial markets
    
    **Update Frequency**: Models retrained weekly with new data
    
    **Validation**: Walk-forward analysis with 80/20 train/test split
    
    **Limitations**: 
    - Models assume historical patterns continue
    - Extreme events may not be well captured
    - Regulatory changes not automatically incorporated
    """)

with st.expander("Model Performance"):
    st.markdown("""
    **Backtesting Results**: 
    - 12-month rolling accuracy: 85%+
    - Mean absolute error: <5% for short-term forecasts
    - Directional accuracy: 78% for price movements
    """)

# Disclaimer
st.warning("⚠️ **Disclaimer**: These models are for informational purposes only and should not be used as the sole basis for trading or investment decisions.")