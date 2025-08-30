#!/usr/bin/env python3
"""
Basic Crypto Streamer
Phase 3 of Pulse Element Project

Real-time crypto data streaming from Alpaca using WebSocket JSON protocol.
Unlike options (MSGPACK), crypto uses standard JSON format.
24/7 operation - crypto markets never close.
"""

import json
import websocket
import threading
import time
from datetime import datetime
from env_config import API_KEY, SECRET_KEY, CRYPTO_WS_URL, STREAM_TYPES

class AlpacaCryptoStreamer:
    """WebSocket streamer for Alpaca crypto data"""
    
    def __init__(self):
        self.ws = None
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.ws_url = CRYPTO_WS_URL
        self.is_connected = False
        self.is_authenticated = False
        self.subscribed_symbols = set()
        
    def connect(self):
        """Connect to crypto WebSocket"""
        try:
            print(f"🔌 Connecting to crypto WebSocket...")
            
            # Create WebSocket connection with headers
            headers = {
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.secret_key
            }
            
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                header=[f"{k}: {v}" for k, v in headers.items()],
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Start WebSocket in background thread
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
            # Wait for connection
            for _ in range(50):  # 5 seconds max
                if self.is_connected:
                    break
                time.sleep(0.1)
            
            if not self.is_connected:
                raise Exception("Failed to connect within timeout")
                
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def _on_open(self, ws):
        """Handle WebSocket connection opened"""
        print("🔗 Crypto WebSocket connected")
        self.is_connected = True
        
        # DO NOT send auth message - headers handle authentication automatically!
        print("🔐 Authentication via headers (automatic)...")
    
    def _on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Handle different message types
            if isinstance(data, list):
                # Multiple messages in array
                for item in data:
                    self._process_message(item)
            else:
                # Single message
                self._process_message(data)
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
        except Exception as e:
            print(f"❌ Message processing error: {e}")
    
    def _process_message(self, msg):
        """Process individual message"""
        msg_type = msg.get("T")
        
        if msg_type == "success":
            if msg.get("msg") == "connected":
                print("✅ Connected to crypto stream")
            elif msg.get("msg") == "authenticated":
                print("✅ Crypto authenticated successfully")
                self.is_authenticated = True
            
        elif msg_type == "subscription":
            # Subscription confirmation
            if msg.get("msg") == "subscribed":
                streams = msg.get("trades", []) + msg.get("quotes", []) + msg.get("bars", [])
                print(f"✅ Subscribed to crypto streams: {streams}")
            
        elif msg_type == "t":
            # Trade data
            self._handle_trade(msg)
            
        elif msg_type == "q": 
            # Quote data
            self._handle_quote(msg)
            
        elif msg_type == "b":
            # Bar data (minute bars)
            self._handle_bar(msg)
            
        elif msg_type == "d":
            # Daily bar data
            self._handle_daily_bar(msg)
            
        elif msg_type == "o":
            # Orderbook data
            self._handle_orderbook(msg)
            
        elif msg_type == "error":
            # Skip "already authenticated" - it's expected with header auth
            if "already authenticated" not in str(msg.get("msg", "")):
                print(f"❌ API Error: {msg.get('msg', 'Unknown error')}")
    
    def _handle_trade(self, trade):
        """Handle crypto trade data"""
        symbol = trade.get("S", "N/A")
        price = trade.get("p", 0)
        size = trade.get("s", 0)
        timestamp = trade.get("t", "")
        taker_side = trade.get("tks", "")  # B=buyer, S=seller
        
        # Format timestamp
        time_str = self._format_timestamp(timestamp)
        
        # Format taker side
        side_indicator = "📈 BUY" if taker_side == "B" else "📉 SELL"
        
        print(f"[{time_str}] 💰 {symbol} TRADE: ${price:,.2f} | "
              f"Size: {size:,.4f} | {side_indicator}")
    
    def _handle_quote(self, quote):
        """Handle crypto quote data"""
        symbol = quote.get("S", "N/A")
        bid = quote.get("bp", 0)
        ask = quote.get("ap", 0)
        bid_size = quote.get("bs", 0)
        ask_size = quote.get("as", 0)
        timestamp = quote.get("t", "")
        
        time_str = self._format_timestamp(timestamp)
        spread = ask - bid
        spread_pct = (spread / bid * 100) if bid > 0 else 0
        
        print(f"[{time_str}] 📊 {symbol} QUOTE: "
              f"${bid:,.2f} / ${ask:,.2f} | "
              f"Spread: ${spread:.2f} ({spread_pct:.3f}%)")
    
    def _handle_bar(self, bar):
        """Handle crypto minute bar data"""
        symbol = bar.get("S", "N/A")
        open_price = bar.get("o", 0)
        high = bar.get("h", 0)
        low = bar.get("l", 0)
        close = bar.get("c", 0)
        volume = bar.get("v", 0)
        vwap = bar.get("vw", 0)  # Volume weighted average price
        timestamp = bar.get("t", "")
        
        time_str = self._format_timestamp(timestamp)
        
        print(f"[{time_str}] 📈 {symbol} BAR: "
              f"O:${open_price:,.2f} H:${high:,.2f} L:${low:,.2f} C:${close:,.2f} | "
              f"Vol: {volume:,.2f} | VWAP: ${vwap:,.2f}")
    
    def _handle_daily_bar(self, bar):
        """Handle crypto daily bar data"""
        symbol = bar.get("S", "N/A")
        open_price = bar.get("o", 0)
        high = bar.get("h", 0)
        low = bar.get("l", 0)
        close = bar.get("c", 0)
        volume = bar.get("v", 0)
        
        print(f"📊 {symbol} DAILY: O:${open_price:,.2f} H:${high:,.2f} "
              f"L:${low:,.2f} C:${close:,.2f} | Vol: {volume:,.2f}")
    
    def _handle_orderbook(self, orderbook):
        """Handle crypto orderbook data"""
        symbol = orderbook.get("S", "N/A")
        bid = orderbook.get("b", 0)
        ask = orderbook.get("a", 0)
        
        print(f"📚 {symbol} ORDERBOOK: Bid: ${bid:,.2f} | Ask: ${ask:,.2f}")
    
    def _format_timestamp(self, timestamp_str):
        """Format timestamp for display"""
        if not timestamp_str:
            return datetime.now().strftime("%H:%M:%S")
        
        try:
            # Parse RFC3339 timestamp
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%H:%M:%S")
        except:
            return timestamp_str[:8] if len(timestamp_str) > 8 else timestamp_str
    
    def subscribe_to_crypto(self, symbols, streams=None):
        """Subscribe to crypto data streams"""
        if not self.is_authenticated:
            print("❌ Not authenticated. Cannot subscribe.")
            return False
        
        if streams is None:
            streams = ["trades", "quotes", "bars"]  # Default streams
        
        # Build subscription message per official Alpaca docs
        subscription = {"action": "subscribe"}
        
        # Use correct field names as per API documentation
        for stream in streams:
            if stream == "trades":
                subscription["trades"] = symbols
            elif stream == "quotes":
                subscription["quotes"] = symbols
            elif stream == "bars":
                subscription["bars"] = symbols
            elif stream == "daily_bars":
                subscription["dailyBars"] = symbols
            elif stream == "orderbook":
                subscription["orderbooks"] = symbols
        
        try:
            self.ws.send(json.dumps(subscription))
            self.subscribed_symbols.update(symbols)
            print(f"📡 Subscribed to {len(symbols)} crypto symbols: {', '.join(symbols)}")
            print(f"📊 Stream types: {', '.join(streams)}")
            return True
            
        except Exception as e:
            print(f"❌ Subscription failed: {e}")
            return False
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"❌ Crypto WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        print(f"🔌 Crypto WebSocket closed: {close_status_code} - {close_msg}")
        self.is_connected = False
        self.is_authenticated = False
    
    def disconnect(self):
        """Disconnect from WebSocket"""
        if self.ws:
            self.ws.close()
        self.is_connected = False
        self.is_authenticated = False
        print("🔌 Crypto streamer disconnected")

