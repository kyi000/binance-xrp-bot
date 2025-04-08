# data_collector.py
# Module for collecting market data from Binance

import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import time
from datetime import datetime, timedelta
from loguru import logger
import config

class DataCollector:
    def __init__(self, client):
        """
        Initialize the data collector
        
        Args:
            client: Binance API client object
        """
        self.client = client
        self.symbol = config.SYMBOL
        self.timeframes = config.TIMEFRAMES
        self.data_cache = {tf: None for tf in self.timeframes}  # Cache for each timeframe
        self.last_update = {tf: None for tf in self.timeframes}  # Last update time
    
    def get_historical_klines(self, timeframe, limit=100):
        """
        Get historical candlestick data for a specific timeframe
        
        Args:
            timeframe: Time interval (e.g. '1m', '5m', '15m')
            limit: Number of candles to retrieve
            
        Returns:
            DataFrame: OHLCV data
        """
        try:
            # Request klines data from current time for the specified limit
            klines = self.client.futures_klines(
                symbol=self.symbol,
                interval=timeframe,
                limit=limit
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convert data types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
                
            # Select needed columns
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            df.set_index('timestamp', inplace=True)
            
            # Update cache
            self.data_cache[timeframe] = df
            self.last_update[timeframe] = datetime.now()
            
            logger.debug(f"{timeframe} timeframe data collected: {len(df)} candles")
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Data collection error: {e}")
            return None
    
    def get_latest_data(self, timeframe, force_update=False):
        """
        Get latest data with caching functionality
        
        Args:
            timeframe: Time interval
            force_update: Force refresh data
            
        Returns:
            DataFrame: Latest OHLCV data
        """
        # Get new data if cache is empty or force update
        if self.data_cache[timeframe] is None or force_update:
            return self.get_historical_klines(timeframe)
        
        # Set appropriate update interval based on timeframe
        update_intervals = {
            '1m': timedelta(seconds=30),
            '5m': timedelta(minutes=1),
            '15m': timedelta(minutes=3),
            '1h': timedelta(minutes=10),
            '4h': timedelta(minutes=30)
        }
        
        # Update if past the update interval
        if (datetime.now() - self.last_update[timeframe]) > update_intervals.get(timeframe, timedelta(minutes=1)):
            return self.get_historical_klines(timeframe)
        
        return self.data_cache[timeframe]
    
    def get_order_book(self, limit=20):
        """
        Get order book data
        
        Args:
            limit: Number of price levels
            
        Returns:
            dict: Order book data
        """
        try:
            order_book = self.client.futures_order_book(symbol=self.symbol, limit=limit)
            return order_book
        except Exception as e:
            logger.error(f"Error fetching order book: {e}")
            return None
    
    def get_recent_trades(self, limit=100):
        """
        Get recent trades
        
        Args:
            limit: Number of trades
            
        Returns:
            list: Recent trades
        """
        try:
            trades = self.client.futures_recent_trades(symbol=self.symbol, limit=limit)
            return trades
        except Exception as e:
            logger.error(f"Error fetching recent trades: {e}")
            return None
    
    def analyze_order_book_imbalance(self):
        """
        Analyze order book imbalance
        
        Returns:
            float: Order book imbalance indicator (-1 to 1, positive means more buy pressure)
        """
        order_book = self.get_order_book(limit=20)
        if not order_book:
            return 0
        
        # Calculate buy/sell volumes
        bids_volume = sum(float(bid[1]) for bid in order_book['bids'])
        asks_volume = sum(float(ask[1]) for ask in order_book['asks'])
        
        # Calculate imbalance (-1 to 1)
        if bids_volume + asks_volume > 0:
            imbalance = (bids_volume - asks_volume) / (bids_volume + asks_volume)
            return imbalance
        return 0
    
    def get_funding_rate(self):
        """
        Get current funding rate
        
        Returns:
            float: Current funding rate
        """
        try:
            funding_rate = self.client.futures_funding_rate(symbol=self.symbol, limit=1)[0]
            return float(funding_rate['fundingRate'])
        except Exception as e:
            logger.error(f"Error fetching funding rate: {e}")
            return 0
    
    def detect_abnormal_volume(self, timeframe=config.MAIN_TIMEFRAME, threshold=2.0):
        """
        Detect abnormal trading volume
        
        Args:
            timeframe: Timeframe to check
            threshold: Volume threshold multiplier versus average
            
        Returns:
            bool: True if abnormal volume detected
        """
        df = self.get_latest_data(timeframe)
        if df is None or len(df) < 20:
            return False
        
        # Calculate average volume of last 20 candles
        avg_volume = df['volume'].tail(20).mean()
        current_volume = df['volume'].iloc[-1]
        
        # Return True if current volume exceeds threshold
        return current_volume > avg_volume * threshold
