#!/usr/bin/env python3
"""
Script to download 2 years of historical data for energy ETFs and proxies using yfinance.
This script overwrites existing CSV files in data/financial/yfinance/ each time it runs.
"""

import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Energy commodity proxies and ETFs
TICKERS = {
    # Commodity ETFs/Proxies
    'USO': 'United States Oil Fund',
    'UNG': 'United States Natural Gas Fund', 
    'URA': 'Global X Uranium ETF',
    'COAL': 'VanEck Coal ETF',
    
    # Energy Sector ETFs
    'XLE': 'Energy Select Sector SPDR Fund',
    'XOP': 'SPDR S&P Oil & Gas Exploration & Production ETF',
    'VDE': 'Vanguard Energy ETF',
    'IYE': 'iShares U.S. Energy ETF',
    
    # Major Energy Companies
    'XOM': 'Exxon Mobil Corporation',
    'CVX': 'Chevron Corporation',
    'COP': 'ConocoPhillips',
    'SLB': 'Schlumberger Limited',
    'HAL': 'Halliburton Company',
    'BKR': 'Baker Hughes Company',
    'OXY': 'Occidental Petroleum Corporation',
    
    # Futures (if available)
    'CL=F': 'WTI Crude Oil Futures',
    'NG=F': 'Natural Gas Futures',
    'BZ=F': 'Brent Crude Oil Futures',
    'RB=F': 'Gasoline RBOB Futures',
    'HO=F': 'Heating Oil Futures'
}

def ensure_output_directory():
    """Ensure the output directory exists."""
    output_dir = os.path.join('data', 'financial', 'yfinance')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def download_ticker_data(ticker, name, period='2y'):
    """
    Download historical data for a single ticker.
    
    Args:
        ticker (str): The ticker symbol
        name (str): Human readable name
        period (str): Period to download (default: 2y)
    
    Returns:
        pd.DataFrame or None: Historical data or None if failed
    """
    try:
        logger.info(f"Downloading data for {ticker} ({name})")
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, auto_adjust=True, prepost=True)
        
        if data.empty:
            logger.warning(f"No data found for {ticker}")
            return None
            
        # Add ticker and name columns for reference
        data['Ticker'] = ticker
        data['Name'] = name
        
        logger.info(f"Successfully downloaded {len(data)} rows for {ticker}")
        return data
        
    except Exception as e:
        logger.error(f"Error downloading data for {ticker}: {e}")
        return None

def save_data_to_csv(data, ticker, output_dir):
    """Save data to CSV file."""
    if data is None or data.empty:
        return False
        
    filename = f"{ticker.replace('=', '_')}.csv"
    filepath = os.path.join(output_dir, filename)
    
    try:
        data.to_csv(filepath, index=True)
        logger.info(f"Saved data to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving data for {ticker}: {e}")
        return False

def main():
    """Main function to download and save all ticker data."""
    logger.info("Starting yfinance data update")
    
    output_dir = ensure_output_directory()
    success_count = 0
    total_count = len(TICKERS)
    
    for ticker, name in TICKERS.items():
        data = download_ticker_data(ticker, name)
        if save_data_to_csv(data, ticker, output_dir):
            success_count += 1
    
    logger.info(f"Completed: {success_count}/{total_count} tickers successfully updated")
    
    # Create a summary file with last update time
    summary = {
        'last_updated': datetime.now().isoformat(),
        'total_tickers': total_count,
        'successful_downloads': success_count,
        'failed_downloads': total_count - success_count
    }
    
    summary_path = os.path.join(output_dir, 'update_summary.json')
    import json
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Update summary saved to {summary_path}")

if __name__ == "__main__":
    main()