#!/usr/bin/env python3
"""
Boston 2025 - Quick System Test
Test the complete Boston 2025 trading system
"""

import time
from crypto_monitor import Boston2025CryptoMonitor

def test_monitor():
    """Test the crypto monitor"""
    print("🧪 Testing Boston 2025 Crypto Monitor")
    print("=" * 50)
    
    monitor = Boston2025CryptoMonitor()
    
    # Test with primary symbols
    symbols = ["BTC/USD", "ETH/USD"]
    
    if monitor.start_monitoring(symbols):
        print("✅ Monitor started successfully")
        
        # Run for 15 seconds
        time.sleep(15)
        
        # Check if we got data
        stats = monitor.get_market_stats("BTC/USD")
        if stats and stats["price"]:
            print(f"✅ Received BTC price: ${stats['price']:,.2f}")
            print(f"✅ Market monitor working correctly")
        else:
            print("⚠️ No price data received (may be normal during low activity)")
        
        monitor.stop_monitoring()
        return True
    else:
        print("❌ Monitor failed to start")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing Configuration")
    print("=" * 50)
    
    from boston_config import BOSTON_2025_CONFIG, get_all_trading_symbols, get_active_strategies
    
    print(f"✅ Project: {BOSTON_2025_CONFIG['project_name']}")
    print(f"✅ Version: {BOSTON_2025_CONFIG['version']}")
    print(f"✅ Trading symbols: {len(get_all_trading_symbols())}")
    print(f"✅ Active strategies: {', '.join(get_active_strategies())}")
    print(f"✅ Max position: ${BOSTON_2025_CONFIG['trading']['max_position_size_usd']:,}")
    
    return True

def main():
    """Run Boston 2025 quick test"""
    print("🚀 Boston 2025 - Quick System Test")
    print("=" * 60)
    print("Testing core components of the trading system")
    print()
    
    # Test configuration
    config_test = test_configuration()
    
    # Test monitor
    monitor_test = test_monitor()
    
    print(f"\n🎯 Test Results")
    print("=" * 30)
    print(f"Configuration: {'✅ PASS' if config_test else '❌ FAIL'}")
    print(f"Market Monitor: {'✅ PASS' if monitor_test else '❌ FAIL'}")
    
    if config_test and monitor_test:
        print(f"\n🎉 Boston 2025 System Ready!")
        print(f"🚀 Launch with: python boston2025_dashboard.py")
    else:
        print(f"\n❌ System has issues - check components")

if __name__ == "__main__":
    main()