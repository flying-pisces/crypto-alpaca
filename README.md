# Crypto Alpaca - Minimalist Cryptocurrency Trading System

A clean, consolidated cryptocurrency trading system using Alpaca Markets API with real-time 24/7 WebSocket streaming.

## 🚀 Quick Start

### Prerequisites
```bash
pip install websocket-client
```

### Setup
1. Add your Alpaca API credentials to `.env` file:
```
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

2. Run the test to verify everything works:
```bash
cd tests
python test_crypto_market.py
```

3. For interactive streaming:
```bash
cd tests
python crypto_alpaca.py
```

## 📁 Minimal Structure

```
crypto-alpaca/
├── .env                        # API credentials (secure)
├── tests/
│   ├── crypto_alpaca.py       # Consolidated crypto trading class
│   └── test_crypto_market.py  # Comprehensive testing
└── README.md                   # This file
```

## 🪙 Features

- **24/7 Operation**: Crypto markets never close
- **Real-time Streaming**: WebSocket connection for live data
- **Multiple Crypto Pairs**: BTC, ETH, SOL, AVAX, ADA, DOGE, and more
- **Clean Architecture**: Single class with all functionality
- **Secure Configuration**: Environment variables for API keys

## 💻 Usage

### Basic Streaming
```python
from crypto_alpaca import CryptoAlpaca

crypto = CryptoAlpaca()
crypto.stream_for_duration(["BTC/USD", "ETH/USD"], duration=30)
```

### Interactive Session
```python
from crypto_alpaca import interactive_session

interactive_session()
```

### Quick Price Check
```python
from crypto_alpaca import quick_stream

prices = quick_stream(["BTC/USD", "ETH/USD"], duration=10)
print(prices)
```

## 🔧 API Methods

- `connect()` - Connect to WebSocket
- `subscribe(symbols, streams)` - Subscribe to crypto pairs
- `disconnect()` - Close connection
- `get_latest_price(symbol)` - Get current price
- `stream_for_duration(symbols, duration)` - Stream for X seconds
- `run_interactive()` - Interactive streaming session

## 📊 Supported Data Types

- **Trades**: Individual trade executions
- **Quotes**: Bid/ask spreads
- **Bars**: OHLC minute bars

## ✅ Testing

Run the comprehensive test to verify all functionality:
```bash
cd tests
python test_crypto_market.py
```

Expected output includes connection status, authentication, data reception, and 24/7 operation verification.

## 🌟 Advantages

- Crypto markets operate 24/7/365
- No market hours restrictions
- Global trading opportunities
- High volatility for active trading
- Weekend and holiday trading

## 📝 License

MIT