import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Insights", page_icon="📝", layout="wide")

st.title("📝 Market Insights & Analysis")

# Sidebar filters
st.sidebar.header("Filter Insights")
category = st.sidebar.selectbox(
    "Category",
    ["All", "Market Commentary", "Technical Analysis", "Fundamental Analysis", "Policy & Regulation"]
)

time_filter = st.sidebar.selectbox(
    "Time Period",
    ["Last Week", "Last Month", "Last Quarter", "All Time"]
)

author_filter = st.sidebar.selectbox(
    "Author",
    ["All Authors", "Energy Team", "Data Science Team", "Guest Contributors"]
)

# Featured insight
st.subheader("🔥 Featured Analysis")

with st.container():
    st.markdown("""
    ### Natural Gas Storage Reaches Critical Levels as Winter Approaches
    
    **Published**: December 15, 2024 | **Author**: Energy Analysis Team
    
    **Key Takeaways**:
    - Underground storage levels are 8% below five-year average
    - Cold weather forecasts suggest increased heating demand
    - LNG export capacity continues to grow, adding demand pressure
    
    **Market Impact**: Short-term price volatility expected, with potential for price spikes during cold snaps.
    """)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Read Full Analysis"):
            st.info("Full analysis would open here")
    with col2:
        st.markdown("📊 **Views**: 1,247")
    with col3:
        st.markdown("🏷️ **Tags**: Natural Gas, Storage, Winter Outlook")

st.markdown("---")

# Recent insights
st.subheader("📰 Recent Insights")

insights_data = [
    {
        "title": "Renewable Energy Capacity Additions Accelerate",
        "date": "2024-12-14",
        "author": "Data Science Team",
        "category": "Fundamental Analysis",
        "preview": "Solar and wind installations exceeded expectations in Q4, with grid integration challenges emerging...",
        "tags": ["Renewables", "Grid", "Capacity"],
        "views": 892
    },
    {
        "title": "Crude Oil Inventory Patterns Signal Market Shift",
        "date": "2024-12-13", 
        "author": "Energy Team",
        "category": "Technical Analysis",
        "preview": "Weekly inventory data shows unusual patterns suggesting potential supply disruptions ahead...",
        "tags": ["Crude Oil", "Inventory", "Supply"],
        "views": 1156
    },
    {
        "title": "Federal Energy Policy Changes Impact Market Dynamics",
        "date": "2024-12-12",
        "author": "Guest Contributors",
        "category": "Policy & Regulation",
        "preview": "New regulatory framework creates opportunities and challenges for energy market participants...",
        "tags": ["Policy", "Regulation", "Market Structure"],
        "views": 743
    },
    {
        "title": "Regional Power Market Convergence Analysis",
        "date": "2024-12-11",
        "author": "Energy Team", 
        "category": "Market Commentary",
        "preview": "Cross-regional price correlations suggest increasing market integration despite transmission constraints...",
        "tags": ["Power Markets", "Regional", "Transmission"],
        "views": 634
    }
]

for insight in insights_data:
    if category == "All" or insight["category"] == category:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {insight['title']}")
                st.markdown(f"**{insight['date']}** | {insight['author']} | *{insight['category']}*")
                st.markdown(insight['preview'])
                
                # Tags
                tags_str = " | ".join([f"#{tag}" for tag in insight['tags']])
                st.markdown(f"🏷️ {tags_str}")
            
            with col2:
                st.markdown(f"👁️ **Views**: {insight['views']}")
                if st.button(f"Read More", key=insight['title']):
                    st.info("Full article would open here")
            
            st.markdown("---")

# Analytics dashboard
st.subheader("📊 Content Analytics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Articles", "47", "↑ 3")

with col2:
    st.metric("Monthly Views", "12,847", "↑ 1,234")

with col3:
    st.metric("Avg. Read Time", "4.2 min", "↑ 0.3 min")

with col4:
    st.metric("Engagement Rate", "68%", "↑ 5%")

# Popular tags
st.subheader("🔥 Trending Topics")

popular_tags = [
    ("Natural Gas", 23),
    ("Crude Oil", 19), 
    ("Renewables", 15),
    ("Power Markets", 12),
    ("Policy", 8),
    ("Storage", 7),
    ("LNG", 6)
]

cols = st.columns(len(popular_tags))
for i, (tag, count) in enumerate(popular_tags):
    with cols[i]:
        st.metric(f"#{tag}", f"{count} articles")

# Newsletter signup
st.markdown("---")
st.subheader("📧 Stay Updated")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Subscribe to Energy Insights Weekly**
    
    Get the latest market analysis, data insights, and energy trends delivered to your inbox every Monday.
    """)
    
    email = st.text_input("Email Address", placeholder="your.email@example.com")
    
    if st.button("Subscribe"):
        if email:
            st.success("✅ Subscription request submitted! Check your email for confirmation.")
        else:
            st.error("Please enter a valid email address")

with col2:
    st.markdown("**Newsletter Stats**")
    st.metric("Subscribers", "2,847")
    st.metric("Open Rate", "34.2%")
    st.metric("Click Rate", "8.7%")

# Content submission
st.markdown("---")
st.subheader("✍️ Contribute")

with st.expander("Submit Guest Analysis"):
    st.markdown("""
    **Guest Contribution Guidelines**:
    - Original analysis and insights
    - Data-driven content preferred
    - 800-2000 words
    - Include sources and methodology
    
    **Topics of Interest**:
    - Market analysis and forecasting
    - Policy impact assessments  
    - Technology trends in energy
    - Regional market dynamics
    """)
    
    if st.button("Submit Proposal"):
        st.info("Submission form would open here")