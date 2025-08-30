#!/usr/bin/env python3
"""
Simple Crypto Demo
Working demonstration of crypto streaming with real prices
"""

import json
import websocket
import threading
import time
from datetime import datetime
from env_config import API_KEY, SECRET_KEY, CRYPTO_WS_URL

class SimpleCryptoDemo:
    """Simple working crypto streamer"""
    
    def __init__(self):
        self.ws = None
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.ws_url = CRYPTO_WS_URL
        self.is_ready = False
        self.received_data = False
        
    def connect_and_stream(self, symbols=None, duration=15):
        """Connect and stream for specified duration"""
        if symbols is None:
            symbols = ["BTC/USD", "ETH/USD"]
        
        print(f"🚀 Simple Crypto Demo - Real Price Test")
        print(f"=" * 50)
        print(f"🎯 Testing: {', '.join(symbols)}")
        print(f"⏱️ Duration: {duration} seconds")
        print(f"💰 Crypto markets are open 24/7!")
        print()
        
        # Create WebSocket with headers
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
        
        # Start in background
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # Wait for ready
        print("🔌 Connecting...")
        for _ in range(50):
            if self.is_ready:
                break
            time.sleep(0.1)
        
        if not self.is_ready:
            print("❌ Connection failed")
            return False
        
        # Subscribe to symbols
        subscription = {
            "action": "subscribe",
            "trades": symbols,
            "quotes": symbols
        }
        
        print(f"📡 Subscribing to crypto data...")
        self.ws.send(json.dumps(subscription))
        
        print(f"\n🔴 STREAMING LIVE DATA")
        print("=" * 50)
        
        # Stream for specified duration
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(1)
        
        # Close connection
        self.ws.close()
        
        print(f"\n🛑 Demo completed!")
        if self.received_data:
            print(f"✅ SUCCESS: Received real crypto prices!")
            print(f"💰 Your API credentials work for crypto streaming")
        else:
            print(f"⚠️ No data received - check symbols or connection")
        
        return self.received_data
    
    def _on_open(self, ws):
        """WebSocket opened"""
        print("✅ Connected!")
    
    def _on_message(self, ws, message):
        """Process messages"""
        try:
            data = json.loads(message)
            
            if isinstance(data, list):
                for item in data:
                    self._process_message(item)
            else:
                self._process_message(data)
                
        except json.JSONDecodeError:
            pass
    
    def _process_message(self, msg):
        """Process individual message"""
        msg_type = msg.get("T")
        
        if msg_type == "success" and "authenticated" in str(msg.get("msg", "")):
            print("✅ Authenticated!")
            self.is_ready = True
        
        elif msg_type == "subscription":
            print("✅ Subscribed to crypto streams!")
        
        elif msg_type == "t":  # Trade
            symbol = msg.get("S", "N/A")
            price = msg.get("p", 0)
            size = msg.get("s", 0)
            side = "📈 BUY" if msg.get("tks") == "B" else "📉 SELL"
            
            print(f"💰 {symbol} TRADE: ${price:,.2f} | Size: {size:.4f} | {side}")
            self.received_data = True
        
        elif msg_type == "q":  # Quote
            symbol = msg.get("S", "N/A") 
            bid = msg.get("bp", 0)
            ask = msg.get("ap", 0)
            spread = ask - bid
            
            print(f"📊 {symbol} QUOTE: ${bid:,.2f} / ${ask:,.2f} | Spread: ${spread:.2f}")
            self.received_data = True
        
        elif msg_type == "error" and "already authenticated" not in str(msg.get("msg", "")):
            print(f"❌ Error: {msg.get('msg', 'Unknown')}")
    
    def _on_error(self, ws, error):
        """Handle errors"""
        if "already authenticated" not in str(error):
            print(f"❌ WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket closed"""
        print(f"🔌 Connection closed")

def main():
    """Run simple crypto demo"""
    demo = SimpleCryptoDemo()
    
    # Test with Bitcoin and Ethereum (most liquid)
    success = demo.connect_and_stream(["BTC/USD", "ETH/USD"], duration=15)
    
    print(f"\n" + "=" * 50)
    if success:
        print(f"🎉 CRYPTO STREAMING IS WORKING!")
        print(f"✅ Real-time prices confirmed")
        print(f"✅ Your API credentials support crypto")
        print(f"✅ No subscription upgrade needed")
        print(f"\n🚀 Ready to use:")
        print(f"   python interactive_crypto_streamer.py")
    else:
        print(f"❌ No data received")
        print(f"💡 Try again in a few minutes (rate limiting)")

if __name__ == "__main__":
    main()