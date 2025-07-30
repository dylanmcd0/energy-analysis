"""
Utility functions for the energy analysis platform
"""

import pandas as pd
import numpy as np
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging


# Logging setup
def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """Setup logging configuration"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        filename=log_file
    )
    
    return logging.getLogger(__name__)


# Configuration management
class Config:
    """Configuration management class"""
    
    def __init__(self, config_file: str = '.env'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, str]:
        """Load configuration from environment file"""
        config = {}
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        
        # Override with environment variables
        for key in config:
            env_value = os.getenv(key)
            if env_value:
                config[key] = env_value
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: str):
        """Set configuration value"""
        self.config[key] = value


# Data validation utilities
def validate_price_data(data: pd.DataFrame, price_column: str = 'price') -> Dict[str, Any]:
    """Validate price data for anomalies and quality issues"""
    validation_results = {
        'is_valid': True,
        'issues': [],
        'warnings': [],
        'statistics': {}
    }
    
    if price_column not in data.columns:
        validation_results['is_valid'] = False
        validation_results['issues'].append(f"Price column '{price_column}' not found")
        return validation_results
    
    prices = data[price_column].copy()
    
    # Check for missing values
    missing_count = prices.isnull().sum()
    if missing_count > 0:
        validation_results['warnings'].append(f"Found {missing_count} missing values")
    
    # Check for negative prices
    negative_count = (prices < 0).sum()
    if negative_count > 0:
        validation_results['issues'].append(f"Found {negative_count} negative prices")
        validation_results['is_valid'] = False
    
    # Check for zero prices
    zero_count = (prices == 0).sum()
    if zero_count > 0:
        validation_results['warnings'].append(f"Found {zero_count} zero prices")
    
    # Statistical checks
    if len(prices.dropna()) > 0:
        mean_price = prices.mean()
        std_price = prices.std()
        
        # Check for extreme outliers (beyond 5 standard deviations)
        outliers = prices[(prices > mean_price + 5 * std_price) | (prices < mean_price - 5 * std_price)]
        if len(outliers) > 0:
            validation_results['warnings'].append(f"Found {len(outliers)} extreme outliers")
        
        validation_results['statistics'] = {
            'mean': mean_price,
            'std': std_price,
            'min': prices.min(),
            'max': prices.max(),
            'median': prices.median()
        }
    
    return validation_results


def clean_commodity_name(commodity: str) -> str:
    """Standardize commodity names"""
    commodity_mapping = {
        'natgas': 'natural_gas',
        'ng': 'natural_gas',
        'natural gas': 'natural_gas',
        'crude': 'crude_oil',
        'oil': 'crude_oil',
        'wti': 'crude_oil',
        'brent': 'crude_oil',
        'power': 'electricity',
        'electric': 'electricity',
        'electricity': 'electricity'
    }
    
    return commodity_mapping.get(commodity.lower().strip(), commodity.lower().strip())


# Database utilities
class DatabaseManager:
    """Database management utilities"""
    
    def __init__(self, db_path: str = 'data/database.db'):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure database and directory exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            # Create empty database
            conn = sqlite3.connect(self.db_path)
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Execute a SQL query and return results as DataFrame"""
        conn = sqlite3.connect(self.db_path)
        try:
            if params:
                result = pd.read_sql_query(query, conn, params=params)
            else:
                result = pd.read_sql_query(query, conn)
        finally:
            conn.close()
        
        return result
    
    def insert_data(self, data: pd.DataFrame, table_name: str, if_exists: str = 'append'):
        """Insert data into database table"""
        conn = sqlite3.connect(self.db_path)
        try:
            data.to_sql(table_name, conn, if_exists=if_exists, index=False)
        finally:
            conn.close()
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get information about a database table"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (table_name,))
            
            if not cursor.fetchone():
                return {'exists': False}
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            return {
                'exists': True,
                'columns': [{'name': col[1], 'type': col[2]} for col in columns],
                'row_count': row_count
            }
        
        finally:
            conn.close()


