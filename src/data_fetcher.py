"""
Data fetching module for energy market APIs and CSV data loading
"""

import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
import glob


class EnergyDataFetcher:
    """Main class for fetching energy market data from various APIs"""
    
    def __init__(self):
        self.eia_api_key = os.getenv('EIA_API_KEY')
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')
        self.db_path = 'data/database.db'
    
    def fetch_eia_data(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetch data from EIA API
        
        Args:
            series_id: EIA series identifier
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with time series data
        """
        if not self.eia_api_key:
            raise ValueError("EIA API key not found in environment variables")
        
        # TODO: Implement EIA API calls
        # This is a placeholder structure
        pass
    
    def fetch_natural_gas_prices(self) -> pd.DataFrame:
        """Fetch natural gas price data"""
        # TODO: Implement natural gas price fetching
        pass
    
    def fetch_crude_oil_prices(self) -> pd.DataFrame:
        """Fetch crude oil price data"""
        # TODO: Implement crude oil price fetching
        pass
    
    def fetch_power_demand_data(self, region: str = 'US') -> pd.DataFrame:
        """Fetch electricity demand data by region"""
        # TODO: Implement power demand data fetching
        pass
    
    def fetch_storage_data(self, commodity: str = 'natural_gas') -> pd.DataFrame:
        """Fetch storage level data"""
        # TODO: Implement storage data fetching
        pass
    
    def fetch_equity_data(self, symbols: List[str]) -> pd.DataFrame:
        """Fetch energy sector equity data"""
        # TODO: Implement equity data fetching using yfinance or Alpha Vantage
        pass
    
    def save_to_database(self, data: pd.DataFrame, table_name: str):
        """Save data to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
    
    def load_from_database(self, table_name: str) -> pd.DataFrame:
        """Load data from SQLite database"""
        conn = sqlite3.connect(self.db_path)
        data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return data


class WeatherDataFetcher:
    """Fetch weather data for demand forecasting"""
    
    def __init__(self):
        # NOAA API doesn't require key for basic access
        self.base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"
    
    def fetch_temperature_data(self, location: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch temperature data for demand modeling"""
        # TODO: Implement NOAA weather data fetching
        pass


# Utility functions
def create_database_schema():
    """Create initial database schema"""
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    
    # Create tables for different data types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS natural_gas_prices (
            date DATE PRIMARY KEY,
            price REAL,
            volume REAL,
            source TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crude_oil_prices (
            date DATE PRIMARY KEY,
            wti_price REAL,
            brent_price REAL,
            volume REAL,
            source TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS power_demand (
            datetime TIMESTAMP PRIMARY KEY,
            region TEXT,
            demand_mw REAL,
            source TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storage_levels (
            date DATE,
            commodity TEXT,
            storage_level REAL,
            unit TEXT,
            PRIMARY KEY (date, commodity)
        )
    ''')
    
    conn.commit()
    conn.close()


class YFinanceDataLoader:
    """Load and process data from yfinance CSV files"""
    
    def __init__(self, data_dir: str = 'data/financial/yfinance'):
        self.data_dir = data_dir
        
    def get_available_tickers(self) -> List[str]:
        """Get list of available tickers from CSV files"""
        csv_files = glob.glob(os.path.join(self.data_dir, "*.csv"))
        tickers = []
        for file in csv_files:
            filename = os.path.basename(file)
            if filename != 'update_summary.json':
                ticker = filename.replace('.csv', '').replace('_', '=')
                tickers.append(ticker)
        return sorted(tickers)
    
    def load_ticker_data(self, ticker: str, days: int = None) -> pd.DataFrame:
        """
        Load historical data for a specific ticker
        
        Args:
            ticker: Ticker symbol (e.g., 'XLE', 'CL=F')
            days: Number of recent days to return (None for all data)
            
        Returns:
            DataFrame with OHLCV data
        """
        # Convert ticker format for filename
        filename = ticker.replace('=', '_') + '.csv'
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No data file found for ticker {ticker}")
        
        df = pd.read_csv(filepath, index_col=0, parse_dates=True)
        
        if days:
            df = df.tail(days)
            
        return df
    
    def get_latest_prices(self, tickers: List[str] = None) -> pd.DataFrame:
        """
        Get latest price and change for specified tickers
        
        Args:
            tickers: List of ticker symbols (None for all available)
            
        Returns:
            DataFrame with latest price data
        """
        if tickers is None:
            tickers = self.get_available_tickers()
        
        results = []
        for ticker in tickers:
            try:
                data = self.load_ticker_data(ticker, days=2)  # Get last 2 days for change calc
                if len(data) >= 1:
                    latest = data.iloc[-1]
                    prev = data.iloc[-2] if len(data) >= 2 else data.iloc[-1]
                    
                    change = latest['Close'] - prev['Close']
                    change_pct = (change / prev['Close']) * 100
                    
                    results.append({
                        'Ticker': ticker,
                        'Name': latest.get('Name', ''),
                        'Price': latest['Close'],
                        'Change': change,
                        'Change_%': change_pct,
                        'Volume': latest['Volume'],
                        'Date': data.index[-1]
                    })
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def get_commodity_prices(self) -> Dict[str, Dict]:
        """Get latest prices for commodity-related tickers"""
        commodity_tickers = ['CL=F', 'NG=F', 'BZ=F', 'RB=F', 'HO=F', 'USO', 'UNG']
        price_data = self.get_latest_prices(commodity_tickers)
        
        commodity_map = {
            'CL=F': 'WTI Crude Oil',
            'NG=F': 'Natural Gas',
            'BZ=F': 'Brent Crude',
            'RB=F': 'Gasoline',
            'HO=F': 'Heating Oil',
            'USO': 'US Oil Fund',
            'UNG': 'US Natural Gas Fund'
        }
        
        result = {}
        for _, row in price_data.iterrows():
            ticker = row['Ticker']
            if ticker in commodity_map:
                result[commodity_map[ticker]] = {
                    'price': row['Price'],
                    'change': row['Change'],
                    'change_pct': row['Change_%'],
                    'volume': row['Volume']
                }
        
        return result
    
    def get_equity_prices(self) -> Dict[str, Dict]:
        """Get latest prices for energy equity tickers"""
        equity_tickers = ['XLE', 'XOP', 'VDE', 'IYE', 'XOM', 'CVX', 'COP', 'SLB', 'HAL', 'BKR', 'OXY']
        price_data = self.get_latest_prices(equity_tickers)
        
        equity_map = {
            'XLE': 'Energy Select Sector SPDR',
            'XOP': 'SPDR S&P Oil & Gas Exploration',
            'VDE': 'Vanguard Energy ETF',
            'IYE': 'iShares U.S. Energy ETF',
            'XOM': 'Exxon Mobil',
            'CVX': 'Chevron',
            'COP': 'ConocoPhillips',
            'SLB': 'Schlumberger',
            'HAL': 'Halliburton',
            'BKR': 'Baker Hughes',
            'OXY': 'Occidental Petroleum'
        }
        
        result = {}
        for _, row in price_data.iterrows():
            ticker = row['Ticker']
            if ticker in equity_map:
                result[equity_map[ticker]] = {
                    'ticker': ticker,
                    'price': row['Price'],
                    'change': row['Change'],
                    'change_pct': row['Change_%'],
                    'volume': row['Volume']
                }
        
        return result


if __name__ == "__main__":
    # Initialize database schema
    create_database_schema()
    print("Database schema created successfully")