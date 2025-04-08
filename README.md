# XRP Futures Trading Bot

A complete automated trading bot for XRP futures on Binance with volume-based breakout strategy, bidirectional (long/short) trading, and multi-layered risk management.

## Features

- **Volume-Based Breakout Strategy**: Identifies high-probability entry points when price breaks key levels with high volume
- **Bidirectional Trading**: Automatically trades both long and short positions
- **Multi-Timeframe Analysis**: Analyzes 1m, 5m, 15m, 1h, and 4h timeframes for confirmation
- **Automated Risk Management**:
  - Take Profit (5%) and Stop Loss (3%) automatic placement
  - Trailing stop-loss implementation
  - Partial profit-taking capability
  - Daily and weekly loss limits
  - Consecutive loss protection
- **Performance Monitoring**: Generates detailed performance reports
- **5x Leverage**: Configured for 5x leverage trading

## Installation

### Prerequisites

- Python 3.8 or higher
- Binance API key with futures trading permissions

### Setup

1. Clone this repository
```bash
git clone https://github.com/kyi000/binance-xrp-bot.git
cd binance-xrp-bot
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on the provided `.env.example`
```bash
cp .env.example .env
# Edit .env with your Binance API credentials
```

## Configuration

You can customize the bot behavior by editing `config.py`. Key settings include:

- `SYMBOL`: Target trading pair (default: 'XRPUSDT')
- `LEVERAGE`: Trading leverage (default: 5x)
- `TP_PERCENTAGE`: Take profit percentage (default: 5%)
- `SL_PERCENTAGE`: Stop loss percentage (default: 3%)
- `USE_MAX_BALANCE`: Whether to use entire available balance (default: True)
- `TESTNET`: Test mode (set to True for testing)
- Risk management parameters (daily/weekly loss limits, etc.)

## Usage

Run the trading bot with:

```bash
python main.py
```

### Testing Mode

It's strongly recommended to test the bot on Binance's testnet before using real funds:

1. Set `TESTNET = True` in `config.py`
2. Obtain testnet API keys from Binance Futures testnet
3. Run the bot and monitor its behavior

## Project Structure

- `config.py` - Configuration settings
- `data_collector.py` - Market data collection from Binance
- `indicator_calculator.py` - Technical indicator calculations
- `signal_generator.py` - Trading signal generation
- `risk_manager.py` - Position sizing and risk control
- `order_executor.py` - Order execution
- `performance_monitor.py` - Trading performance analysis
- `main.py` - Main execution script

## Disclaimer

This trading bot is provided for educational purposes only. Cryptocurrency futures trading involves substantial risk and is not suitable for all investors. Use this software at your own risk. The author is not responsible for any financial losses incurred while using this bot.

## License

MIT