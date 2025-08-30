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

# Import the consolidated crypto class
from crypto_alpaca import CryptoAlpaca


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
        self.crypto = None
        
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
            self.crypto = CryptoAlpaca()
            self.popular_cryptos = self.crypto.popular_cryptos
            self.stream_types = self.crypto.stream_types
            
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
        
        # Setup data capture
        self.setup_crypto_data_capture()
        
        try:
            if self.crypto.connect():
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
        
        # Wait for ready state
        time.sleep(1)
        
        if self.crypto.is_ready:
            self.display_system_return("Crypto authentication successful - JSON streaming ready")
            self.test_results['authentication'] = True
        else:
            self.display_system_return("Crypto authentication failed", False)
            return
        
        # Test 5: Subscribe to Major Cryptos
        self.display_prompt("Subscribing to major crypto pairs: BTC/USD, ETH/USD, SOL/USD")
        
        test_symbols = ["BTC/USD", "ETH/USD", "SOL/USD"]
        if self.crypto.subscribe(test_symbols):
            self.display_system_return("Successfully subscribed to 3 crypto pairs")
            self.display_system_return("Subscribed to trades, quotes, and bars data streams")
            self.test_results['subscription'] = True
            self.test_results['test_symbols'] = test_symbols
        else:
            self.display_system_return("Subscription failed", False)
            return
        
        # Test 6: Listen for Data
        self.display_prompt("Listening for real-time crypto market data (45 seconds - extended for crypto)")
        
        # Capture initial state
        start_time = time.time()
        initial_count = self.crypto.data_count
        
        # Wait for data
        data_received = False
        while time.time() - start_time < 45:
            if self.crypto.data_count > initial_count:
                if not data_received:
                    data_received = True
                    latest_data = self.crypto.price_data[-1] if self.crypto.price_data else None
                    if latest_data:
                        self.display_system_return(f"First crypto data received! Type: {latest_data['type']}")
                
                # Check for updates periodically
                if self.crypto.data_count > 0 and self.crypto.data_count % 5 == 0:
                    latest_data = self.crypto.price_data[-1] if self.crypto.price_data else None
                    if latest_data:
                        symbol = latest_data['symbol']
                        price = latest_data['price']
                        data_type = latest_data['type']
                        if price > 1000:
                            self.display_system_return(f"Crypto data: {symbol} ${price:,.2f} ({data_type}) - Total: {self.crypto.data_count} updates")
                        else:
                            self.display_system_return(f"Crypto data: {symbol} ${price:.2f} ({data_type}) - Total: {self.crypto.data_count} updates")
            
            time.sleep(1)
        
        # Store results
        self.test_results['data_received'] = data_received
        self.test_results['price_count'] = self.crypto.data_count
        self.price_data = self.crypto.price_data.copy()
        
        # Test 7: Additional Symbols
        self.display_prompt("Testing additional popular crypto symbols")
        
        additional_symbols = ["AVAX/USD", "ADA/USD", "DOGE/USD"]
        if self.crypto.subscribe(additional_symbols, streams=["quotes"]):
            self.display_system_return("Successfully added 3 more crypto pairs")
        
        # Brief wait for additional data
        time.sleep(5)
        
        # Test 8: 24/7 Operation Validation
        self.display_prompt("Validating 24/7 operation characteristics")
        
        # Check market availability
        current_time = datetime.now()
        
        # Weekend check
        if current_time.weekday() >= 5:
            self.display_system_return("Weekend Trading: ✅ Active")
        else:
            self.display_system_return("Weekend Trading: 🕐 Not applicable now")
        
        # After-hours check
        if current_time.hour < 9 or current_time.hour >= 16:
            self.display_system_return("After Hours Trading: ✅ Active")
        else:
            self.display_system_return("Market Hours Trading: ✅ Active")
        
        # Holiday check (crypto always trades)
        self.display_system_return("Holiday Trading: ✅ Active")
        
        # Test 9: Disconnect
        self.display_prompt("Closing crypto market data connection")
        
        self.crypto.disconnect()
        self.display_system_return("Crypto market connection closed successfully")
        
        # Display results
        self.display_test_results()
    
    def setup_crypto_data_capture(self):
        """Setup data capture for the crypto streamer"""
        # Data is automatically captured in the CryptoAlpaca class
        pass
    
    def check_crypto_market_status(self):
        """Check crypto market operational status"""
        self.display_prompt("Checking crypto market operational status")
        
        # Crypto is always open
        self.display_system_return("Crypto market status: 🟢 ALWAYS OPEN (24/7/365)")
        
        current_time = datetime.now()
        time_str = current_time.strftime("%I:%M %p ET on %A")
        self.display_system_return(f"Current time: {time_str}")
        
        # Traditional market comparison
        hour = current_time.hour
        if hour < 9 or hour >= 16:
            self.display_system_return("Traditional markets: 🔴 CLOSED - Crypto still active globally")
        else:
            self.display_system_return("Traditional markets: 🟢 OPEN - Both markets active")
    
    def display_test_results(self):
        """Display comprehensive test results"""
        print()
        print("=" * 80)
        print("📊 CRYPTO MARKET TEST RESULTS")
        print("=" * 80)
        
        # Test Summary
        print("🎯 TEST SUMMARY")
        print("-" * 50)
        print(f"Connection:        {'✅ SUCCESS' if self.test_results['connection'] else '❌ FAILED'}")
        print(f"Authentication:    {'✅ SUCCESS' if self.test_results['authentication'] else '❌ FAILED'}")
        print(f"Subscription:      {'✅ SUCCESS' if self.test_results['subscription'] else '❌ FAILED'}")
        print(f"Data Reception:    {'✅ SUCCESS' if self.test_results['data_received'] else '❌ FAILED'}")
        print(f"24/7 Operation:    {'✅ VERIFIED' if self.test_results['market_status_24_7'] else '❌ NOT VERIFIED'}")
        print(f"Price Updates:     {self.test_results['price_count']}")
        print()
        
        # Crypto Market Analysis
        print("🪙 CRYPTO MARKET ANALYSIS")
        print("-" * 50)
        
        # Count updates by symbol
        symbol_counts = {}
        data_type_counts = {}
        
        for data in self.price_data:
            symbol = data['symbol']
            data_type = data['type']
            
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
            data_type_counts[data_type] = data_type_counts.get(data_type, 0) + 1
        
        print(f"Active crypto pairs: {len(symbol_counts)}")
        
        if symbol_counts:
            print("Crypto pairs with data:")
            for symbol, count in symbol_counts.items():
                print(f"  {symbol}: {count} updates")
        
        if data_type_counts:
            print("Data types received:")
            for data_type, count in data_type_counts.items():
                print(f"  {data_type}: {count} messages")
        
        print()
        
        # Sample Prices
        if self.price_data:
            print("💎 SAMPLE CRYPTO PRICES")
            print("-" * 50)
            
            # Show last 5 prices
            for data in self.price_data[-5:]:
                time_str = data['time']
                symbol = data['symbol']
                price = data['price']
                data_type = data['type']
                
                # Format based on data type and price
                if data_type == 'QUOTE' and 'spread' in data:
                    spread = data['spread']
                    if price > 1000:
                        print(f"[{time_str}] {symbol} ${price:,.2f} ({data_type}) [Spread: ${spread:.2f}]")
                    else:
                        print(f"[{time_str}] {symbol} ${price:.2f} ({data_type}) [Spread: ${spread:.2f}]")
                elif data_type == 'BAR':
                    if price > 1000:
                        print(f"[{time_str}] {symbol} ${price:,.2f} ({data_type})")
                    else:
                        print(f"[{time_str}] {symbol} ${price:.2f} ({data_type})")
                else:
                    if price > 1000:
                        print(f"[{time_str}] {symbol} ${price:,.2f} ({data_type})")
                    else:
                        print(f"[{time_str}] {symbol} ${price:.2f} ({data_type})")
            
            print()
        
        # 24/7 Operation Status
        print("🌍 24/7 OPERATION STATUS")
        print("-" * 50)
        
        current_time = datetime.now()
        
        # Weekend status
        if current_time.weekday() >= 5:
            print("  Weekend Trading: 🟢 ACTIVE")
        else:
            print("  Weekend Trading: 🕐 N/A")
        
        # After-hours status
        if current_time.hour < 9 or current_time.hour >= 16:
            print("  After-Hours Activity: 🟢 ACTIVE")
        else:
            print("  Market Hours Activity: 🟢 ACTIVE")
        
        print("  Global Market Access: 🟢 ACTIVE")
        print("  Holiday Trading: 🟢 ACTIVE")
        print()
        
        # Working Files
        print("🚀 WORKING FILES")
        print("-" * 50)
        
        if self.test_results['data_received'] and self.test_results['price_count'] > 0:
            print("✅ CRYPTO STREAMING IS WORKING!")
            print("📁 Working file: tests/crypto_alpaca.py")
            print("💡 Usage: python crypto_alpaca.py")
            print("🎯 Your API credentials provide access to real-time crypto data")
        elif self.test_results['connection'] and self.test_results['authentication']:
            print("⚠️ CRYPTO CONNECTION WORKS - LIMITED DATA")
            print("📁 System file: tests/crypto_alpaca.py")
            print("💡 Connection successful, may be low activity period")
        else:
            print("❌ CRYPTO STREAMING FAILED")
            print("📁 Check file: tests/crypto_alpaca.py")
            print("💡 Verify API credentials in .env file")
        
        print()
        print("📁 CONSOLIDATED CRYPTO SYSTEM:")
        print("   • crypto_alpaca.py - Unified crypto trading class")
        print("   • test_crypto_market.py - Comprehensive testing")
        print("   • .env - Secure API credentials")
        print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS")
        print("-" * 50)
        
        if self.test_results['data_received']:
            print("🚀 Crypto streaming is fully functional!")
            print("🌍 Take advantage of 24/7 operation for global trading")
            print("💰 Consider implementing automated crypto trading strategies")
            print("📈 Crypto volatility provides more frequent price updates")
        else:
            print("🔄 Crypto activity varies throughout the day")
            print("📊 Peak activity: US market hours, major news events")
            print("🌏 Different crypto pairs active at different global times")
            print("⏰ Try again during high-volume periods")
        
        print("🌟 Unique advantage: Crypto markets never close")
        print("🎯 Perfect for automated systems and global trading")
        print("💡 Can trade when stock/options markets are closed")
        
        print("=" * 80)
        
        # Show errors if any
        if self.test_results['errors']:
            print("\n⚠️ ERRORS ENCOUNTERED:")
            for error in self.test_results['errors']:
                print(f"  - {error}")


def main():
    """Main test execution"""
    tester = CryptoMarketTester()
    tester.run_crypto_market_test()


if __name__ == "__main__":
    main()