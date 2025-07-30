import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Fundamentals", page_icon="📈", layout="wide")

st.title("📈 Market Fundamentals")

# Sidebar controls
st.sidebar.header("Analysis Controls")
commodity = st.sidebar.selectbox(
    "Select Commodity",
    ["Natural Gas", "Crude Oil", "Electricity", "Coal", "Renewable Energy"]
)

analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Supply & Demand", "Storage Levels", "Production Data", "Import/Export"]
)

region = st.sidebar.selectbox(
    "Region",
    ["US Total", "Northeast", "Southeast", "Midwest", "West", "Texas"]
)

# Main content based on selections
st.subheader(f"{commodity} - {analysis_type}")

if commodity == "Natural Gas":
    if analysis_type == "Supply & Demand":
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
        
        # Sample storage data
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
    st.subheader("Crude Oil Fundamentals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("US Production", "13.2 MMbbl/d", "↑ 0.3 MMbbl/d")
        st.metric("Strategic Petroleum Reserve", "351 MMbbl", "↓ 2.1 MMbbl")
        st.metric("Commercial Inventory", "421 MMbbl", "↑ 1.8 MMbbl")
    
    with col2:
        st.metric("Refinery Utilization", "89.2%", "↑ 2.1%")
        st.metric("Net Imports", "6.1 MMbbl/d", "↓ 0.4 MMbbl/d")
        st.metric("Days of Supply", "31.8 days", "↑ 0.2 days")

elif commodity == "Electricity":
    st.subheader("Electricity Generation Mix")
    
    generation_data = {
        'Source': ['Natural Gas', 'Coal', 'Nuclear', 'Hydro', 'Wind', 'Solar', 'Other'],
        'Generation (TWh)': [1720, 880, 850, 260, 430, 180, 95]
    }
    df = pd.DataFrame(generation_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(df, values='Generation (TWh)', names='Source',
                    title="US Electricity Generation by Source (2024)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(df, x='Source', y='Generation (TWh)',
                    title="Annual Generation by Source")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info(f"{commodity} fundamentals data will be displayed here")

# Data notes
st.markdown("---")
st.markdown("**Data Sources**: EIA, FERC, Bloomberg")
st.markdown("**Last Updated**: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M EST"))