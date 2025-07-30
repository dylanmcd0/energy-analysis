"""
Data processing and transformation module
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sqlite3
from pathlib import Path


class EnergyDataProcessor:
    """Process and clean energy market data"""
    
    def __init__(self, db_path: str = 'data/database.db'):
        self.db_path = db_path
    
    def clean_price_data(self, data: pd.DataFrame, price_column: str = 'price') -> pd.DataFrame:
        """
        Clean and validate price data
        
        Args:
            data: Raw price data DataFrame
            price_column: Name of the price column
            
        Returns:
            Cleaned DataFrame
        """
        # Remove outliers using IQR method
        Q1 = data[price_column].quantile(0.25)
        Q3 = data[price_column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Filter outliers
        data_cleaned = data[
            (data[price_column] >= lower_bound) & 
            (data[price_column] <= upper_bound)
        ].copy()
        
        # Handle missing values
        data_cleaned[price_column] = data_cleaned[price_column].fillna(
            data_cleaned[price_column].rolling(window=7).mean()
        )
        
        return data_cleaned
    
    def calculate_returns(self, data: pd.DataFrame, price_column: str = 'price') -> pd.DataFrame:
        """Calculate price returns"""
        data = data.copy()
        data['daily_return'] = data[price_column].pct_change()
        data['log_return'] = np.log(data[price_column] / data[price_column].shift(1))
        return data
    
    def add_technical_indicators(self, data: pd.DataFrame, price_column: str = 'price') -> pd.DataFrame:
        """Add technical analysis indicators"""
        data = data.copy()
        
        # Moving averages
        data['ma_7'] = data[price_column].rolling(window=7).mean()
        data['ma_30'] = data[price_column].rolling(window=30).mean()
        data['ma_90'] = data[price_column].rolling(window=90).mean()
        
        # Volatility
        data['volatility_30'] = data[price_column].rolling(window=30).std()
        
        # RSI (Relative Strength Index)
        delta = data[price_column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        return data
    
    def process_seasonal_patterns(self, data: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
        """Extract seasonal patterns from time series data"""
        data = data.copy()
        data[date_column] = pd.to_datetime(data[date_column])
        
        # Extract time components
        data['year'] = data[date_column].dt.year
        data['month'] = data[date_column].dt.month
        data['day_of_year'] = data[date_column].dt.dayofyear
        data['week_of_year'] = data[date_column].dt.isocalendar().week
        data['day_of_week'] = data[date_column].dt.dayofweek
        
        # Seasonal indicators
        data['is_summer'] = data['month'].isin([6, 7, 8]).astype(int)
        data['is_winter'] = data['month'].isin([12, 1, 2]).astype(int)
        data['is_shoulder'] = data['month'].isin([3, 4, 5, 9, 10, 11]).astype(int)
        
        return data
    
    def aggregate_regional_data(self, data: pd.DataFrame, region_column: str = 'region') -> Dict[str, pd.DataFrame]:
        """Aggregate data by region"""
        regional_data = {}
        
        for region in data[region_column].unique():
            regional_data[region] = data[data[region_column] == region].copy()
        
        return regional_data
    
    def create_model_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create features for predictive modeling"""
        data = data.copy()
        
        # Lag features
        for lag in [1, 7, 30]:
            data[f'price_lag_{lag}'] = data['price'].shift(lag)
        
        # Rolling statistics
        for window in [7, 30, 90]:
            data[f'price_mean_{window}'] = data['price'].rolling(window=window).mean()
            data[f'price_std_{window}'] = data['price'].rolling(window=window).std()
            data[f'price_min_{window}'] = data['price'].rolling(window=window).min()
            data[f'price_max_{window}'] = data['price'].rolling(window=window).max()
        
        return data
    
    def validate_data_quality(self, data: pd.DataFrame) -> Dict[str, any]:
        """Perform data quality checks"""
        quality_report = {
            'total_records': len(data),
            'missing_values': data.isnull().sum().to_dict(),
            'duplicate_records': data.duplicated().sum(),
            'date_range': {
                'start': data.index.min() if isinstance(data.index, pd.DatetimeIndex) else None,
                'end': data.index.max() if isinstance(data.index, pd.DatetimeIndex) else None
            },
            'data_types': data.dtypes.to_dict()
        }
        
        # Check for anomalies in numeric columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        anomalies = {}
        
        for col in numeric_columns:
            if col in data.columns:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                anomalies[col] = {
                    'outliers_count': len(data[(data[col] < lower_bound) | (data[col] > upper_bound)]),
                    'outliers_percentage': len(data[(data[col] < lower_bound) | (data[col] > upper_bound)]) / len(data) * 100
                }
        
        quality_report['anomalies'] = anomalies
        
        return quality_report


class DataPipeline:
    """Orchestrate the complete data processing pipeline"""
    
    def __init__(self, db_path: str = 'data/database.db'):
        self.processor = EnergyDataProcessor(db_path)
        self.db_path = db_path
    
    def run_pipeline(self, commodity: str = 'natural_gas') -> Dict[str, any]:
        """Run the complete data processing pipeline"""
        pipeline_results = {
            'timestamp': datetime.now(),
            'commodity': commodity,
            'status': 'started'
        }
        
        try:
            # Load raw data
            raw_data = self.load_raw_data(commodity)
            pipeline_results['raw_records'] = len(raw_data)
            
            # Process data
            processed_data = self.process_commodity_data(raw_data, commodity)
            pipeline_results['processed_records'] = len(processed_data)
            
            # Quality check
            quality_report = self.processor.validate_data_quality(processed_data)
            pipeline_results['quality_report'] = quality_report
            
            # Save processed data
            self.save_processed_data(processed_data, commodity)
            pipeline_results['status'] = 'completed'
            
        except Exception as e:
            pipeline_results['status'] = 'failed'
            pipeline_results['error'] = str(e)
        
        return pipeline_results
    
    def load_raw_data(self, commodity: str) -> pd.DataFrame:
        """Load raw data from database"""
        conn = sqlite3.connect(self.db_path)
        
        table_mapping = {
            'natural_gas': 'natural_gas_prices',
            'crude_oil': 'crude_oil_prices',
            'power': 'power_demand'
        }
        
        table_name = table_mapping.get(commodity, f'{commodity}_data')
        
        try:
            data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        except:
            # Return empty DataFrame if table doesn't exist
            data = pd.DataFrame()
        
        conn.close()
        return data
    
    def process_commodity_data(self, data: pd.DataFrame, commodity: str) -> pd.DataFrame:
        """Process data specific to commodity type"""
        if data.empty:
            return data
        
        # Common processing steps
        if 'price' in data.columns:
            data = self.processor.clean_price_data(data)
            data = self.processor.calculate_returns(data)
            data = self.processor.add_technical_indicators(data)
        
        if 'date' in data.columns:
            data = self.processor.process_seasonal_patterns(data)
        
        # Commodity-specific processing
        if commodity == 'power' and 'region' in data.columns:
            regional_data = self.processor.aggregate_regional_data(data)
            # For now, return combined data
            data = data
        
        return data
    
    def save_processed_data(self, data: pd.DataFrame, commodity: str):
        """Save processed data to database"""
        conn = sqlite3.connect(self.db_path)
        table_name = f'{commodity}_processed'
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()


# Utility functions
def setup_data_directories():
    """Create necessary data directories"""
    directories = ['data/raw', 'data/processed']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Setup directories
    setup_data_directories()
    
    # Run pipeline example
    pipeline = DataPipeline()
    results = pipeline.run_pipeline('natural_gas')
    print(f"Pipeline results: {results}")