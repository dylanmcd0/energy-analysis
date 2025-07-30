# US Energy Markets Analysis Platform

A personal web application for learning about and analyzing US energy markets including power, oil & gas, and energy equities using public data sources and open-source tools.

## 🎯 Project Overview

This platform aims to provide (near) real-time insights and analysis of US energy markets through:
- **Power Markets**: Grid data, pricing, demand/supply metrics
- **Oil & Gas**: Production, pricing, inventory levels
- **Energy Equities**: Stock performance, sector analysis
- **Blog-style Insights**: Market commentary and analysis

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit (streamlined web interface)
- **Pages**: 
  - Home/Dashboard: Market overview and key metrics
  - Fundamentals: Core market data and trends
  - Models: Predictive analytics and forecasting
  - Insights: Blog-style market analysis
  - About: Project information

### Data Storage Plan
- **Local**: CSV files and SQLite database for development
- **Cloud**: AWS S3 Free Tier for production data and blog content
- **Caching**: Local storage for frequently accessed data

### Automation
- **GitHub Actions**: Scheduled data pulls from public APIs
- **Data Sources**: EIA, FERC, Yahoo Finance, Alpha Vantage
- **Frequency**: Daily/hourly updates depending on data type

### Hosting & Deployment
- **Primary**: Streamlit Community Cloud with custom domain

## 📊 Data Sources

### Public APIs & Datasets Plan
- **EIA (Energy Information Administration)**: Power generation, consumption
- **FERC**: Transmission and market data  
- **Yahoo Finance**: Energy sector equities
- **Alpha Vantage**: Financial market data
- **NOAA**: Weather data for demand forecasting

## 🚀 Getting Started

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/energy-analysis.git
cd energy-analysis

# Create virtual environment
python -m venv energy-env
source energy-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
```bash
# Copy environment template
cp .env.example .env

# Add your API keys
# EIA_API_KEY=your_eia_key
# ALPHA_VANTAGE_KEY=your_av_key
# AWS_ACCESS_KEY_ID=your_aws_key (optional)
# AWS_SECRET_ACCESS_KEY=your_aws_secret (optional)
```

### Start Locally
```bash
streamlit run app.py
```

## 📁 Project Structure Plan

```
energy-analysis/
├── app.py                 # Main Streamlit application
├── pages/                 # Multi-page app structure
│   ├── 1_Dashboard.py     # Home dashboard
│   ├── 2_Fundamentals.py  # Market fundamentals
│   ├── 3_Models.py        # Predictive models
│   ├── 4_Insights.py      # Blog-style insights  
│   └── 5_About.py         # About page
├── data/                  # Local data storage
│   ├── raw/              # Raw downloaded data
│   ├── processed/        # Cleaned datasets
│   └── database.db       # SQLite database
├── src/                   # Source code modules
│   ├── data_fetcher.py   # API data collection
│   ├── data_processor.py # Data cleaning/transformation
│   ├── models.py         # Analytical models
│   └── utils.py          # Utility functions
├── .github/
│   └── workflows/
│       └── data_update.yml # Automated data collection
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔄 Automated Data Pipeline

### GitHub Actions Workflow
- **Schedule**: Runs daily at 6 AM EST
- **Process**: 
  1. Fetch latest data from APIs
  2. Process and clean data
  3. Update local/cloud storage
  4. Commit changes to repository

### Data Flow
```
Public APIs → GitHub Actions → Data Processing → Storage (CSV/SQLite/S3) → Streamlit App
```

## 📝 Blog/Insights Feature

### Content Management
- **Creation**: Markdown files for blog posts
- **Storage**: S3 bucket for scalability
- **Display**: Streamlit components for rendering
- **Upload**: S3 integration for content management



## 🔧 Development

### Adding New Data Sources
1. Add API credentials to `.env`
2. Create fetcher function in `src/data_fetcher.py`
3. Add processing logic in `src/data_processor.py`
4. Update GitHub Actions workflow

### Planned Improvements
1. Add weather to Dashboard page
2. Integrate some form of local storage
3. Set-up AWS S3 free tier
4. Start looking into models

## 📞 Contact

Dylan McDonald: mcdonalddylan2020@gmail.com

Project Link: [https://github.com/yourusername/energy-analysis](https://github.com/yourusername/energy-analysis)

Website Link: [Haven't Done Yet](https://github.com/yourusername/energy-analysis)
