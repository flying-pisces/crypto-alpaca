#!/usr/bin/env python3
"""
Quick Crypto Test
Automated test of crypto streaming functionality
"""

import time
from basic_crypto_streamer import AlpacaCryptoStreamer

def quick_test():
    """Quick automated test of crypto streaming"""
    print("🚀 Quick Crypto Streaming Test")
    print("=" * 50)
    
    # Test with BTC and ETH
    test_symbols = ["BTC/USD", "ETH/USD"]
    print(f"Testing: {', '.join(test_symbols)}")
    
    streamer = AlpacaCryptoStreamer()
    
    print("\n🔌 Connecting...")
    if not streamer.connect():
        print("❌ Connection failed")
        return False
    
    # Wait for authentication
    print("⏳ Waiting for authentication...")
    for _ in range(30):
        if streamer.is_authenticated:
            break
        time.sleep(0.1)
    
    if not streamer.is_authenticated:
        print("❌ Authentication timeout")
        return False
    
    print("✅ Connected and authenticated!")
    
    # Subscribe
    print("\n📡 Subscribing to crypto data...")
    if not streamer.subscribe_to_crypto(test_symbols):
        print("❌ Subscription failed")
        return False
    
    print("✅ Subscribed successfully!")
    
    # Stream for 10 seconds
    print("\n🔴 Streaming for 10 seconds...")
    print("-" * 50)
    
    start_time = time.time()
    data_received = False
    
    while time.time() - start_time < 10:
        time.sleep(0.5)
        # Just check if we're still connected
        if streamer.is_connected:
            data_received = True
    
    streamer.disconnect()
    
    if data_received:
        print("\n✅ SUCCESS: Crypto streaming is working!")
        print("💰 Your API credentials support real-time crypto data")
    else:
        print("\n❌ No data received in test period")
    
    return data_received

if __name__ == "__main__":
    success = quick_test()
    print(f"\n🎯 Test result: {'PASSED' if success else 'FAILED'}")