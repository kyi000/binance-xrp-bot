# main.py
# Main execution file for the XRP futures trading bot

import os
import time
import json
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
from loguru import logger
import config
from data_collector import DataCollector

# Set up logging
logger.remove()
logger.add(
    config.LOG_FILE,
    rotation="500 MB",
    compression="zip",
    level=config.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
logger.add(
    lambda msg: print(msg),
    level=config.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

def setup_binance_client():
    """
    Initialize Binance API client
    
    Returns:
        Client: Binance API client object
    """
    api_key = config.API_KEY
    api_secret = config.API_SECRET
    
    if not api_key or not api_secret:
        logger.error("API keys not configured. Check config.py file.")
        raise ValueError("API keys required.")
    
    try:
        if config.TESTNET:
            client = Client(api_key, api_secret, testnet=True)
            logger.info("Connected to Binance testnet mode.")
        else:
            client = Client(api_key, api_secret)
            logger.info("Connected to Binance live trading mode.")
        
        return client
    except Exception as e:
        logger.error(f"Binance client initialization error: {e}")
        raise

def check_connection(client):
    """
    Verify Binance server connection
    
    Args:
        client: Binance API client object
        
    Returns:
        bool: Connection success
    """
    try:
        server_time = client.get_server_time()
        local_time = int(time.time() * 1000)
        time_diff = abs(server_time['serverTime'] - local_time)
        
        logger.info(f"Server time: {datetime.fromtimestamp(server_time['serverTime']/1000).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Local time: {datetime.fromtimestamp(local_time/1000).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Time difference: {time_diff}ms")
        
        if time_diff > 10000:  # More than 10 seconds difference
            logger.warning("Large time difference between local system and server. Consider syncing your system time.")
        
        return True
    except Exception as e:
        logger.error(f"Binance server connection check error: {e}")
        return False

def main():
    """
    Main execution function
    """
    logger.info("XRP Futures Trading Bot Starting")
    
    try:
        # Initialize Binance client
        client = setup_binance_client()
        
        # Check connection
        if not check_connection(client):
            logger.error("Cannot connect to Binance server. Exiting program.")
            return
        
        # Initialize components
        # Note: For now, only the DataCollector is implemented
        # Other components would be initialized here in the full implementation
        components = {
            'client': client,
            'data_collector': DataCollector(client),
            'last_signal_time': datetime.now(),
        }
        
        # Main loop
        logger.info("Trading loop starting")
        
        # Demo loop - in a real implementation, this would include signal generation and order execution
        for i in range(3):  # Just run 3 iterations for demo
            try:
                # 1. Collect market data
                for tf in config.TIMEFRAMES:
                    data = components['data_collector'].get_latest_data(tf, force_update=True)
                    if data is not None:
                        logger.info(f"Collected {len(data)} candles for {tf} timeframe")
                
                # 2. Check order book imbalance
                imbalance = components['data_collector'].analyze_order_book_imbalance()
                logger.info(f"Order book imbalance: {imbalance:.2f}")
                
                # 3. Check for abnormal volume
                abnormal = components['data_collector'].detect_abnormal_volume()
                logger.info(f"Abnormal volume detected: {abnormal}")
                
                # 4. Get funding rate
                funding = components['data_collector'].get_funding_rate()
                logger.info(f"Current funding rate: {funding:.6f}")
                
                # Wait before next iteration
                logger.info("Waiting 10 seconds before next data collection...")
                time.sleep(10)
                
            except BinanceAPIException as e:
                logger.error(f"Binance API error: {e}")
                time.sleep(10)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(60)
        
        logger.info("Demo completed. In a real implementation, the bot would continue running.")
        logger.info("For full implementation, you would need to:")
        logger.info("1. Implement indicator_calculator.py")
        logger.info("2. Implement signal_generator.py")
        logger.info("3. Implement risk_manager.py")
        logger.info("4. Implement order_executor.py")
        logger.info("5. Implement performance_monitor.py")
        logger.info("6. Expand this main.py file to use all components")
    
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
    except Exception as e:
        logger.critical(f"Critical error causing program termination: {e}")
    finally:
        logger.info("XRP Futures Trading Bot Terminated")

if __name__ == "__main__":
    main()
