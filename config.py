# config.py
# Configuration file for the XRP futures trading bot

import os
from dotenv import load_dotenv

# Load environment variables from .env file (API keys)
load_dotenv()

# API Keys
API_KEY = os.getenv('BINANCE_API_KEY', '')
API_SECRET = os.getenv('BINANCE_API_SECRET', '')

# Trading Settings
SYMBOL = 'XRPUSDT'  # Trading pair
LEVERAGE = 5  # Leverage setting (5x)
TP_PERCENTAGE = 5  # Take profit percentage (5%)
SL_PERCENTAGE = 3  # Stop loss percentage (3%)
USE_MAX_BALANCE = True  # Use entire available balance

# Exchange Settings
TESTNET = False  # Set to True for testing mode

# Strategy Settings
TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h']  # Timeframes to analyze
MAIN_TIMEFRAME = '15m'  # Main timeframe
LONG_MA_PERIOD = 50  # Long-term moving average period
SHORT_MA_PERIOD = 20  # Short-term moving average period
RSI_PERIOD = 14  # RSI period
BB_PERIOD = 20  # Bollinger Bands period
BB_STD = 2  # Bollinger Bands standard deviation
VOLUME_THRESHOLD = 1.5  # Volume threshold (vs average)

# Risk Management Settings
DAILY_LOSS_LIMIT = 5  # Daily max loss limit (% of account value)
WEEKLY_LOSS_LIMIT = 15  # Weekly max loss limit (% of account value)
MAX_CONSECUTIVE_LOSSES = 3  # Max consecutive losses
PARTIAL_TP_ENABLED = True  # Enable partial take profit
PARTIAL_TP_PERCENTAGE = 50  # Partial take profit target (% of target)
PARTIAL_TP_SIZE = 30  # Partial take profit size (% of position)
TRAILING_STOP_ENABLED = True  # Enable trailing stop
TRAILING_STOP_ACTIVATION = 2  # Trailing stop activation condition (% profit)
TRAILING_STOP_CALLBACK = 0.5  # Trailing stop callback rate

# Order Execution Settings
ORDER_TYPE = 'MARKET'  # Order type (MARKET or LIMIT)
ORDER_TIME_IN_FORCE = 'GTC'  # Order time in force (GTC: Good Till Cancel)

# Logging Settings
LOG_LEVEL = 'INFO'  # Log level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE = 'trading_bot.log'  # Log filename

# Performance Monitoring Settings
PERFORMANCE_REPORT_ENABLED = True  # Enable performance reporting
PERFORMANCE_REPORT_INTERVAL = 24  # Report generation interval (hours)