# Time series utilities
def resample_time_series(data: pd.DataFrame, freq: str, 
                        date_column: str = 'date', 
                        agg_methods: Dict[str, str] = None) -> pd.DataFrame:
    """Resample time series data to different frequency"""
    if agg_methods is None:
        agg_methods = {'price': 'mean', 'volume': 'sum'}
    
    data = data.copy()
    data[date_column] = pd.to_datetime(data[date_column])
    data = data.set_index(date_column)
    
    # Resample with specified aggregation methods
    resampled = data.resample(freq).agg(agg_methods)
    
    return resampled.reset_index()


def calculate_correlation_matrix(data: pd.DataFrame, 
                               numeric_columns: List[str] = None) -> pd.DataFrame:
    """Calculate correlation matrix for numeric columns"""
    if numeric_columns is None:
        numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    return data[numeric_columns].corr()


def detect_anomalies(data: pd.Series, method: str = 'iqr', 
                    threshold: float = 1.5) -> pd.Series:
    """Detect anomalies in time series data"""
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        return (data < lower_bound) | (data > upper_bound)
    
    elif method == 'zscore':
        z_scores = np.abs((data - data.mean()) / data.std())
        return z_scores > threshold
    
    else:
        raise ValueError(f"Unknown anomaly detection method: {method}")


# File management utilities
def ensure_directory_exists(directory_path: str):
    """Ensure a directory exists, create if it doesn't"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def save_json(data: Dict[str, Any], filepath: str):
    """Save dictionary as JSON file"""
    ensure_directory_exists(os.path.dirname(filepath))
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file as dictionary"""
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, 'r') as f:
        return json.load(f)


# API utilities
class APIRateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = datetime.now()
        
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls 
                     if (now - call_time).seconds < 60]
        
        # Check if we need to wait
        if len(self.calls) >= self.calls_per_minute:
            oldest_call = min(self.calls)
            wait_time = 60 - (now - oldest_call).seconds
            if wait_time > 0:
                time.sleep(wait_time)
        
        # Record this call
        self.calls.append(now)


def format_currency(value: float, currency: str = 'USD') -> str:
    """Format numeric value as currency"""
    if currency == 'USD':
        return f"${value:.2f}"
    else:
        return f"{value:.2f} {currency}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format numeric value as percentage"""
    return f"{value:.{decimals}f}%"


def format_large_number(value: float, unit: str = '') -> str:
    """Format large numbers with appropriate suffixes"""
    if abs(value) >= 1e9:
        return f"{value/1e9:.1f}B {unit}".strip()
    elif abs(value) >= 1e6:
        return f"{value/1e6:.1f}M {unit}".strip()
    elif abs(value) >= 1e3:
        return f"{value/1e3:.1f}K {unit}".strip()
    else:
        return f"{value:.1f} {unit}".strip()


# Performance monitoring
class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = datetime.now()
    
    def end_timer(self, operation: str):
        """End timing an operation and record duration"""
        if operation in self.start_times:
            duration = (datetime.now() - self.start_times[operation]).total_seconds()
            
            if operation not in self.metrics:
                self.metrics[operation] = []
            
            self.metrics[operation].append(duration)
            del self.start_times[operation]
            
            return duration
        return None
    
    def get_average_time(self, operation: str) -> float:
        """Get average execution time for an operation"""
        if operation in self.metrics and self.metrics[operation]:
            return sum(self.metrics[operation]) / len(self.metrics[operation])
        return 0.0
    
    def get_summary(self) -> Dict[str, Dict[str, float]]:
        """Get performance summary for all operations"""
        summary = {}
        
        for operation, times in self.metrics.items():
            if times:
                summary[operation] = {
                    'count': len(times),
                    'average': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times),
                    'total': sum(times)
                }
        
        return summary


# Initialize global instances
config = Config()
db_manager = DatabaseManager()
performance_monitor = PerformanceMonitor()
logger = setup_logging()

# Example usage and testing
if __name__ == "__main__":
    print("Testing utility functions...")
    
    # Test configuration
    print(f"Config loaded: {len(config.config)} settings")
    
    # Test database
    db_info = db_manager.get_table_info('test_table')
    print(f"Test table exists: {db_info.get('exists', False)}")
    
    # Test performance monitoring
    performance_monitor.start_timer('test_operation')
    # Simulate some work
    import time
    time.sleep(0.1)
    duration = performance_monitor.end_timer('test_operation')
    print(f"Test operation took: {duration:.3f} seconds")
    
    print("Utility functions initialized successfully!")