def main():
    """Test crypto streaming with popular symbols"""
    print("🚀 Alpaca Crypto Streamer - 24/7 Real-time Data")
    print("=" * 60)
    
    # Get user input for crypto symbols
    print("\n💰 Popular crypto pairs:")
    from env_config import POPULAR_CRYPTOS
    for i, crypto in enumerate(POPULAR_CRYPTOS, 1):
        print(f"  {i:2d}. {crypto}")
    
    print("\nEnter crypto symbols to stream (comma-separated):")
    print("Example: BTC/USD,ETH/USD,AVAX/USD")
    
    user_input = input("Symbols: ").strip()
    if not user_input:
        symbols = ["BTC/USD", "ETH/USD"]  # Default
        print(f"Using default: {', '.join(symbols)}")
    else:
        symbols = [s.strip().upper() for s in user_input.split(",")]
    
    print(f"\n🎯 Streaming {len(symbols)} crypto pairs...")
    print("💡 Crypto markets are open 24/7 - real-time data available!")
    print()
    
    # Create and connect streamer
    streamer = AlpacaCryptoStreamer()
    
    if not streamer.connect():
        print("❌ Failed to connect to crypto streams")
        return
    
    # Wait for authentication
    for _ in range(30):
        if streamer.is_authenticated:
            break
        time.sleep(0.1)
    
    if not streamer.is_authenticated:
        print("❌ Failed to authenticate")
        return
    
    # Subscribe to symbols
    if not streamer.subscribe_to_crypto(symbols):
        print("❌ Failed to subscribe to crypto data")
        return
    
    print("\n🔴 STREAMING LIVE (Press Ctrl+C to stop)")
    print("=" * 60)
    
    try:
        # Stream indefinitely
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping crypto stream...")
        streamer.disconnect()
        print("✅ Crypto streaming stopped")

if __name__ == "__main__":
    main()