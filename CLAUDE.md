# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Pulse Crypto Project** - a comprehensive cryptocurrency trading system leveraging Alpaca Markets APIs for real-time crypto data streaming and automated trading strategies.

## Project Architecture

### Core Structure
The project focuses exclusively on cryptocurrency markets with specialized streaming and trading implementations:

```
pulse_crypto/
├── references/
│   └── alpaca-crypto-streaming/             # Crypto data streaming (Phase 3)
├── Boston2025-CryptoTrading/               # Advanced crypto trading system
├── tests/                                  # Testing framework
└── [documentation files]
```

### Cryptocurrency Streaming Framework

**Crypto Data Streaming:**
- WebSocket: `wss://stream.data.alpaca.markets/v1beta3/crypto`
- Format: JSON messages
- Data: 24/7 crypto trades, quotes, bars with real-time streaming
- Primary file: `references/alpaca-crypto-streaming/fixed_crypto_streamer.py`
- Features: 24/7 operation, multiple crypto pairs, real-time price updates

### Key Technical Patterns

1. **24/7 Operation**: Unlike traditional markets, crypto markets never close
2. **WebSocket-Based**: All streaming uses websocket-client library with header authentication
3. **Multi-Asset Support**: BTC/USD, ETH/USD, SOL/USD, AVAX/USD, ADA/USD, DOGE/USD
4. **Real-time Data**: Live trades, quotes, and 1-minute bars
5. **Interactive Workflows**: User-friendly interfaces for crypto selection and monitoring

## Development Commands

### Crypto Data Testing

**Primary Crypto Streaming:**
```bash
cd references/alpaca-crypto-streaming
python fixed_crypto_streamer.py
# Interactive: Enter symbols like BTC/USD,ETH/USD,SOL/USD
```

**Interactive Crypto Interface:**
```bash
cd references/alpaca-crypto-streaming
python interactive_crypto_streamer.py
# User-friendly interface for crypto selection and streaming
```

**Simple Demo:**
```bash
cd references/alpaca-crypto-streaming
python simple_crypto_demo.py
# Quick testing of crypto connections
```

**Comprehensive Testing:**
```bash
cd tests
python test_crypto_market.py
# Full crypto market functionality test
```

### Boston 2025 Advanced Trading System

**Launch Trading System:**
```bash
cd Boston2025-CryptoTrading
python core/crypto_monitor.py
# Real-time crypto monitoring and analysis
```

**Web Dashboard:**
```bash
cd Boston2025-CryptoTrading
python dashboard/web_dashboard.py
# Web-based crypto trading dashboard
```

### Dependencies

**Crypto Streaming:**
```bash
pip install websocket-client
pip install pytest  # for testing
```

**Advanced Trading System:**
```bash
pip install pandas numpy
pip install asyncio aiohttp
pip install websocket-client
```

## Configuration Management

### API Credentials
Crypto streaming uses secure environment variables via `.env` file:
```bash
# references/alpaca-crypto-streaming/.env
API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

The system automatically loads credentials from the `.env` file using the `env_config.py` module for enhanced security.

### Supported Cryptocurrency Pairs

**Tier 1 - Primary Trading Pairs:**
- **BTC/USD** - Bitcoin (highest volume)
- **ETH/USD** - Ethereum (smart contracts)
- **SOL/USD** - Solana (high performance)

**Tier 2 - Secondary Pairs:**
- **AVAX/USD** - Avalanche
- **ADA/USD** - Cardano  
- **DOGE/USD** - Dogecoin

## Data Flow Patterns

### Crypto Data Flow
```
User Input → 24/7 WebSocket Connection → JSON Parsing → Real-time Display → Trading Decisions
```

### Trading System Flow
```
Market Data → Strategy Analysis → Risk Management → Order Execution → Portfolio Tracking
```

## Current Development Status

**Completed:**
- ✅ **Crypto Streaming**: Real-time cryptocurrency data streaming with 24/7 operation
- ✅ **Testing Framework**: Comprehensive crypto market testing
- ✅ **Boston 2025 Foundation**: Advanced trading system architecture

**Active Development:**
- 🔄 **Trading Strategies**: Momentum, mean reversion, and arbitrage algorithms
- 🔄 **Risk Management**: Advanced portfolio optimization and risk controls
- 🔄 **Analytics Dashboard**: Real-time performance monitoring

## Testing Strategy

### Crypto-Specific Testing
- **Integration Tests**: `tests/test_crypto_market.py` - Complete crypto functionality validation
- **Connection Tests**: WebSocket connectivity and authentication
- **Data Quality Tests**: Real-time price accuracy and update frequency
- **24/7 Operation Tests**: Weekend and holiday market access verification

### Critical Test Cases
1. **Authentication**: WebSocket connection and API key validation
2. **Data Reception**: Real crypto data vs simulated data verification
3. **Multi-Symbol Support**: Simultaneous streaming of multiple crypto pairs
4. **24/7 Availability**: Market access during traditional market closures
5. **Error Handling**: Graceful handling of connection failures and data issues

## Key Implementation Insights

### WebSocket Authentication
Crypto streaming uses HTTP header authentication:
```python
headers = {
    'APCA-API-KEY-ID': api_key,
    'APCA-API-SECRET-KEY': secret_key
}
```

### 24/7 Market Advantages
- **Always Available**: No market hours restrictions
- **Global Operation**: Trading across all time zones
- **High Volatility**: More frequent price updates and trading opportunities
- **Weekend Trading**: Active markets when traditional exchanges are closed

### Crypto Symbol Format
Standard crypto pairs use simple format:
- **BTC/USD**: Bitcoin to US Dollar
- **ETH/USD**: Ethereum to US Dollar
- **SOL/USD**: Solana to US Dollar

## Performance Characteristics

- **Crypto Data**: Real-time streaming with minimal latency
- **Throughput**: Multi-symbol simultaneous streaming
- **Availability**: 24/7/365 operation with no downtime
- **Update Frequency**: High-frequency price updates due to crypto market volatility

## Boston 2025 Trading System

The advanced crypto trading system (`Boston2025-CryptoTrading/`) provides institutional-grade features:

### Core Components
- **Real-time Monitoring**: 24/7 crypto market surveillance
- **Trading Strategies**: Momentum, mean reversion, and arbitrage algorithms
- **Risk Management**: Position sizing, stop-loss, and portfolio diversification
- **Portfolio Analytics**: Performance tracking, P&L monitoring, risk metrics

### Trading Strategies
- **Momentum Strategy**: Trend following with technical indicators
- **Mean Reversion Strategy**: Bollinger Bands and statistical analysis
- **Arbitrage Strategy**: Cross-exchange and triangular arbitrage
- **ML Predictions**: Machine learning-based price forecasting

### Key Features
- Multi-asset crypto portfolio management
- Real-time risk monitoring and controls
- Advanced performance analytics
- Web dashboard and CLI interfaces
- Automated trading execution

This system leverages the proven crypto streaming infrastructure to provide professional-grade cryptocurrency trading capabilities optimized for the unique characteristics of 24/7 crypto markets.