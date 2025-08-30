#!/usr/bin/env python3
"""
Fixed Crypto Streamer
Phase 3 of Pulse Element Project

Fixed version that handles authentication correctly.
The issue: Alpaca auto-authenticates via headers, no need for auth message.
"""

import json
import websocket
import threading
import time
from datetime import datetime
from env_config import API_KEY, SECRET_KEY, CRYPTO_WS_URL

class FixedAlpacaCryptoStreamer:
    """Fixed WebSocket streamer for Alpaca crypto data"""
    
    def __init__(self):
        self.ws = None
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.ws_url = CRYPTO_WS_URL
        self.is_connected = False
        self.is_ready = False  # Ready to subscribe (not "authenticated")
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
            
            # Wait for ready state
            for _ in range(50):  # 5 seconds max
                if self.is_ready:
                    break
                time.sleep(0.1)
            
            if not self.is_ready:
                raise Exception("Failed to reach ready state within timeout")
                
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def _on_open(self, ws):
        """Handle WebSocket connection opened"""
        print("🔗 Crypto WebSocket connected")
        self.is_connected = True
        # DO NOT send auth message - headers handle authentication!
    
    def _on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Handle message arrays
            if isinstance(data, list):
                for item in data:
                    self._process_message(item)
            else:
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
                print("✅ Crypto authenticated via headers")
                self.is_ready = True  # Ready to subscribe
            
        elif msg_type == "subscription":
            # Subscription confirmation
            if msg.get("msg") == "subscribed":
                trades = msg.get("trades", [])
                quotes = msg.get("quotes", [])
                bars = msg.get("bars", [])
                all_streams = trades + quotes + bars
                print(f"✅ Subscribed to crypto streams: {all_streams}")
            
        elif msg_type == "error":
            # Skip "already authenticated" - it's expected
            if "already authenticated" not in str(msg.get("msg", "")):
                print(f"❌ API Error: {msg.get('msg', 'Unknown error')}")
            
        elif msg_type == "t":
            # Trade data
            self._handle_trade(msg)
            
        elif msg_type == "q": 
            # Quote data
            self._handle_quote(msg)
            
        elif msg_type == "b":
            # Bar data
            self._handle_bar(msg)
    
    def _handle_trade(self, trade):
        """Handle crypto trade data"""
        symbol = trade.get("S", "N/A")
        price = trade.get("p", 0)
        size = trade.get("s", 0)
        timestamp = trade.get("t", "")
        taker_side = trade.get("tks", "")
        
        time_str = self._format_timestamp(timestamp)
        side_indicator = "📈 BUY" if taker_side == "B" else "📉 SELL"
        
        print(f"[{time_str}] 💰 {symbol} TRADE: ${price:,.2f} | "
              f"Size: {size:,.4f} | {side_indicator}")
    
    def _handle_quote(self, quote):
        """Handle crypto quote data"""
        symbol = quote.get("S", "N/A")
        bid = quote.get("bp", 0)
        ask = quote.get("ap", 0)
        timestamp = quote.get("t", "")
        
        time_str = self._format_timestamp(timestamp)
        spread = ask - bid
        spread_pct = (spread / bid * 100) if bid > 0 else 0
        
        print(f"[{time_str}] 📊 {symbol} QUOTE: "
              f"${bid:,.2f} / ${ask:,.2f} | "
              f"Spread: ${spread:.2f} ({spread_pct:.3f}%)")
    
    def _handle_bar(self, bar):
        """Handle crypto bar data"""
        symbol = bar.get("S", "N/A")
        open_price = bar.get("o", 0)
        high = bar.get("h", 0)
        low = bar.get("l", 0)
        close = bar.get("c", 0)
        volume = bar.get("v", 0)
        vwap = bar.get("vw", 0)
        timestamp = bar.get("t", "")
        
        time_str = self._format_timestamp(timestamp)
        
        print(f"[{time_str}] 📈 {symbol} BAR: "
              f"O:${open_price:,.2f} H:${high:,.2f} L:${low:,.2f} C:${close:,.2f} | "
              f"Vol: {volume:,.2f} | VWAP: ${vwap:,.2f}")
    
    def _format_timestamp(self, timestamp_str):
        """Format timestamp for display"""
        if not timestamp_str:
            return datetime.now().strftime("%H:%M:%S")
        
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%H:%M:%S")
        except:
            return timestamp_str[:8] if len(timestamp_str) > 8 else timestamp_str
    
    def subscribe_to_crypto(self, symbols, streams=None):
        """Subscribe to crypto data streams"""
        if not self.is_ready:
            print("❌ Not ready for subscription. Connection issue?")
            return False
        
        if streams is None:
            streams = ["trades", "quotes", "bars"]
        
        # Build subscription message
        subscription = {"action": "subscribe"}
        
        # Build subscription per official Alpaca docs
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
        self.is_ready = False
    
    def disconnect(self):
        """Disconnect from WebSocket"""
        if self.ws:
            self.ws.close()
        self.is_connected = False
        self.is_ready = False
        print("🔌 Crypto streamer disconnected")

def test_mainstream_crypto():
    """Test with mainstream crypto pairs for price validation"""
    print("🚀 Testing Mainstream Crypto Price Streaming")
    print("=" * 60)
    print("🎯 Testing with Bitcoin and Ethereum - most liquid crypto pairs")
    print("💰 Crypto markets are open 24/7 - should get real-time data!")
    print()
    
    # Use most mainstream cryptos
    test_symbols = ["BTC/USD", "ETH/USD"]
    
    print(f"🔴 Testing symbols: {', '.join(test_symbols)}")
    print("⏳ Connecting and waiting for live prices...")
    print()
    
    # Create streamer
    streamer = FixedAlpacaCryptoStreamer()
    
    if not streamer.connect():
        print("❌ Failed to connect")
        return False
    
    # Wait a moment for full connection
    time.sleep(2)
    
    # Subscribe to test symbols
    if not streamer.subscribe_to_crypto(test_symbols, ["trades", "quotes"]):
        print("❌ Failed to subscribe")
        return False
    
    print("🔴 STREAMING LIVE DATA (Press Ctrl+C to stop)")
    print("=" * 60)
    
    try:
        # Stream for 30 seconds to validate
        start_time = time.time()
        while time.time() - start_time < 30:
            time.sleep(1)
    
    except KeyboardInterrupt:
        pass
    
    print(f"\n🛑 Stopping test...")
    streamer.disconnect()
    
    print(f"\n✅ Mainstream crypto test completed!")
    print(f"💡 If you saw live prices above, crypto streaming is working!")
    
    return True

if __name__ == "__main__":
    test_mainstream_crypto()