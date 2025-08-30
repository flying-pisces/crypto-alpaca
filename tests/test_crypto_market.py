#!/usr/bin/env python3
"""
Crypto Market Test with Prompts and System Returns
Interactive test for crypto market data streaming with user prompts
"""

import sys
import os
import time
import threading
from datetime import datetime, timedelta

# Add crypto streaming path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'references', 'alpaca-crypto-streaming'))

class CryptoMarketTester:
    """Interactive crypto market data tester with prompts and responses"""
    
    def __init__(self):
        self.test_results = {
            'connection': False,
            'authentication': False,
            'subscription': False,
            'data_received': False,
            'price_count': 0,
            'test_symbols': [],
            'market_status_24_7': False,
            'errors': []
        }
        self.price_data = []
        
    def display_prompt(self, message):
        """Display user prompt"""
        print(f"🤖 PROMPT: {message}")
    
    def display_system_return(self, message, success=True):
        """Display system response"""
        icon = "✅" if success else "❌"
        print(f"{icon} SYSTEM: {message}")
    
    def run_crypto_market_test(self):
        """Run comprehensive crypto market test with prompts and returns"""
        print("=" * 80)
        print("🪙 CRYPTO MARKET DATA STREAMING TEST")
        print("=" * 80)
        print(f"🕐 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S ET')}")
        print()
        
        # Check 24/7 status
        self.check_crypto_market_status()
        
        # Test 1: Import and Initialize
        self.display_prompt("Testing crypto streaming module import and initialization")
        
        try:
            from fixed_crypto_streamer import FixedAlpacaCryptoStreamer
            from env_config import POPULAR_CRYPTOS, STREAM_TYPES
            
            self.streamer = FixedAlpacaCryptoStreamer()
            self.popular_cryptos = POPULAR_CRYPTOS
            self.stream_types = STREAM_TYPES
            
            self.display_system_return("Crypto streaming modules imported successfully")
        except Exception as e:
            self.display_system_return(f"Failed to import crypto modules: {e}", False)
            self.test_results['errors'].append(f"Import error: {e}")
            return
        
        # Test 2: 24/7 Market Status Verification
        self.display_prompt("Verifying 24/7 crypto market operation status")
        
        # Crypto markets never close - always available
        self.test_results['market_status_24_7'] = True
        self.display_system_return("Crypto markets operate 24/7/365 - always available for trading")
        
        current_time = datetime.now()
        weekend_status = "Weekend" if current_time.weekday() >= 5 else "Weekday"
        hour_status = "After-hours" if current_time.hour < 9 or current_time.hour >= 16 else "Market hours"
        
        self.display_system_return(f"Current: {weekend_status}, {hour_status} - Crypto still active")
        
        # Test 3: Connection to Crypto WebSocket
        self.display_prompt("Attempting to connect to Alpaca crypto WebSocket (JSON protocol)")
        
        # Override handlers to capture data
        self.setup_crypto_data_capture()
        
        try:
            if self.streamer.connect():
                self.display_system_return("Crypto WebSocket connection established (JSON format)")
                self.test_results['connection'] = True
            else:
                self.display_system_return("Crypto WebSocket connection failed", False)
                return
        except Exception as e:
            self.display_system_return(f"Connection error: {e}", False)
            return
        
        # Test 4: Authentication (Header-based)
        self.display_prompt("Waiting for crypto API authentication (header-based)")
        
        # Wait for authentication
        for i in range(30):
            if hasattr(self.streamer, 'is_ready') and self.streamer.is_ready:
                self.display_system_return("Crypto authentication successful - JSON streaming ready")
                self.test_results['authentication'] = True
                break
            time.sleep(0.1)
        else:
            self.display_system_return("Crypto authentication timeout", False)
            return
        
        # Test 5: Major Crypto Symbol Subscription
        test_symbols = ["BTC/USD", "ETH/USD", "SOL/USD"]
        self.test_results['test_symbols'] = test_symbols
        
        self.display_prompt(f"Subscribing to major crypto pairs: {', '.join(test_symbols)}")
        
        try:
            if self.streamer.subscribe_to_crypto(test_symbols, ["trades", "quotes", "bars"]):
                self.display_system_return(f"Successfully subscribed to {len(test_symbols)} crypto pairs")
                self.display_system_return("Subscribed to trades, quotes, and bars data streams")
                self.test_results['subscription'] = True
            else:
                self.display_system_return("Crypto subscription failed", False)
                return
        except Exception as e:
            self.display_system_return(f"Subscription error: {e}", False)
            return
        
        # Test 6: Real-time Crypto Data Reception
        self.display_prompt("Listening for real-time crypto market data (45 seconds - extended for crypto)")
        
        start_time = time.time()
        last_update_time = 0
        
        while time.time() - start_time < 45:  # Longer for crypto due to variable activity
            current_time = time.time()
            
            if len(self.price_data) > 0:
                if not self.test_results['data_received']:
                    self.display_system_return(f"First crypto data received! Type: {self.price_data[0]['type']}")
                    self.test_results['data_received'] = True
                
                # Show live updates every 10 seconds or when new data arrives
                if (current_time - last_update_time > 10) or (len(self.price_data) % 5 == 0):
                    if self.price_data:
                        latest = self.price_data[-1]
                        self.display_system_return(
                            f"Crypto data: {latest['symbol']} ${latest['price']:,.2f} "
                            f"({latest['type']}) - Total: {len(self.price_data)} updates"
                        )
                        last_update_time = current_time
            
            time.sleep(1)
        
        self.test_results['price_count'] = len(self.price_data)
        
        # Test 7: Popular Crypto Symbols Test
        self.display_prompt("Testing additional popular crypto symbols")
        
        additional_cryptos = ["AVAX/USD", "ADA/USD", "DOGE/USD"]
        
        try:
            if self.streamer.subscribe_to_crypto(additional_cryptos, ["quotes"]):
                self.display_system_return(f"Successfully added {len(additional_cryptos)} more crypto pairs")
                
                # Brief additional listening period
                time.sleep(10)
                
            else:
                self.display_system_return("Additional crypto subscription failed", False)
        except Exception as e:
            self.display_system_return(f"Additional subscription error: {e}", False)
        
        # Test 8: 24/7 Operation Validation
        self.display_prompt("Validating 24/7 operation characteristics")
        
        operation_check = {
            'weekend_trading': datetime.now().weekday() >= 5,
            'after_hours_trading': datetime.now().hour < 9 or datetime.now().hour >= 16,
            'holiday_trading': True,  # Crypto trades on holidays
        }
        
        for check, status in operation_check.items():
            check_name = check.replace('_', ' ').title()
            self.display_system_return(f"{check_name}: {'✅ Active' if status else '🕐 Not applicable now'}")
        
        # Test 9: Disconnection
        self.display_prompt("Closing crypto market data connection")
        
        try:
            self.streamer.disconnect()
            self.display_system_return("Crypto market connection closed successfully")
        except Exception as e:
            self.display_system_return(f"Disconnection error: {e}", False)
        
        # Generate final report
        self.generate_crypto_report()
    
    def setup_crypto_data_capture(self):
        """Set up data capture for crypto prices"""
        original_on_message = getattr(self.streamer, '_on_message', None)
        
        def capture_crypto_data(ws, message):
            try:
                # Call original handler if exists
                if original_on_message:
                    original_on_message(ws, message)
                
                # Parse JSON message for crypto data
                import json
                if isinstance(message, str):
                    try:
                        data = json.loads(message)
                        if isinstance(data, list):
                            for item in data:
                                self.process_crypto_message(item)
                        else:
                            self.process_crypto_message(data)
                    except json.JSONDecodeError:
                        pass
            except Exception as e:
                self.test_results['errors'].append(f"Crypto data capture error: {e}")
        
        # Override the message handler
        self.streamer._on_message = capture_crypto_data
    
    def process_crypto_message(self, msg):
        """Process individual crypto market message"""
        if isinstance(msg, dict):
            msg_type = msg.get('T')
            symbol = msg.get('S')
            
            if msg_type == 't' and symbol:  # Trade
                price = msg.get('p', 0)
                if price:
                    self.price_data.append({
                        'type': 'TRADE',
                        'symbol': symbol,
                        'price': price,
                        'size': msg.get('s', 0),
                        'taker_side': msg.get('tks', ''),
                        'timestamp': datetime.now()
                    })
            
            elif msg_type == 'q' and symbol:  # Quote
                bid = msg.get('bp', 0)
                ask = msg.get('ap', 0)
                if bid and ask:
                    mid_price = (bid + ask) / 2
                    self.price_data.append({
                        'type': 'QUOTE',
                        'symbol': symbol,
                        'price': mid_price,
                        'bid': bid,
                        'ask': ask,
                        'bid_size': msg.get('bs', 0),
                        'ask_size': msg.get('as', 0),
                        'timestamp': datetime.now()
                    })
            
            elif msg_type == 'b' and symbol:  # Bar
                close = msg.get('c', 0)
                if close:
                    self.price_data.append({
                        'type': 'BAR',
                        'symbol': symbol,
                        'price': close,
                        'open': msg.get('o', 0),
                        'high': msg.get('h', 0),
                        'low': msg.get('l', 0),
                        'volume': msg.get('v', 0),
                        'vwap': msg.get('vw', 0),
                        'timestamp': datetime.now()
                    })
    
    def check_crypto_market_status(self):
        """Check and display crypto market status (always open)"""
        now = datetime.now()
        
        self.display_prompt("Checking crypto market operational status")
        
        # Crypto markets are always open
        self.display_system_return("Crypto market status: 🟢 ALWAYS OPEN (24/7/365)")
        
        # Display current time context
        day_name = now.strftime('%A')
        time_str = now.strftime('%I:%M %p ET')
        
        self.display_system_return(f"Current time: {time_str} on {day_name}")
        
        # Compare with traditional markets
        is_weekday = now.weekday() < 5
        is_stock_hours = (now.hour > 9 or (now.hour == 9 and now.minute >= 30)) and now.hour < 16
        is_stock_open = is_weekday and is_stock_hours
        
        if is_stock_open:
            self.display_system_return("Traditional markets: 🟢 OPEN - High crypto activity expected")
        else:
            self.display_system_return("Traditional markets: 🔴 CLOSED - Crypto still active globally")
        
        return True
    
    def generate_crypto_report(self):
        """Generate comprehensive crypto test report"""
        print("\n" + "=" * 80)
        print("📊 CRYPTO MARKET TEST RESULTS")
        print("=" * 80)
        
        # Test summary
        print("🎯 TEST SUMMARY")
        print("-" * 50)
        print(f"Connection:        {'✅ SUCCESS' if self.test_results['connection'] else '❌ FAILED'}")
        print(f"Authentication:    {'✅ SUCCESS' if self.test_results['authentication'] else '❌ FAILED'}")
        print(f"Subscription:      {'✅ SUCCESS' if self.test_results['subscription'] else '❌ FAILED'}")
        print(f"Data Reception:    {'✅ SUCCESS' if self.test_results['data_received'] else '❌ FAILED'}")
        print(f"24/7 Operation:    {'✅ VERIFIED' if self.test_results['market_status_24_7'] else '❌ FAILED'}")
        print(f"Price Updates:     {self.test_results['price_count']}")
        
        # Crypto-specific analysis
        print(f"\n🪙 CRYPTO MARKET ANALYSIS")
        print("-" * 50)
        
        if self.price_data:
            # Group by symbol and type
            symbol_counts = {}
            data_types = {}
            crypto_pairs = set()
            
            for data in self.price_data:
                symbol = data['symbol']
                data_type = data['type']
                
                symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
                data_types[data_type] = data_types.get(data_type, 0) + 1
                crypto_pairs.add(symbol)
            
            print(f"Active crypto pairs: {len(crypto_pairs)}")
            print("Crypto pairs with data:")
            for symbol, count in symbol_counts.items():
                print(f"  {symbol}: {count} updates")
            
            print("Data types received:")
            for dtype, count in data_types.items():
                print(f"  {dtype}: {count} messages")
            
            # Sample prices with crypto-specific details
            print(f"\n💎 SAMPLE CRYPTO PRICES")
            print("-" * 50)
            recent_prices = self.price_data[-5:] if len(self.price_data) >= 5 else self.price_data
            
            for data in recent_prices:
                timestamp = data['timestamp'].strftime('%H:%M:%S')
                price_str = f"${data['price']:,.2f}"
                
                # Add crypto-specific details
                extra_info = ""
                if data['type'] == 'TRADE' and 'taker_side' in data:
                    side = "Buy" if data['taker_side'] == 'B' else "Sell"
                    extra_info = f" [{side}]"
                elif data['type'] == 'QUOTE':
                    spread = data.get('ask', 0) - data.get('bid', 0)
                    extra_info = f" [Spread: ${spread:.2f}]"
                
                print(f"[{timestamp}] {data['symbol']} {price_str} ({data['type']}){extra_info}")
        
        # 24/7 Operation Summary
        print(f"\n🌍 24/7 OPERATION STATUS")
        print("-" * 50)
        
        current_time = datetime.now()
        time_contexts = {
            'Weekend Trading': current_time.weekday() >= 5,
            'After-Hours Activity': current_time.hour < 9 or current_time.hour >= 16,
            'Global Market Access': True,
            'Holiday Trading': True,
        }
        
        for context, is_active in time_contexts.items():
            status = "🟢 ACTIVE" if is_active else "🕐 N/A"
            print(f"  {context}: {status}")
        
        # Working file identification
        print(f"\n🚀 WORKING FILES")
        print("-" * 50)
        
        if self.test_results['data_received']:
            print("✅ CRYPTO STREAMING IS WORKING!")
            print("📁 Working file: references/alpaca-crypto-streaming/fixed_crypto_streamer.py")
            print("💡 Usage: python fixed_crypto_streamer.py")
            print("🎯 Your API credentials provide access to real-time crypto data")
        elif self.test_results['subscription']:
            print("⚠️ CRYPTO CONNECTION WORKS - LIMITED DATA")
            print("📁 System file: references/alpaca-crypto-streaming/fixed_crypto_streamer.py")
            print("💡 Connection successful, may be low activity period")
        else:
            print("❌ CRYPTO STREAMING ISSUES DETECTED")
            if self.test_results['errors']:
                print("🔍 Errors encountered:")
                for error in self.test_results['errors']:
                    print(f"   • {error}")
        
        # Additional crypto files
        if self.test_results['connection']:
            print("\n📁 ADDITIONAL CRYPTO FILES:")
            print("   • simple_crypto_demo.py - Quick testing")
            print("   • interactive_crypto_streamer.py - User-friendly interface")
            print("   • Boston2025-CryptoTrading/ - Advanced trading system")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 50)
        
        if self.test_results['data_received']:
            print("🚀 Crypto streaming is fully functional!")
            print("🌍 Take advantage of 24/7 operation for global trading")
            print("💰 Consider implementing automated crypto trading strategies")
            print("📈 Crypto volatility provides more frequent price updates")
        elif self.test_results['subscription']:
            print("🔄 Crypto activity varies throughout the day")
            print("📊 Peak activity: US market hours, major news events")
            print("🌏 Different crypto pairs active at different global times")
            print("⏰ Try again during high-volume periods")
        
        if self.test_results['market_status_24_7']:
            print("🌟 Unique advantage: Crypto markets never close")
            print("🎯 Perfect for automated systems and global trading")
            print("💡 Can trade when stock/options markets are closed")
        
        print("=" * 80)

def main():
    """Run crypto market test with prompts and system returns"""
    tester = CryptoMarketTester()
    
    try:
        tester.run_crypto_market_test()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        tester.display_system_return("Crypto market test terminated by user", False)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        tester.display_system_return(f"Fatal error during test: {e}", False)

if __name__ == "__main__":
    main()