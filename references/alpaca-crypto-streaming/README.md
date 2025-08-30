# 🚀 Alpaca Crypto Streaming - Phase 3

**Real-time cryptocurrency data streaming with 24/7 operation**

Phase 3 of the Pulse Element project implementing comprehensive crypto data streaming capabilities using Alpaca's WebSocket API.

## 🌟 Key Features

### 24/7 Market Operation
- **Always Live**: Cryptocurrency markets never close
- **No Market Hours**: No weekend/holiday restrictions  
- **Real-time Data**: Continuous streaming from Alpaca's crypto exchange
- **Global Coverage**: Major crypto pairs (BTC/USD, ETH/USD, etc.)

### Technical Architecture
- **JSON WebSocket**: Simple JSON format (unlike options' MSGPACK)
- **Multiple Streams**: Trades, quotes, bars, orderbooks
- **Real-time Validation**: Live price verification for selected pairs
- **Interactive Interface**: 4-step user-friendly workflow

## 📁 Project Structure

```
references/alpaca-crypto-streaming/
├── .env                             # Secure environment variables
├── env_config.py                    # Environment configuration loader
├── basic_crypto_streamer.py         # Core WebSocket streamer  
├── interactive_crypto_streamer.py   # Interactive user interface
├── test_crypto_streaming.py         # Comprehensive test suite
├── requirements.txt                 # Dependencies
└── README.md                        # This documentation
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd references/alpaca-crypto-streaming/
pip install -r requirements.txt
```

### 2. Run Interactive Streaming
```bash
python interactive_crypto_streamer.py
```

### 3. Or Test Basic Streaming
```bash
python basic_crypto_streamer.py
```

## 💰 Supported Crypto Pairs

Popular cryptocurrencies included:
- **BTC/USD** - Bitcoin
- **ETH/USD** - Ethereum  
- **AVAX/USD** - Avalanche
- **ADA/USD** - Cardano
- **SOL/USD** - Solana
- **DOGE/USD** - Dogecoin
- **LTC/USD** - Litecoin
- **DOT/USD** - Polkadot
- **LINK/USD** - Chainlink
- **UNI/USD** - Uniswap

## 📊 Data Stream Types

### Available Streams:
1. **Trades** (`t`) - Individual buy/sell transactions
2. **Quotes** (`q`) - Best bid/ask prices  
3. **Bars** (`b`) - 1-minute OHLC price bars
4. **Daily Bars** (`d`) - Daily price summaries
5. **Orderbook** (`o`) - Level 1 order book data

## 🔄 Interactive Workflow

### 4-Step Process:
1. **Select Crypto Pairs**: Choose from popular list or custom symbols
2. **Choose Data Streams**: Pick trade, quote, and/or bar data
3. **Connect & Authenticate**: Automatic WebSocket setup
4. **Stream with Validation**: Live data with price verification

## 🧪 Testing & Validation

### Run Test Suite:
```bash
python test_crypto_streaming.py
```

### Test Coverage:
- ✅ Configuration validation
- ✅ WebSocket connection simulation  
- ✅ 24/7 operation awareness
- ✅ JSON message parsing
- ✅ Price validation features
- ✅ Interactive workflow components

## 🌐 WebSocket Details

### Endpoint:
```
wss://stream.data.alpaca.markets/v1beta3/crypto/us
```

### Authentication:
- Same API credentials as stock/options
- HTTP headers for initial auth
- Message-based subscription

### Message Format:
```json
{
  "action": "subscribe",
  "trades": ["BTC/USD", "ETH/USD"],
  "quotes": ["BTC/USD"], 
  "bars": ["BTC/USD"]
}
```

## 📈 Sample Output

### Trade Stream:
```
[14:32:15] 💰 BTC/USD TRADE: $45,123.45 | Size: 0.0250 | 📈 BUY
[14:32:16] 💰 ETH/USD TRADE: $3,201.75 | Size: 1.5000 | 📉 SELL
```

### Quote Stream:
```
[14:32:17] 📊 BTC/USD QUOTE: $45,120.00 / $45,125.00 | Spread: $5.00 (0.011%)
[14:32:18] 📊 ETH/USD QUOTE: $3,200.50 / $3,202.00 | Spread: $1.50 (0.047%)
```

### Bar Stream:
```
[14:33:00] 📈 BTC/USD BAR: O:$45,120.00 H:$45,130.00 L:$45,115.00 C:$45,125.00 | 
           Vol: 12.45 | VWAP: $45,122.50
```

## 🔗 Integration with Phase 1 & 2

### Shared Components:
- **Authentication**: Same Alpaca API credentials
- **Architecture**: Similar modular design pattern
- **WebSocket Base**: Common connection handling

### Differences from Stock/Options:
- **Format**: JSON vs MSGPACK (options) 
- **Market Hours**: 24/7 vs business hours
- **Complexity**: Simpler than options streaming
- **Symbol Format**: BTC/USD vs AAPL240315C00172500

## ⚡ Performance Notes

### Advantages:
- **JSON Simplicity**: Easier parsing than binary MSGPACK
- **24/7 Availability**: No market close complications
- **High Frequency**: Crypto trades happen continuously
- **Global Market**: Not limited to US trading hours

### Considerations:
- **Volume**: High-activity pairs generate many messages
- **Volatility**: Crypto prices change rapidly
- **Network**: Continuous streaming requires stable connection

## 🛠️ Development

### Adding New Crypto Pairs:
```python
# Add to crypto_config.py
POPULAR_CRYPTOS.append("NEW/USD")
```

### Custom Stream Handlers:
```python
def custom_trade_handler(trade):
    symbol = trade.get("S")
    price = trade.get("p")
    # Custom processing logic
```

## 📋 Todo & Future Enhancements

### Potential Additions:
- [ ] Historical crypto data integration
- [ ] Crypto portfolio tracking
- [ ] Price alerts and notifications
- [ ] Technical indicators for crypto
- [ ] Multi-exchange aggregation
- [ ] Crypto options (if available)

## 🔧 Troubleshooting

### Common Issues:
1. **Connection Fails**: Check API credentials in .env file
2. **No Data**: Verify crypto pair format (BTC/USD not BTCUSD)
3. **JSON Errors**: Ensure websocket-client is installed
4. **Timeout**: Crypto servers may be under high load

### Debug Mode:
```python
# Enable debug in basic_crypto_streamer.py
websocket.enableTrace(True)
```

---

## 📞 Support

For issues with this crypto streaming implementation:
- Check test results: `python test_crypto_streaming.py`
- Verify configuration: Review .env file
- Test basic connection: `python basic_crypto_streamer.py`

**Part of Pulse Element Project Phase 3** - Building on successful stock (Phase 1) and options (Phase 2) streaming implementations.