#!/usr/bin/env python3
"""
Interactive Crypto Streamer
Phase 3 of Pulse Element Project

Complete interactive cryptocurrency streaming system with:
1. User-friendly crypto pair selection
2. Real-time price display and validation  
3. 24/7 operation (crypto markets never close)
4. Multiple data stream types (trades, quotes, bars)
"""

import json
import time
import sys
import os
from datetime import datetime
from basic_crypto_streamer import AlpacaCryptoStreamer
from env_config import POPULAR_CRYPTOS, STREAM_TYPES

class InteractiveCryptoStreamer:
    """Interactive interface for crypto streaming"""
    
    def __init__(self):
        self.streamer = AlpacaCryptoStreamer()
        self.selected_cryptos = []
        self.selected_streams = []
        self.latest_prices = {}  # Store latest prices for validation
        
    def run_interactive_workflow(self):
        """Run complete interactive crypto workflow"""
        print("🚀 Interactive Crypto Streamer - 24/7 Real-time Data")
        print("=" * 60)
        print("💰 Cryptocurrency markets never close - always live data!")
        print()
        
        # Step 1: Select crypto pairs
        if not self._select_crypto_pairs():
            print("❌ No crypto pairs selected. Exiting.")
            return
        
        # Step 2: Select data streams
        if not self._select_data_streams():
            print("❌ No data streams selected. Exiting.")
            return
        
        # Step 3: Connect and authenticate
        if not self._connect_and_authenticate():
            print("❌ Failed to connect. Exiting.")
            return
        
        # Step 4: Start streaming with price validation
        self._start_streaming_with_validation()
    
    def _select_crypto_pairs(self):
        """Step 1: Interactive crypto pair selection"""
        print("📋 Step 1: Select Crypto Pairs")
        print("=" * 40)
        
        print("\n💰 Popular cryptocurrency pairs:")
        for i, crypto in enumerate(POPULAR_CRYPTOS, 1):
            print(f"  {i:2d}. {crypto}")
        
        print(f"\n💡 Options:")
        print(f"  • Enter numbers (1-{len(POPULAR_CRYPTOS)}) separated by commas")
        print(f"  • Or type custom symbols like: BTC/USD,ETH/USD,DOGE/USD")
        print(f"  • Press Enter for default (BTC/USD, ETH/USD)")
        
        user_input = input("\nYour selection: ").strip()
        
        if not user_input:
            # Default selection
            self.selected_cryptos = ["BTC/USD", "ETH/USD"]
            print(f"✅ Using default: {', '.join(self.selected_cryptos)}")
        
        elif all(c.isdigit() or c in ',. ' for c in user_input):
            # Number selection
            try:
                numbers = [int(x.strip()) for x in user_input.replace(',', ' ').split()]
                self.selected_cryptos = []
                for num in numbers:
                    if 1 <= num <= len(POPULAR_CRYPTOS):
                        self.selected_cryptos.append(POPULAR_CRYPTOS[num-1])
                
                if self.selected_cryptos:
                    print(f"✅ Selected: {', '.join(self.selected_cryptos)}")
                else:
                    print("❌ No valid numbers selected")
                    return False
                    
            except ValueError:
                print("❌ Invalid number format")
                return False
        
        else:
            # Custom symbol input
            symbols = [s.strip().upper() for s in user_input.replace(',', ' ').split()]
            self.selected_cryptos = [s for s in symbols if '/' in s]  # Basic validation
            
            if self.selected_cryptos:
                print(f"✅ Custom selection: {', '.join(self.selected_cryptos)}")
            else:
                print("❌ No valid crypto symbols found (format: BTC/USD)")
                return False
        
        print(f"\n🎯 Will stream {len(self.selected_cryptos)} crypto pairs")
        return True
    
    def _select_data_streams(self):
        """Step 2: Select data stream types"""
        print(f"\n📊 Step 2: Select Data Streams")
        print("=" * 40)
        
        stream_options = [
            ("trades", "Individual buy/sell transactions"),
            ("quotes", "Best bid/ask prices"),
            ("bars", "1-minute price bars (OHLC)"),
            ("daily_bars", "Daily price summaries"),
            ("orderbook", "Order book level 1 data")
        ]
        
        print("\n📡 Available data streams:")
        for i, (stream, desc) in enumerate(stream_options, 1):
            print(f"  {i}. {stream:12} - {desc}")
        
        print(f"\n💡 Options:")
        print(f"  • Enter numbers (1-{len(stream_options)}) separated by commas")
        print(f"  • Press Enter for default (trades, quotes, bars)")
        
        user_input = input("\nStream selection: ").strip()
        
        if not user_input:
            # Default streams
            self.selected_streams = ["trades", "quotes", "bars"]
            print(f"✅ Using default streams: {', '.join(self.selected_streams)}")
        
        else:
            try:
                numbers = [int(x.strip()) for x in user_input.replace(',', ' ').split()]
                self.selected_streams = []
                for num in numbers:
                    if 1 <= num <= len(stream_options):
                        self.selected_streams.append(stream_options[num-1][0])
                
                if self.selected_streams:
                    print(f"✅ Selected streams: {', '.join(self.selected_streams)}")
                else:
                    print("❌ No valid streams selected")
                    return False
                    
            except ValueError:
                print("❌ Invalid number format")
                return False
        
        return True
    
    def _connect_and_authenticate(self):
        """Step 3: Connect and authenticate to crypto WebSocket"""
        print(f"\n🔌 Step 3: Connecting to Crypto WebSocket")
        print("=" * 40)
        
        print("🌐 Connecting to Alpaca crypto streams...")
        if not self.streamer.connect():
            return False
        
        print("🔐 Authenticating...")
        # Wait for authentication
        for _ in range(30):
            if self.streamer.is_authenticated:
                break
            time.sleep(0.1)
        
        if not self.streamer.is_authenticated:
            print("❌ Authentication timeout")
            return False
        
        print("✅ Connected and authenticated successfully!")
        return True
    
    def _start_streaming_with_validation(self):
        """Step 4: Start streaming with price validation"""
        print(f"\n🔴 Step 4: Starting Live Crypto Streaming")
        print("=" * 40)
        
        # Subscribe to selected crypto pairs and streams
        if not self.streamer.subscribe_to_crypto(self.selected_cryptos, self.selected_streams):
            print("❌ Failed to subscribe to crypto streams")
            return
        
        print(f"\n💰 Streaming Configuration:")
        print(f"   Crypto pairs: {', '.join(self.selected_cryptos)}")
        print(f"   Data streams: {', '.join(self.selected_streams)}")
        print(f"   Market status: 🟢 ALWAYS OPEN (24/7)")
        print()
        
        print("🎯 Price Validation Mode:")
        print("   • Monitoring real-time prices for validation")
        print("   • Will display latest prices every 30 seconds")
        print("   • Press Ctrl+C to stop")
        print()
        
        # Override message handlers for price tracking
        original_handle_trade = self.streamer._handle_trade
        original_handle_quote = self.streamer._handle_quote
        original_handle_bar = self.streamer._handle_bar
        
        def track_trade(trade):
            symbol = trade.get("S")
            price = trade.get("p", 0)
            if symbol and price:
                self.latest_prices[symbol] = {
                    "price": price,
                    "type": "trade",
                    "timestamp": datetime.now()
                }
            original_handle_trade(trade)
        
        def track_quote(quote):
            symbol = quote.get("S")
            bid = quote.get("bp", 0)
            ask = quote.get("ap", 0)
            if symbol and bid and ask:
                mid_price = (bid + ask) / 2
                self.latest_prices[symbol] = {
                    "price": mid_price,
                    "bid": bid,
                    "ask": ask,
                    "type": "quote", 
                    "timestamp": datetime.now()
                }
            original_handle_quote(quote)
        
        def track_bar(bar):
            symbol = bar.get("S")
            close = bar.get("c", 0)
            if symbol and close:
                self.latest_prices[symbol] = {
                    "price": close,
                    "type": "bar",
                    "timestamp": datetime.now()
                }
            original_handle_bar(bar)
        
        # Monkey patch the handlers
        self.streamer._handle_trade = track_trade
        self.streamer._handle_quote = track_quote
        self.streamer._handle_bar = track_bar
        
        print("🔴 LIVE STREAMING - Real-time Data")
        print("=" * 60)
        
        try:
            last_validation = time.time()
            
            while True:
                time.sleep(1)
                
                # Show price validation every 30 seconds
                if time.time() - last_validation > 30:
                    self._display_price_validation()
                    last_validation = time.time()
        
        except KeyboardInterrupt:
            print(f"\n\n🛑 Stopping crypto streaming...")
            self.streamer.disconnect()
            
            # Final price validation
            print(f"\n📊 Final Price Validation:")
            self._display_price_validation()
            
            print(f"\n✅ Crypto streaming session completed!")
            print(f"💰 Total crypto pairs tracked: {len(self.latest_prices)}")
    
    def _display_price_validation(self):
        """Display latest prices for validation"""
        if not self.latest_prices:
            print("⏳ No price data received yet...")
            return
        
        print(f"\n💰 Latest Crypto Prices (Validation):")
        print("─" * 60)
        
        for symbol in self.selected_cryptos:
            if symbol in self.latest_prices:
                data = self.latest_prices[symbol]
                price = data["price"]
                data_type = data["type"]
                age = (datetime.now() - data["timestamp"]).seconds
                
                if data_type == "quote" and "bid" in data:
                    print(f"  {symbol:10} ${price:>10,.2f} (mid) | "
                          f"Bid: ${data['bid']:,.2f} Ask: ${data['ask']:,.2f} | "
                          f"{age}s ago | ✅ REAL")
                else:
                    print(f"  {symbol:10} ${price:>10,.2f} ({data_type}) | "
                          f"{age}s ago | ✅ REAL")
            else:
                print(f"  {symbol:10} {'No data yet':>15} | ⏳ Waiting...")
        
        print("─" * 60)

def main():
    """Run interactive crypto streaming"""
    try:
        streamer = InteractiveCryptoStreamer()
        streamer.run_interactive_workflow()
    
    except KeyboardInterrupt:
        print(f"\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()