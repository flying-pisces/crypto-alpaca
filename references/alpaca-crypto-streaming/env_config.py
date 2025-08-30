#!/usr/bin/env python3
"""
Environment Configuration Loader
Secure configuration loading from .env file
"""

import os
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables on import
load_env_file()

# Alpaca API Credentials
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# Crypto WebSocket Configuration
CRYPTO_WS_URL = os.getenv('CRYPTO_WS_URL', "wss://stream.data.alpaca.markets/v1beta3/crypto/us")

# Popular crypto symbols for testing
POPULAR_CRYPTOS = os.getenv('POPULAR_CRYPTOS', '').split(',') if os.getenv('POPULAR_CRYPTOS') else [
    "BTC/USD", "ETH/USD", "AVAX/USD", "ADA/USD", "SOL/USD", 
    "DOGE/USD", "LTC/USD", "DOT/USD", "LINK/USD", "UNI/USD"
]

# Data stream types
STREAM_TYPES = {
    "trades": "t",      # Individual trades
    "quotes": "q",      # Best bid/ask quotes  
    "bars": "b",        # Minute bars
    "daily_bars": "d",  # Daily bars
    "orderbook": "o"    # Order book updates (level 1)
}

# Default subscription for interactive mode
DEFAULT_STREAMS = os.getenv('DEFAULT_STREAMS', '').split(',') if os.getenv('DEFAULT_STREAMS') else ["trades", "quotes", "bars"]